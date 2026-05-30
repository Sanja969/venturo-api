from rest_framework import serializers

from experiences.models import Experience
from .models import Participation


class ParticipationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    experience = serializers.ReadOnlyField(source="experience.title")

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
