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
