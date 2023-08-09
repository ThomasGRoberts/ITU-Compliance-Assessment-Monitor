"""
Name: 			compliance_historical.py
Description: 	Check whether GEO satellites' historical positions match any filed ITU space networks.
Author:        Thomas G. Roberts (thomasgr@mit.edu / thomasgroberts.com)
Date: 			June 29, 2023

Inputs:			../Data/Longitude Inputs/longitudes_historical.csv
					../Data/SNL Archives/[YYYYMMDD]/networks_historical_[YYYYMMDD].csv	
Outputs:			../Data/Compliance Grades/grades_historical_[YYYYMMDD].csv
"""

## This script issues a compliance rating for GEO satellites given their NORAD ID and longitudinal position. A shortlist of nearby filings is also produced for each GEO satellite.

import numpy as np
import csv
from datetime import datetime
import pandas as pd
import os

## Import relevant data
# Import the list of licenses created using snl_historical.py
df_licenses = pd.read_csv('../Data/Historical Analysis/networks_historical_20230702.csv')
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

## A quick function for making a progress bar in the console
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

# Make a pandas dataframe to house the assessment results
df_longitudes = pd.read_csv('../Data/Longitude Inputs/longitudes_historical_shorter.csv')
df_results = df_longitudes.copy()

# Import the lists of GEO satellites and the historical dates for assessment
satcats = list(df_longitudes.columns.values)[1:]
dates = []
for i in np.arange(len(df_longitudes)):
	dates.append(df_longitudes.at[i, 'Date'])

satcats = ['41838']
	
# For each satellite, at each of it's longitudinal positions 
for i in np.arange(len(satcats)):
	satcat = str(satcats[i])
	# printProgressBar(0, len(df_longitudes), prefix = str("{:03d}".format(i+1))+' of '+str(len(satcats)), suffix = 'Complete', length = 50)
	for m in np.arange(len(df_longitudes)):
		eval_date = datetime.strptime(dates[m], '%m/%d/%y')
		if (eval_date >= datetime.strptime('2018-01-01 00:00:00', "%Y-%m-%d %H:%M:%S") and eval_date <datetime.strptime('2019-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")):
			df_results.at[m, satcat] = 'TBD'
			longitude = df_longitudes.at[m, satcat]
			if np.isnan(longitude):
				df_results.at[m, satcat] = 'n/a'
			else:
				longitude = float(longitude)
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
						df_nearbyshortlist.at[licensecount, 'Filing Maturity'] = 'Early-Stage'
						if pd.isna(df_licenses.at[j,'Late-Stage Filing Date']) == False:
							if datetime.strptime(df_licenses.at[j,'Late-Stage Filing Date'], '%Y-%m-%d') <= eval_date:
								df_nearbyshortlist.at[licensecount, 'Filing Maturity'] = 'Late-Stage'
						if pd.isna(df_licenses.at[j,'Suspensions']):
							df_nearbyshortlist.at[licensecount, 'Suspended'] = 'No'
						else:
							df_nearbyshortlist.at[licensecount, 'Suspended'] = 'No'
							suspension_list = eval(df_licenses.at[j,'Suspensions'])
							for suspension in suspension_list[::-1]:
								suspension_type, suspension_start, suspension_end = suspension
								if suspension_end == 'n/a':
									if eval_date >= datetime.strptime(suspension_start, '%Y-%m-%d'):
										if suspension_type == 'T':
											df_nearbyshortlist.at[licensecount, 'Suspended'] = 'Total'
										if suspension_type == 'P':
											df_nearbyshortlist.at[licensecount, 'Suspended'] = 'Partial'
								else:
									if (eval_date >= datetime.strptime(suspension_start, '%Y-%m-%d') and eval_date < datetime.strptime(suspension_end, '%Y-%m-%d')):
										if suspension_type == 'T':
											df_nearbyshortlist.at[licensecount, 'Suspended'] = 'Total'
										if suspension_type == 'P':
											df_nearbyshortlist.at[licensecount, 'Suspended'] = 'Partial'
						df_nearbyshortlist.at[licensecount, 'Link'] = df_licenses.at[j,'Link']
						df_nearbyshortlist.at[licensecount, 'Longitudinal Distance'] = longitudinal_distance
						df_nearbyshortlist.at[licensecount, 'Brought into Use'] = 'No'
						if pd.isna(df_licenses.at[j,'Brought-into-Use Date']) == False:
							if eval_date >= datetime.strptime(df_licenses.at[j,'Brought-into-Use Date'], '%Y-%m-%d'):
								df_nearbyshortlist.at[licensecount, 'Brought into Use'] = 'Yes'
						licensecount += 1
				# Drop blank rows in the dataframe
				df_nearbyshortlist = df_nearbyshortlist[df_nearbyshortlist['ITU Administration'] != 0]
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
					if df_nearbyshortlist.at[j, 'Filing Maturity'] == 'Late-Stage':
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
							if (df_nearbyshortlist.at[j, 'Filing Maturity'] == 'Late-Stage'):
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
								license_maturity = df_nearbyshortlist.at[j, 'Filing Maturity']
								license_broughtintouse = df_nearbyshortlist.at[j, 'Brought into Use']
								license_match = df_nearbyshortlist.at[j, 'Due Diligence Match']
								license_suspended = df_nearbyshortlist.at[j, 'Suspended']
				print(df_nearbyshortlist)
				# Evaluate compliance
				note = 'n/a'
				note_brief = 'n/a'
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
					if license_name == 'n/a':
						note = 'There are no space networks within 0.1 degrees for which any filings have been submitted by a corresponding ITU administration.'
					else:
						note = 'There exists a space network within 0.1 degrees held by a corresponding ITU administration, but its filings are in their early stages: this satellite is not protected from harmful interference.'
					if license_maturity == 'Late-Stage':
						note = 'There exists a space network within 0.1 degrees filed by a corresponding ITU administration that is eligible for bringing into use, but the corresponding ITU administration has not yet done so.'
				# Drop the longitudinal distance column
				df_results.at[m, satcat] = compliance + '. ' + note
				# printProgressBar(m + 1, len(df_longitudes), prefix = str("{:03d}".format(i+1))+' of '+str(len(satcats)), suffix = 'Complete', length = 50)
# Save the file		
# df_results.to_csv('../Data/Compliance Grades/grades_historical_shorter_20230702.csv', index = None)
			print(eval_date, compliance + '. ' + note, longitude) 
			

