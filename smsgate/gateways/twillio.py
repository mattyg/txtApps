# SETTINGS #
# Twilio REST API version
API_VERSION = '2010-04-01'

# Twilio AccountSid and AuthToken
ACCOUNT_SID = 'APe7a5a83847caba6f4370d0e30be864f8'
ACCOUNT_TOKEN = '33a786b504cf1962c903bd9b79b580c6'

# Outgoing Caller ID previously validated with Twilio
#CALLER_ID = 'NNNNNNNNNN';


def incoming(request):
	if request.method == 'GET':
		body = request.GET['Body'].replace("+"," ")
		fromcell = request.GET['From']
		return body,fromcell
	else:
		raise Exception

