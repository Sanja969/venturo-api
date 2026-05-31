from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from experiences.models import Experience, Category
from participations.models import Participation
from reviews.models import Review


class ReviewApiTests(APITestCase):
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
            start_date=timezone.now() - timedelta(days=2),
            end_date=timezone.now() - timedelta(days=2, hours=-5),
            max_participants=10,
            price=0,
        )
        
    def test_participant_can_create_review(self):
        self.client.force_authenticate(user=self.user)

        Participation.objects.create(
            user=self.user,
            experience=self.experience,
            status="going",
        )

        response = self.client.post(
            f"/api/experiences/{self.experience.id}/reviews/",
            {
                "rating": 5,
                "comment": "Great experience!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)

        review = Review.objects.first()
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.experience, self.experience)
        self.assertEqual(review.rating, 5)
        
    def test_non_participant_cannot_create_review(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            f"/api/experiences/{self.experience.id}/reviews/",
            {
                "rating": 5,
                "comment": "Great experience!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Review.objects.count(), 0)

    def test_user_cannot_review_same_experience_twice(self):
        self.client.force_authenticate(user=self.user)

        Participation.objects.create(
            user=self.user,
            experience=self.experience,
            status="going",
        )

        Review.objects.create(
            user=self.user,
            experience=self.experience,
            rating=4,
            comment="Nice",
        )

        response = self.client.post(
            f"/api/experiences/{self.experience.id}/reviews/",
            {
                "rating": 5,
                "comment": "Again",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Review.objects.count(), 1)
        
    def test_list_reviews_for_experience(self):
        Review.objects.create(
            user=self.user,
            experience=self.experience,
            rating=5,
            comment="Great",
        )

        response = self.client.get(
            f"/api/experiences/{self.experience.id}/reviews/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
# Create your tests here.
