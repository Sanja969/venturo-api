from django.utils import timezone

from rest_framework import serializers
from .models import Experience


class ExperienceSerializer(serializers.ModelSerializer):
    organizer = serializers.ReadOnlyField(source="organizer.username")
    class Meta:
        model = Experience
        fields = "__all__"
        
    def validate(self, data):
      start_date = data["start_date"]
      end_date = data["end_date"]
      
      if start_date and start_date < timezone.now():
        raise serializers.ValidationError({"start_date": "Experience cannot start in the past."})
    
      if start_date and end_date and start_date > end_date:
        raise serializers.ValidationError({"start_date": "Experience cannot start in the past."})
      
      return data
      
