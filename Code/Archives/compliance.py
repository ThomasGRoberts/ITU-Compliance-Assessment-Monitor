"""
Name:			    compliance.py
Description:	 Check whether GEO satellites' positions match any filed ITU space networks.
Author:		    Thomas G. Roberts (thomasgr@mit.edu / thomasgroberts.com)
Date: 			 August 3, 2023

Inputs:			 ../Data/Daily Analysis/[YYYYMMDD]/longitudes_[YYYYMMDD].csv
					 ../Data/SNL Archives/[YYYYMMDD]/networks_[YYYYMMDD].csv	
Outputs:			 ../Data/Nearby Shortlists/[YYYYMMDD]/[satcat]_[YYYYMMDD.csv]					
					 ../Data/Compliance Grades/grades_[YYYYMMDD].csv
"""

## This script issues a compliance rating for GEO satellites given their NORAD ID and longitudinal position. A shortlist of nearby filings is also produced for each GEO satellite.

import numpy as np
import csv
from datetime import datetime
import pandas as pd
import os
import sys

# Choose a date to run the assessment
assessmentdate = datetime.today().strftime('%Y%m%d')

# Check to see if a longitudes file has been put in the right sub-direcotry
file_path = os.path.join('../Data/Daily Analysis/' + assessmentdate, 'longitudes_' + assessmentdate + '.csv')
if os.path.exists(file_path):
	pass
else:
	print('A correctly named longitude file hasn\'t been added to the assessment dates\'s sub-directory. Please add it and run this script again.')
	sys.exit()

## Import relevant data
# Import the list of licenses created using snl.py
df_licenses = pd.read_csv('../Data/Daily Analysis/' + assessmentdate + '/SNL Archives/networks_' + assessmentdate + '.csv')
# Import a dictionary to convert ITU country symbols to designations
reader = csv.reader(open('../Data/Reference Files/ITUcountries.csv', 'r'))
countries_dictionary = {}
for row in reader:
   k, v = row
   countries_dictionary[k] = v
# Write a dictionary for the full names of filings type
filings_dictionary = {
	'A' 				: 'Advance Public Information (A)',
	'C'   			: 'Coordination Request (C)',
	'N'				: 'Notification of Space Station (N)',
	'U'				: 'Due Diligence (U)',
	'P'  				: 'Planned (P)',
	'P/Plan/List' 	: 'Planned (P/Plan/List)'
	}

# Write a maturity rank order of the various filings types 
filings_rankorder = ['Advance Public Information (A)', 'Planned (P/Plan/List)', 'Planned (P)', 'Coordination Request (C)', 'Notification of Space Station (N)', 'Due Diligence (U)']
# Import local launch history database as lists
locallaunchdatabase_cospar_list = []
locallaunchdatabase_norad_list = []
locallaunchdatabase_satname_list = []
locallaunchdatabase_country_list = []
locallaunchdatabase_launchdate_list = []
locallaunchdatabase_site_list = []
locallaunchdatabase_spaceport_list = []
locallaunchdatabase_decay_list = []
locallaunchdatabase_vehiclefamily_list = []
locallaunchdatabase_satellitemanufacturer_list = []
with open("../Data/Reference Files/satellitecatalog.csv") as f:
	reader = csv.reader(f, delimiter=",")
	for row in reader:
		if row[0] != 'COSPAR':
			locallaunchdatabase_cospar_list.append(row[0])
			locallaunchdatabase_norad_list.append(row[1])
			locallaunchdatabase_satname_list.append(row[2])
			locallaunchdatabase_country_list.append(row[3])
			launchdate_datetime = datetime.strptime(row[4], '%m/%d/%y')
			if launchdate_datetime.year > 2022: 
				launchdate_datetime2 = launchdate_datetime.replace(year = launchdate_datetime.year-100)
			else:
				launchdate_datetime2 = launchdate_datetime
			locallaunchdatabase_launchdate_list.append(launchdate_datetime2)
			locallaunchdatabase_site_list.append(row[5])
			locallaunchdatabase_spaceport_list.append(row[6])
			locallaunchdatabase_decay_list.append(row[7])
			locallaunchdatabase_vehiclefamily_list.append(row[8])
			locallaunchdatabase_satellitemanufacturer_list.append(row[9])
