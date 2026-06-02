from django.urls import path

from .views import (
    ExperienceDetailApiView,
    ExperienceListApiView,
    FavoriteExperienceApi,
    FavoriteExperienceListApiView,
    MyOrganizedExperiencesApiView
)

urlpatterns = [
    path("", ExperienceListApiView.as_view()),
    path("<int:pk>/", ExperienceDetailApiView.as_view()),
    path("<int:pk>/favorite/", FavoriteExperienceApi.as_view()),
    path("favorites/", FavoriteExperienceListApiView.as_view()),
]
