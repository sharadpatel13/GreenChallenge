from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Challenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty_points = models.IntegerField(default=10)  # Points awarded for completing
    duration = models.DurationField(help_text="e.g., 7 days, 1 month")
    created_at = models.DateTimeField(auto_now_add=True)
    badge = models.ForeignKey("Badge", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='badges/', null=True, blank=True)

    def __str__(self):
        return self.name
class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE) # change the "challenge" instead of challenge_title
    start_date = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"

class UserProofUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge_title = models.CharField(max_length=200)
    file_upload = models.FileField(upload_to='proof_uploads/')
    date_uploaded = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    badge_awarded = models.ForeignKey(Badge, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.user.username} - {self.challenge_title}"

class LeaderboardEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.points} pts"