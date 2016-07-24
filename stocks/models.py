from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Stock(models.Model):
  company_name = models.CharField(max_length = 200 , null = False)
  symbol = models.CharField(max_length = 20, null = False)
  invested_price = models.FloatField(null = False)
  N_stocks = models.IntegerField(null = False)
  target_price = models.FloatField(null = False)
  trigger_price_low = models.FloatField(null = False)
  trigger_price_high = models.FloatField(null=False)
  user = models.ForeignKey(User,null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class WatchStock(models.Model):
  company_name = models.CharField(max_length = 200 , null = False)
  symbol = models.CharField(max_length = 20, null = False)
  trigger_price_low = models.FloatField(null = False)
  trigger_price_high = models.FloatField(null=False)
  user = models.ForeignKey(User,null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Company(models.Model):
  name = models.CharField(max_length=200, null = False)
  symbol = models.CharField(max_length=20, null= False, unique=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def natural_key(self):
    return {"name": self.name, "symbol": self.symbol }

class FinanceParams(models.Model):
  STANDALONE = "S"
  CONSOLIDATED = "C"
  PARAMS_TYPES = ((STANDALONE, "STANDALONE"),(CONSOLIDATED,"CONSOLIDATED"))

  company = models.ForeignKey(Company, null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  market_cap = models.FloatField(null=True)
  book_value = models.FloatField(null=True)
  p_by_e = models.FloatField(null=True)
  div_perc = models.FloatField(null=True)
  industry_p_by_e = models.FloatField(null=True)
  eps = models.FloatField(null=True)
  price_by_book = models.FloatField(null=True)
  div_yield_perc = models.FloatField(null=True)
  put_by_call = models.FloatField(null=True)
  params_type = models.CharField(max_length=1, choices=PARAMS_TYPES, default = STANDALONE)

  class Meta:
    unique_together = ('company', 'params_type',)
