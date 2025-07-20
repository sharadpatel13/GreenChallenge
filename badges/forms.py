from django import forms
from .models import UserProofUpload

class SubmitProofForm(forms.ModelForm):
    class Meta:
        model = UserProofUpload
        fields = ['challenge', 'proof']
        widgets = {
            'challenge': forms.Select(attrs={'class': 'form-control'}),
            'proof': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
