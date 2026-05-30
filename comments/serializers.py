from rest_framework import serializers

from .models import ActivityComment, RideComment

class ActivityCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    experience = serializers.ReadOnlyField(source="experience.title")

    class Meta:
        model = ActivityComment
        fields = "__all__"
        
class RideCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    ride_offer = serializers.ReadOnlyField(source="ride_offer.id")

    class Meta:
        model = RideComment
        fields = "__all__"