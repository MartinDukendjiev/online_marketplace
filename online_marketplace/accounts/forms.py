from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model

from online_marketplace.accounts.models import Comment, Rating

UserModel = get_user_model()


class RegisterUserForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        result = super().save(commit)
        return result


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value']