# Create a dictionary for mapping SpaceTrack country names to ITU symbols
SpaceTrackcountries_list = []
ITUcountrycodes_list = []
with open("../Data/Reference Files/SpaceTrackcountries.csv") as f:
	reader = csv.reader(f, delimiter=",")
	for row in reader:
		if row[0] != "SpaceTrack Abbreviation":
			SpaceTrackcountries_list.append(row[0])
			row_list = [row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30], row[31]]
			while('' in row_list):
				row_list.remove('')
			if len(row_list) == 0:
				row_list = ['n/a']
			ITUcountrycodes_list.append(row_list)
SpaceTrackcountries_dict = {SpaceTrackcountries_list[i]: ITUcountrycodes_list[i] for i in range(len(SpaceTrackcountries_list))}
# Create a dictionary to map compliance grades to the 4.0 grade point. 
grades_dictionary = {
	4 	: 'A',
	3  : 'B',
	2	: 'C',
	1 	: 'D',
	0  : 'F'
	}

## Create a shortlist of nearby filings for each GEO satellite.
# Check whether today's directory exists:
MYDIR = ('../Data/Daily Analysis/' + assessmentdate + '/Nearby Shortlists')
CHECK_FOLDER = os.path.isdir(MYDIR)
# If it doesn't exist, then create it.
if not CHECK_FOLDER:
    os.makedirs(MYDIR)
    print("created folder : ", MYDIR)
# If it does exist, then empty it, so that the new files don't contain any duplicate entries.
else:
	for f in os.listdir(MYDIR):
	    os.remove(os.path.join(MYDIR, f))
# Make a file to house the letter grade results
with open('../Data/Daily Analysis/' + assessmentdate + '/compliance_' + assessmentdate + '.csv', 'w') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(['NORAD ID', 'Longitude', 'Compliance Assessment', 'Note'])
# Import the list of GEO satellites and their longitudinal positions
satcats = []
longitudes = []
with open('../Data/Daily Analysis/' + assessmentdate + '/longitudes_' + assessmentdate + '.csv') as f:
	reader = csv.reader(f, delimiter=",")
	for row in reader:
		satcats.append(row[0])
		longitudes.append(row[1])
