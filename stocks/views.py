from django.shortcuts import render
import urllib, re, datetime, json, math
import HTMLParser
import sys
import code
from django.db.models import Max
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseNotFound
from rest_framework_jwt.views import verify_jwt_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.exceptions import ObjectDoesNotExist
from nsetools import Nse
import nsemodule
from django.shortcuts import get_object_or_404
from django.core import serializers
from stocks.models import Stock, Company, WatchStock, FinanceParams, models
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
  company = Company.objects.filter(name__contains = query)[0:5]
  companyDict = serializers.serialize("json", company)
  filteredList = [ item['fields'] for item in json.loads(companyDict)]
  return HttpResponse(json.dumps(filteredList))

def fetch_ipo_info(request):
  nse = nsemodule.Nse()
  response = nse.fetch_ipo_info()
  return HttpResponse(response['response'])

@require_http_methods(["GET"])
def fetch_or_return_company_key_ratios(request):
  stock = get_object_or_404(Company, symbol = request.GET.get('symbol', None))
  fields = ('market_cap','book_value','p_by_e','div_perc','industry_p_by_e','eps','price_by_book','div_yield_perc','put_by_call','params_type')
  
  params = FinanceParams.objects.filter(company = stock)

  if len(params) != 0 :
    paramsDict = serializers.serialize("json", params , fields = fields)
    filteredList = {stock.symbol : [item['fields'] for item in json.loads(paramsDict)]}
    response = HttpResponse(json.dumps(filteredList))
  else:
    nse = nsemodule.Nse()
    f_response = nse.get_finance_params(stock.symbol)
    if f_response['status'] == 200:
      params = f_response['response']
      obj1,create1 = FinanceParams.objects.update_or_create(company = stock, **params['standalone'])
      obj2,create2 = FinanceParams.objects.update_or_create(company = stock, params_type = 'C', **params['consolidated'])
      paramsDict = serializers.serialize("json", [obj1,obj2,], fields = fields)
      filteredList = {stock.symbol : [item['fields'] for item in json.loads(paramsDict)]}
      response = HttpResponse(json.dumps(filteredList))
    else:
      response = HttpResponseNotFound('Unable to fetch Params')

  return response

@require_http_methods(["GET"])
def fetch_stocks(request):
  fields = ('market_cap','p_by_e','div_perc','eps','price_by_book','put_by_call','p_by_e_relative')
  params_fields = ('market_cap','book_value','p_by_e','div_perc','industry_p_by_e','eps','price_by_book','div_yield_perc','put_by_call','params_type','company')
  filter_dict = {}
  company_name_like = request.GET.get("name", None )
  value = ""
  for field in fields:
    value = request.GET.get(field,None)
    if value != None:
      val_list = value.split(",")
      if field == 'p_by_e_relative' :
        field_name = 'p_by_e'
        if len(val_list) == 3:
          filter_dict["{0}__lte".format(field_name)] = float(val_list[2])*models.F('industry_p_by_e')
          filter_dict["{0}__gte".format(field_name)] = float(val_list[1])*models.F('industry_p_by_e')
        elif len(val_list) == 2:
          if int(val_list[0]) == 1 :
            filter_dict["{0}__gte".format(field_name)] = float(val_list[1])*models.F('industry_p_by_e')
          else:
            filter_dict["{0}__lte".format(field_name)] = float(val_list[1])*models.F('industry_p_by_e')
      else:
        if len(val_list) == 3:
          filter_dict["{0}__lte".format(field)] = float(val_list[2])
          filter_dict["{0}__gte".format(field)] = float(val_list[1])
        elif len(val_list) == 2:
          if int(val_list[0]) == 1 :
            filter_dict["{0}__gte".format(field)] = float(val_list[1])
          else:
            filter_dict["{0}__lte".format(field)] = float(val_list[1])
  if company_name_like != None and len(company_name_like) > 0:
    filter_dict['company__name__contains'] = company_name_like

  if len(filter_dict.keys()) > 0:
    paramsDict = serializers.serialize("json",  FinanceParams.objects.filter(**filter_dict).order_by('company__name')[:100],use_natural_foreign_keys=True, fields=params_fields)
    filteredList =  [ item['fields'] for item in json.loads(paramsDict) ]
    response = HttpResponse(json.dumps(filteredList))
  else:
    response = HttpResponseBadRequest("Bad Request")

  return response

@require_http_methods(["GET"])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def update_company_list(request):
  # Format updated DB
  last_created = Company.objects.all().aggregate(Max('created_at'))['created_at__max']
  # Subtract 1 day to remove TZ effect
  # Format last created
  target_date = (last_created - datetime.timedelta(days=1)).strftime('%d-%b-%Y')
  
  nse = nsemodule.Nse()
  response = nse.get_list_of_companies(target_date)
  
  if response['status'] == 200:
    companies_list = json.loads(response['response'])
    new_companies = []
    for company in companies_list:
      try:
        obj = Company.objects.get(symbol = company[0].strip())
      except ObjectDoesNotExist:
        if len(company) == 2:
          obj = Company.objects.create(symbol = company[0].strip(), name = company[1].strip())
          new_companies.append(company[1])
    if len(new_companies) > 0:
      response = {"count": len(new_companies), "companies" : new_companies }
    else:
      response = {"msg": "No new companies added!"}
  else:
    response = {"msg" : "Unable to fetch data"}

  return HttpResponse(json.dumps(response))

def company_info(request,symbol):
  
  try:
    company = Company.objects.get(symbol = symbol)
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
  indexes = ['NIFTY 50','NIFTY MIDCAP 50','NIFTY MID100 FREE','NIFTY SML100 FREE','NIFTY 500']
  values = nse.get_indices(indexes)['response']
  values = { i["indexName"].lower().replace(" ","_") : i for i in values }
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
def get_stock_price(request):
  symbol = request.GET.get('symbol',None)
  response = None
  status = 204
  if symbol != None:
    try:
      stock = Company.objects.get(symbol = symbol)
      nse = nsemodule.Nse()
      keys = ['lastPrice','previousClose','companyName','symbol','low52','high52','dayHigh','dayLow']
      symbols = [(HTMLParser.HTMLParser().unescape(stock.symbol)).encode('ascii','ignore')]
      response = json.dumps(nse.get_equity_quotes(symbols,keys)['response'])
      status = nse.get_equity_quotes(symbols,keys)['status'] 
    except ObjectDoesNotExist:
      response = "Bad Request"
      status = 400

  return HttpResponse(response,status = status) 

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def watchlist(request):

  stocks = WatchStock.objects.filter(user=request.user)
  results = get_quote_WatchList(stocks)

  return HttpResponse(json.dumps(results))