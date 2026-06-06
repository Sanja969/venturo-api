from django.utils import timezone

from django.shortcuts import get_object_or_404
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView, PermissionDenied, Response
from django.db.models import Q, Prefetch
from django.db import models
from django.db.models import Avg, Count, Q, F, IntegerField, ExpressionWrapper

from participations.models import Participation
from reviews.models import Review

from .permissions import IsExperienceOrganizerOrReadOnly

from .serializers import (
    CategorySerializer,
    ExperienceImageCreateSerializer,
    ExperienceSerializer,
)

from .models import Experience, FavoriteExperience, FavoriteExperience, Category
from .selectors import get_optimized_experience_queryset


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
        queryset = get_optimized_experience_queryset(self.request.user)
        category = self.request.query_params.get("category")
        location = self.request.query_params.get("location")
        difficulty = self.request.query_params.get("difficulty")
        is_spontaneous = self.request.query_params.get("is_spontaneous")
        search = self.request.query_params.get("search")
        timeframe = self.request.query_params.get("timeframe", "upcoming")

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
    def get_queryset(self):
        return get_optimized_experience_queryset(self.request.user)

    serializer_class = ExperienceSerializer
    permission_classes = [IsExperienceOrganizerOrReadOnly]


class FavoriteExperienceListApiView(generics.ListAPIView):
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            get_optimized_experience_queryset(self.request.user)
            .filter(favorited_by__user=self.request.user)
            .distinct()
        )


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


class CategoryListApiView(generics.ListAPIView):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = []


class MyOrganizedExperiencesApiView(generics.ListAPIView):
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            get_optimized_experience_queryset(self.request.user)
            .filter(organizer=self.request.user)
            .order_by("-created_at")
        )


class ExperienceImageCreateApiView(generics.CreateAPIView):
    serializer_class = ExperienceImageCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        experience = get_object_or_404(
            Experience,
            pk=self.kwargs["experience_id"],
        )

        if experience.organizer != self.request.user:
            raise PermissionDenied(
                "Only organizer can upload images for this experience."
            )

        serializer.save(experience=experience)
