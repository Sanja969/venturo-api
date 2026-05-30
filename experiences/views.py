from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAuthenticatedOrReadOnly, IsExperienceOrganizerOrReadOnly

from .serializers import ExperienceSerializer

from .models import Experience


class ExperienceListApiView(generics.ListCreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        breakpoint()
        serializer.save(organizer=self.request.user)
        breakpoint()


class ExperienceDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsExperienceOrganizerOrReadOnly]
