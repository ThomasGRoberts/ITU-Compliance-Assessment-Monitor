"""
Name: 			snl_historical.py
Description: 	Downloads historical network information from the ITU's Space Network List.
Author:			Thomas G. Roberts (thomasgr@mit.edu / thomasgroberts.com)
Date: 			August 3, 2023

Input:			n/a
Output:			../Data/SNL Downloads/[YYYYMMDD]/networks_[YYYYMMDD].csv	
"""

## The ITU Space Network List includes relevant information about space network filings in four places. One place has filing data associated with non-planned space networks, another has filing data planned space networks, a third has information that describes which networks have been brought into use, and a fourth describes periods in which some networks have been suspended and/or resumed service. This script downloads those four datasets and organizes them into one easy-to-read file. 

import os
from datetime import datetime
import csv
import numpy as np
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup

# Choose a date to run the assessment
assessmentdate = datetime.today().strftime('%Y%m%d')

## The data on the ITU SNL may change as new filings are added or old filings are amended. Today's data should be saved in a sub-directory named with today'y date. 
# Check whether today's subdirectory exists in the relevant SNL Downloads sub-directory
MYDIR = ('../Data/SNL Downloads/' + assessmentdate)
CHECK_FOLDER = os.path.isdir(MYDIR)
# If it doesn't exist, then create it and run the scrape scripts.
if not CHECK_FOLDER:
	os.makedirs(MYDIR)
	print("New sub-directory created: ", MYDIR)
	os.system('python3 snl_unplanned_scrape.py')
	print("The non-planned portion of the SNL has been scraped and saved.")
	os.system('python3 snl_planned_scrape.py')
	print("The planned portion of the SNL has been scraped and saved.")
	os.system('python3 snl_broughtintouse_download.py')
	print("The SNL's brought-into-use data has been downloaded.")
	os.system('python3 snl_suspended_download.py')
	print("The SNL's suspension data has been downloaded.")
	os.system('python3 snl_namechange_download.py')
	print("The SNL's name-change data has been downloaded.")
# If it does exist, clear it (to avoid duplicates) and run the scrape scripts.
else:
	for f in os.listdir(MYDIR):
		os.remove(os.path.join(MYDIR, f))
	print("Existing sub-directory emptied: ", MYDIR)	
	os.system('python3 snl_unplanned_scrape.py')
	print("The non-planned portion of the SNL has been scraped and saved.")
	os.system('python3 snl_planned_scrape.py')
	print("The planned portion of the SNL has been scraped and saved.")
	os.system('python3 snl_broughtintouse_download.py')
	print("The SNL's brought-into-use data has been downloaded.")
	os.system('python3 snl_suspended_download.py')
	print("The SNL's suspension data has been downloaded.")
	os.system('python3 snl_namechange_download.py')
	print("The SNL's name-change data has been downloaded.")

## Create a quick dictionary for mapping ssn_ref symbols to filing types
ssnref_list = []
notifreasons_list = []
with open("../Data/Reference Files/ssnrefs.csv") as f:
	reader = csv.reader(f, delimiter=",")
	for row in reader:
		if row[0] != "ssn_ref":
			ssnref_list.append(row[0])
			notifreasons_list.append(row[1])
ssnref_dict = {ssnref_list[i]: notifreasons_list[i] for i in range(len(ssnref_list))}

## Import the list of networks that have had their names changed
newnames_list = []
oldnames_list = []
with open('../Data/SNL Downloads/' + assessmentdate + '/snl_namechange_' + assessmentdate + '.csv') as f:
	reader = csv.reader(f, delimiter=",")
	for row in reader:
		if row[0] != 'New Name':
			newnames_list.append(row[0])
			oldnames_list.append(row[1])

## Now let's organize the data into one easy-to-read file. 
# Write lists that ranks the order of the various filing types that can be found in the unplanned and planned list by maturity. More mature filings types appear later in these lists.
unplanned_types = ['A', 'U', 'C', 'N']
planned_types = ['P/Plan/List', 'P', 'U', 'N']
# Make a list of planned networks and their most-mature filing categories.
unplanned_license_names = []
unplanned_license_types = []
with open('../Data/SNL Downloads/' + assessmentdate + '/snl_unplanned_' + assessmentdate + '.csv') as f:
	reader = csv.reader(f, delimiter=",")
	for row in reader:
		if row[2] not in unplanned_license_names:
			unplanned_license_names.append(row[2])
			unplanned_license_types.append(row[3])
		else: 
			index = unplanned_license_names.index(row[2])
			unplanned_license_types[index] = unplanned_types[max(unplanned_types.index(row[3]), unplanned_types.index(unplanned_license_types[index]))]
# Make a list of planned networks and their most-mature filing categories.
planned_license_names = []
planned_license_types = []
with open('../Data/SNL Downloads/' + assessmentdate + '/snl_planned_' + assessmentdate + '.csv') as f:
	reader = csv.reader(f, delimiter=",")
	for row in reader:
		if row[2] not in planned_license_names:
			planned_license_names.append(row[2])
			planned_license_types.append(row[4])
		else: 
			index = planned_license_names.index(row[2])
			planned_license_types[index] = planned_types[max(planned_types.index(row[4]), planned_types.index(planned_license_types[index]))]
