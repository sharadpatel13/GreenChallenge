from django import forms
from .models import UserProofUpload

class SubmitProofForm(forms.ModelForm):
    class Meta:
        model = UserProofUpload
        fields = ['challenge_title', 'file_upload']
