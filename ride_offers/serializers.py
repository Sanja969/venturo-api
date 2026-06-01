from rest_framework import serializers

from ride_offers.models import RideOffer

class RideOfferSerializer(serializers.ModelSerializer):
      driver = serializers.ReadOnlyField(source="driver.username")
      experience_title = serializers.ReadOnlyField(source="experience.title")
      destination = serializers.ReadOnlyField(source="experience.location")
  
      class Meta:
          model = RideOffer
          fields = "__all__"