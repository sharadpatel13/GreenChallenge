from django import forms
from .models import UserProofUpload
from .models import Challenge, Badge, UserProgress
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User

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

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email address'
        })
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New password',
            'autocomplete': 'new-password',
        })
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password',
            'autocomplete': 'new-password',
        })
    )

class CustomSignUpForm(UserCreationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    email = forms.EmailField(
        label='Email address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')