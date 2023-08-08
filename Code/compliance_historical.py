"""
Name: 			compliance_historical.py
Description: 	
				Check whether GEO satellites' historical positions match any filed ITU space networks.
Author:        	Thomas G. Roberts (thomasgr@mit.edu / thomasgroberts.com)
Date: 			August 3, 2023

Inputs:			
				../Data/Historical Analysis/[YYYYMMDD]/longitudes_[YYYYMMDD].csv
				../Data/Historical Analysis/[YYYYMMDD]/networks_historical_[YYYYMMDD].csv
Outputs:	
				../Data/Historical Analysis/[YYYYMMDD]/Historical Compliance Assessments/compliance_[satcat]_[YYYYMMDD].csv
				../Data/Historical Analysis/[YYYYMMDD]/Historical Nearby Shortlists/[YYYYMMDD]/nearbyshortlist_[satcat]_[YYYYMMDD].csv
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

# Since this script may take more 24 hours to run, consider hardcoding the assessment date
assessmentdate = '20230808'

# Write a quick function for cleaning directories
def remove_files_except(filename, directory):
	entries = os.listdir(directory)
	for entry in entries:
		entry_path = os.path.join(directory, entry)
		if entry == filename:
			continue
		if os.path.isfile(entry_path):
			os.remove(entry_path)
		elif os.path.isdir(entry_path):
			remove_files_except(filename, entry_path)
			os.rmdir(entry_path)

# Check for where the assessment date's sub-directory in the Historical Analysis directory has already been made
MYDIR = ('../Data/Historical Analysis/' + assessmentdate)
CHECK_FOLDER = os.path.isdir(MYDIR)
# If it doesn't exist, then create it 
if not CHECK_FOLDER:
	os.makedirs(MYDIR)
# If it does exist, clear everything (to avoid duplicates) except the historical longitudes file
else:
	remove_files_except('longitudes_' + assessmentdate + '.csv', MYDIR)
# Add another sub-directory to house the historical nearby shortlists
MYDIR = ('../Data/Historical Analysis/' + assessmentdate + '/Historical Nearby Shortlists')
CHECK_FOLDER = os.path.isdir(MYDIR)
# If it doesn't exist, then create it
if not CHECK_FOLDER:
	os.makedirs(MYDIR)
# If it does exist, clear it (to avoid duplicates) and run the scrape scripts.
else:
	for f in os.listdir(MYDIR):
		os.remove(os.path.join(MYDIR, f))
# Add another sub-directory to house the compliance assessment results
MYDIR = ('../Data/Historical Analysis/' + assessmentdate + '/Historical Compliance Assessments')
CHECK_FOLDER = os.path.isdir(MYDIR)
# If it doesn't exist, then create it and run the scrape scripts.
if not CHECK_FOLDER:
	os.makedirs(MYDIR)
# If it does exist, clear it (to avoid duplicates) and run the scrape scripts.
else:
	for f in os.listdir(MYDIR):
		os.remove(os.path.join(MYDIR, f))

## Import relevant data
# Import the most recent list of networks created using snl.py
historicalanalysis_directories_names = next(os.walk('../Data/SNL Downloads/'))[1]
try:
	historicalanalysis_directories_names.remove('Archives')
except ValueError:
	pass
historicalanalysis_directories_datetimes = [datetime.strptime(i, '%Y%m%d') for i in historicalanalysis_directories_names]
historicalanalysis_directory = historicalanalysis_directories_names[historicalanalysis_directories_datetimes.index(max(historicalanalysis_directories_datetimes))]
df_licenses = pd.read_csv('../Data/SNL Downloads/' + historicalanalysis_directory + '/networks_' + historicalanalysis_directory + '.csv')
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

# Write a maturity rank order of the various filings types 
filings_rankorder = ['Advance Public Information (A)', 'Planned (P/Plan/List)', 'Planned (P)', 'Coordination Request (C)', 'Notification of Space Station (N)', 'Due Diligence (U)']
# Import local launch history database as lists
locallaunchdatabase_cospar_list = []
locallaunchdatabase_norad_list = []
locallaunchdatabase_satname_list = []
locallaunchdatabase_country_list = []
locallaunchdatabase_launchdate_list = []
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
	4  : 'A',
	3  : 'B',
	2  : 'C',
	1  : 'D',
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

# Check to see if a longitudes file has been put in the right sub-direcotry
file_path = os.path.join('../Data/Historical Analysis/' + assessmentdate, 'longitudes_' + assessmentdate + '.csv')
if os.path.exists(file_path):
	pass
else:
	print('A correctly named longitude file hasn\'t been added to the assessment dates\'s sub-directory. Please add it and run this script again.')
	sys.exit()

# Make a pandas dataframe to house the assessment results
df_longitudes = pd.read_csv('../Data/Historical Analysis/' + assessmentdate + '/longitudes_' + assessmentdate + '.csv')
df_results_batched = df_longitudes.copy()

# Import the lists of GEO satellites and the historical dates for assessment
satcats = list(df_longitudes.columns.values)[1:]
dates = []
for i in np.arange(len(df_longitudes)):
	dates.append(df_longitudes.at[i, 'Date'])

compliance_assessments = []
notes = []
# For each satellite, at each of it's longitudinal positions 
for i in np.arange(len(satcats)):
	satcat = str(satcats[i])
	print('Evaluating historical compliance for Satellite #'+str(satcat)+' ...')
	for m in np.arange(len(df_longitudes)):
		eval_date = datetime.strptime(dates[m], '%Y-%m-%d')
		# eval_date = datetime.strptime(dates[m], '%m/%d/%y')
		# Create a subdirectory to house the nearby shortlists for this date, if it doesn't exist already
		MYDIR = ('../Data/Historical Analysis/' + assessmentdate + '/Historical Nearby Shortlists/' + eval_date.strftime('%Y%m%d'))
		CHECK_FOLDER = os.path.isdir(MYDIR)
		# If it doesn't exist, then create it and run the scrape scripts.
		if not CHECK_FOLDER:
			os.makedirs(MYDIR)
		df_results_batched.at[m, satcat] = 'TBD'
		longitude = df_longitudes.at[m, satcat]
		if np.isnan(longitude):
			df_results_batched.at[m, satcat] = 'n/a. No longitudinal position available for this date.'
		else:
			longitude = float(longitude)
			for j, k in zip(locallaunchdatabase_norad_list, locallaunchdatabase_country_list):
				if j == satcat:
					catalog_country = k
			df_nearbyshortlist = pd.DataFrame(0, columns = ['Network', 'ITU Administration', 'Longitude', 'Network Type', 'Filing Maturity', 'Brought into Use', 'Due Diligence Match', 'Suspended', 'Longitudinal Distance', 'Eligible', 'Link', 'Grandfather', 'ITUAdm'], index = np.arange(1000))
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
					# Check if the network has grandfathered station-keeping requirements
					df_nearbyshortlist.at[licensecount, 'Grandfather'] = 'No'
					if (pd.isna(df_licenses.at[j,'Brought-into-Use Date']) == False and datetime.strptime(df_licenses.at[j,'Brought-into-Use Date'], '%Y-%m-%d') < datetime(1982, 1, 1)):
						df_nearbyshortlist.at[licensecount, 'Grandfather'] = 'Yes'
					if (pd.isna(df_licenses.at[j,'Brought-into-Use Date']) == False and datetime.strptime(df_licenses.at[j,'Brought-into-Use Date'], '%Y-%m-%d') < datetime(1987, 1, 1) and pd.isna(df_licenses.at[j,'Early-Stage Filing Date']) == False and datetime.strptime(df_licenses.at[j,'Early-Stage Filing Date'], '%Y-%m-%d') < datetime(1982, 1, 1)):
						df_nearbyshortlist.at[licensecount, 'Grandfather'] = 'Yes'					
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
			duediligence_directories_names = [x[0].rsplit('/', 1) for x in os.walk('../Data/Reference Files/Due Diligence Matches/')][-1][1:]
			duediligence_directories_datetimes = [datetime.strptime(i, '%Y%m%d') for i in duediligence_directories_names]
			duediligence_directory = duediligence_directories_names[duediligence_directories_datetimes.index(max(duediligence_directories_datetimes))]
			df_duediligence = pd.read_csv('../Data/Reference Files/Due Diligence Matches/' + duediligence_directory + '/' + satcat + '.csv')
			for j in np.arange(len(df_nearbyshortlist)):
				df_nearbyshortlist.at[j, 'Due Diligence Match'] = 'n/a'
				license = df_nearbyshortlist.at[j, 'Network']
				if df_nearbyshortlist.at[j, 'Filing Maturity'] == 'Late-Stage':
					df_nearbyshortlist.at[j, 'Due Diligence Match'] = 'No'
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
			# Now use the short list to assess compliance
			license_names = []
			license_scores = []
			for j in np.arange(len(df_nearbyshortlist)):
				score = 0
				license_names.append(df_nearbyshortlist.at[j, 'Network'])
				if ((df_nearbyshortlist.at[j, 'Longitudinal Distance'] <= 0.1 and df_nearbyshortlist.at[j, 'Network Type'] == 'Planned') or (df_nearbyshortlist.at[j, 'Longitudinal Distance'] <= 0.5 and df_nearbyshortlist.at[j, 'Network Type'] == 'Non-Planned') or df_nearbyshortlist.at[j, 'Grandfather'] == 'Yes'):
					ITUAdm = df_nearbyshortlist.at[j, 'ITUAdm']
					if ITUAdm in SpaceTrackcountries_dict[catalog_country]:
						score += 1
						score += df_nearbyshortlist.at[j, 'Longitudinal Distance']
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
				if score != 0:
					df_nearbyshortlist.at[j, 'Eligible'] = 'Yes \U0001F7E2'
				else:
					df_nearbyshortlist.at[j, 'Eligible'] = 'No \U0001F534'
			bestscore = max(license_scores)
			license_type = 'n/a'
			license_name = 'n/a'
			license_maturity = 'n/a'
			license_broughtintouse = 'n/a'
			license_match = 'n/a'
			license_suspended = 'n/a'
			license_grandfather = 'n/a'
			if bestscore != 0:
				bestlicense_index = license_scores.index(max(license_scores))
				license_name = license_names[bestlicense_index]
				for j in np.arange(len(df_nearbyshortlist)):
					if df_nearbyshortlist.at[j, 'Network'] == license_name:
							license_type = df_nearbyshortlist.at[j, 'Network Type']
							license_maturity = df_nearbyshortlist.at[j, 'Filing Maturity']
							license_broughtintouse = df_nearbyshortlist.at[j, 'Brought into Use']
							license_match = df_nearbyshortlist.at[j, 'Due Diligence Match']
							license_suspended = df_nearbyshortlist.at[j, 'Suspended']
							license_grandfather = df_nearbyshortlist.at[j, 'Grandfather']
			# Evaluate compliance
			note = 'n/a'
			note_brief = 'n/a'
			if license_broughtintouse == 'Yes':
				compliance = 'Yes'
				if (license_suspended == 'n/a' or license_suspended == 'No'):
					if license_grandfather == 'Yes':
						note = 'There exists a space network with a nominal orbital position within 1.0 degree that was brought into use before January 1, 1987, with the advance publication information for the network having been published before January 1, 1982, complying with ITU Radio Regulations Article 22, Section III (22.15 to 22.17).'
					else:
						if license_type == 'Planned':
							note = 'There exists a planned space network with a nominal orbital position within 0.1 degrees that was brought into use before the date of assessment, complying with ITU Radio Regulations Article 22, Section III (22.6 to 22.8).'
						if license_type == 'Non-Planned':
							note = 'There exists a non-planned space network with a nominal orbital position within 0.5 degrees that was brought into before the date of assessment, complying with ITU Radio Regulations Article 22, Section III (22.11 to 22.13).'
				else:
					if license_suspended == 'Partial':
						if license_type == 'Planned':
							note = 'There exists a planned space network with a nominal orbital position within 0.1 degrees that was brought into use before the date of assessment, complying with ITU Radio Regulations Article 22, Section III (22.6 to 22.8). As of the date of assessment, the identified network is partially suspended.'
						if license_type == 'Non-Planned':
							note = 'There exists a non-planned space network with a nominal orbital position within 0.5 degrees that was brought into use before the date of assessment, complying with ITU Radio Regulations Article 22, Section III (22.11 to 22.13). As of the date of assessment, the identified network is partially suspended.'
					else:
						if license_suspended == 'Total':
							compliance = 'No'
							if license_type == 'Planned':
								note = 'There exists a planned space network with a nominal orbital position within 0.1 degrees that was brought into use before the date of assessment, but it has since been totally suspended.'
							if license_type == 'Non-Planned':
								note = 'There exists a non-planned space network with a nominal orbital position within 0.5 degrees that was brought into use before the date of assessment, but it has since been totally suspended.'
						else:
							if license_type == 'Planned':
								note = 'There exists a planned space network with a nominal orbital position within 0.1 degrees that was brought into use before the date of assessment, complying with ITU Radio Regulations Article 22, Section III (22.6 to 22.8). The identified network was previous suspended, but has since resumed operation.'
							if license_type == 'Non-Planned':
								note = 'There exists a non-planned space network with a nominal orbital position within 0.5 degrees that was brought into use before the date of assessment, complying with ITU Radio Regulations Article 22, Section III (22.11 to 22.13). The identified network was previous suspended, but has since resumed operation.'
			else:
				compliance = 'No'
				if license_name == 'n/a':
					note = 'There are no space networks within station-keeping requirements for which any filings have been submitted by a corresponding ITU administration.'
				else:
					note = 'There exists a space network within station-keeping requirements held by a corresponding ITU administration, but its filings are in their early stages: this satellite is not protected from harmful interference.'
				if license_maturity == 'Late-Stage':
					note = 'There exists a space network within station-keeping requirements held by a corresponding ITU administration that is eligible for bringing into use, but the corresponding ITU administration has not yet done so.'
			df_results_batched.at[m, satcat] = compliance + '. ' + note
			printProgressBar(m + 1, len(df_longitudes), prefix = str("{:03d}".format(i+1))+' of '+str(len(satcats)), suffix = 'Complete', length = 50)
			# Drop the ITUadm and grandfather columns from the nearby shortlist
			df_nearbyshortlist = df_nearbyshortlist.drop(['Grandfather', 'ITUAdm'], axis=1)
			# # Drop the Due Diligence Match column from the nearby shortlist
			# df_nearbyshortlist = df_nearbyshortlist.drop('Due Diligence Match', axis=1)
			# Round the 'Longitudinal Distance' column to two decimal places
			df_nearbyshortlist['Longitudinal Distance'] = df_nearbyshortlist['Longitudinal Distance'].round(2)
			# Add a degree symbol to the values in the 'Longitudinal Distance' column
			df_nearbyshortlist['Longitudinal Distance'] = df_nearbyshortlist['Longitudinal Distance'].apply(lambda x: f'{x:.2f}°')
			# Save the shortlist to a CSV 
			df_nearbyshortlist.to_csv('../Data/Historical Analysis/' + assessmentdate + '/Historical Nearby Shortlists/' + eval_date.strftime('%Y%m%d') + '/nearbyshortlist_' + satcat + '_' + eval_date.strftime('%Y%m%d') + '.csv', index = None)
# # Now let's do a check to see whether any satellites not in compliance were sufficiently far away from compliant satellites on the date of assessment
# for i in np.arange(len(satcats)):
# 	satcat = str(satcats[i])
# 	for m in np.arange(len(df_longitudes)):
# 		longitude = df_longitudes.at[m, satcat]
# 		neighbor_compliance = False
# 		# For satellites not in compliance, check to see if any other satellites within 0.5 degrees are in compliance
# 		if df_results_batched.at[m, satcat][0] == 'N':
# 			for j in np.arange(len(satcats)):
# 				satcat_scan = str(satcats[j])
# 				if satcat_scan != satcat:
# 					longitude_scan = df_longitudes.at[m, satcat_scan]
# 					if abs(longitude - longitude_scan) <= 0.5:
# 						if df_results_batched.at[m, satcat_scan][0] == 'Y':
# 							neighbor_compliance = True
# 			if neighbor_compliance == False:
# 				df_results_batched.at[m, satcat] = 'Maybe. Although there are no space networks within station-keeping requirements for which any filings have been submitted by a corresponding ITU administration, there are also no other compliant satellites within 0.5 degrees, meaning this satellite could be in compliance with ITU Radio Regulations Article 22, Section III: 22.10 or 22.14.'

# Save the results
for satcat in satcats:
	# Make a CSV to house results
	with open('../Data/Historical Analysis/' + assessmentdate + '/Historical Compliance Assessments/compliance_' + str(satcat) + '_' + assessmentdate + '.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['Date', 'Longitude', 'Compliance Assessment', 'Note'])
	compliance_list = [sentence.split('.')[0] for sentence in df_results_batched[satcat]]
	note_list = [sentence.split('.', 1)[-1].strip() for sentence in df_results_batched[satcat]]
	for i in np.arange(len(dates)):
		with open('../Data/Historical Analysis/' + assessmentdate + '/Historical Compliance Assessments/compliance_' + str(satcat) + '_' + assessmentdate + '.csv', 'a') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow([dates[i], df_longitudes[satcat].tolist()[i], compliance_list[i], note_list[i]])



				

			

