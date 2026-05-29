from rest_framework import generics

from .models import Review
from .serializers import ReviewSerializer

class ReviewListApiView(generics.ListCreateAPIView):
  serializer_class=ReviewSerializer
  
  def get_queryset(self):
    experience_id= self.kwargs.get("experience_id")
    return Review.objects.filter(experience_id = experience_id)
  
