from django.contrib import admin
from .models import Badge, UserProofUpload, LeaderboardEntry

admin.site.register(Badge)
admin.site.register(UserProofUpload)
admin.site.register(LeaderboardEntry)

