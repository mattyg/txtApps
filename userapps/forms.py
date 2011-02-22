from django import forms
from userapps.models import UserCommand

class InputForm(forms.ModelForm): 
	class Meta:
		model = UserCommand
		fields = ['input']

class OutputForm(forms.ModelForm):
	class Meta:
		model = UserCommand
		fields = ['output']
