from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import ActivityComment
from .permissions import IsCommentAuthorOrReadOnly
from .serializers import ActivityCommentSerializer


class ActivityCommentListCreateApiView(generics.ListCreateAPIView):
    serializer_class = ActivityCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user, experience_id=self.kwargs.get("experience_id")
        )

    def get_queryset(self):
        return ActivityComment.objects.filter(
            experience_id=self.kwargs.get("experience_id")
        )

class ActivityCommentDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivityCommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthorOrReadOnly]

    def get_queryset(self):
        return ActivityComment.objects.all()
