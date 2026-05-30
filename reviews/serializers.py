from rest_framework import serializers

from experiences.models import Experience

from .models import Review
from participations.models import Participation


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    experience = serializers.ReadOnlyField(source="experience.title")

    class Meta:
        model = Review
        fields = "__all__"

    def validate(self, data):
        request = self.context["request"]
        user = request.user

        experience = getattr(self.instance, "experience", None)

        if experience is None:

            experience_id = self.context["view"].kwargs.get("experience_id")

            experience = Experience.objects.filter(id=experience_id).first()

        if experience is None:

            raise serializers.ValidationError("Experience is required.")

        has_participation = Participation.objects.filter(
            user=user,
            experience=experience,
            status="going",
        ).exists()

        if not has_participation:

            raise serializers.ValidationError(
                "You can only review experiences you attended."
            )

        already_reviewed = (
            Review.objects.filter(user=user, experience=experience)
            .exclude(pk=self.instance.pk if self.instance else None)
            .exists()
        )
        if already_reviewed:
            raise serializers.ValidationError(
                "You already gave review for this experience"
            )
        return data
