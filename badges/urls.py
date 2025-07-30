from django.urls import path
from .views import (
    ChallengeCreateView,
    ChallengeListView,
    ChallengeDetailView,
    LeaderboardView,
    MyChallengesView,
    SubmitProofView,
    assign_badge_view,
    JoinChallengeView,
    ReviewProofsView,
    LoginView,
    LogoutView,
    ForgotPasswordView,
    ForgotPasswordDoneView,
    ForgotPasswordConfirmView,
    ForgotPasswordCompleteView,
    SignUpView,
    AboutView
)

urlpatterns = [
    path('challenges/create/', ChallengeCreateView.as_view(), name='create_challenge'),
    path('challenges/', ChallengeListView.as_view(), name='challenge_list'),
    path('challenges/<int:pk>/', ChallengeDetailView.as_view(), name='challenge_detail'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('my-challenges/', MyChallengesView.as_view(), name='my-challenges'),
    path('submit-proof/', SubmitProofView.as_view(), name='submit-proof'),
    path('assign-badge/<int:proof_id>/', assign_badge_view, name='assign-badge'),
    path('review-proofs/', ReviewProofsView.as_view(), name='review_proofs'),
    path('challenges/<int:challenge_id>/join/', JoinChallengeView.as_view(), name='join_challenge'),
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', ForgotPasswordView.as_view(), name='password_reset'),
    path('password-reset/done/',ForgotPasswordDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',ForgotPasswordConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',ForgotPasswordCompleteView.as_view(),name='password_reset_complete'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('about/', AboutView.as_view(), name='about'),


]