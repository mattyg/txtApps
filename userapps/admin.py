from django.contrib import admin
from userapps.models import *

class AppAdmin(admin.ModelAdmin):
	pass
admin.site.register(App,AppAdmin)	

class UserCommandAdmin(admin.ModelAdmin):
	pass
admin.site.register(UserCommand,UserCommandAdmin)