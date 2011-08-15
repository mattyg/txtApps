from userapps.decorators import superuser_only
from django.conf import settings
# models
from userapps.models import App, UserConfigKeyValue, DefaultUserConfig

# processes
from subprocess import Popen,PIPE
import shlex

# json
import json,re
from userapps.exceptions import BadJson

#@tasks(update_interval) RUN EVERY 5 mins or something
def refreshapps():
	#settings.APPS_PATH
	# for each directory name, search filepaths of apps to find a match, if no match, search each for directory name. 	
	cmdargs = ["ls","-1"]
	filelist = Popen(cmdargs,cwd=settings.APPS_PATH,stdout=PIPE).communicate()[0]
	filelist = filelist.split('\n')
	newappcount = 0
	for eachfile in filelist:
		if eachfile != "":
			try:
				App.objects.get(runfile__contains=eachfile)
			except App.DoesNotExist:
				try:
					parseappconfig(eachfile)
					newappcount += 1
				except IOError:
					# File is not a directory, or config.json file not found
					pass
				except BadJson:
					raise BadJson,"App could not be loaded due to badly formatted json config"
	return newappcount

def parseappconfig(appdir):
	# read config file to dict
	try:
		configfile = open(settings.APPS_PATH+appdir+"/config.json",'r+')
		#raise Exception({str(configfile.read())})
		config = str(re.sub('[\n\t\r]','',configfile.read())).replace(r"'",r"\\'")
		#raise Exception({str(config)})
		try:
			config = json.loads(str(config))
		except ValueError:
			raise BadJson,"Malformed Json"
		# create app
		napp = App.objects.create(name=config['app']['name'],version=config['app']['version'],category=config['app']['category'],author=config['app']['author'],description=config['app']['description'],manpage=config['app']['manpage'].replace(r"\'",r"'"),website=config['app']['website'],defaultcommand=config['app']['defaultcommand'],runfile=appdir+"/"+config['app']['runfile'])
		# create DefaultUserConfig
		if len(config['user'].viewkeys()) > 0:
			duc = DefaultUserConfig.objects.create()
			for each in config['user']:
				kv = UserConfigKeyValue.objects.create(key=str(each),value=str(config['user'][each]))
				kv.save()
				duc.keyvalues.add(kv)
			duc.save()
			napp.defaultuserconfig = duc
		napp.save()
	except IOError:
		# CONFIG FILE not found
		raise IOError
	
