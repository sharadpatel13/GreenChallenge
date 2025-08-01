from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProofUpload, LeaderboardEntry, Badge, UserActivity
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone

@receiver(post_save, sender=UserProofUpload)
def award_badge_on_approval(sender, instance, created, **kwargs):
    # Only act if instance is approved and badge_awarded is not set
    if not created and instance.approved and not instance.badge_awarded:
        user = instance.user

        points_to_award = 10

        leaderboard_entry, created = LeaderboardEntry.objects.get_or_create(user=user)
        leaderboard_entry.points += points_to_award
        leaderboard_entry.save()

        badge, _ = Badge.objects.get_or_create(name='Challenge Completer')
        instance.badge_awarded = badge

        # Save with update_fields to minimize triggers
        instance.save(update_fields=['badge_awarded'])

@receiver(user_logged_in)
def increment_login_count(sender, request, user, **kwargs):
    activity, _ = UserActivity.objects.get_or_create(user=user)
    activity.login_count += 1
    activity.last_login = timezone.now()
    activity.save()
    # Optional: store in session for quick template access
    request.session['login_count'] = activity.login_count

