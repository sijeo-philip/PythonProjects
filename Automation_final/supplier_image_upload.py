#! /usr/bin/env python3
import requests
import os


file_location = "/home/student-02-abb769c733f4/supplier-data/images"
url = "http://localhost/upload/"
for files in os.listdir(file_location):
  try:
    filename, ext = os.path.splitext(files)
    if ext == '.jpeg':
      with open(file_location+ '/' + files, 'rb') as opened:
        r = requests.post(url, files = {'file': opened})
  except:
    print(r.text)