# Write a Pandas dataframe house the organized data
df_licenses = pd.DataFrame(0, columns = ['Network Name', 'Longitude', 'ITU Administration', 'Previous Name', 'Planned or Non-Planned', 'Highest Maturity', 'Brought-into-Use Date', 'Late-Stage Filing Date', 'Early-Stage Filing Date', 'Suspensions', 'Link'], index = np.arange(len(planned_license_names) + len(unplanned_license_names)))
# Drop in the lists of unique licenses
df_licenses['Network Name'] = unplanned_license_names + planned_license_names
df_licenses['Planned or Non-Planned'] = ['Non-Planned']*len(unplanned_license_names) + ['Planned']*len(planned_license_names)
df_licenses['Highest Maturity'] = unplanned_license_types + planned_license_types 
# Quickly import the four raw datasets
df_planned = pd.read_csv('../Data/SNL Downloads/' + assessmentdate + '/snl_planned_' + assessmentdate + '.csv', header = None)
df_unplanned = pd.read_csv('../Data/SNL Downloads/' + assessmentdate + '/snl_unplanned_' + assessmentdate + '.csv', header = None)
df_broughtintouse = pd.read_csv('../Data/SNL Downloads/' + assessmentdate + '/snl_broughtintouse_' + assessmentdate + '.csv')
df_suspended = pd.read_csv('../Data/SNL Downloads/' + assessmentdate + '/snl_suspended_' + assessmentdate + '.csv')
# Fill in the rest of the dataframe
for i in np.arange(len(df_licenses)):
	print('Fetching network information for', df_licenses.at[i, 'Network Name'], '...')
	if df_licenses.at[i, 'Planned or Non-Planned'] == 'Non-Planned':
		for j in np.arange(len(df_unplanned)):
			if (df_unplanned.iat[j, 2] == df_licenses.at[i, 'Network Name'] and df_unplanned.iat[j, 3] == df_licenses.at[i,'Highest Maturity']):
				df_licenses.at[i, 'Longitude'] = df_unplanned.iat[j, 0]	
				df_licenses.at[i, 'ITU Administration'] = df_unplanned.iat[j, 1]
				df_licenses.at[i, 'Link'] = 'https:' + df_unplanned.iat[j, 6]
	if df_licenses.at[i, 'Planned or Non-Planned'] == 'Planned':
		for j in np.arange(len(df_planned)):
			if (df_planned.iat[j, 2] == df_licenses.at[i, 'Network Name'] and df_planned.iat[j, 4] == df_licenses.at[i,'Highest Maturity']):
				df_licenses.at[i, 'Longitude'] = df_planned.iat[j, 0]	
				df_licenses.at[i, 'ITU Administration'] = df_planned.iat[j, 1]
				df_licenses.at[i, 'Link'] = 'https:' + df_planned.iat[j, 7]
	dates = []
	for j in np.arange(len(df_broughtintouse)):
		if str(df_broughtintouse.iat[j, 0]) == str(df_licenses.at[i, 'Network Name']):
			dates.append(datetime.strptime(df_broughtintouse.iat[j, 4], '%d.%m.%Y'))
	if len(dates) == 0:
		df_licenses.at[i, 'Brought-into-Use Date'] = 'n/a'
	else:
		date = str(min(dates))[0:10] 
		df_licenses.at[i, 'Brought-into-Use Date'] = date
	df_licenses.at[i, 'Previous Name'] = 'n/a'
	for j in np.arange(len(newnames_list)):
		newname = newnames_list[j]
		oldname = oldnames_list[j]
		if df_licenses.at[i, 'Network Name'] == newname:
			df_licenses.at[i, 'Previous Name'] = oldname
	suspensions = []
	for j in np.arange(len(df_suspended)):
		suspension = []
		if str(df_suspended.iat[j, 1]) == str(df_licenses.at[i, 'Network Name']):
			suspension = [str(df_suspended.iat[j, 6]).strip()]
			# Check if the suspension date field is filled
			if len(str(df_suspended.iat[j, 8])) > 4:
				suspension.append(str(datetime.strptime(df_suspended.iat[j, 8], '%d.%m.%Y'))[0:10])
			if len(str(df_suspended.iat[j, 10])) > 4:
				suspension.append(str(datetime.strptime(df_suspended.iat[j, 10], '%d.%m.%Y'))[0:10])
			else:
				suspension.append('n/a')
		if (len(suspension) > 0 and suspension not in suspensions):
			suspensions.append(suspension)
	if suspensions == []:
		df_licenses.at[i, 'Suspensions'] = 'n/a'
	else:
		df_licenses.at[i, 'Suspensions'] = suspensions

	# Visit the network's associated page on the SNL and find its early- and late-stage filing dates
	df_licenses.at[i, 'Early-Stage Filing Date'] = 'n/a'
	df_licenses.at[i, 'Late-Stage Filing Date'] = 'n/a'
	try:
		earlystage_dates = []
		latestage_dates = []
		nameforlink = df_licenses.at[i, 'Network Name'].replace(' ', '%20')
		nameforlink = nameforlink.replace('&', '%26')
		url_network_textexport = 'https://www.itu.int/net/ITU-R/space/snl/bresult/radvanceall.asp?sel_satname=' + nameforlink + '&sel_esname=&sel_adm=&sel_org=&sel_ific=&sel_year=&sel_date_from=&sel_date_to=&sel_rcpt_from=&sel_rcpt_to=&sel_orbit_from=&sel_orbit_to=&sup=&q_reference=&q_ref_numero=&q_sns_id=&res32=&norder=&nmod='
		source = urllib.request.urlopen(url_network_textexport).read()
		soup = BeautifulSoup(source,'html.parser')
		tables = soup.find_all('table')

		try:
			table_rows = tables[2].find_all('tr')
			output_rows = []

			for table_row in tables[2].findAll('tr'):
				columns = table_row.findAll('td')
				links = table_row.findAll('a')
				output_row = []
				for column in columns:
					output_row.append(column.text)
				for link in links:
					output_row.append(link.get('href'))
				if output_row[6].replace('\xa0', ' ').strip() != 'Date of receipt': 
					ssn_ref = output_row[7].replace('\xa0', ' ').strip()
					try:
						notif_reason = ssnref_dict[ssn_ref]
						if len(output_row[6].replace('\xa0', ' ').strip()) == 10:
							if notif_reason in ['P', 'A', 'C', 'U']:
								earlystage_dates.append(datetime.strptime(output_row[6].replace('\xa0', ' ').strip(), '%d.%m.%Y'))
							else:
								latestage_dates.append(datetime.strptime(output_row[6].replace('\xa0', ' ').strip(), '%d.%m.%Y'))
					except KeyError as keyerror:
						print('An identified ssn_ref does not appear in the ssn_ref dictionary:', keyerror)
		except IndexError:
			pass
		if len(earlystage_dates) != 0:
			df_licenses.at[i, 'Early-Stage Filing Date'] = str(min(earlystage_dates))[0:10]
		if len(latestage_dates) != 0:
			df_licenses.at[i, 'Late-Stage Filing Date'] = str(min(latestage_dates))[0:10]
	except UnicodeEncodeError:
		pass

