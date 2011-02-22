# settings
from django.conf import settings

# temporary for TESTING
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect,HttpResponse

# SMSGATE_GATEWAY = 'smsgate.gateways.twillio'

# smsgate incoming sms
def incoming(request):
	#settings.SMSGATE_GATEWAY.incoming(request) # reads in sms message (decifered through gateway functions)
	# calls txtapp with text & user
	# txapp adds task to celery to read in, get response
	# txtapp sends to outgoing
	print request

# smsgate outgoing sms
def outgoing(request):
	pass