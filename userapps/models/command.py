from django.db import models
from django.contrib.auth.models import User

class UserCommand(models.Model):
	app = models.ForeignKey('App')
	# input is custom command for user, shorter preferabally
	input = models.CharField(max_length=160)
	# output is full command for user, including any custom parameters
	# default is value of defaultcommand of App
	output = models.CharField(max_length=300) # max_length=300 so that longer UserCommands can be stored
	users = models.ManyToManyField(User)
	class Meta:
		app_label = 'userapps'
	def __unicode__(self):
		return self.input