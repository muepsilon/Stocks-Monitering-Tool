from django.shortcuts import render
from django.http import HttpResponse
import json
from nsetools import Nse
from django.core import serializers

# Create your views here.
def index(request):
  return HttpResponse(json.dumps({'foo':'bar'}))

def portfolio(request):

  nse = Nse()
  results = []
  response = None

  stocks = ['ifbind','ptc']

  for stock in stocks:
    response = nse.get_quote(stock)
    results.append(response)

  return HttpResponse(json.dumps(results))