from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model

from online_marketplace.accounts.models import Comment

UserModel = get_user_model()


class RegisterUserForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        result = super().save(commit)
        return result


class LoginUserForm(auth_forms.AuthenticationForm):
    username = forms.CharField()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']