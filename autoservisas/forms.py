from django import forms
from .models import UzsakymasReview, Profile, User


class UzsakymasReviewForm(forms.ModelForm):
    class Meta:
        model = UzsakymasReview
        fields = ('content', 'uzsakymas', 'reviewer')
        widgets = {
            'uzsakymas': forms.HiddenInput(),
            'reviewer': forms.HiddenInput()
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('picture',)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
