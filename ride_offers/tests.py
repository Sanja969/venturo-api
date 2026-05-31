from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from experiences.models import Experience, Category
from ride_offers.models import RideOffer


class RideOfferApiTests(APITestCase):
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
        
    def test_list_all_ride_offers(self):
        response = self.client.get("/api/ride-offers/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        
    def test_list_ride_offers_for_experience(self):
        response = self.client.get(
            f"/api/experiences/{self.experience.id}/ride-offers/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_authenticated_user_can_create_ride_offer(self):
        self.client.force_authenticate(user=self.other_user)

        data = {
            "departure_location": "Novi Sad",
            "destination": "Tara",
            "departure_time": (timezone.now() + timedelta(days=7)).isoformat(),
            "available_seats": 2,
            "note": "Krećem ujutru.",
        }

        response = self.client.post(
            "/api/ride-offers/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RideOffer.objects.count(), 2)

        created_ride = RideOffer.objects.get(destination="Tara")
        self.assertEqual(created_ride.driver, self.other_user)
        
    def test_owner_can_update_ride_offer(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            f"/api/ride-offers/{self.ride_offer.id}/",
            {"available_seats": 4},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.ride_offer.refresh_from_db()
        self.assertEqual(self.ride_offer.available_seats, 4)
        
    def test_non_owner_cannot_update_ride_offer(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.patch(
            f"/api/ride-offers/{self.ride_offer.id}/",
            {"available_seats": 4},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
