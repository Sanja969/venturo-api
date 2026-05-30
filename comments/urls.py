from django.urls import path

from .views import ActivityCommentDetailApiView, ActivityCommentListCreateApiView, RideCommentDetailApiView, RideCommentListCreateApiView

urlpatterns = [
    path("experiences/<int:experience_id>/comments/", ActivityCommentListCreateApiView.as_view()),
    path("comments/<int:pk>/", ActivityCommentDetailApiView.as_view()),
    path("ride-offers/<int:ride_offer_id>/comments/", RideCommentListCreateApiView.as_view()),
    path("ride-comments/<int:pk>/", RideCommentDetailApiView.as_view()),
]