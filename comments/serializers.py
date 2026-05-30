from rest_framework import serializers

from .models import ActivityComment

class ActivityCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    experience = serializers.ReadOnlyField(source="experience.title")

    class Meta:
        model = ActivityComment
        fields = "__all__"