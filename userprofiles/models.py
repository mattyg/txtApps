from django.db import models
from django.contrib.auth.models import User
from userapps.models import App
from userapps.models import UserCommand

class Profile(models.Model):
	user = models.ForeignKey(User,unique=True)
	cellnumber = models.IntegerField("Cell Number", max_length=30)
	apps = models.ManyToManyField(App)
	appcommands = models.ManyToManyField(UserCommand)
	
	def __unicode__(self):
		return self.user.username
	
User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])