from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField( required=True)
    last_name = forms.CharField( required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'profile_picture', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        phone_number = self.cleaned_data.get('phone_number')
        profile_picture = self.cleaned_data.get('profile_picture')

        if not profile_picture:
            profile_picture = 'profile_pics/default.jpg'

        if commit:
            user.save()

        Profile.objects.update_or_create(
            user=user,
            defaults={'phone_number': phone_number, 'profile_picture': profile_picture},
        )
        
        return user   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ['phone_number', 'profile_picture']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Get the user instance passed during initialization
        super().__init__(*args, **kwargs)
        self.user = user

        # Add user fields to the form
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email

        # Ensure user fields are added first
        user_fields = ['first_name', 'last_name', 'email']
        profile_fields = list(self.fields.keys())  # Existing profile fields
        ordered_fields = user_fields + [f for f in profile_fields if f not in user_fields]

        # Reorder the fields
        self.fields = {key: self.fields[key] for key in ordered_fields}

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        # Save user info
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        self.user.email = self.cleaned_data['email']
        if commit:
            self.user.save()

        # Save profile info
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile