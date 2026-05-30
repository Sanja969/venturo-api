from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .permissions import IsParticipationOwner

from .serializers import ParticipationSerializer
from .models import Participation


class ParticipationListApiView(generics.ListCreateAPIView):
    serializer_class = ParticipationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Participation.objects.filter(user=self.request.user)


class ParticipationDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ParticipationSerializer
    permission_classes = [IsAuthenticated, IsParticipationOwner]

    def get_queryset(self):
        return Participation.objects.filter(user=self.request.user)
