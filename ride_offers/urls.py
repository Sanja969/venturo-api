from django.urls import path

from .views import RideOfferDetailApiView, RideOfferListCreateApiView

urlpatterns = [
    path("ride-offers/", RideOfferListCreateApiView.as_view()),
    path("experiences/<int:experience_id>/ride-offers/", RideOfferListCreateApiView.as_view()),
    path("ride-offers/<int:pk>/", RideOfferDetailApiView.as_view()),
]