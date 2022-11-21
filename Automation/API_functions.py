import requests
import csv
import time

import my_secrets

api_token = my_secrets.api_token
data_center = my_secrets.data_center
file_format = ["csv", "csv", "spss"]

# Setting static parameters
headers = {
    "content-type": "application/json",
    "x-api-token": api_token
}


# This starts the download process by requesting the data from Qualtrics.
def initiate_request(survey_id, data_center=data_center, api_token=api_token):
	initiate_request_url = "https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses/".format(data_center, survey_id)
	initiate_request_payload = {
		"format": file_format[0],
		"breakoutSets": False,
		"multiselectSeenUnansweredRecode": 0,
		"seenUnansweredRecode": -99,
		"useLabels": True
	}

	initiate_response = requests.request("POST", initiate_request_url, json=initiate_request_payload, headers=headers)

	return initiate_response.json()


# Here we are checking to see if the file is ready to be downloaded. We need to wait until it is fully loaded before
# downloading it.
def check_request_progress(survey_id, progress_id, data_center=data_center, api_token=api_token):
	progress = 0
	progress_status = "in progress"

	# This will keep running the progress request until the file is ready for download.
	while(progress < 100 and progress_status != "complete"):
		check_request_url = "https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses/{2}".format(data_center, survey_id, progress_id)
		check_request_response = requests.request('GET', check_request_url, headers=headers)
		
		# If progress hits 100, the loop breaks even if the download fails.
		progress = check_request_response.json()['result']['percentComplete']

		# This is to make sure we aren't making too many calls to the API (0.5 seconds is arbitrary).
		time.sleep(0.5)

	return check_request_response.json()

# This is for downloading the file.
def download_request(survey_id, file_id, data_center=data_center, api_token=api_token):
	download_request_url = "https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses/{2}/file".format(data_center, survey_id, file_id)
	request_download = requests.request('GET', download_request_url, headers=headers, stream=True)
	return request_download

















