from django.db import models
from django.contrib.auth.models import User
from userapps.models import App,AppCommand,UserConfig

class Profile(models.Model):
	user = models.ForeignKey(User,unique=True)
	cellnumber = models.IntegerField("Cell Number", max_length=30)
	apps = models.ManyToManyField(App,blank=True,null=True)
	appcommands = models.ManyToManyField(AppCommand,blank=True,null=True)
	appconfigs = models.ManyToManyField(UserConfig,blank=True,null=True)

	def __unicode__(self):
		return self.user.username
	
User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
