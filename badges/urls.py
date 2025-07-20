from django.urls import path
from .views import SubmitProofView, MyChallengesView

urlpatterns = [
    path('submit-proof/', SubmitProofView.as_view(), name='submit-proof'),
    path('my-challenges/', MyChallengesView.as_view(), name='my-challenges'),
]

