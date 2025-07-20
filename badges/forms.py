from django import forms
from .models import UserProofUpload

class SubmitProofForm(forms.ModelForm):
    class Meta:
        model = UserProofUpload
        fields = ['challenge_title', 'file_upload']
        widgets = {
            'challenge_title': forms.TextInput(attrs={'class': 'form-control'}),
            'file_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class BadgeAssignForm(forms.ModelForm):
    class Meta:
        model = UserProofUpload
        fields = ['badge_awarded']
        widgets = {
            'badge_awarded': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'badge_awarded': 'Assign Badge',
        }
