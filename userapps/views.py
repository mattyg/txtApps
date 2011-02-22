#http,template,messages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context,RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.contrib import messages
#login
from django.contrib.auth.decorators import login_required
#models
from userapps.models import App

@login_required
def showuserapps(request):
	data = RequestContext(request,{
		'title':'My Apps',
		'apps':request.user.profile.apps.all(),
	})
	return render_to_response('userapps/showallapps.html',data)
	
@login_required
def edituserapps(request):
	if request.method == 'POST': # recieved POST data
		# clean data
		appid = request.POST['appid']
		input = request.POST['input']
		output = request.POST['output']
		if App.objects.get(id=appid): # if this app exists
			if request.POST.has_key('appcommandid'): # check if request.user has UserCommand for this app
				appcommand = request.user.profile.appcommands.get(id=request.POST['appcommandid'])
				appcommand.input = input
				appcommand.output = output
				appcommand.save()
			else: # otherwise create UserCommand for this user and app
				appcommand = request.user.profile.appcommands.create(app=App.objects.get(id=appid),input=input,output=output)
				appcommand.save()
			messages.success(request,'Command modified for '+App.objects.get(id=appid).name)
	return HttpResponseRedirect(request.POST['next'])

@login_required
def addusercommand(request):
	if request.method == 'POST': # recieved POST data
		appid = request.POST['appid']
		if App.objects.get(id=appid): # if this app exists
			request.user.profile.appcommands.create(app=App.objects.get(id=appid),input='',output=App.objects.get(id=appid).defaultcommand)
	return HttpResponseRedirect(request.POST['next'])