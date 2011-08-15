from django.conf.urls.defaults import *
from userprofiles.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^txtApps_django/', include('txtApps_django.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

	# my pages
	(r'^my/dashboard/$', 'userprofiles.views.showdashboard'),
	(r'^my/apps/$', 'userapps.views.showuserapps'),

	# admin pages
	(r'^super/dashboard/$', 'userprofiles.views.showadmindashboard'),
	
	# my edit pages
	#apps
	(r'^my/apps/commands/edit/$','userapps.views.edituserapps'),
	(r'^my/apps/commands/add/$','userapps.views.addusercommand'),
	(r'^my/apps/add/$','userapps.views.adduserapp'),
	(r'^my/apps/(?P<appid>\d*)/$', 'userapps.views.showuserapp'),
	#info
	(r'^my/info/edit/$','userprofiles.views.editcellnumber'),

	# browse all apps
	(r'^all/apps/$', 'userapps.views.showallapps'),
	(r'^all/apps/(?P<sortby>\w*)/(?P<sortorder>\w*)/(?P<page>\d+)/$', 'userapps.views.showallapps'),
	
	# login/logout
	(r'^login/$', 'userprofiles.views.dologin'),
	(r'^logout/$', 'userprofiles.views.dologout'),
	# register
	(r'^register/$', 'userprofiles.views.register'),
	
	# sms gateway
	(r'^smsgate/incoming/$', 'smsgate.views.incoming'),
	
	# main page redirect
	(r'^$', 'userprofiles.views.main'),
)
import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
