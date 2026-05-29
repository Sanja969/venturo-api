from django.db import models
from django.conf import settings


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings"
    )

    experience = models.ForeignKey(
        "experiences.Experience", on_delete=models.CASCADE, related_name="bookings"
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
      constraints = [models.UniqueConstraint(fields=["user", "experience"], name="unique_user_experience_booking")]

    def __str__(self):
        return f"{self.user.username} booked {self.experience.title}"
  