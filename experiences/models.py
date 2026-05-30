from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Experience(models.Model):
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organized_experiences",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="experiences",
    )

    title = models.CharField(max_length=255)

    description = models.TextField()

    location = models.CharField(max_length=255)

    difficulty = models.CharField(max_length=30, blank=True, default="")
    meeting_point = models.CharField(max_length=255, blank=True, default="")
    is_spontaneous = models.BooleanField(default=False)

    start_date = models.DateTimeField()

    end_date = models.DateTimeField()

    max_participants = models.PositiveIntegerField(
        default=10, validators=[MinValueValidator(1)]
    )

    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def going_count(self):
        return self.participations.filter(status="going").count()

    @property
    def spots_left(self):
        return self.max_participants - self.going_count


class ExperienceImage(models.Model):
    experience = models.ForeignKey(
        Experience, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="experiences/")
    caption = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.experience.title}"
