from django.utils import timezone

from rest_framework import serializers
from .models import Category, Experience, ExperienceImage, FavoriteExperience


class ExperienceImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ExperienceImage
        fields = ["id", "image", "image_url", "caption", "created_at"]

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None


class ExperienceImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienceImage
        fields = ["id", "image", "caption", "created_at"]
        read_only_fields = ["id", "created_at"]


class ExperienceSerializer(serializers.ModelSerializer):
    organizer = serializers.ReadOnlyField(source="organizer.username")
    category_title = serializers.ReadOnlyField(source="category.name")

    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    spots_left = serializers.SerializerMethodField()
    going_count = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    user_participation_status = serializers.SerializerMethodField()
    user_participation_id = serializers.SerializerMethodField()
    can_review = serializers.SerializerMethodField()
    can_ride = serializers.SerializerMethodField()

    images = ExperienceImageSerializer(many=True, read_only=True)
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = "__all__"

    def get_going_count(self, obj):
      if hasattr(obj, "going_count_db"):
          return obj.going_count_db

      return obj.going_count

    def get_average_rating(self, obj):
      if hasattr(obj, "avg_rating"):
          return obj.avg_rating

      return obj.average_rating

    def get_review_count(self, obj):
          if hasattr(obj, "reviews_count"):
              return obj.reviews_count

          return obj.review_count

    def get_spots_left(self, obj):
        return max(0, obj.max_participants - self.get_going_count(obj))

    def get_cover_image_url(self, obj):
        prefetched_images = getattr(obj, "_prefetched_objects_cache", {}).get("images")

        images = (
            prefetched_images
            if prefetched_images is not None
            else list(obj.images.all())
        )

        if not images:
            return None

        first_image = images[0]

        if not first_image.image:
            return None

        return first_image.image.url

    def get_is_favorite(self, obj):
        if hasattr(obj, "user_favorites"):
            return bool(obj.user_favorites)
        user = self.context.get("request").user
        if user.is_authenticated:
            return FavoriteExperience.objects.filter(user=user, experience=obj).exists()
        return False

    def get_user_participation_status(self, obj):
        if hasattr(obj, "user_participations"):
            participation = (
                obj.user_participations[0] if obj.user_participations else None
            )
            return participation.status if participation else None
        return None

    def get_user_participation_id(self, obj):
        if hasattr(obj, "user_participations"):
            participation = (
                obj.user_participations[0] if obj.user_participations else None
            )
            return participation.id if participation else None
        return None

    def get_can_review(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        user = request.user
        is_past = obj.end_date < timezone.now()
        if hasattr(obj, "user_participations"):
            has_participation = any(
                participation.status == "going"
                for participation in obj.user_participations
            )
        else:
            has_participation = obj.participations.filter(
                user=user,
                status="going",
            ).exists()
        if hasattr(obj, "user_reviews"):
            already_reviewed = bool(obj.user_reviews)
        else:               
          already_reviewed = obj.reviews.filter(user=user).exists()
        is_organizer = obj.organizer == user

        return (
            is_past and has_participation and not already_reviewed and not is_organizer
        )

    def get_can_ride(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        is_future = obj.end_date > timezone.now()
        return is_future

    def validate(self, data):
        start_date = data.get("start_date") or getattr(
            self.instance, "start_date", None
        )
        end_date = data.get("end_date") or getattr(self.instance, "end_date", None)

        if "start_date" in data and start_date < timezone.now():
            raise serializers.ValidationError(
                {"start_date": "Experience cannot start in the past."}
            )

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError(
                {"end_date": "End date must be after start date."}
            )

        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
