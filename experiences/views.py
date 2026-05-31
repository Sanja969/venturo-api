from django.utils import timezone

from django.shortcuts import get_object_or_404
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView, Response
from django.db.models import Q
from django.db import models
from django.db.models import Avg, Count, Q, F, IntegerField, ExpressionWrapper

from .permissions import IsExperienceOrganizerOrReadOnly

from .serializers import ExperienceSerializer

from .models import Experience, FavoriteExperience, FavoriteExperience


class ExperienceListApiView(generics.ListCreateAPIView):
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [filters.OrderingFilter]
    ordering_fields = [
        "start_date",
        "created_at",
        "price",
        "max_participants",
        "avg_rating",
        "reviews_count",
        "going_count_db",
    ]
    ordering = ["start_date"]

    def get_queryset(self):
        category = self.request.query_params.get("category")
        location = self.request.query_params.get("location")
        difficulty = self.request.query_params.get("difficulty")
        is_spontaneous = self.request.query_params.get("is_spontaneous")
        search = self.request.query_params.get("search")
        timeframe = self.request.query_params.get("timeframe", "upcoming")

        queryset = Experience.objects.annotate(
            avg_rating=models.Avg("reviews__rating"),
            reviews_count=models.Count("reviews", distinct=True),
            going_count_db=models.Count(
                "participations",
                filter=Q(participations__status="going"),
                distinct=True,
            ),
        )

        if category:
            queryset = queryset.filter(category__name__icontains=category)

        if location:
            queryset = queryset.filter(location__icontains=location)
        if is_spontaneous is not None:
            is_spontaneous = is_spontaneous.lower() == "true"
            queryset = queryset.filter(is_spontaneous=is_spontaneous)
        if difficulty:
            queryset = queryset.filter(difficulty__iexact=difficulty)
        if search:
            terms = search.split()
            for term in terms:
                queryset = queryset.filter(
                    Q(title__icontains=term)
                    | Q(description__icontains=term)
                    | Q(location__icontains=term)
                    | Q(category__name__icontains=term)
                )
        if timeframe == "upcoming":
            queryset = queryset.filter(start_date__gte=timezone.now())
        elif timeframe == "past":
            queryset = queryset.filter(end_date__lt=timezone.now())
        elif timeframe == "all":
            pass

        return queryset

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
        _, created = FavoriteExperience.objects.get_or_create(
            user=request.user, experience=experience
        )

        if not created:
            return Response(
                {"status": "experience already in favorites"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"status": "experience added to favorites"}, status=status.HTTP_201_CREATED
        )

    def delete(self, request, pk):
        experience = get_object_or_404(Experience, pk=pk)
        favorite = FavoriteExperience.objects.filter(
            user=request.user, experience=experience
        ).first()
        if not favorite:
            return Response(
                {"status": "experience not in favorites"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        favorite.delete()
        return Response(
            {"status": "experience removed from favorites"},
            status=status.HTTP_204_NO_CONTENT,
        )
