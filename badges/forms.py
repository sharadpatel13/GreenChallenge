from django import forms
from .models import UserProofUpload
from .models import Challenge, Badge, UserProgress

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
class ChallengeForm(forms.ModelForm):
    badge = forms.ModelChoiceField(
        queryset=Badge.objects.all(),
        empty_label="-- Select a Badge --", # optional, shows a default choice
        required=False # Adjust based on if a badge is always required
    )

    class Meta:
        model = Challenge
        fields = ['title', 'description', 'difficulty_points', 'duration', 'badge']  #Include the badge

class JoinChallengeForm(forms.Form):
    challenge_id = forms.IntegerField(widget=forms.HiddenInput())