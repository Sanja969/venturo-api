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
    going_count = serializers.ReadOnlyField()
    category_title = serializers.ReadOnlyField(source="category.name")
    spots_left = serializers.ReadOnlyField()
    average_rating = serializers.ReadOnlyField()
    review_count = serializers.ReadOnlyField()
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

    def get_cover_image_url(self, obj):

        first_image = obj.images.first()

        if first_image and first_image.image:

            return first_image.image.url

        return None

    def get_is_favorite(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return FavoriteExperience.objects.filter(user=user, experience=obj).exists()
        return False

    def get_user_participation_status(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            participation = obj.participations.filter(user=user).first()
            if participation:
                return participation.status
        return None

    def get_user_participation_id(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            participation = obj.participations.filter(user=user).first()
            if participation:
                return participation.id
        return None

    def get_can_review(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        user = request.user
        is_past = obj.end_date < timezone.now()
        has_participation = obj.participations.filter(
            user=user,
            status="going",
        ).exists()
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
