from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from game_store.apps.users.models import UserRole, UserProfile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=[(role.value, role.name) for role in UserRole],
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=True)
        user_profile = UserProfile(user=user, role=self.cleaned_data['role'])
        user_profile.save()
        return user_profile