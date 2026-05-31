from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from experiences.models import Experience, Category, FavoriteExperience


class ExperienceApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="sanja",
            email="sanja@test.com",
            password="testpass123",
        )

        self.other_user = User.objects.create_user(
            username="bane",
            email="bane@test.com",
            password="testpass123",
        )

        self.category = Category.objects.create(name="Hiking")

        self.experience = Experience.objects.create(
            organizer=self.user,
            category=self.category,
            title="Rtanj hike",
            description="Nice hiking trip",
            location="Rtanj",
            difficulty="easy",
            start_date=timezone.now() + timedelta(days=5),
            end_date=timezone.now() + timedelta(days=5, hours=5),
            max_participants=10,
            price=0,
        )
        
    def test_authenticated_user_can_create_experience(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "category": self.category.id,
            "title": "Tara hike",
            "description": "Beautiful trip",
            "location": "Tara",
            "difficulty": "easy",
            "start_date": (timezone.now() + timedelta(days=10)).isoformat(),
            "end_date": (timezone.now() + timedelta(days=10, hours=4)).isoformat(),
            "max_participants": 12,
            "price": "0.00",
        }

        response = self.client.post("/api/experiences/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Experience.objects.count(), 2)

        created_experience = Experience.objects.get(title="Tara hike")
        self.assertEqual(created_experience.organizer, self.user)
    
    def test_anonymous_user_cannot_create_experience(self):
        data = {
            "category": self.category.id,
            "title": "Tara hike",
            "description": "Beautiful trip",
            "location": "Tara",
            "difficulty": "easy",
            "start_date": (timezone.now() + timedelta(days=10)).isoformat(),
            "end_date": (timezone.now() + timedelta(days=10, hours=4)).isoformat(),
            "max_participants": 12,
            "price": "0.00",
        }

        response = self.client.post("/api/experiences/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_organizer_can_update_experience(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            f"/api/experiences/{self.experience.id}/",
            {"title": "Updated Rtanj hike"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Updated Rtanj hike")
        
    def test_non_organizer_cannot_update_experience(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.patch(
            f"/api/experiences/{self.experience.id}/",
            {"title": "Hacked title"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Rtanj hike")
        
    def test_authenticated_user_can_favorite_experience(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            f"/api/experiences/{self.experience.id}/favorite/"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FavoriteExperience.objects.count(), 1)