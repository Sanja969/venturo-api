from django.urls import path

from .views import ActivityCommentDetailApiView, ActivityCommentListCreateApiView

urlpatterns = [
    path("experiences/<int:experience_id>/comments/", ActivityCommentListCreateApiView.as_view()),
    path("comments/<int:pk>/", ActivityCommentDetailApiView.as_view()),
]