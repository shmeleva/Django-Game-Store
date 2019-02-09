from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from game_store.apps.users.models import UserRole, UserProfile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=150)
    role = forms.ChoiceField(
        choices=[(role.value, role.name) for role in UserRole],
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=True)
        user_profile = UserProfile(user=user, role=self.cleaned_data['role'])
        user_profile.save()
        return user_profile