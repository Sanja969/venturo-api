from django.urls import path

from .views import (
    RideOfferDetailApiView,
    RideOfferListCreateApiView,
    RideRequestCreateApiView,
    RideRequestDetailApiView,
)

urlpatterns = [
    path("ride-offers/", RideOfferListCreateApiView.as_view()),
    path(
        "experiences/<int:experience_id>/ride-offers/",
        RideOfferListCreateApiView.as_view(),
    ),
    path("ride-offers/<int:pk>/", RideOfferDetailApiView.as_view()),
    path(
        "ride-offers/<int:ride_offer_id>/requests/", RideRequestCreateApiView.as_view()
    ),
    path(
        "ride-requests/<int:pk>/",
        RideRequestDetailApiView.as_view(),
    ),
]
