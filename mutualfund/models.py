from django.db import models

# Create your models here.

class Mutualfund(models.Model):
  code = models.IntegerField(null = False, unique=True)
  fund_name = models.CharField(max_length = 300 , null = False)
  nav = models.FloatField(null=False)
