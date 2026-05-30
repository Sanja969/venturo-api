from django.urls import path

from .views import ParticipationListApiView, ParticipationDetailApiView

urlpatterns = [
    path("", ParticipationListApiView.as_view()),
    path("<int:pk>/", ParticipationDetailApiView.as_view()),
]
