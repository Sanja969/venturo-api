from django.urls import path

from .views import ReviewListCreateApiView, ReviewDetailApiView

urlpatterns = [
    path("experiences/<int:experience_id>/reviews/", ReviewListCreateApiView.as_view()),
    path("reviews/<int:pk>/", ReviewDetailApiView.as_view()),
]