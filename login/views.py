from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
import json
from django.http import HttpResponse,HttpResponseBadRequest, JsonResponse
# Create your views here.

def loginUser(request):
  params = json.loads(request.body)
  if request.method != 'POST':
    return HttpResponseBadRequest( "Bad request, Post method required", status = 400)
  if 'email' not in params or 'password' not in params:
    return HttpResponseBadRequest( "Bad request, email or password missing", status = 400)

  username = params['email']
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
  return JsonResponse({})

def signupUser(request):
  pass

def is_logged_in(request):
  try:
    if request.user.is_authenticated():
      return JsonResponse({"login": True, "first_name": request.user.first_name, "email": request.user.email})
    else:
      return JsonResponse({"login": False})
  except:
    return JsonResponse({"login": False})