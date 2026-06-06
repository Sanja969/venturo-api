from django.db import models
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from experiences.models import Experience, FavoriteExperience
from django.db.models import Q, Prefetch

from reviews.models import Review

from .permissions import IsParticipationOwner

from .serializers import ExperienceParticipantSerializer, ParticipationSerializer
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
        return (
            (
                Participation.objects.filter(user=self.request.user).select_related(
                    "user",
                    "experience",
                    "experience__organizer",
                    "experience__category",
                )
            )
            .prefetch_related(
                "experience__images",
                Prefetch(
                    "experience__favorited_by",
                    queryset=FavoriteExperience.objects.filter(user=self.request.user),
                    to_attr="user_favorites",
                ),
                Prefetch(
                    "experience__participations",
                    queryset=Participation.objects.filter(user=self.request.user),
                    to_attr="user_participations",
                ),
                Prefetch(
                    "experience__reviews",
                    queryset=Review.objects.filter(user=self.request.user),
                    to_attr="user_reviews",
                ),
            )
            .annotate(
                experience_avg_rating=models.Avg("experience__reviews__rating"),
                experience_reviews_count=models.Count(
                    "experience__reviews",
                    distinct=True,
                ),
                experience_going_count_db=models.Count(
                    "experience__participations",
                    filter=Q(experience__participations__status="going"),
                    distinct=True,
                ),
            )
            .order_by("-created_at")
            .distinct()
        )


class ParticipationDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ParticipationSerializer
    permission_classes = [IsAuthenticated, IsParticipationOwner]

    def get_queryset(self):
        return Participation.objects.filter(user=self.request.user)


class ExperienceParticipantsApiView(generics.ListAPIView):
    serializer_class = ExperienceParticipantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        experience_id = self.kwargs["experience_id"]

        experience = get_object_or_404(
            Experience,
            pk=experience_id,
        )

        if experience.organizer != self.request.user:
            raise PermissionDenied()

        return (Participation.objects.filter(experience=experience)).select_related(
            "user",
        ).order_by("-created_at")
