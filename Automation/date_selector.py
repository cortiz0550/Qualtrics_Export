''' This function will select surveys from the Report Schedule file
	based on which of them need reporting that day. '''

import datetime
import pandas as pd

date_cols = ["Start_Date", "End_Date"]
path = # Path to Report_Schedule.csv

report_schedule_df = pd.read_csv(path, parse_dates=date_cols)
today = datetime.date.today()

weekday_mapping = {day: index for index, day in enumerate((
	"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"))}

surveys = []

for i in range(len(report_schedule_df['Survey_ID'])):

	start_date = report_schedule_df['Start_Date'][i] if not pd.isnull(report_schedule_df['Start_Date'][i]) else datetime.date.min
	end_date = report_schedule_df['End_Date'][i] if not pd.isnull(report_schedule_df['End_Date'][i]) else datetime.date.max
	print(start_date, end_date)

	if (start_date <= today) and (today <= end_date):
		days = report_schedule_df['Schedule'][i].split(";")

		selected_weekdays = []

		for day in days:
			selected_weekdays.append(weekday_mapping.get(day,day))
		print(selected_weekdays)

	print(today.weekday())
	if today.weekday() in selected_weekdays:

		surveys.append({
			"survey_id": report_schedule_df['Survey_ID'][i],
			"survey_name": report_schedule_df['Survey_Name'][i],
			"schedule": days})



