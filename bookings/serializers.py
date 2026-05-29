from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Booking
        fields = "__all__"
        extra_kwargs = {

            "status": {

                "error_messages": {

                    "invalid_choice": "Status must be pending, confirmed or cancelled."

                }

            }

        }

    def validate(self, data):
        request = self.context["request"]
        user = request.user

        experience = data.get("experience")

        if experience:
            already_booked = (
                Booking.objects.filter(user=user, experience=experience)
                .exclude(pk=self.instance.pk if self.instance else None)
                .exists()
            )

            if already_booked:
                raise serializers.ValidationError("You already booked this experience.")
            if experience.spots_left <= 0:
                raise serializers.ValidationError("This experience is fully booked.")

        return data
