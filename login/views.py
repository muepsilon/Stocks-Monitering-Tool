from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json
from django.http import HttpResponse,HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_protect
# Create your views here.

def loginUser(request):
  params = json.loads(request.body)
  if request.method != 'POST':
    return HttpResponseBadRequest( "Bad request, Post method required", status = 400)
  if 'username_email' not in params or 'password' not in params:
    return HttpResponseBadRequest( "Bad request, email or password missing", status = 400)
  if '@' in params['username_email']:
    email = params['username_email']
    user = User.objects.get(email=email)
    if user is not None:
      username = getattr(user,'username')
      password = params['password']
      user = authenticate(username=username, password=password)
  else:
    username = params['username_email']
    password = params['password']
    user = authenticate(username=username, password=password)
  
  if user is not None:
    if user.is_active:
      login(request, user)
      return HttpResponse(json.dumps({"is_logged_in": True, "msg" : "User is logged in! ","first_name": user.first_name, "email": user.email}))
    else:
      # Return a 'disabled account' error message
      return HttpResponse(json.dumps({"is_logged_in": False, "msg" : "Disabled Account"}))

  else:
    # Return an 'invalid login' error message.
      return HttpResponse(json.dumps({"is_logged_in": False, "msg" : "Invalid Credentials"}))

def logoutUser(request):
  logout(request)
  return JsonResponse({"is_logout": True})

def registerUser(request):
  params = json.loads(request.body)
  required_fields = ['email','username','password','first_name','last_name']

  if request.method != 'POST':
    return HttpResponseBadRequest( "Bad request, Post method required", status = 400)

  if not validate_params(params,required_fields):
    return HttpResponseBadRequest( "Bad request,parameters missing", status = 400)

  if User.objects.filter(username = params['username']).exists():
    return HttpResponseBadRequest("Username already exist", status= 202)

  if User.objects.filter(email = params['email']).exists():
    return HttpResponseBadRequest("Email already exist", status= 202)

  user = User.objects.create_user(username = params['username'],
    email = params['email'], password = params['password'], 
    first_name = params['first_name'], last_name = params['last_name'])
  user.save()
  user = authenticate(username=params['username'], password=params['password'])
  if user is not None:
      login(request, user)
      return HttpResponse(json.dumps({"is_logged_in": True, "msg" : "User is logged in! ","first_name": user.first_name, "email": user.email}))
  else:
    # Return an 'invalid login' error message.
      return HttpResponse(json.dumps({"is_created": False, "msg" : "Unable to create user!"}))

  pass

def validate_params(params,fields):
  isValid = True
  for field in fields:
    if field not in params:
      isValid = False
  return isValid

def duplicateCheck(request):
  if request.method == 'GET':
    username = request.GET.get('username',None)
    email = request.GET.get('email',None)

    if username is None and email is None:
      return HttpResponseBadRequest( "Bad request, Email or Username required", status = 400)

    response = {"username_taken": False, "email_taken": False}

    if username is not None and User.objects.filter(username = username).exists():
      response["username_taken"] = True

    if email is not None and User.objects.filter(email = email).exists():
      response["email_taken"] = True
      
    return HttpResponse(json.dumps(response))

  else:
    return HttpResponseBadRequest("Method not allowed", status = 405)

def is_logged_in(request):
  try:
    if request.user.is_authenticated():
      return JsonResponse({"login": True, "first_name": request.user.first_name, "email": request.user.email})
    else:
      return JsonResponse({"login": False})
  except:
    return JsonResponse({"login": False})