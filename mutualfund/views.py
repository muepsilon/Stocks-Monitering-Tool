from django.shortcuts import render
import urllib
from mutualfund.models import Mutualfund
from django.http import HttpResponse
import json
# Create your views here.

def update_database(request):
  
  response = urllib.urlopen("http://portal.amfiindia.com/spages/NAV0.txt")

  text_response =  response.read()
  text_response_lines = text_response.split("\n")
  entrylist = []
  firstlineskip = False # Skiping the scheme in first row
  mf_list = [ item[0] for item in Mutualfund.objects.values_list('code')] # To check if the Fund is unique
  
  for line in text_response_lines:
    
    splitted_row = line.split(";")

    if len(splitted_row) == 8:
      
      if firstlineskip:
        try:
          if int(splitted_row[0]) not in mf_list:
            entrylist.append(Mutualfund(code = int(splitted_row[0]), fund_name = splitted_row[3], nav = float(splitted_row[4])))
        except Exception:
          print("Data not available", splitted_row[0],splitted_row[3],splitted_row[4])
      firstlineskip = True

  Mutualfund.objects.bulk_create(entrylist)

  return HttpResponse(json.dumps({"data":"updated"}))