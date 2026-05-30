from django.urls import path

from .views import ParticipationDetailApiView, ParticipationListCreateApiView, UserParticipationListApiView

urlpatterns = [
    path("participations/", UserParticipationListApiView.as_view()),
    path("experiences/<int:experience_id>/participations/", ParticipationListCreateApiView.as_view()),
    path("participations/<int:pk>/", ParticipationDetailApiView.as_view()),
]
