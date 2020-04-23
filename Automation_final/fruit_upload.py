#! /usr/bin/env python3

import os
import requests

def create_dict_payload(text_file, image_file):
  payload = {}
  try:
    with open(text_file, 'r') as description:
      payload["name"] = description.readline().strip()
      fruit_wt = description.readline().strip()
      payload["weight"] = int(fruit_wt.split(" ")[0])
      payload["description"] = description.read().rstrip('\n')
      payload["image_name"] = image_file
  except Exception as e:
    print(e)
  return payload


if __name__ == "__main__":
  file_location =  "/home/student-03-b3b366a6ca1b/supplier-data/descriptions"
  url = "http://35.225.44.229/fruits/"
  for desc in os.listdir(file_location):
      filename, ext = os.path.splitext(desc)
      filename = filename + '.jpeg'
      print(filename)
      data = create_dict_payload(file_location+'/'+desc, filename)
      print(data)
      try:
        r = requests.post(url, data=create_dict_payload(file_location+'/'+desc,filename))
        r.raise_for_status()
      except Exception as e:
        print(r.text)
