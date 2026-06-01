from datetime import timezone

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from comments import serializers
from experiences.models import Experience
from ride_offers.models import RideOffer
from .permissions import IsRideOfferAuthorOrReadOnly
from .serializers import RideOfferSerializer
from django.shortcuts import get_object_or_404


class RideOfferListCreateApiView(generics.ListCreateAPIView):
    serializer_class = RideOfferSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        experience = get_object_or_404(Experience, pk=self.kwargs["experience_id"])
        if experience.end_date < timezone.now():
            raise serializers.ValidationError("Cannot offer a ride for a past experience.")
        serializer.save(
            driver=self.request.user, experience = experience, destination=experience.location
        )

    def get_queryset(self):
        queryset = RideOffer.objects.all()
        experience_id = self.kwargs.get("experience_id")
        if experience_id:
            return queryset.filter(experience_id=experience_id)

        return queryset


class RideOfferDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RideOfferSerializer
    permission_classes = [IsAuthenticated, IsRideOfferAuthorOrReadOnly]

    def get_queryset(self):
        return RideOffer.objects.all()
