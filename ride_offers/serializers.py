from rest_framework import serializers

from ride_offers.models import RideOffer, RideRequest


class RideRequestSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = RideRequest
        fields = "__all__"
        read_only_fields = [
            "user",
            "ride_offer",
            "created_at",
        ]

    def validate(self, data):
        request = self.context["request"]
        if not self.instance:
            ride_offer = RideOffer.objects.get(
                pk=self.context["view"].kwargs["ride_offer_id"]
            )

            if ride_offer.driver == request.user:
                raise serializers.ValidationError("You cannot request your own ride.")
        return data


class RideOfferSerializer(serializers.ModelSerializer):
    driver = serializers.ReadOnlyField(source="driver.username")
    experience_title = serializers.ReadOnlyField(source="experience.title")
    destination = serializers.ReadOnlyField(source="experience.location")
    requests_count = serializers.IntegerField(read_only=True)
    requests = RideRequestSerializer(many=True, read_only=True)
    is_driver = serializers.SerializerMethodField()
    user_request_status = serializers.SerializerMethodField()
    user_request_id = serializers.SerializerMethodField()

    class Meta:
        model = RideOffer
        fields = "__all__"

    def get_is_driver(self, obj):
        request = self.context.get("request")
        return bool(
            request and request.user.is_authenticated and obj.driver == request.user
        )

    def get_user_request_status(self, obj):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return None

        ride_request = obj.requests.filter(user=request.user).first()

        if not ride_request:
            return None

        return ride_request.status

    def get_user_request_id(self, obj):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return None

        ride_request = obj.requests.filter(user=request.user).first()

        if not ride_request:
            return None

        return ride_request.id
