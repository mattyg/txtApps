from django.db import models
from django.contrib.auth.models import User

class UserConfig(models.Model):
	app = models.ForeignKey('App')
	keyvalues = models.ManyToManyField('UserConfigKeyValue')

	def __unicode__(self):
		string = []
		for each in self.keyvalues.all():
			string.append(str(each.key)+":"+str(each.value))
		return ", ".join(string)

class UserConfigKeyValue(models.Model):
	key = models.CharField(max_length=500)
	value = models.TextField()

	def __unicode__(self):
		return str(self.key)+":"+str(self.value)

class DefaultUserConfig(models.Model):
	keyvalues = models.ManyToManyField('UserConfigKeyValue',blank=True,null=True)

	def __unicode__(self):
		string = []
		for each in self.keyvalues.all():
			string.append(str(each.key)+":"+str(each.value))
		return ", ".join(string)

class App(models.Model):
	name = models.CharField(max_length=200)
	version = models.CharField(max_length=10)
	category_choices = (
		('weather','Weather'),
		('utility','Utility'),
		('game','Game'),
		('finance','Finance'),
		('entertainment','Entertainment'),
		('calendar','Calendar'),
		('networking','Social Networking'),
		('reference','Reference'),
		('news','News'),
		('productivity','Productivity'),
		('travel','Travel'),
		('sports','Sports'),
		('txtapps','Internal txtApps Actions'),
	)
	category = models.CharField(max_length=50,choices=category_choices)
	author = models.CharField(max_length=255)
	website = models.URLField(blank=True)
	defaultcommand = models.CharField(max_length=160)
	description = models.TextField(max_length=2000)
	manpage = models.TextField(max_length=2000)
	runfile = models.CharField(max_length=255)
	defaultuserconfig = models.OneToOneField('DefaultUserConfig',blank=True,null=True)
	
	def __unicode__(self):
		return self.name

class AppCommand(models.Model):
	app = models.OneToOneField('App')
	#app = models.ForeignKey('App')
	# input is custom command for user, shorter preferabally
	input = models.CharField(max_length=160)
	# output is full command for user, including any custom parameters
	output = models.CharField(max_length=300) # max_length=300 so that longer UserCommands can be stored

	def __unicode__(self):
		return self.input
