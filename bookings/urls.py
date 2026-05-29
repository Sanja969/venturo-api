from django.urls import path

from .views import BookingListApiView, BookingDetailApiView

urlpatterns = [
    path("", BookingListApiView.as_view()),
    path("<int:pk>/", BookingDetailApiView.as_view()),
]