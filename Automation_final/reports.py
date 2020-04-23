#! /usr/bin/env python3

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os

filepath = './description'

def generate_report(filename, title, paragraph):
  story = []
  try:
    styles = getSampleStyleSheet()
    report = SimpleDocTemplate(filename)
    report_title = Paragraph(title, styles["h1"])
    story.append(report_title)
    for data in paragraph:
      story.append(Paragraph("name: {} <br /> weight: {} lbs <br /> ".format(data["name"], data["weight"]) , styles["BodyText"]))
      print(story)
      story.append(Spacer(1,20))
    report.build(story)
  except Exception as e:
    print(e)

def create_dict_payload(text_file):
  payload = {}
  try:
    with open(text_file, 'r') as description:
      payload["name"] = description.readline().strip()
      fruit_wt = description.readline().strip()
      payload["weight"] = int(fruit_wt.split(" ")[0])
  except Exception as e:
    print(e)
  return payload

if __name__ == "__main__":
	data_list = []
	for textFile in os.listdir(filepath):
		data_list.append(create_dict_payload(filepath +'/'+textFile))
	generate_report(filepath+'/processed.pdf', "This is Dummy PDF", data_list)
