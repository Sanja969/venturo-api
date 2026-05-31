from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView, Response
from .permissions import IsExperienceOrganizerOrReadOnly

from .serializers import ExperienceSerializer

from .models import Experience, FavoriteExperience, FavoriteExperience


class ExperienceListApiView(generics.ListCreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):

        serializer.save(organizer=self.request.user)


class ExperienceDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsExperienceOrganizerOrReadOnly]
    
class FavoriteExperienceListApiView(generics.ListAPIView):
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Experience.objects.filter(favorited_by__user=self.request.user)

class FavoriteExperienceApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        experience = get_object_or_404(Experience, pk=pk)
        breakpoint()
        _, created = FavoriteExperience.objects.get_or_create(
            user=request.user, experience=experience
        )
        
        if not created:
            return Response(
                {"status": "experience already in favorites"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"status": "experience added to favorites"}, status=status.HTTP_201_CREATED
        )

    def delete(self, request, pk):
        experience = get_object_or_404(Experience, pk=pk)
        favorite = FavoriteExperience.objects.filter(user=request.user, experience=experience).first()
        if not favorite:
            return Response(
                {"status": "experience not in favorites"}, status=status.HTTP_400_BAD_REQUEST
            )
        favorite.delete()
        return Response({"status": "experience removed from favorites"}, status=status.HTTP_204_NO_CONTENT)