from django.urls import path
from .views import SubmitProofView, MyChallengesView, LeaderboardView, assign_badge_view, review_proofs

urlpatterns = [
    path('submit-proof/', SubmitProofView.as_view(), name='submit-proof'),
    path('my-challenges/', MyChallengesView.as_view(), name='my-challenges'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('assign-badge/<int:proof_id>/', assign_badge_view, name='assign-badge'),
    path('review-proofs/', review_proofs, name='review-proofs'),
]

