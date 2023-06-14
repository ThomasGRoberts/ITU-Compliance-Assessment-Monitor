"""
Name: 			snl.py
Description: 	Downloads license information from the ITU's Space Network List.
Author:         Thomas G. Roberts (thomasgr@mit.edu / thomasgroberts.com)
Date: 			June 8, 2023

Input:			n/a
Output:			../Data/SNL Archives/[YYYYMMDD]/licenses_[YYYYMMDD].csv	
"""

## The ITU Space Network List includes relevant information about space network filings in three places. One place has filing data associated with unplanned space network licenses, another has filing data planned space network licenses, and a third has information describes whether both the unplanned and planned licenses have been brought into use. This script downloads those three datasets and organizes them into one easy-to-read file. 

import os
from datetime import datetime
import csv
import numpy as np
import pandas as pd

## The data on the ITU SNL may change as new filings are added or old filings are amended. Today's data should be saved in a sub-directory named with today'y date: ../Data/SNL Archives/[YYYYMMDD]. 
# Check whether today's directory exists:
MYDIR = ('../Data/SNL Archives/' + datetime.today().strftime('%Y%m%d'))
CHECK_FOLDER = os.path.isdir(MYDIR)
# If it doesn't exist, then create it.
if not CHECK_FOLDER:
    os.makedirs(MYDIR)
    print("created folder : ", MYDIR)
# If it does exist, then empty it, so that the new files don't contain any duplicate entries.
else:
	for f in os.listdir(MYDIR):
	    os.remove(os.path.join(MYDIR, f))

## Run the three scripts associated with pulling data from the three sources
os.system('python3 snl_unplanned_scrape.py')
print("The non-planned portion of the SNL has been scraped and saved.")
os.system('python3 snl_planned_scrape.py')
print("The planned portion of the SNL has been scraped and saved.")
os.system('python3 snl_broughtintouse_download.py')
print("The SNL's brought-into-use data has been downloaded.")

## Now let's organize the data into one easy-to-read file. 
# Write lists that ranks the order of the various filing types that can be found in the unplanned and planned list. More mature filings types appear later in these lists.
unplanned_types = ['A', 'C', 'N', 'U']
planned_types = ['P/Plan/List', 'P', 'N', 'U']
# Make a list of planned licenses and their most-mature filing categories.
unplanned_license_names = []
unplanned_license_types = []
with open('../Data/SNL Archives/' + datetime.today().strftime('%Y%m%d') + '/snl_unplanned_' + datetime.today().strftime('%Y%m%d') + '.csv') as f:
	reader = csv.reader(f, delimiter=",")
	for row in reader:
		if row[2] not in unplanned_license_names:
			unplanned_license_names.append(row[2])
			unplanned_license_types.append(row[3])
		else: 
			index = unplanned_license_names.index(row[2])
			unplanned_license_types[index] = unplanned_types[max(unplanned_types.index(row[3]), unplanned_types.index(unplanned_license_types[index]))]
# Make a list of planned licenses and their most-mature filing categories.
planned_license_names = []
planned_license_types = []
with open('../Data/SNL Archives/' + datetime.today().strftime('%Y%m%d') + '/snl_planned_' + datetime.today().strftime('%Y%m%d') + '.csv') as f:
	reader = csv.reader(f, delimiter=",")
	for row in reader:
		if row[2] not in planned_license_names:
			planned_license_names.append(row[2])
			planned_license_types.append(row[4])
		else: 
			index = planned_license_names.index(row[2])
			planned_license_types[index] = planned_types[max(planned_types.index(row[4]), planned_types.index(planned_license_types[index]))]
# Write a Pandas dataframe house the organized data
df_licenses = pd.DataFrame(0, columns = ['License Name', 'Longitude', 'ITU Administration', 'Planned or Non-Planned', 'Highest Maturity', 'Brought-into-Use Date', 'Link'], index = np.arange(len(planned_license_names) + len(unplanned_license_names)))
# Drop in the lists of unique licenses
df_licenses['License Name'] = unplanned_license_names + planned_license_names
df_licenses['Planned or Non-Planned'] = ['Non-Planned']*len(unplanned_license_names) + ['Planned']*len(planned_license_names)
df_licenses['Highest Maturity'] = unplanned_license_types + planned_license_types 
# Quickly import the three raw datasets
df_planned = pd.read_csv('../Data/SNL Archives/' + datetime.today().strftime('%Y%m%d') + '/snl_planned_' + datetime.today().strftime('%Y%m%d') + '.csv', header = None)
df_unplanned = pd.read_csv('../Data/SNL Archives/' + datetime.today().strftime('%Y%m%d') + '/snl_unplanned_' + datetime.today().strftime('%Y%m%d') + '.csv', header = None)
df_broughtintouse = pd.read_csv('../Data/SNL Archives/' + datetime.today().strftime('%Y%m%d') + '/snl_broughtintouse_' + datetime.today().strftime('%Y%m%d') + '.csv')
# Fill in the rest of the dataframe
for i in np.arange(len(df_licenses)):
	print('Fetching license information for', df_licenses.at[i, 'License Name'], '...')
	if df_licenses.at[i, 'Planned or Non-Planned'] == 'Non-Planned':
		for j in np.arange(len(df_unplanned)):
			if (df_unplanned.iat[j, 2] == df_licenses.at[i, 'License Name'] and df_unplanned.iat[j, 3] == df_licenses.at[i,'Highest Maturity']):
				df_licenses.at[i, 'Longitude'] = df_unplanned.iat[j, 0]	
				df_licenses.at[i, 'ITU Administration'] = df_unplanned.iat[j, 1]
				df_licenses.at[i, 'Link'] = 'https:' + df_unplanned.iat[j, 6]
	if df_licenses.at[i, 'Planned or Non-Planned'] == 'Planned':
		for j in np.arange(len(df_planned)):
			if (df_planned.iat[j, 2] == df_licenses.at[i, 'License Name'] and df_planned.iat[j, 4] == df_licenses.at[i,'Highest Maturity']):
				df_licenses.at[i, 'Longitude'] = df_planned.iat[j, 0]	
				df_licenses.at[i, 'ITU Administration'] = df_planned.iat[j, 1]
				df_licenses.at[i, 'Link'] = 'https:' + df_planned.iat[j, 7]
	dates = []
	for j in np.arange(len(df_broughtintouse)):
		if str(df_broughtintouse.iat[j, 0]) == str(df_licenses.at[i, 'License Name']):
			dates.append(datetime.strptime(df_broughtintouse.iat[j, 4], '%d.%m.%Y'))
	if len(dates) == 0:
		df_licenses.at[i, 'Brought-into-Use Date'] = 'n/a'
	else:
		date = str(min(dates))[0:10] 
		df_licenses.at[i, 'Brought-into-Use Date'] = date
# Sort the data by longitude
df_licenses = df_licenses.sort_values('Longitude', ascending = True)
# Save the file to a CSV
df_licenses.to_csv('../Data/SNL Archives/' + datetime.today().strftime('%Y%m%d') + '/licenses_' + datetime.today().strftime('%Y%m%d') + '.csv', index = None)


