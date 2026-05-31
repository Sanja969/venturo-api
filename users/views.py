from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.models import User
from users.serializers import ProfileSerializer

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
    def post(self, request):
        call_command("seed")
        return Response({"detail": "Database seeded successfully."})