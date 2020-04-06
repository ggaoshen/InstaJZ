from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from Insta.models import InstaUser

# forms defined here handles user inputs

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta): # define meta data
        model = InstaUser # override AbstractUser from UserCreationForm
        fields = ('username', 'email', 'profile_pic') # 'username', 'email' from AbstractUser, profile_pic defined in InstaUser