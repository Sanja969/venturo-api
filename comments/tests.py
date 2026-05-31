from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from experiences.models import Experience, Category
from ride_offers.models import RideOffer
from comments.models import ActivityComment, RideComment


class CommentsApiTests(APITestCase):
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
            description="Nice trip",
            location="Rtanj",
            difficulty="easy",
            start_date=timezone.now() + timedelta(days=5),
            end_date=timezone.now() + timedelta(days=5, hours=5),
            max_participants=10,
            price=0,
        )

        self.ride_offer = RideOffer.objects.create(
            driver=self.user,
            experience=self.experience,
            departure_location="Belgrade",
            destination="Rtanj",
            departure_time=timezone.now() + timedelta(days=5),
            available_seats=3,
        )

    def test_authenticated_user_can_create_activity_comment(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            f"/api/experiences/{self.experience.id}/comments/",
            {"text": "Ima li mesta?"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ActivityComment.objects.count(), 1)
        
    def test_authenticated_user_can_create_ride_comment(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.post(
            f"/api/ride-offers/{self.ride_offer.id}/comments/",
            {"text": "Možeš li da staneš kod Autokomande?"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RideComment.objects.count(), 1)

    def test_list_activity_comments_for_experience(self):
        ActivityComment.objects.create(
            user=self.user,
            experience=self.experience,
            text="Super event",
        )

        response = self.client.get(
            f"/api/experiences/{self.experience.id}/comments/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)