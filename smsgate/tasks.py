#from celery.task import task
#from celery.task.sets import subtask
from subprocess import Popen, PIPE
import shlex

# models #
from userprofiles.models import Profile
from userapps.models import AppCommand, App

# settings #
from django.conf import settings

# tmp json file
import json
import tempfile
import re

#@task
def parserun(cellnumber,text):
	# parse command

	# run command
	pass

#@task
def outgoing(text):
	pass


# INTERPRETE APP COMMANDS
#@task
def parsecommand(cellnumber,text):
	if text.find(' ') != -1:
		cmd = text.split(' ',1)[:1][0]
		args = text.split(' ',1)[1:][0]
	else:
		cmd = text
		args = ""
	# try READing profile from cellnumber
	try:
		userprofile = Profile.objects.get(cellnumber=cellnumber)
		# CHECK if usercommand from user & command
		try:
			if userprofile.appcommands is None:
				raise AppCommand.DoesNotExist
			usercommand = userprofile.appcommands.get(input=cmd)
			cmdtext = str(usercommand.output)+" "+str(args)
			cmdtext.strip()
			if cmdtext.find(' ') != -1:
				args = cmdtext.split(' ',1)[1:][0]
			return usercommand.app.id,userprofile.id,args
		except AppCommand.DoesNotExist:
			# CHECK if defaultcommand from cmd
			try:
				app = App.objects.get(defaultcommand=cmd)
				return app.id,userprofile.id,args
			except App.DoesNotExist:
				# RESPOND with possible apps they meant to write
				# statistically closest app input 
				raise App.DoesNotExist,"No App found"
	except Profile.DoesNotExist:
		# RESPOND with txt-based registration instructions
		raise Profile.DoesNotExist,"No Profile found"

#@task
def runapp(appid,userprofileid,args):
	# GET app, userprofile models
	app = App.objects.get(id=appid)
	userprofile = Profile.objects.get(id=userprofileid)
	# WRITE user id & first_name to config
	uconfig = {}
	uconfig['id'] = userprofile.user.id
	uconfig['first_name'] = str(userprofile.user.first_name).format('r')

	# WRITE UserConfig to config
	try:
		userconfig = userprofile.appconfigs.get(app=app)
		for each in userconfig.keyvalues.all():
			uconfig[str(each.key).format('r')] = str(each.value).format('r')
	except UserConfig.DoesNotExist:
		pass
	import pdb; pdb.set_trace()
	uconfig = json.dumps(uconfig)

	tmpfile = tempfile.NamedTemporaryFile(dir=settings.MAIN_PATH+'tmp')
	tmpfile.write(uconfig)
	tmpfile.flush()
	# RUN app with arguement userconfig=/home/gabrenya/www/txtApps_django/tmp/uconfig2343.json
	appslog = open(settings.APPS_LOG,'w')
	try:
		cargs = shlex.split(str(settings.APPS_PATH)+str(app.runfile)+" "+str(args.replace('\'','\\"'))+" userconfig=%s" %(tmpfile.name))
		appslog.write(str(cargs))
		workingdir = str(settings.APPS_PATH)+str(app.runfile)
		workingdir = "/".join(workingdir.split("/")[:-1])
		proc = Popen(cargs,stderr=appslog,stdout=PIPE,cwd=workingdir)
		textout = proc.communicate()[0]
	except:
		pass
	appslog.close()

	# REMOVE temporary UserConfig JSON file
	tmpfile.close()

	# CLEAN TEXT RESPONSE for GSM permitted characters
	textout = re.sub(ur'[^\t\u0040\u00A3\u0024\u00A5\u00E8\u00E9\u00F9\u00EC\u00F2\u00C7\u000A\u00D8\u00F8\u000D\u00C5\u00E5\u0394\u005F\u03A6\u0393\u039B\u03A9\u03A0\u03A8\u03A3\u0398\u039E\u00C6\u00E6\u00DF\u00C9\u0020\u0021\u0022\u0023\u00A4\u0025\u0026\u0027\u0028\u0029\u002A\u002B\u002C\u002D\u002E\u002F\u0030\u0031\u0032\u0033\u0034\u0035\u0036\u0037\u0038\u0039\u003A\u003B\u003C\u003D\u003E\u003F\u00A1\u0041\u0042\u0043\u0044\u0045\u0046\u0047\u0048\u0049\u004A\u004B\u004C\u004D\u004E\u004F\u0050\u0051\u0052\u0053\u0054\u0055\u0056\u0057\u0058\u0059\u005A\u00C4\u00D6\u00D1\u00DC\u00A7\u00BF\u0061\u0062\u0063\u0064\u0065\u0066\u0067\u0068\u0069\u006A\u006B\u006C\u006D\u006E\u006F\u0070\u0071\u0072\u0073\u0074\u0075\u0076\u0077\u0078\u0079\u007A\u00E4\u00F6\u00F1\u00FC\u00E0\u20AC\u005B\u005C\u005D\u005E\u007B\u007C\u007D\u007E][\n]','',textout)

	# send result
	return str(textout).format('r')
