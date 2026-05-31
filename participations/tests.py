from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from experiences.models import Experience, Category
from participations.models import Participation


class ParticipationApiTests(APITestCase):
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
            organizer=self.other_user,
            category=self.category,
            title="Rtanj hike",
            description="Nice trip",
            location="Rtanj",
            difficulty="easy",
            start_date=timezone.now() + timedelta(days=5),
            end_date=timezone.now() + timedelta(days=5, hours=5),
            max_participants=2,
            price=0,
        )
        
    def test_authenticated_user_can_create_participation(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            f"/api/experiences/{self.experience.id}/participations/",
            {"status": "going"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Participation.objects.count(), 1)

        participation = Participation.objects.first()
        self.assertEqual(participation.user, self.user)
        self.assertEqual(participation.experience, self.experience)
        self.assertEqual(participation.status, "going")
        
    def test_anonymous_user_cannot_create_participation(self):
        response = self.client.post(
            f"/api/experiences/{self.experience.id}/participations/",
            {"status": "going"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_user_cannot_participate_twice_same_experience(self):
        self.client.force_authenticate(user=self.user)

        Participation.objects.create(
            user=self.user,
            experience=self.experience,
            status="going",
        )

        response = self.client.post(
            f"/api/experiences/{self.experience.id}/participations/",
            {"status": "going"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Participation.objects.count(), 1)
        
    def test_list_participations_for_experience(self):
        self.client.force_authenticate(user=self.user)

        Participation.objects.create(
            user=self.user,
            experience=self.experience,
            status="going",
        )

        response = self.client.get(
            f"/api/experiences/{self.experience.id}/participations/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

# Create your tests here.
