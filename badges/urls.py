from django.urls import path
from .views import SubmitProofView

urlpatterns = [
    path('submit-proof/', SubmitProofView.as_view(), name='submit-proof'),
]
