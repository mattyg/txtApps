#http,template,messages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context,RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.contrib import messages
#login
from django.contrib.auth.decorators import login_required
#models
from userapps.models import App, AppCommand, UserConfig, UserConfigKeyValue
from userprofiles.models import Profile
from django.db.models import Count
#decorators
from userapps.decorators import superuser_only
#tasks
from userapps.tasks import refreshapps

# USER-APP CRUD
@login_required
def showuserapps(request):
	if request.user.profile.apps is not None:
		apps = request.user.profile.apps.all()
	else:
		apps = []
	data = RequestContext(request,{
		'title':'My Apps',
		'apps':apps,
	})
	return render_to_response('userapps/showallapps.html',data)
	
@login_required
def edituserapps(request):
	if request.method == 'POST': # recieved POST data
		# clean data
		appid = request.POST['appid']
		input = request.POST['input']
		output = request.POST['output']
		try:
			App.objects.get(id=appid)
			if request.POST.has_key('appcommandid'): # check if request.user has UserCommand for this app
				appcommand = request.user.profile.appcommands.get(id=request.POST['appcommandid'])
				appcommand.input = input
				appcommand.output = output
				appcommand.save()
			else: # otherwise create UserCommand for this user and app
				appcommand = request.user.profile.appcommands.create(app=App.objects.get(id=appid),input=input,output=output)
				appcommand.save()
			messages.success(request,'Command modified for '+App.objects.get(id=appid).name)
		except:
			messages.error(request,"Error: exception")
	return HttpResponseRedirect(request.POST['next'])

@login_required
def addusercommand(request):
	if request.method == 'POST': # recieved POST data
		appid = request.POST['appid']
		try:
			App.objects.get(id=appid)
			request.user.profile.appcommands.create(app=App.objects.get(id=appid),input='',output=App.objects.get(id=appid).defaultcommand)
		except App.DoesNotExist:
			pass
	return HttpResponseRedirect(request.POST['next'])

@login_required
def showuserapp(request,appid):
	#try:
	app = App.objects.get(id=appid)
	userconfig = request.user.profile.appconfigs.get(app=app)
	data = RequestContext(request,{
			'title':'My Apps: %s' %(app.name),
			'app':app,
			'userconfig':userconfig,
		})
	return render_to_response('userapps/showuserapp.html',data)
	#except:
	#	raise Http404

@login_required
def edituserconfigkeyvalue(request):
	if request.method == 'POST':
		keyvalueid = request.POST['userconfigkeyvalueid']
		key = request.POST['key']
		value = request.POST['value']
		return HttpResponseRedirect(request.POST['next'])
	else:
		raise Http404

@login_required
def adduserapp(request):
	if request.method == "POST":
		if request.POST.__contains__('appid'):
			appid = request.POST['appid']
			try:
				app = App.objects.get(id=appid)
				request.user.profile.apps.add(app)
				uc = UserConfig.objects.create(app=app)
				for each in app.defaultuserconfig.keyvalues.all():
					kv = UserConfigKeyValue(key=each.key,value=each.value)
					kv.save()
					uc.keyvalues.add(kv)
				uc.save()
				request.user.profile.appconfigs.add(uc)
				messages.success(request,"%s added to your apps." %(app.name))
			except:
				messages.error(request,"Adding app failed.")
	return HttpResponseRedirect(request.POST['next'])


## ALL APPS browsing ##
def showallapps(request,sortby='popularity',sortorder='desc',page=1):
	allapps = None
	appsperpage = 25
	title = 'All Apps'
	if sortby == 'popularity':
		if sortorder == 'desc':
			allapps = App.objects.annotate(profile_count=Count('profile')).order_by('-profile_count')[((int(page)-1)*appsperpage):(int(page)*appsperpage)]
			title += '  --  sort by '+sortby+' descending'
		elif sortorder == 'asc':
			pass
	elif sortby == 'category':
		if sortorder == 'desc':
			pass
		elif sortorder == 'asc':
			pass
	elif sortby == 'author':
		if sortorder == 'desc':
			pass
		elif sortorder == 'asc':
			pass

	data = RequestContext(request,{'title':title,
					'apps':allapps})
	return render_to_response('userapps/showallapps.html',data)

def showapp(request):
	pass
