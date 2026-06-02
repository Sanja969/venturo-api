from django.urls import path

from .views import (
    ExperienceParticipantsApiView,
    ParticipationDetailApiView,
    ParticipationListCreateApiView,
)

urlpatterns = [
    path("participations/", ParticipationListCreateApiView.as_view()),
    path(
        "experiences/<int:experience_id>/participations/",
        ParticipationListCreateApiView.as_view(),
    ),
    path("participations/<int:pk>/", ParticipationDetailApiView.as_view()),
    path(
        "experiences/<int:experience_id>/participants/",
        ExperienceParticipantsApiView.as_view(),
    ),
]
