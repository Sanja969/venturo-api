from django.urls import path

from .views import (
    ProfileDetailApiView,
    PublicProfileDetailApiView,
    PublicProfileListApiView,
    SeedDatabaseApiView,
    CreateAdminApiView,
)

urlpatterns = [
    path("profile/", ProfileDetailApiView.as_view()),
    path("users/", PublicProfileListApiView.as_view()),
    path("users/<int:pk>/", PublicProfileDetailApiView.as_view()),
    path("admin/seed/", SeedDatabaseApiView.as_view()),
]
