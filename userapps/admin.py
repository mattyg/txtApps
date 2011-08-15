from django.contrib import admin
from userapps.models import App, AppCommand, UserConfig, DefaultUserConfig, UserConfigKeyValue

class AppAdmin(admin.ModelAdmin):
	pass

class AppCommandAdmin(admin.ModelAdmin):
	pass

class UserConfigAdmin(admin.ModelAdmin):
	pass

class DefaultUserConfigAdmin(admin.ModelAdmin):
	pass

class UserConfigKeyValueAdmin(admin.ModelAdmin):
	pass

admin.site.register(App,AppAdmin)	
admin.site.register(AppCommand,AppCommandAdmin)
admin.site.register(UserConfig,UserConfigAdmin)
admin.site.register(DefaultUserConfig,DefaultUserConfigAdmin)
admin.site.register(UserConfigKeyValue,UserConfigKeyValueAdmin)
