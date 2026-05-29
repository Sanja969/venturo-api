from django.db import models
from django.conf import settings


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    experience = models.ForeignKey(
        "experiences.Experience", on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
      constraints = [models.UniqueConstraint(fields=["user", "experience"], name="unique_user_experience_review")]

    def __str__(self):
        return f"{self.user.username} reviewed for {self.experience.title}"
