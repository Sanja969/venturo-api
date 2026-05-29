from rest_framework import serializers

from .models import Review
from bookings.models import Booking


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    class Meta:
        model = Review
        fields = "__all__"

    def validate(self, data):
        request = self.context["request"]
        user = request.user

        experience = data.get("experience")

        if experience:
            has_booking = Booking.objects.filter(
                user=user,
                experience=experience,
                status="confirmed",
            ).exists()

            if not has_booking:

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
