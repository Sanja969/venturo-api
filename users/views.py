from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.models import User
from users.serializers import ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.management import call_command

class ProfileDetailApiView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class PublicProfileDetailApiView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    
class PublicProfileListApiView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    
class SeedDatabaseApiView(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request):

        call_command("seed")

        return Response({"detail": "Database seeded successfully."})