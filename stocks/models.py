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

class CompanyList(models.Model):
  name = models.CharField(max_length=200, null = False)
  symbol = models.CharField(max_length=20, null= False, unique=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)