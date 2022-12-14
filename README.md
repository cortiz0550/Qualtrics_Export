# PURPOSE

Reporting is such an important part of our role, but it can be very time consuming to manually go in and 
download the files, unzip them, and put them in their necessary places. This program is meant to automatically 
download surveys based on their reporting schedules, so that all you have to do is run one thing, and you will
get the data exports in a separate folder based on the project they are associated with. Hopefully it saves you a 
bunch of time!

# STRUCTURE

The main folder contains three sub folders: Automation, Reporting, and Logs. The Automation folder holds all of the programs
and code that is needed to download the data exports, while the Reporting folder holds a list of your surveys with
their reporting schedules ("Report_Schedule.csv") and will hold the completed data export downloads. The Logs folder will keep track of all the requests, and give you info on whether or not they were successful.


# STEPS

0a- Find your data center ID and generate an API token in your Qx account. Then once you have those, open the "my_secrets.py" file and fill those two variables in.
*This is VERY important, otherwise the rest of the programs will not work. These two items allow Qualtrics to connect
to your account to grab any data on it.*

0b- This is not a mandatory step, but it will be helpful later on. Again, in the Automations folder, you can run the
"import_qualtrics.py" script which will generate a json document with all the surveys and their IDs in your account.
This is helpful to grab IDs from or get an idea of what your account looks like.

1- Now, you are ready to start building your report schedule. Using the IDs from the last step (or some other way), fill
out the "Report_Schedule.csv" file. For the schedule column, do not use spaces between days. So if you need reporting on
Tuesday and Thursday, the entry should look like Tuesday;Thursday.

2- Once your schedule is ready, save it and close it. Then navigate to the Automation folder and run "get_survey_exports.py"
and all the surveys you have added to "Report_Schedule.csv" will automatically be downloaded from Qualtrics!

3- You can check for any issues with downloading the reports in the "status_log_[date].csv" file. This is found in the "Logs" folder. Here we see if any of the downloaded surveys ran into issues, or if they were successfully completed. The log is helpful for troubleshooting.

# RESOURCES

The documentation for the Qualtrics API is really good, so check that out if you'd like: https://api.qualtrics.com/48f1226327f89-overview
