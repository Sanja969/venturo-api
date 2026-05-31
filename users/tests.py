from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User


class UserProfileApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="sanja",
            email="sanja@test.com",
            password="testpass123",
            bio="Outdoor lover",
            location="Belgrade",
        )

        self.other_user = User.objects.create_user(
            username="bane",
            email="bane@test.com",
            password="testpass123",
            bio="Hiker",
            location="Uzice",
        )
        
    def test_authenticated_user_can_view_profile(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/profile/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "sanja")
        self.assertEqual(response.data["email"], "sanja@test.com")
        
    def test_anonymous_user_cannot_view_profile(self):
        response = self.client.get("/api/profile/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_public_users_list(self):
        response = self.client.get("/api/users/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        
    def test_public_user_detail(self):
        response = self.client.get(f"/api/users/{self.user.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "sanja")
        self.assertNotIn("email", response.data)
