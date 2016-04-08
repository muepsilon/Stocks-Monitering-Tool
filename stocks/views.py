from django.shortcuts import render
import urllib, re, datetime, json, math
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse,HttpResponseBadRequest
from rest_framework_jwt.views import verify_jwt_token
from nsetools import Nse
from django.core import serializers
from stocks.models import Stock, CompanyList
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes, permission_classes

# Create your views here.
def index(request, page_slug = None):
  return render(request,'stocks/index.html')

@require_http_methods(["GET"])
def getCompanyNames(request):
   
  query = request.GET.get('query','').encode('ascii','ignore')

  companyList = CompanyList.objects.filter(name__contains = query)[0:5]

  companyListDict = serializers.serialize("python", companyList)
  
  filteredList = [ item['fields'] for item in companyListDict ]

  return HttpResponse(json.dumps(filteredList))


def company_info(request,symbol):
  
  try:
    company = CompanyList.objects.get(symbol = symbol)
    isValid = True
  except:
    isValid = False

  if isValid:
    
    symbol = symbol.encode('ascii','ignore')

    if 'timeframe' in request.GET:
      timeframe = request.GET.get('timeframe')
      if timeframe is not None and timeframe != '':
        if re.search('[0-9]+[my]',timeframe):
          if re.search('[0-9]+[m]',timeframe):
            months = re.search('[0-9]+',timeframe).group(0)
            start_date = datetime.date.today() - datetime.timedelta(days=30*int(months))
            collapse = 'daily'
          else:
            years = re.search('[0-9]+',timeframe).group(0)
            start_date = datetime.date.today() - datetime.timedelta(days=365*int(years))
            collapse = 'weekly'   
        else:
          return HttpResponseBadRequest("timeframe parameter is invalid", status = 400)
      else:
        return HttpResponseBadRequest("timeframe parameter is invalid", status = 400)
    else:
      start_date = datetime.date.today() - datetime.timedelta(days=1*365)
      collapse = 'weekly'

    start_date = start_date.strftime('%Y-%m-%d')
    response = urllib.urlopen('https://www.quandl.com/api/v3/datasets/NSE/'+ \
       symbol + ".json?api_key=o3Bix1gXUrHz3dFPCM9x&start_date="+ start_date + "&collapse=" + collapse)
    
    return HttpResponse(response.read())

  else:

    return HttpResponseBadRequest("Bad Request", status = 400)

def get_quote(stock):
  # Get value from NSE
  nse = Nse()
  keys = ['lastPrice','low52','high52','previousClose','companyName','symbol']

  response = nse.get_quote(stock.symbol.encode('ascii','ignore'))

  # Filter out required fields
  filter_response = { key : response[key] for key in keys }

  # Process and add data
  filter_response['id'] = stock.pk
  filter_response['target_price'] = stock.target_price
  filter_response['N_stocks'] = stock.N_stocks
  filter_response['trigger_price_low'] = stock.trigger_price_low
  filter_response['trigger_price_high'] = stock.trigger_price_high
  filter_response['latest_value'] = stock.N_stocks*filter_response['lastPrice']
  filter_response['invested_price'] = stock.invested_price
  filter_response['invested_amount'] = math.ceil(stock.invested_price*stock.N_stocks)
  filter_response['amount_change'] = math.ceil(stock.N_stocks*(filter_response['lastPrice'] - stock.invested_price))
  filter_response['overall_change'] = math.ceil(((filter_response['lastPrice']/filter_response['invested_price'] - 1)*100)*100)/100
  filter_response['daily_change'] = math.ceil(((filter_response['lastPrice']/filter_response['previousClose'] - 1)*100)*100)/100
  filter_response['daily_amount_change'] = stock.N_stocks*(filter_response['lastPrice']-filter_response['previousClose'])
  
  return filter_response

def get_stock_info(request,param):
  stock = Stock.objects.get(pk = param.encode('ascii','ignore'))
  result = get_quote(stock)
  return HttpResponse(json.dumps(result))

def stocks_list(request):
  stocks = serializers.serialize("json", Stock.objects.all())
  return HttpResponse(stocks)

@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication))
@permission_classes((IsAuthenticated,))
def example_view(request, format=None):
    content = {
        'user': unicode(request.user),  # `django.contrib.auth.User` instance.
        'auth': unicode(request.auth),  # None
    }
    return Response(content)

def portfolio(request):

  stocks = Stock.objects.all()
  results = []
  for stock in stocks:

    # Append the results
    results.append(get_quote(stock))

  return HttpResponse(json.dumps(results))