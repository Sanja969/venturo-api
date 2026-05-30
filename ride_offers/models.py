from django.utils import timezone

from django.db import models
from django.conf import settings

from django.core.validators import MinValueValidator


class RideOffer(models.Model):
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ride_offers"
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        related_name="ride_offers",
        null=True,
        blank=True,
    )
    available_seats = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    departure_time = models.DateTimeField(null=True, default=timezone.now)
    departure_location = models.CharField(max_length=255, blank=True, default="")
    destination = models.CharField(max_length=255)
    note = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.experience:
            return f"Ride offer by {self.driver.username} for {self.experience.title}"
        return f"Ride offer by {self.driver.username}"
