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
        user.userprofile.role = self.cleaned_data['role']
        user.save()
        return user.userprofile

class ProfileForm(forms.ModelForm):
    username = forms.CharField(required=False, widget=forms.TextInput(attrs={'disabled':'disabled'}))
    email = forms.CharField(required=False, widget=forms.TextInput(attrs={'disabled':'disabled'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_username(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.username
        else:
            return self.cleaned_data['username']

    def clean_email(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.email
        else:
            return self.cleaned_data['email']

class AccessTokenForm(forms.Form):
    access_token = forms.CharField(max_length=128, required=False, widget=forms.TextInput(attrs={'disabled':'disabled'}))

class UserTypeForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('role',)