from django.shortcuts import render
import urllib, re, datetime, json, math
import HTMLParser
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse,HttpResponseBadRequest
from rest_framework_jwt.views import verify_jwt_token
from django.views.decorators.csrf import ensure_csrf_cookie
from nsetools import Nse
import nsemodule
from django.core import serializers
from stocks.models import Stock, CompanyList, WatchStock
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes, permission_classes

# Create your views here.
@ensure_csrf_cookie
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
       symbol + ".json?api_key=o3Bix1gXUrHz3dFPCM9x&start_date="+ start_date + "&order=asc&collapse=" + collapse)
    
    return HttpResponse(response.read())

  else:

    return HttpResponseBadRequest("Bad Request", status = 400)

def get_quote(stocks):
  # Get value from NSE
  nse = nsemodule.Nse()
  keys = ['lastPrice','low52','high52','previousClose','companyName','symbol','dayHigh','dayLow']
  symbols = []
  for stock in stocks:
    symbols.append((HTMLParser.HTMLParser().unescape(stock.symbol)).encode('ascii','ignore')) 
  filter_response = nse.get_equity_quotes(symbols,keys)['response']
  # Process and add data
  for i in xrange(len(filter_response)):
    filter_response[i]['id'] = stocks[i].pk
    filter_response[i]['target_price'] = stocks[i].target_price
    filter_response[i]['N_stocks'] = stocks[i].N_stocks
    filter_response[i]['trigger_price_low'] = stocks[i].trigger_price_low
    filter_response[i]['trigger_price_high'] = stocks[i].trigger_price_high
    filter_response[i]['latest_value'] = stocks[i].N_stocks*filter_response[i]['lastPrice']
    filter_response[i]['invested_price'] = stocks[i].invested_price
    filter_response[i]['invested_amount'] = math.ceil(stocks[i].invested_price*stocks[i].N_stocks)
    filter_response[i]['amount_change'] = math.ceil(stocks[i].N_stocks*(filter_response[i]['lastPrice'] - stocks[i].invested_price))
    filter_response[i]['overall_change'] = math.ceil(((filter_response[i]['lastPrice']/filter_response[i]['invested_price'] - 1)*100)*100)/100
    filter_response[i]['daily_change'] = math.ceil(((filter_response[i]['lastPrice']/filter_response[i]['previousClose'] - 1)*100)*100)/100
    filter_response[i]['daily_amount_change'] = stocks[i].N_stocks*(filter_response[i]['lastPrice']-filter_response[i]['previousClose'])
  
  return filter_response

def get_quote_WatchList(stocks):
  # Get value from NSE
  nse = nsemodule.Nse()
  keys = ['lastPrice','previousClose','companyName','symbol','low52','high52','dayHigh','dayLow']
  symbols = []
  for stock in stocks:
    symbols.append((HTMLParser.HTMLParser().unescape(stock.symbol)).encode('ascii','ignore')) 
  filter_response = nse.get_equity_quotes(symbols,keys)['response']

  # Process and add data
  for i in xrange(len(filter_response)):
    filter_response[i]['id'] = stocks[i].pk
    filter_response[i]['trigger_price_low'] = stocks[i].trigger_price_low
    filter_response[i]['trigger_price_high'] = stocks[i].trigger_price_high
  
  return filter_response

def get_index_info(request):
  nse = nsemodule.Nse()
  indexes = ['NIFTY 50','NIFTY MIDCAP 50']
  values = nse.get_indices(indexes)['response']
  return HttpResponse(json.dumps(values))

def get_stock_info(request,param):
  stock = Stock.objects.get(pk = param.encode('ascii','ignore'))
  result = get_quote(stock)
  return HttpResponse(json.dumps(result))

def stocks_list(request):
  stocks = serializers.serialize("json", Stock.objects.all())
  return HttpResponse(stocks)

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def portfolio(request):
  
  stocks = Stock.objects.filter(user=request.user)
  results = get_quote(stocks)

  return HttpResponse(json.dumps(results))

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def portfolio_stock(request):
  stocktypes = ['portfolio', 'watchlist']
  symbol = request.GET.get('symbol',None)
  stockType = request.GET.get('type',stocktypes[0])
  response = None
  status = 204
  if symbol != None and stockType in stocktypes:
    if stockType == stocktypes[0]:
      stocks = Stock.objects.filter(user = request.user, symbol = symbol)
    else:
      stocks = WatchStock.objects.filter(user = request.user, symbol = symbol)
    if len(stocks) != 0 :
      if stockType == stocktypes[0] :
        response = json.dumps(get_quote(stocks[0]))
      else:
        response = json.dumps(get_quote_WatchList(stocks[0]))
      status = 200
  return HttpResponse(response, status = status)

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def watchlist(request):

  stocks = WatchStock.objects.filter(user=request.user)
  results = get_quote_WatchList(stocks)

  return HttpResponse(json.dumps(results))