# Consider networks with name changes
for i in np.arange(len(df_licenses)):
	if df_licenses.at[i, 'Previous Name'] != 'n/a':
		oldname = df_licenses.at[i, 'Previous Name']
		for j in np.arange(len(df_licenses)):
			if df_licenses.at[i, 'Network Name'] == oldname:
				oldnetwork_broughtintouse = df_licenses.at[j, 'Brought-into-Use Date']
				oldnetwork_latestage = df_licenses.at[j, 'Late-Stage Filing Date']
				oldnetwork_earlystage = df_licenses.at[j, 'Early-Stage Filing Date']
				oldnetwork_suspensions = df_licenses.at[j, 'Suspensions']
				# Consider cases in which the older network has some data associated with it
				if oldnetwork_broughtintouse != 'n/a':
					if df_licenses.at[i, 'Brought-into-Use Date'] == 'n/a':
						df_licenses.at[i, 'Brought-into-Use Date'] = oldnetwork_broughtintouse
					else:
						df_licenses.at[i, 'Brought-into-Use Date'] = min(datetime.strptime(df_licenses.at[i, 'Brought-into-Use Date'], '%Y-%m-%d'), oldnetwork_broughtintouse)[0:10]
				if oldnetwork_latestage != 'n/a':
					if df_licenses.at[i, 'Late-Stage Filing Date'] == 'n/a':
						df_licenses.at[i, 'Late-Stage Filing Date'] = oldnetwork_latestage
					else:
						df_licenses.at[i, 'Late-Stage Filing Date'] = min(datetime.strptime(df_licenses.at[i, 'Late-Stage Filing Date'], '%Y-%m-%d'), oldnetwork_latestage)[0:10]
				if oldnetwork_earlystage != 'n/a':
					if df_licenses.at[i, 'Early-Stage Filing Date'] == 'n/a':
						df_licenses.at[i, 'Early-Stage Filing Date'] = oldnetwork_earlystage
					else:
						df_licenses.at[i, 'Early-Stage Filing Date'] = min(datetime.strptime(df_licenses.at[i, 'Early-Stage Filing Date'], '%Y-%m-%d'), oldnetwork_earlystage)[0:10]
				if oldnetwork_suspensions != []:
					newnetwork_suspensions = df_licenses.at[i, 'Suspensions']
					if newnetwork_suspensions == 'n/a':
						df_licenses.at[i, 'Suspensions'] = oldnetwork_suspensions
					else:
						for suspension in oldnetwork_suspensions:
							if suspension not in newnetwork_suspensions:
								newnetwork_suspensions.append(suspension)
						df_licenses.at[i, 'Suspensions'] = newnetwork_suspensions
# Sort the data by longitude
df_licenses = df_licenses.sort_values('Longitude', ascending = True)
# Save the file to a CSV
df_licenses.to_csv('../Data/SNL Downloads/' + assessmentdate + '/networks_' + assessmentdate + '.csv', index = None)


