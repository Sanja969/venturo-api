from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from ride_offers.models import RideOffer
from .permissions import IsRideOfferAuthorOrReadOnly
from .serializers import RideOfferSerializer


class RideOfferListCreateApiView(generics.ListCreateAPIView):
    serializer_class = RideOfferSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(
            driver=self.request.user, experience_id=self.kwargs.get("experience_id")
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
