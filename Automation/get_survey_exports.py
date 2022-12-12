''' The purpose of this program is to download Qualtrics exports according to
	a report schedule. It will only download data as needed following the schedule '''

import pandas as pd
import zipfile, io
import os

import date_selector
import API_functions
import paths

# This will hold the statuses at each stage of the download for each survey.
statuses = []

dir_save_survey = paths.dir_save_survey

surveys_to_report = date_selector.surveys

# We dont want to go through any of the steps if there are no surveys to report on.
if len(surveys_to_report) == 0:
	print("No surveys to download today.")

else:
	# The program will go through these steps for every survey in the report schedule
	# that requires reporting (based on the "Schedule" column).
	for i in range(len(surveys_to_report)):
		survey = surveys_to_report[i]['survey_id']
		survey_name = surveys_to_report[i]["survey_name"]
		folder = survey_name.split('_')[0]
		file_format = surveys_to_report[i]["file_format"]
		breakout_sets = surveys_to_report[i]["split_columns"] or False
		use_labels = surveys_to_report[i]["use_labels"] or True


		print("Download of " + survey_name + " in progress...")
		# Step 1: Create the Data Export
		request_response = API_functions.initiate_request(survey_id=survey,file_format=file_format, breakout_sets=breakout_sets, use_labels=use_labels)

		# Step 2: Check the status of the file until it's ready for download
		if request_response['meta']['httpStatus'] == '200 - OK':
			request_progress = API_functions.check_request_progress(survey_id=survey, progress_id=request_response['result']['progressId'])

		# Step 3: Download the file
		if request_progress['meta']['httpStatus'] == '200 - OK':
			request_download = API_functions.download_request(survey_id=survey, file_id=request_progress['result']['fileId'])

		complete = request_response['meta']['httpStatus'] == '200 - OK'	and request_progress['meta']['httpStatus'] == '200 - OK' and str(request_download) == '<Response [200]>'

		statuses.append([
			survey,
			surveys_to_report[i]["survey_name"],
			request_response['meta']['httpStatus'],
			request_progress['meta']['httpStatus'],
			str(request_download),
			complete])

		# Step 4: Unzip the file if downloaded
		if complete:
			zipfile.ZipFile(io.BytesIO(request_download.content)).extractall(dir_save_survey + folder)
			print(surveys_to_report[i]["survey_name"] + " downloaded.")
			print('') # This is just to make reading the content easier when you run the program.
		else:
			print("Error: " + surveys_to_report[i]["survey_name"] + " was not downloaded.")
			print('') # This is just to make reading the content easier when you run the program.


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
	today = str(date_selector.today) # This is today's date
	log_name = "status_log" + today + ".csv"
	log_dir = paths.log_dir
	# Make a new Logs directory if it doesn't already exist.
	if not os.path.exists(log_dir):
	    os.mkdirs(log_dir)

	fullname = os.path.join(log_dir, log_name)

	status_df.to_csv(fullname)
	print("Downloads completed.")
