from django.shortcuts import render
from rest_framework import generics

from .permissions import IsExperienceOrganizerOrReadOnly, IsOrganizerOrReadOnly

from .serializers import ExperienceSerializer

from .models import Experience

class ExperienceListApiView(generics.ListCreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsOrganizerOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class ExperienceDetailApiView(generics.RetrieveAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    
class ExperienceDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsExperienceOrganizerOrReadOnly]
    