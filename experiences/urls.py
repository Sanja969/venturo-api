from django.urls import path

from .views import ExperienceDetailApiView, ExperienceListApiView

urlpatterns = [
    path("", ExperienceListApiView.as_view()),
     path("<int:pk>/", ExperienceDetailApiView.as_view()),
]