satcats = satcats[1:]
longitudes = longitudes[1:]
# For each satellite, find all ITU filings within 1.0 degrees longitude
for i in np.arange(len(satcats)):
	satcat = satcats[i]
	print('Evaluating compliance for Satellite #', satcat, '...')
	longitude = float(longitudes[i])
	for j, k in zip(locallaunchdatabase_norad_list, locallaunchdatabase_country_list):
		if j == satcat:
			catalog_country = k
	df_nearbyshortlist = pd.DataFrame(0, columns = ['Network', 'ITU Administration', 'Longitude', 'Network Type', 'Filing Maturity', 'Brought into Use', 'Due Diligence Match', 'Suspended', 'Link', 'Longitudinal Distance', 'ITUAdm'], index = np.arange(1000))
	licensecount = 0
	for j in np.arange(len(df_licenses)):
		longitudinal_distance = abs(df_licenses.at[j,'Longitude']-longitude)
		if longitudinal_distance > 180:
			longitudinal_distance = 360 - longitudinal_distance
		if longitudinal_distance <= 1.0:
			df_nearbyshortlist.at[licensecount, 'Network'] = df_licenses.at[j,'Network Name']
			df_nearbyshortlist.at[licensecount, 'ITU Administration'] = countries_dictionary[df_licenses.at[j,'ITU Administration'].strip()]
			ITUAdm = df_licenses.at[j,'ITU Administration'].strip()
			df_nearbyshortlist.at[licensecount, 'ITUAdm'] = ITUAdm
			if df_licenses.at[j,'Longitude'] < 0:
				longitude_formatted = str(-1*df_licenses.at[j,'Longitude']) + u'\N{DEGREE SIGN}' + 'W'
			else:
				longitude_formatted = str(df_licenses.at[j,'Longitude']) + u'\N{DEGREE SIGN}' + 'E'
			df_nearbyshortlist.at[licensecount, 'Longitude'] = longitude_formatted
			df_nearbyshortlist.at[licensecount, 'Network Type'] = df_licenses.at[j,'Planned or Non-Planned']
			df_nearbyshortlist.at[licensecount, 'Filing Type'] = filings_dictionary[df_licenses.at[j,'Highest Maturity']]
			df_nearbyshortlist.at[licensecount, 'Suspended'] = 'n/a'
			if df_licenses.at[j,'Suspension Type'] == 'T':
				df_nearbyshortlist.at[licensecount, 'Suspended'] = 'Full'
			if df_licenses.at[j,'Suspension Type'] == 'P':
				df_nearbyshortlist.at[licensecount, 'Suspended'] = 'Partial'
			# Check if the suspended license has been resumed
			if df_nearbyshortlist.at[licensecount, 'Suspended'] != 'n/a':
				if (df_licenses.at[j, 'Resumption Date'] != 'n/a' and type(df_licenses.at[j, 'Resumption Date']) != float):
					if datetime.today() > datetime.strptime(str(df_licenses.at[j, 'Resumption Date']), '%Y-%m-%d'):
						df_nearbyshortlist.at[licensecount, 'Suspended'] = 'Resumed'
			df_nearbyshortlist.at[licensecount, 'Link'] = df_licenses.at[j,'Link']
			df_nearbyshortlist.at[licensecount, 'Longitudinal Distance'] = longitudinal_distance
			if (df_licenses.at[j,'Highest Maturity'] == 'U' or df_licenses.at[j,'Highest Maturity'] == 'N'):
				if df_licenses.at[j,'Brought-into-Use Date'] == 'n/a':
					df_nearbyshortlist.at[licensecount, 'Brought into Use'] = 'No'
				else:
					df_nearbyshortlist.at[licensecount, 'Brought into Use'] = 'Yes'
			else:
				df_nearbyshortlist.at[licensecount, 'Brought into Use'] = 'No'
			licensecount += 1
	# Drop blank rows in the dataframe
	df_nearbyshortlist = df_nearbyshortlist.loc[~(df_nearbyshortlist==0).all(axis=1)]
	# Sort the frame by longitudinal distance
	df_nearbyshortlist = df_nearbyshortlist.sort_values('Longitudinal Distance', ascending = True)
	df_nearbyshortlist = df_nearbyshortlist.reset_index(drop=True)
	# Find the most recent due-diligence match data available
	duediligence_directories_names = [x[0].rsplit('/', 1) for x in os.walk('../Data/Due Diligence Matches/')][-1][1:]
	duediligence_directories_datetimes = [datetime.strptime(i, '%Y%m%d') for i in duediligence_directories_names]
	duediligence_directory = duediligence_directories_names[duediligence_directories_datetimes.index(max(duediligence_directories_datetimes))]
	df_duediligence = pd.read_csv('../Data/Due Diligence Matches/' + duediligence_directory + '/' + satcat + '.csv')
	for j in np.arange(len(df_nearbyshortlist)):
		df_nearbyshortlist.at[j, 'Due Diligence Match'] = 'n/a'
		license = df_nearbyshortlist.at[j, 'Network']
		if df_nearbyshortlist.at[j, 'Network Type'] == 'Due Diligence (U)':
				df_nearbyshortlist.at[j, 'Due Diligence Match'] = 'None'
		for k in np.arange(len(df_duediligence)):
			if (df_duediligence.at[k, 'Satellite Name'] == license and df_duediligence.at[k, 'Launch Country Match'] == 1):
				launchdatematch = 0
				if df_duediligence.at[k, 'Launch Offset (days)'] <= 365:
					launchdatematch = 1
				matchsum = launchdatematch + df_duediligence.at[k, 'Launch Spaceport Match'] + df_duediligence.at[k, 'Launch Vehicle Match'] + df_duediligence.at[k, 'Satellite Manufacturer Match'] 
				if matchsum  >= 1:
					df_nearbyshortlist.at[j, 'Due Diligence Match'] = 'Partial'
				if matchsum == 4:
					df_nearbyshortlist.at[j, 'Due Diligence Match'] = 'Full'
	# Now use the short list to make a letter grade
	license_names = []
	license_scores = []
	for j in np.arange(len(df_nearbyshortlist)):
		score = 0
		license_names.append(df_nearbyshortlist.at[j, 'Network'])
		if df_nearbyshortlist.at[j, 'Longitudinal Distance'] <= 0.1:
			ITUAdm = df_nearbyshortlist.at[j, 'ITUAdm']
			if ITUAdm in SpaceTrackcountries_dict[catalog_country]:
				score += 1
				if (df_nearbyshortlist.at[j, 'Filing Type'] == 'Notification of Space Station (N)' or df_nearbyshortlist.at[j, 'Filing Type'] == 'Due Diligence (U)'):
					score += 1
				if df_nearbyshortlist.at[j, 'Brought into Use'] == 'Yes':
					score += 1
					if (df_nearbyshortlist.at[j, 'Due Diligence Match'] != 'n/a' or df_nearbyshortlist.at[j, 'Due Diligence Match'] != 'None'):
						if df_nearbyshortlist.at[j, 'Due Diligence Match'] == 'Partial':
							score += 1
						if df_nearbyshortlist.at[j, 'Due Diligence Match'] == 'Full':
							score += 2
				if df_nearbyshortlist.at[j, 'Suspended'] == 'Totally':
					score = 0
		license_scores.append(score)
	bestscore = max(license_scores)
	license_name = 'n/a'
	license_maturity = 'n/a'
	license_broughtintouse = 'n/a'
	license_match = 'n/a'
	license_suspended = 'n/a'
	if bestscore != 0:
		bestlicense_index = license_scores.index(max(license_scores))
		license_name = license_names[bestlicense_index]
		for j in np.arange(len(df_nearbyshortlist)):
			if df_nearbyshortlist.at[j, 'Network'] == license_name:
					license_maturity = df_nearbyshortlist.at[j, 'Filing Type']
					license_broughtintouse = df_nearbyshortlist.at[j, 'Brought into Use']
					license_match = df_nearbyshortlist.at[j, 'Due Diligence Match']
					license_suspended = df_nearbyshortlist.at[j, 'Suspended']
	# Evaluate compliance
	note = 'n/a'
	if license_broughtintouse == 'Yes':
		compliance = 'Yes'
		if (license_suspended == 'n/a' or license_suspended == 'No'):
			note = 'There exists a space network within 0.1 degrees that has been brought into use by a corresponding ITU administration.'
		else:
			if license_suspended == 'Partial':
				note = 'There exists a space network within 0.1 degrees that has been brought into use by a corresponding ITU administration. The identified network is currently partially suspended.'
			else:
				if license_suspended == 'Total':
					compliance = 'No'
					note = 'There exists a space network within 0.1 degrees that was brought into use by a corresponding ITU administration, but it has since been totally suspended.'
				else:
					note = 'There exists a space network within 0.1 degrees that has been brought into use by a corresponding ITU administration. The identified network was previous suspended, but has since resumed operation.'
	else:
		compliance = 'No'
		if (license_maturity == 'Notification of Space Station (N)' or license_maturity == 'Due Diligence (U)'):
			note = 'There exists a space network within 0.1 degrees filed by a corresponding ITU administration that is eligible for bringing into use, but the corresponding ITU administration has not yet done so.'
		if license_name == 'n/a':
			note = 'There are no space networks within 0.1 degrees for which any filings have been submitted by a corresponding ITU administration.'
		else:
			note = 'There exists a space network within 0.1 degrees held by a corresponding ITU administration, but its filings are in their early stages: this satellite is not protected from harmful interference.'
	# Drop the longitudinal distance column
	df_nearbyshortlist = df_nearbyshortlist.drop(['Longitudinal Distance', 'ITUAdm'], axis=1)
	# Save the short list to a CSV 
	df_nearbyshortlist.to_csv('../Data/Nearby Shortlists/' + assessmentdate + '/' + satcat + '_' + assessmentdate + '.csv', index = None)
	with open('../Data/Compliance Grades/grades_' + assessmentdate + '.csv', 'a') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow([satcat, round(longitude, 2), compliance, note])



				

			

