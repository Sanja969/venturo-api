from rest_framework import serializers

from users.models import User


class ProfileSerializer(serializers.ModelSerializer):
    organized_count = serializers.SerializerMethodField()
    participated_count = serializers.SerializerMethodField()
    favorite_count = serializers.SerializerMethodField()
    rides_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "bio",
            "location",
            "organized_count",
            "participated_count",
            "favorite_count",
            "rides_count",
        ]
    def get_organized_count(self, obj):
      return obj.organized_experiences.count()

    def get_participated_count(self, obj):
      return obj.participations.count()
    
    def get_favorite_count(self, obj):
      return obj.favorites.count()

    def get_rides_count(self, obj):
      return obj.ride_offers.count()
    
class PublicProfileSerializer(serializers.ModelSerializer):
    organized_count = serializers.SerializerMethodField()
    participated_count = serializers.SerializerMethodField()
    rides_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "bio",
            "location",
            "organized_count",
            "participated_count",
            "favorite_count",
            "rides_count",
        ]

    def get_organized_count(self, obj):
        return obj.organized_experiences.count()

    def get_participated_count(self, obj):
        return obj.participations.count()

    def get_rides_count(self, obj):
        return obj.ride_offers.count()