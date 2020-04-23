#! /usr/bin/env python3

from PIL import Image
import os

file_location = "/home/student-02-abb769c733f4/supplier-data/images"
for file in os.listdir(file_location):
  try:
    with Image.open(file_location + '/' + file) as Imagefile:
      Imagefile = Imagefile.resize((600,400))
      Imagefile.convert("RGB")
      filename , ext = os.path.splitext(file)
      filename = filename + '.jpeg'
      Imagefile.save(file_location + '/' + filename, "JPEG")
  except Exception as e:
    print(e)
