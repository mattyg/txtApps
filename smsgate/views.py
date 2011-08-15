# settings
from django.conf import settings
# template
from django.shortcuts import render_to_response

# SMS GATEWAY
import sys
gateway = __import__(settings.SMS_GATEWAY)
gateway = sys.modules[settings.SMS_GATEWAY]

# parse apps, run apps
from smsgate.tasks import parsecommand,runapp
from userapps.models import App
from userprofiles.models import Profile


# smsgate incoming sms
def incoming(request):	
	# get TEXT & CELL# from gateway request
	textin,cellnumber = gateway.incoming(request)

	try:
		# get COMMAND+ARGS from text & cell#
		appid,userprofileid,arguements = parsecommand(cellnumber,textin)
		# RUN command
		textout = runapp(appid,userprofileid,arguements)
	except App.DoesNotExist:
		textout = "App not found."
	except Profile.DoesNotExist:
		textout = "To join txtApps respond with 'txtapps join username password'"
	
	# make RESPONSE from command results
	if len(textout) > 0:
		data = {}
		data['textout'] = textout
		return render_to_response('smsgate/outgoing.xml',data,mimetype='text/xml')

# smsgate outgoing sms
def outgoing(textmessage):
	print "Responding...",request
	gateway.outgoing(request)
