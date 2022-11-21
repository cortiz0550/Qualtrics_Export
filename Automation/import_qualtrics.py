# All of these libraries are built into the base Python so you shouldn't have to install any. 
import requests
import json
import time


# my_secrets is just a .py file in the same folder as this script.
# It holds the variables that we don't want others to see in the code.
# (probably not necessary but good practice)
import my_secrets


# These are variables in the my_secrets.py file that we imported above.
api_token = my_secrets.api_token
data_center = my_secrets.data_center


# Here is the url we are using to grab the info from, along with the header info.
next_page = "https://{0}.qualtrics.com/API/v3/surveys".format(data_center)
headers = {
	"x-api-token": api_token,
	}


# This is an object that will have all our data from the request.
json_data = {}

# Qualtrics only spits out 100 surveys at a time, so we have to loop through until
# the "next_page" is Null (None).
while next_page is not None:
	response = requests.get(next_page, headers=headers)
	page_data = json.loads(response.text)

	# THIS NEEDS TO BE CLEANED UP!
	if len(json_data) == 0:
		json_data = page_data
	else:
		# Here we're appending the data from the new page onto our previous data
		# so its all in one place.
		for survey in page_data['result']['elements']:
			json_data['result']['elements'].append(survey)
	next_page = page_data['result']['nextPage']
	time.sleep(0.5)


# This just writes the response to a .json file
with open("surveys.json", "w", encoding="utf-8") as out_file:
	json.dump(json_data, out_file, ensure_ascii=False, indent=4)