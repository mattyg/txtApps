from django import forms
from django.contrib.auth.models import User
from userprofiles.models import Profile

class UserForm(forms.ModelForm): 
	class Meta:
		model = User
		fields = ['username','password','email']

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['cellnumber']
		
class UserLoginForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username','password']