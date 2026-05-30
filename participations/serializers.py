from rest_framework import serializers
from .models import Participation


class ParticipationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

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
        experience = data.get("experience") or getattr(self.instance, "experience", None)
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
