from django.db import models

# Create your models here.
class Stock(models.Model):
  company_name = models.CharField(max_length = 200 , null = False)
  symbol = models.CharField(max_length = 20, null = False, unique=True)
  invested_price = models.FloatField(null = False)
  N_stocks = models.IntegerField(null = False)
  target_price = models.FloatField(null = False)
  trigger_price_low = models.FloatField(null = False)
  trigger_price_high = models.FloatField(null=False)

class CompanyList(models.Model):
  name = models.CharField(max_length=200, null = False)
  symbol = models.CharField(max_length=20, null= False, unique=True)