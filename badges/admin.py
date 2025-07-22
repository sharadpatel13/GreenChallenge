from django.contrib import admin
from .models import Badge, UserProofUpload, LeaderboardEntry, Challenge

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description') # customize what is displayed

@admin.register(UserProofUpload)
class UserProofUploadAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge_title', 'approved', 'rejected')

@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'points')

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty_points', 'duration', 'created_at', 'badge')  # Customize this
    list_filter = ('difficulty_points', 'created_at', 'badge') #This displays them on the right side so you can easily see and customize it
    search_fields = ('title', 'description')