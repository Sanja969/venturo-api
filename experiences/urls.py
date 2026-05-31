from django.urls import path

from .views import ExperienceDetailApiView, ExperienceListApiView, FavoriteExperienceApi, FavoriteExperienceListApiView

urlpatterns = [
    path("", ExperienceListApiView.as_view()),
    path("<int:pk>/", ExperienceDetailApiView.as_view()),
    path("favorite/<int:pk>/", FavoriteExperienceApi.as_view()),
    path("favorites/", FavoriteExperienceListApiView.as_view()),
]