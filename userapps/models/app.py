from django.db import models
from django.contrib.auth.models import User
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
	website = models.URLField()
	defaultcommand = models.CharField(max_length=160)
	
	def __unicode__(self):
		return self.name
	
	class Meta:
		app_label = 'userapps'