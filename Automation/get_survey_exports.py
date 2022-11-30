''' The purpose of this program is to download Qualtrics exports according to
	a report schedule. It will only download data as needed following the schedule '''

import pandas as pd
import zipfile, io
import os

import date_selector
import API_functions

# This will hold the statuses at each stage of the download for each survey.
statuses = []

# This dataframe holds the reporting schedule.
report_schedule_df = pd.read_csv('Reporting\\Report_Schedule.csv')

dir_save_survey = # Place where downloaded surveys will be saved within their own folder.

surveys_to_report = date_selector.surveys


# The program will go through these steps for every survey in the report schedule
# that requires reporting (based on the "Schedule" column).
for i in range(len(surveys_to_report)):
	survey = surveys_to_report[i]['survey_id']
	folder = surveys_to_report[i]['survey_name'].split('_')[0]

	# Step 1: Create the Data Export
	request_response = API_functions.initiate_request(survey_id=survey)
	print(request_response)

	# Step 2: Check the status of the file until it's ready for download
	if request_response['meta']['httpStatus'] == '200 - OK':
		request_progress = API_functions.check_request_progress(survey_id=survey, progress_id=request_response['result']['progressId'])
		print(request_progress)

	# Step 3: Download the file
	if request_progress['meta']['httpStatus'] == '200 - OK':
		request_download = API_functions.download_request(survey_id=survey, file_id=request_progress['result']['fileId'])
		print(request_download)

	complete = request_response['meta']['httpStatus'] == '200 - OK'	and request_progress['meta']['httpStatus'] == '200 - OK' and str(request_download) == '<Response [200]>'

	statuses.append([
		survey,
		surveys_to_report[i]["survey_name"],
		request_response['meta']['httpStatus'],
		request_progress['meta']['httpStatus'],
		str(request_download),
		complete])

	# Step 4: Unzip the file
	zipfile.ZipFile(io.BytesIO(request_download.content)).extractall(dir_save_survey + folder)
	print(survey + " downloaded.")


# This dataframe holds all of the data around the statuses of each download.
# It'll help us identify where errors may occur if something doesn't download.
status_df = pd.DataFrame(
	statuses, 
	columns=[
		"Survey ID", 
		"Survey Name", 
		"Create Status", 
		"Ready Status", 
		"Download Status",
		"Complete"]
	)

# Writing this to a csv file so we can review the downloads.
log_name = "status_log.csv"
outdir = # Path to place where log is held.
# Make a new Logs directory if it doesn't already exist.
if not os.path.exists(outdir):
    os.mkdirs(outdir)

fullname = os.path.join(outdir, log_name)

status_df.to_csv(fullname)
print("Downloads completed.")
