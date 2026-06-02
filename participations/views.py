from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from experiences.models import Experience

from .permissions import IsParticipationOwner

from .serializers import ParticipationSerializer
from .models import Participation
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied


class ParticipationListCreateApiView(generics.ListCreateAPIView):
    serializer_class = ParticipationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user, experience_id=self.kwargs.get("experience_id")
        )

    def get_queryset(self):
        return Participation.objects.filter(user=self.request.user).select_related(
            "experience"
        ).order_by("-created_at").distinct()


class ParticipationDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ParticipationSerializer
    permission_classes = [IsAuthenticated, IsParticipationOwner]

    def get_queryset(self):
        return Participation.objects.filter(user=self.request.user)

class ExperienceParticipantsApiView(generics.ListAPIView):
    serializer_class = ParticipationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        experience_id = self.kwargs["experience_id"]

        experience = get_object_or_404(
            Experience,
            pk=experience_id,
        )

        if experience.organizer != self.request.user:
            raise PermissionDenied()

        return Participation.objects.filter(
            experience=experience
        ).select_related("user")