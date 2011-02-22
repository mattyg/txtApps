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
	
	# my edit pages
	#apps
	(r'^my/apps/commands/edit/$','userapps.views.edituserapps'),
	(r'^my/apps/commands/add/$','userapps.views.addusercommand'),
	#info
	(r'^my/info/edit/$','userprofiles.views.editcellnumber'),
	
	# login/logout
	(r'^login/$', 'userprofiles.views.dologin'),
	(r'^logout/$', 'userprofiles.views.dologout'),
	# register
	(r'^register/$', 'userprofiles.views.register'),
	
	# main page redirect
	(r'^$', 'userprofiles.views.main'),
	
	# sms gateway
	(r'^smsgate/incoming/$', 'smsgate.views.incoming'),
	(r'^smsgate/outgoing/$', 'smsgate.views.outgoing'),
)
import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )