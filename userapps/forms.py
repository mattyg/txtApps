from django import forms
from userapps.models import App,AppCommand

class InputForm(forms.ModelForm): 
	class Meta:
		model = AppCommand
		fields = ['input']

class OutputForm(forms.ModelForm):
	class Meta:
		model = AppCommand
		fields = ['output']
