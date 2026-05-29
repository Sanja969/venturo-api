from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .permissions import IsBookingOwner

from .serializers import BookingSerializer
from .models import Booking

class BookingListApiView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class BookingDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsBookingOwner]
        
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)