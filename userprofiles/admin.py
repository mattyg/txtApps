from django.contrib import admin
from userprofiles.models import *

class ProfileAdmin(admin.ModelAdmin):
	pass
admin.site.register(Profile,ProfileAdmin)