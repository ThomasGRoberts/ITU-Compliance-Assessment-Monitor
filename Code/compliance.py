"""
Name: 			compliance.py
Description: 	Check whether GEO satellites' positions match any filed ITU space network licenses.
Author:         Thomas G. Roberts (thomasgr@mit.edu / thomasgroberts.com)
Date: 			June 8, 2023

Inputs:			../Data/Longitude Inputs/longitudes_[YYYYMMDD].csv
				../Data/SNL Archives/[YYYYMMDD]/licenses_[YYYYMMDD].csv	
Outputs:		../Data/Nearby Shortlists/[YYYYMMDD]/[satcat]_[YYYYMMDD.csv]					../Data/Compliance Grades/grades_[YYYYMMDD].csv
"""

## This script issues a compliance rating for GEO satellites given their NORAD ID and longitudinal position. A shortlist of nearby filings is also produced for each GEO satellite.

import numpy as np
import csv
from datetime import datetime
import pandas as pd
import os

## Import relevant data
# Import the list of licenses created using snl.py
df_licenses = pd.read_csv('../Data/SNL Archives/' + datetime.today().strftime('%Y%m%d') + '/licenses_' + datetime.today().strftime('%Y%m%d') + '.csv')
# Import a dictionary to convert ITU country symbols to designations
reader = csv.reader(open('../Data/Reference Files/ITUcountries.csv', 'r'))
countries_dictionary = {}
for row in reader:
   k, v = row
   countries_dictionary[k] = v
# Write a dictionary for the full names of filings type
filings_dictionary = {
	'A' 			: 'Advance Public Information (A)',
	'C'   			: 'Coordination Request (C)',
	'N'				: 'Notification of Space Station (N)',
	'U'				: 'Due Diligence (U)',
	'P'  			: 'Planned (P)',
	'P/Plan/List' 	: 'Planned (P/Plan/List)'
	}
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

## Create a shortlist of nearby filings for each GEO satellite and save it in ../Data/Nearby Shortlists/[YYYYMMDD]. Issue a compliance grade for each sastellite and save it in ../Data/Compliance Grades/grades_YYYYMMDD.csv.
# Check whether today's directory exists:
MYDIR = ('../Data/Nearby Shortlists/' + datetime.today().strftime('%Y%m%d'))
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
with open('../Data/Compliance Grades/grades_' + datetime.today().strftime('%Y%m%d') + '.csv', 'w') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(['NORAD ID', 'Longitude', 'Compliance Grade'])
# Import the list of GEO satellites and their longitudinal positions
satcats = []
longitudes = []
with open('../Data/Longitude Inputs/longitudes_' + datetime.today().strftime('%Y%m%d') + '.csv') as f:
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
	df_nearbyshortlist = pd.DataFrame(0, columns = ['License', 'ITU Administration', 'Longitude', 'License Type', 'Filing Type', 'Brought into Use', 'Matched Characteristics', 'Link', 'Longitudinal Distance', 'ITUAdm'], index = np.arange(1000))
	licensecount = 0
	for j in np.arange(len(df_licenses)):
		longitudinal_distance = abs(df_licenses.at[j,'Longitude']-longitude)
		if longitudinal_distance > 180:
			longitudinal_distance = 360 - longitudinal_distance
		if longitudinal_distance <= 1.0:
			df_nearbyshortlist.at[licensecount, 'License'] = df_licenses.at[j,'License Name']
			df_nearbyshortlist.at[licensecount, 'ITU Administration'] = countries_dictionary[df_licenses.at[j,'ITU Administration'].strip()]
			ITUAdm = df_licenses.at[j,'ITU Administration'].strip()
			df_nearbyshortlist.at[licensecount, 'ITUAdm'] = ITUAdm
			if df_licenses.at[j,'Longitude'] < 0:
				longitude_formatted = str(-1*df_licenses.at[j,'Longitude']) + u'\N{DEGREE SIGN}' + 'W'
			else:
				longitude_formatted = str(df_licenses.at[j,'Longitude']) + u'\N{DEGREE SIGN}' + 'E'
			df_nearbyshortlist.at[licensecount, 'Longitude'] = longitude_formatted
			df_nearbyshortlist.at[licensecount, 'License Type'] = df_licenses.at[j,'Planned or Non-Planned']
			df_nearbyshortlist.at[licensecount, 'Filing Type'] = filings_dictionary[df_licenses.at[j,'Highest Maturity']]
			df_nearbyshortlist.at[licensecount, 'Link'] = df_licenses.at[j,'Link']
			df_nearbyshortlist.at[licensecount, 'Longitudinal Distance'] = longitudinal_distance
			if (df_licenses.at[j,'Highest Maturity'] == 'U' or df_licenses.at[j,'Highest Maturity'] == 'N'):
				if df_licenses.at[j,'Brought-into-Use Date'] == 'n/a':
					df_nearbyshortlist.at[licensecount, 'Brought into Use'] = 'No'
				else:
					df_nearbyshortlist.at[licensecount, 'Brought into Use'] = 'Yes'
			else:
				df_nearbyshortlist.at[licensecount, 'Brought into Use'] = 'n/a'
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
		if df_nearbyshortlist.at[j,'Filing Type'] == 'Due Diligence (U)':
			df_nearbyshortlist.at[j, 'Matched Characteristics'] = 'No'
		else:
			df_nearbyshortlist.at[j, 'Matched Characteristics'] = 'n/a'
		license = df_nearbyshortlist.at[j, 'License']
		for k in np.arange(len(df_duediligence)):
			if (df_duediligence.at[k, 'Satellite Name'] == license and df_duediligence.at[k, 'Launch Offset (days)'] <= 365 and df_duediligence.at[k, 'Launch Country Match'] == 1 and df_duediligence.at[k, 'Launch Spaceport Match'] + df_duediligence.at[k, 'Launch Vehicle Match'] + df_duediligence.at[k, 'Satellite Manufacturer Match'] >= 2):
				df_nearbyshortlist.at[j, 'Matched Characteristics'] = 'Yes'
	# Now use the short list to make a letter grade
	lettergrade = 0
	for j in np.arange(len(df_nearbyshortlist)):
		if df_nearbyshortlist.at[j, 'Longitudinal Distance'] <= 0.1:
			ITUAdm = df_nearbyshortlist.at[j, 'ITUAdm']
			if ITUAdm in SpaceTrackcountries_dict[catalog_country]:
				lettergrade = max(lettergrade, 1)
				if (df_nearbyshortlist.at[j, 'Filing Type'] == 'Notification of Space Station (N)' or df_nearbyshortlist.at[j, 'Filing Type'] == 'Due Diligence (U)'):
					lettergrade = max(lettergrade, 2)
					if df_nearbyshortlist.at[j, 'Brought into Use'] == 'Yes':
						lettergrade = max(lettergrade, 3)
						if df_nearbyshortlist.at[j, 'Matched Characteristics'] == 'Yes':
							lettergrade = max(lettergrade, 4)
	# Drop the longitudinal distance column
	df_nearbyshortlist = df_nearbyshortlist.drop(['Longitudinal Distance', 'ITUAdm'], axis=1)
	# Save the short list to a CSV 
	df_nearbyshortlist.to_csv('../Data/Nearby Shortlists/' + datetime.today().strftime('%Y%m%d') + '/' + satcat + '_' + datetime.today().strftime('%Y%m%d') + '.csv', index = None)
	with open('../Data/Compliance Grades/grades_' + datetime.today().strftime('%Y%m%d') + '.csv', 'a') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow([satcat, round(longitude, 2), grades_dictionary[lettergrade]])



				

			
