from .models import TutoringUser
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignup
from django.forms.widgets import HiddenInput
from django import forms
    
class TutorForm(forms.ModelForm):
    class Meta:
        model = TutoringUser
        fields = ('is_tutor','user','full_name','major', 'locations', 'is_virtual', 'pay_rate')
