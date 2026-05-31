from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from comments.models import ActivityComment, RideComment
import experiences
from participations.models import Participation
from reviews.models import Review
from ride_offers.models import RideOffer
import users
from users.models import User
from experiences.models import Experience, Category, FavoriteExperience
import random

users_data = [
    ("sanja", "sanja@example.com"),
    ("bane", "bane@example.com"),
    ("milica", "milica@example.com"),
    ("marko", "marko@example.com"),
    ("nikola", "nikola@example.com"),
    ("jelena", "jelena@example.com"),
]

locations = [
    "Tara",
    "Rtanj",
    "Kopaonik",
    "Zlatibor",
    "Fruška Gora",
]

category_names = [
    "Hiking",
    "Cycling",
    "Running",
    "Trail Running",
    "Camping",
    "Kayaking",
    "Climbing",
    "Mountaineering",
    "Yoga",
    "Meditation",
    "Volunteering",
    "Tree Planting",
    "Photography",
    "Road Trip",
    "Dog Walking",
    "Bird Watching",
    "Outdoor Fitness",
]

comments = [
    "Da li ima mesta?",
    "Kakav je teren?",
    "Da li neko kreće iz Beograda?",
    "Deluje super!",
    "Vidimo se tamo!",
]

review_comments = [
    "Great experience!",
    "Amazing organization.",
    "Beautiful nature and good people.",
    "Would join again.",
    "Really nice outdoor day.",
]

ride_notes = [
    "Krećem ujutru, mogu da pokupim ljude usput.",
    "Imam mesta za dvoje.",
    "Polazak iz centra.",
    "Mogu da stanem kod pumpe.",
]


class Command(BaseCommand):
    help = "Seed database with sample data"

    def handle(self, *args, **options):
        self.stdout.write("Deleting old seed data...")

        RideComment.objects.all().delete()

        ActivityComment.objects.all().delete()

        Review.objects.all().delete()

        FavoriteExperience.objects.all().delete()

        Participation.objects.all().delete()

        RideOffer.objects.all().delete()

        Experience.objects.all().delete()

        Category.objects.all().delete()

        User.objects.filter(is_superuser=False).delete()

        self.stdout.write("Creating seed data...")

        users = []
        for username, email in users_data:
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={"email": email},
            )

            user.set_password("password123")

            user.save()

            users.append(user)

        categories = []
        for name in category_names:
            category_name, _ = Category.objects.get_or_create(name=name)
            categories.append(category_name)

        experiences = []
        for i in range(20):
            experience, _ = Experience.objects.get_or_create(
                title=f"{random.choice(locations)} Hike #{i+1}",
                defaults={
                    "organizer": random.choice(users),
                    "category": random.choice(categories),
                    "description": "Weekend hiking trip",
                    "location": random.choice(locations),
                    "difficulty": random.choice(["easy", "medium", "hard"]),
                    "start_date": timezone.now() + timedelta(days=7),
                    "end_date": timezone.now() + timedelta(days=7, hours=6),
                    "max_participants": 15,
                    "price": 0,
                },
            )
            experiences.append(experience)

        # Participations
        for experience in experiences:
            selected_users = random.sample(users, random.randint(1, min(4, len(users))))

            for user in selected_users:
                if user != experience.organizer:
                    Participation.objects.get_or_create(
                        user=user,
                        experience=experience,
                        defaults={"status": random.choice(["going", "interested", "maybe"])},
                    )

        # Activity comments
        for experience in experiences:
            for _ in range(random.randint(1, 3)):
                ActivityComment.objects.create(
                    user=random.choice(users),
                    experience=experience,
                    text=random.choice(comments),
                )

        # Reviews only for users who are going
        going_participations = list(Participation.objects.filter(status="going"))

        for participation in random.sample(
            going_participations,
            min(15, len(going_participations)),
        ):
            Review.objects.get_or_create(
                user=participation.user,
                experience=participation.experience,
                defaults={
                    "rating": random.randint(3, 5),
                    "comment": random.choice(review_comments),
                },
            )

        # Ride offers
        ride_offers = []

        for experience in random.sample(experiences, min(10, len(experiences))):
            ride_offer = RideOffer.objects.create(
                driver=random.choice(users),
                experience=experience,
                departure_location=random.choice(["Belgrade", "Novi Sad", "Uzice", "Cacak"]),
                destination=experience.location,
                departure_time=experience.start_date - timedelta(hours=3),
                available_seats=random.randint(1, 4),
                note=random.choice(ride_notes),
            )

            ride_offers.append(ride_offer)

        # Standalone ride offers
        for i in range(5):
            ride_offer = RideOffer.objects.create(
                driver=random.choice(users),
                experience=None,
                departure_location=random.choice(["Belgrade", "Novi Sad", "Uzice", "Cacak"]),
                destination=random.choice(locations),
                departure_time=timezone.now() + timedelta(days=random.randint(1, 30)),
                available_seats=random.randint(1, 4),
                note=random.choice(ride_notes),
            )

            ride_offers.append(ride_offer)

        # Ride comments
        for ride_offer in ride_offers:
            for _ in range(random.randint(1, 2)):
                RideComment.objects.create(
                    user=random.choice(users),
                    ride_offer=ride_offer,
                    text=random.choice(
                        [
                            "Da li imaš još jedno mesto?",
                            "Možeš li da staneš usput?",
                            "Kada tačno krećeš?",
                            "Zainteresovan/a sam za prevoz.",
                        ]
                    ),
                )

        # Favorites
        for user in users:
            favorite_experiences = random.sample(
                experiences,
                random.randint(2, min(5, len(experiences))),
            )

            for experience in favorite_experiences:
                FavoriteExperience.objects.get_or_create(
                    user=user,
                    experience=experience,
                )

                self.stdout.write(self.style.SUCCESS("Seed data created successfully!"))
