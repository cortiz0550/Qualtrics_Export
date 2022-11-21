''' The purpose of this program is to download Qualtrics exports according to
	a report schedule. It will only download data as needed following the schedule '''

import pandas as pd
import zipfile, io

import date_selector
import API_functions as api


# This dataframe holds the reporting schedule.
report_schedule_df = pd.read_csv('C:\\Users\\E33100\\OneDrive - SRI International\\My Stuff\\Me\\Qualtrics\\Reporting\\Report_Schedule.csv')

dir_save_survey = "C:\\Users\\E33100\\OneDrive - SRI International\\My Stuff\\Me\\Qualtrics\\Reporting\\"

surveys_to_report = date_selector.surveys


# The program will go through these steps for every survey in the report schedule
# that requires reporting (based on the "Schedule" column).
for i in range(len(surveys_to_report)):
	survey = surveys_to_report[i]['survey_id']
	folder = surveys_to_report[i]['survey_name'].split('_')[0]

	# Step 1: Create the Data Export
	request_response = api.initiate_request(survey_id=survey)
	print(request_response)

	# Step 2: Check the status of the file until it's ready for download
	request_progress = api.check_request_progress(survey_id=survey, progress_id=request_response['result']['progressId'])
	print(request_progress)

	# Step 3: Download the file
	request_download = api.download_request(survey_id=survey, file_id=request_progress['result']['fileId'])
	print(request_download)

	# Step 4: Unzip the file
	zipfile.ZipFile(io.BytesIO(request_download.content)).extractall(dir_save_survey + folder)
	print(survey + " downloaded.")



