from django.db import models
from django.conf import settings


class Participation(models.Model):
    STATUS_CHOICES = [
        ("interested", "Interested"),
        ("going", "Going"),
        ("maybe", "Maybe"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="participations",
    )

    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        related_name="participations",
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="going")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "experience"],
                name="unique_user_experience_participation",
            )
        ]

    def __str__(self):
        return f"{self.user.username} is {self.status} for {self.experience.title}"
