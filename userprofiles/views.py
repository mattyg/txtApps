#http,template,messages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.contrib import messages
#login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login,authenticate
#models
from userapps.models import App
from userprofiles.models import Profile
from django.contrib.auth.models import User
#forms
from userprofiles.forms import UserForm,ProfileForm,UserLoginForm
from userapps.forms import InputForm,OutputForm

def register(request):
	if request.method == 'POST': # form data submitted
		userform = UserForm({
			'username':request.POST['username'],
			'email':request.POST['email'],
			'password':request.POST['password']
		})
		profileform = ProfileForm({'cellnumber':request.POST['cellnumber']})
		if userform.is_valid() and profileform.is_valid():
			# process data
			
			# save user and profile
			user = User.objects.create_user(request.POST['username'],request.POST['email'],request.POST['password'])
			profile = Profile.objects.create(user=user, cellnumber=request.POST['cellnumber'])
			user.save()
			profile.save()
			
			# authenticate and login user
			authuser = authenticate(username=request.POST['username'],password=request.POST['password'])
			login(request, authuser)
			return HttpResponseRedirect('/my/dashboard')
		else:
			return HttpResponseRedirect('/fail')
	else: # display form
		data = RequestContext(request,{
			'title':'Register',
			'userform':UserForm(),
			'profileform':ProfileForm(),
		})
		return render_to_response('userprofiles/register.html',data)

def dologin(request,next='/my/dashboard'):
	if request.method == 'POST': # form sent, parse input and login
		authuser = authenticate(username=request.POST['username'],password=request.POST['password'])
		if authuser is not None:
			login(request, authuser)
			if request.POST['next'] != "":
				return HttpResponseRedirect(request.POST['next'])
			else:
				return HttpResponseRedirect('/my/dashboard')
		else:
			messages.warning(request,'The username and/or password entered is incorrect.')
			return HttpResponseRedirect('/login/')
	else: # show login form
		data = RequestContext(request,{
			'title':'Log In',
			'form':UserLoginForm(),
		})
		return render_to_response('userprofiles/login.html',data)
		

@login_required
def dologout(request):
	logout(request)
	return HttpResponseRedirect("/")

@login_required
def showdashboard(request):	
	apps = request.user.profile.apps.all()
	appcommands = {}
	for app in apps:
		commands = request.user.profile.appcommands.all().filter(app__id=app.id)
		if commands:
			appcommands[app.id] = commands
	data = RequestContext(request,{
		'title':request.user.username,
		'apps':apps,
		'appcommands':appcommands,
		'cellnumber':request.user.profile.cellnumber,
	})
	
	return render_to_response('userprofiles/showdashboard.html',data)
	
def main(request):
	if request.user.is_authenticated(): # redirect to my/dashboard
		return HttpResponseRedirect('/my/dashboard/')
	else: # main page for new users
		data = RequestContext(request,{
			'title':'Welcome!'
		})
		return render_to_response('userprofiles/main.html',data)
		
@login_required
def editcellnumber(request):
	if request.method == 'POST': # POST data recieved
		cellnumber = request.POST['cellnumber']
		userprofile = request.user.profile
		userprofile.cellnumber = cellnumber
		userprofile.save()
		messages.success(request,'Your cell number has been changed.')
	return HttpResponseRedirect(request.POST['next'])