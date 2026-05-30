from rest_framework import generics

from .permissions import IsReviewOwner

from .models import Review
from .serializers import ReviewSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class ReviewListCreateApiView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        experience_id = self.kwargs.get("experience_id")
        return Review.objects.filter(experience_id=experience_id)

    def perform_create(self, serializer):
        experience_id = self.kwargs.get("experience_id")
        serializer.save(user=self.request.user, experience_id=experience_id)


class ReviewDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewOwner]
    queryset = Review.objects.all()

    
