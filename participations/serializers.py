from rest_framework import serializers

from experiences.models import Experience
from experiences.serializers import ExperienceSerializer
from .models import Participation

class ParticipationExperienceSerializer(serializers.ModelSerializer):
    organizer = serializers.ReadOnlyField(source="organizer.username")
    category_title = serializers.ReadOnlyField(source="category.name")
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id",
            "title",
            "location",
            "start_date",
            "difficulty",
            "organizer",
            "category_title",
            "cover_image_url",
        ]

    def get_cover_image_url(self, obj):
        images = list(obj.images.all())
        return images[0].image.url if images else None
class ParticipationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    experience = ParticipationExperienceSerializer(read_only=True)

    class Meta:
        model = Participation
        fields = "__all__"
        extra_kwargs = {
            "status": {
                "error_messages": {
                    "invalid_choice": "Status must be interested, going, maybe or cancelled."
                }
            }
        }

    def validate(self, data):
        request = self.context["request"]
        user = request.user
        experience = getattr(self.instance, "experience", None)

        if experience is None:

            experience_id = self.context["view"].kwargs.get("experience_id")

            experience = Experience.objects.filter(id=experience_id).first()

        if experience is None:
            raise serializers.ValidationError("Experience is required.")

        status = data.get("status") or getattr(self.instance, "status", "going")


        already_participating = (
            Participation.objects.filter(user=user, experience=experience)
            .exclude(pk=self.instance.pk if self.instance else None)
            .exists()
        )

        if already_participating:
            raise serializers.ValidationError("You already have a participation for this experience.")
        if status == "going" and experience and experience.spots_left <= 0:
            raise serializers.ValidationError("This experience is fully booked.")

        return data

class ExperienceParticipantSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Participation
        fields = ["id", "user", "status", "created_at"]