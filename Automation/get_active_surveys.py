# May not need to import these in each file
import requests
import os
import json

with open("surveys.json", "r") as in_file:
	file = in_file.read()


obj = json.loads(file)

active_surveys = []
for i in range(len(obj['result']['elements'])):
	if obj['result']['elements'][i]['isActive']:
		active_surveys.append(obj['result']['elements'][i]['id'])

print(len(active_surveys))