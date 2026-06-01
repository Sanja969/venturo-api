from django.utils import timezone

from rest_framework import serializers
from .models import Experience, FavoriteExperience


class ExperienceSerializer(serializers.ModelSerializer):
    organizer = serializers.ReadOnlyField(source="organizer.username")
    going_count = serializers.ReadOnlyField()
    spots_left = serializers.ReadOnlyField()
    average_rating = serializers.ReadOnlyField()
    review_count = serializers.ReadOnlyField()
    is_favorite = serializers.SerializerMethodField()
    user_participation_status = serializers.SerializerMethodField()
    user_participation_id = serializers.SerializerMethodField()
    
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
    class Meta:
        model = Experience
        fields = "__all__"

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
