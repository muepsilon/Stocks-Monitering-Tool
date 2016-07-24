from django.core.management import BaseCommand
from django.conf import settings
import os
import pytz
import datetime
import nsemodule
from django.core.exceptions import ObjectDoesNotExist
import logging
from stocks.models import Company, FinanceParams

LOG_FILENAME = "fetch_finance_params.log"
logging.basicConfig(filename=os.path.join(os.path.dirname(os.path.abspath(__file__)),LOG_FILENAME),level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class Command(BaseCommand):

  def handle(self,*args, **options):
    today = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    companies = Company.objects.all()
    N = 10
    count = 0
    for company in companies:
      update_or_create_flag = False
      try:
        params = FinanceParams.objects.get(company = company, params_type = "C")
        delta_days = (today - params.updated_at).days
        if delta_days > 10:
          update_or_create_flag = True
      except ObjectDoesNotExist:
        update_or_create_flag = True

      if update_or_create_flag:
        params = self.get_finance_params(company.symbol,company.name)
        if params != None:
          standalone = params["standalone"]
          consolidated = params["consolidated"]
          obj1,created1 = FinanceParams.objects.update_or_create(company = company, **standalone)
          obj2,created2 = FinanceParams.objects.update_or_create(company = company, params_type = "C", **consolidated)
          count+=1
        
      if count%10 == 0 and count > 0:
        print("Updated/Created " + str(count) + " records")

  def get_finance_params(self,symbol,companyName):
    nse = nsemodule.Nse()
    f_response = nse.get_finance_params(symbol,companyName)
    if f_response['status'] == 200:
      params = f_response['response']
    else:
      print(f_response['response'])
      params = None
    return params
