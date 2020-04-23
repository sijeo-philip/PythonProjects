#! /usr/bin/env python3
import emails
import os
import reports
from datetime import date


file_location = "/home/student-02-abb769c733f4/supplier-data/descriptions"
data_list = []
sender = "automation@example.com"
receiver = "{}@example.com".format(os.environ.get('USER'))
subject = "Upload Completed - Online Fruit Store"
body = "All fruits are uploaded to our website successfully.A detailed list\n\is attached to this email\n"

def create_dict(text_file):
  payload = {}
  try:
    with open(text_file, 'r') as description:
      payload["name"] = description.readline().strip()
      fruit_wt = description.readline().strip()
      payload["weight"] = int(fruit_wt.split(" ")[0])
  except Exception as e:
    print(e)
  return payload


if __name__ == '__main__':
  today = date.today()
  report_date = today.strftime("%B %d, %Y")
  title = "Processed Update on {}".format(report_date)
  for txt_file in os.listdir(file_location):
    data_list.append(create_dict(file_location + '/' + txt_file))
  reports.generate_report('/tmp/processed.pdf', title, data_list)
  message = emails.generate_email(sender, receiver, subject, body, "/tmp/processed.pdf")
  emails.send_email(message)

