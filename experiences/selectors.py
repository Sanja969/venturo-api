from django.db import models
from django.db.models import Q, Prefetch

from experiences.models import Experience, FavoriteExperience
from participations.models import Participation
from reviews.models import Review


def get_optimized_experience_queryset(user=None):
    queryset = (
        Experience.objects
        .select_related("organizer", "category")
        .prefetch_related("images")
        .annotate(
            avg_rating=models.Avg("reviews__rating"),
            reviews_count=models.Count("reviews", distinct=True),
            going_count_db=models.Count(
                "participations",
                filter=Q(participations__status="going"),
                distinct=True,
            ),
        )
    )

    if user and user.is_authenticated:
        queryset = queryset.prefetch_related(
            Prefetch(
                "favorited_by",
                queryset=FavoriteExperience.objects.filter(user=user),
                to_attr="user_favorites",
            ),
            Prefetch(
                "participations",
                queryset=Participation.objects.filter(user=user),
                to_attr="user_participations",
            ),
            Prefetch(
                "reviews",
                queryset=Review.objects.filter(user=user),
                to_attr="user_reviews",
            ),
        )

    return queryset