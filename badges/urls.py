from django.urls import path
from .views import SubmitProofView, MyChallengesView, LeaderboardView, assign_badge_view, review_proofs, ChallengeCreateView, ChallengeListView, ChallengeDetailView, MyProgressView

urlpatterns = [
    path('submit-proof/', SubmitProofView.as_view(), name='submit-proof'),
    path('my-challenges/', MyChallengesView.as_view(), name='my-challenges'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('assign-badge/<int:proof_id>/', assign_badge_view, name='assign-badge'),
    path('review-proofs/', review_proofs, name='review-proofs'),

    path('challenges/create/', ChallengeCreateView.as_view(), name='create_challenge'), #ADD
    path('challenges/', ChallengeListView.as_view(), name='challenge_list'), #ADD
    path('challenges/<int:pk>/', ChallengeDetailView.as_view(), name='challenge_detail'), #ADD
   # path('challenges/<int:pk>/join/', JoinChallengeView.as_view(), name='join_challenge'),  # Remove this, we don't need them anymore
    path('my-progress/', MyProgressView.as_view(), name='my_progress'),  # Add this
]