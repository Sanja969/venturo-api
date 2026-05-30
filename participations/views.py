from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from experiences.models import Experience

from .permissions import IsParticipationOwner

from .serializers import ParticipationSerializer
from .models import Participation

class ParticipationListCreateApiView(generics.ListCreateAPIView):
    serializer_class = ParticipationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, experience_id=self.kwargs.get("experience_id"))

    def get_queryset(self):
        queryset = Participation.objects.all()
        experience_id = self.kwargs.get("experience_id")
        if experience_id:
          return queryset.filter(experience_id=experience_id)
        return queryset


class ParticipationDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ParticipationSerializer
    permission_classes = [IsAuthenticated, IsParticipationOwner]

    def get_queryset(self):
        return Participation.objects.filter(user=self.request.user)
