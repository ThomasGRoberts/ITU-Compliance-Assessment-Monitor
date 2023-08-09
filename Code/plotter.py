import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime, timedelta
import matplotlib.dates
import matplotlib.patches as patches
import pandas as pd
import seaborn as sbs

assessmentdate = '20230808'
# Get a list of satcats
df_longitudes = pd.read_csv('../Data/Historical Analysis/' + assessmentdate + '/longitudes_' + assessmentdate + '.csv')

# Import the lists of GEO satellites and the historical dates for assessment
satcats = list(df_longitudes.columns.values)[1:]
dates = []
for i in np.arange(len(df_longitudes)):
	dates.append(df_longitudes.at[i, 'Date'])

# satcats = ['27632', '40258', '41838']
satcats = ['41838']

# Create a dictionary for SpaceTrack country names (to convert them to ITU country codes)
SpaceTrackcountries_list = []
ITUcountrycodes_list = []
with open('../Data/Reference Files/SpaceTrackcountries.csv') as f:
	reader = csv.reader(f, delimiter=",")
	for row in reader:
		if row[0].strip() != "SpaceTrack Abbreviation":
			SpaceTrackcountries_list.append(row[0])
			row_list = [row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30]]
			while('' in row_list):
				row_list.remove('')
			if len(row_list) == 0:
				row_list = ['n/a']
			ITUcountrycodes_list.append(row_list)
SpaceTrackcountries_dict = {SpaceTrackcountries_list[i]: ITUcountrycodes_list[i] for i in range(len(SpaceTrackcountries_list))}

# Create the dataset for the mini heat map
color_dictionary = {
	'n/a'	:	'lightgray',
	'No'	:	'lightcoral',
	'Yes'	:	'lightgreen',
	'Maybe' :	'khaki'
}

for satcat in satcats:
	with open("../Data/Reference Files/satellitecatalog.csv") as f:
		reader = csv.reader(f, delimiter=",")
		for row in reader:
			if row[0].strip() != 'COSPAR':
				if row[1].strip() == satcat:
					spacetrackcountry = row[3]
					satname = row[2]
					launchdate = datetime.strptime(row[4], '%m/%d/%y')
	# Import the satellite's longitudinal values
	newdates = []
	datetimes = []
	longitudes = []
	firstdate = 0
	for m in np.arange(len(dates)):
		date = dates[m]
		# stringdate = str(datetime.strptime(dates[m], '%m/%d/%y'))[0:19]
		stringdate = str(datetime.strptime(dates[m], '%Y-%m-%d'))[0:19]
		datetimedate = datetime.strptime(stringdate, "%Y-%m-%d %H:%M:%S")
		firstdate = matplotlib.dates.date2num(launchdate)
		datetimes.append(datetimedate)
		newdates.append(matplotlib.dates.date2num(datetimedate)-firstdate)
		longitude = df_longitudes.at[m, satcat]
		if longitude == 'n/a':
			longitudes.append('n/a')
		else:
			if longitude < -180:
				longitude += 360
				longitudes.append(longitude)
			else:
				longitudes.append(longitude)

	newdates = sorted(newdates)
	# Add tickmarks at each calendar year in the study period 
	years = np.arange(2010, 2024)
	years_datenum = [matplotlib.dates.date2num(datetime.strptime(str(i) + '-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")) - firstdate for i in years]
	ticks = []
	for year_datenum in years_datenum:
		if (year_datenum > newdates[0] and year_datenum <= newdates[-1]):
			ticks.append(year_datenum)
	tickyears = []
	for tick in ticks:
		tickyears.append("\'"+str(matplotlib.dates.num2date(tick+firstdate).year)[2:4])

	# Now let's make a list of all the unique longitudinal positions for which the satellite's administration holds an active, non-planned space network
	nonplanned_longs_list = []
	nonplanned_names_list = []
	nonplanned_startdates_list = []
	nonplanned_enddates_list = []
	with open('../Data/SNL Downloads/' + assessmentdate + '/networks_' + assessmentdate + '.csv') as f:
		reader = csv.reader(f, delimiter=",")
		for row in reader:
			if row[0].strip() != "Network Name":
				if (row[2].strip() in SpaceTrackcountries_dict[spacetrackcountry] and row[4].strip() == 'Non-Planned'):
					nonplanned_long = float(row[1])
					nonplanned_name = row[0].strip()
					if row[6].strip() != 'n/a':
						broughtintouse_date = datetime.strptime(row[6].strip(), '%Y-%m-%d')
						# Check if the license has ever been suspended
						if row[9].strip() == 'n/a':
							nonplanned_names_list.append(nonplanned_name)
							nonplanned_startdates_list.append(broughtintouse_date)
							# nonplanned_enddates_list.append(datetime.strptime(dates[-1], '%m/%d/%y'))
							nonplanned_enddates_list.append(datetime.strptime(dates[-1], '%Y-%m-%d'))
							if nonplanned_long < -180:
								nonplanned_long += 360
								nonplanned_longs_list.append(nonplanned_long)
							else:
								nonplanned_longs_list.append(nonplanned_long)
						else:
							suspension_list = eval(row[9].strip())
							for suspension, k in zip(suspension_list[::-1], np.arange(len(suspension_list[::-1]))):
								suspension_type, suspension_start, suspension_end = suspension
								# Consider the periods before or after any suspensions
								if k == 0:
									nonplanned_names_list.append(nonplanned_name)
									nonplanned_startdates_list.append(broughtintouse_date)
									nonplanned_enddates_list.append(datetime.strptime(suspension_start, '%Y-%m-%d'))
									if nonplanned_long < -180:
										nonplanned_long += 360
										nonplanned_longs_list.append(nonplanned_long)
									else:
										nonplanned_longs_list.append(nonplanned_long) 
								if k == len(suspension_list) - 1:
									if suspension_end != 'n/a':
										nonplanned_names_list.append(nonplanned_name)
										nonplanned_startdates_list.append(datetime.strptime(suspension_end, '%Y-%m-%d'))
										# nonplanned_enddates_list.append(datetime.strptime(dates[-1], '%m/%d/%y'))
										nonplanned_enddates_list.append(datetime.strptime(dates[-1], '%Y-%m-%d'))
										if nonplanned_long < -180:
											nonplanned_long += 360
											nonplanned_longs_list.append(nonplanned_long)
										else:
											nonplanned_longs_list.append(nonplanned_long)
								# Consider the period between suspensions
								if (k != 0 and suspension_start > last_suspension_end and suspension_start != 'n/a'):
									nonplanned_names_list.append(nonplanned_name)
									nonplanned_startdates_list.append(datetime.strptime(last_suspension_end, '%Y-%m-%d'))
									nonplanned_enddates_list.append(datetime.strptime(suspension_start, '%Y-%m-%d'))
									if nonplanned_long < -180:
										nonplanned_long += 360
										nonplanned_longs_list.append(nonplanned_long)
									else:
										nonplanned_longs_list.append(nonplanned_long)
								last_suspension_end = suspension_end

	# Now let's make a list of all the unique longitudinal positions for which the satellite's administration holds an active, planned space network
	planned_longs_list = []
	planned_names_list = []
	planned_startdates_list = []
	planned_enddates_list = []
	with open('../Data/SNL Downloads/' + assessmentdate + '/networks_' + assessmentdate + '.csv') as f:
		reader = csv.reader(f, delimiter=",")
		for row in reader:
			if row[0].strip() != "Network Name":
				if (row[2].strip() in SpaceTrackcountries_dict[spacetrackcountry] and row[4].strip() == 'Planned'):
					planned_long = float(row[1])
					planned_name = row[0].strip()
					if row[6].strip() != 'n/a':
						broughtintouse_date = datetime.strptime(row[6].strip(), '%Y-%m-%d')
						# Check if the license has ever been suspended
						if row[9].strip() == 'n/a':
							planned_names_list.append(planned_name)
							planned_startdates_list.append(broughtintouse_date)
							# planned_enddates_list.append(datetime.strptime(dates[-1], '%m/%d/%y'))
							planned_enddates_list.append(datetime.strptime(dates[-1], '%Y-%m-%d'))
							if planned_long < -180:
								planned_long += 360
								planned_longs_list.append(planned_long)
							else:
								planned_longs_list.append(planned_long)
						else:
							suspension_list = eval(row[9].strip())
							for suspension, k in zip(suspension_list[::-1], np.arange(len(suspension_list[::-1]))):
								suspension_type, suspension_start, suspension_end = suspension
								# Consider the periods before or after any suspensions
								if k == 0:
									planned_names_list.append(planned_name)
									planned_startdates_list.append(broughtintouse_date)
									planned_enddates_list.append(datetime.strptime(suspension_start, '%Y-%m-%d'))
									if planned_long < -180:
										planned_long += 360
										planned_longs_list.append(planned_long)
									else:
										planned_longs_list.append(planned_long) 
								if k == len(suspension_list) - 1:
									if suspension_end != 'n/a':
										planned_names_list.append(planned_name)
										planned_startdates_list.append(datetime.strptime(suspension_end, '%Y-%m-%d'))
										# planned_enddates_list.append(datetime.strptime(dates[-1], '%m/%d/%y'))
										planned_enddates_list.append(datetime.strptime(dates[-1], '%Y-%m-%d'))
										if planned_long < -180:
											planned_long += 360
											planned_longs_list.append(planned_long)
										else:
											planned_longs_list.append(planned_long)
								# Consider the period between suspensions
								if (k != 0 and suspension_start > last_suspension_end and suspension_start != 'n/a'):
									planned_names_list.append(planned_name)
									planned_startdates_list.append(datetime.strptime(last_suspension_end, '%Y-%m-%d'))
									planned_enddates_list.append(datetime.strptime(suspension_start, '%Y-%m-%d'))
									if planned_long < -180:
										planned_long += 360
										planned_longs_list.append(planned_long)
									else:
										planned_longs_list.append(planned_long)
								last_suspension_end = suspension_end

	# Now let's make a list of all the unique longitudinal positions for which the satellite's administration holds a space network grandfathered in to the station-keeping rules
	grandfathered_longs_list = []
	grandfathered_names_list = []
	grandfathered_startdates_list = []
	grandfathered_enddates_list = []
	with open('../Data/SNL Downloads/' + assessmentdate + '/networks_' + assessmentdate + '.csv') as f:
		reader = csv.reader(f, delimiter=",")
		for row in reader:
			if row[0].strip() != "Network Name":
				if ((row[2].strip() in SpaceTrackcountries_dict[spacetrackcountry] and row[6].strip() != 'n/a' and datetime.strptime(row[6].strip(), '%Y-%m-%d') < datetime(1982, 1, 1)) or (row[2].strip() in SpaceTrackcountries_dict[spacetrackcountry] and row[6].strip() != 'n/a' and datetime.strptime(row[6].strip(), '%Y-%m-%d') < datetime(1987, 1, 1) and row[8].strip() != 'n/a' and datetime.strptime(row[8].strip(), '%Y-%m-%d') < datetime(1982, 1, 1))):
					grandfathered_long = float(row[1])
					grandfathered_name = row[0].strip()
					broughtintouse_date = datetime.strptime(row[6].strip(), '%Y-%m-%d')
					# Check if the license has ever been suspended
					if row[9].strip() == 'n/a':
						grandfathered_names_list.append(grandfathered_name)
						grandfathered_startdates_list.append(broughtintouse_date)
						# grandfathered_enddates_list.append(datetime.strptime(dates[-1], '%m/%d/%y'))
						grandfathered_enddates_list.append(datetime.strptime(dates[-1], '%Y-%m-%d'))
						if grandfathered_long < -180:
							grandfathered_long += 360
							grandfathered_longs_list.append(grandfathered_long)
						else:
							grandfathered_longs_list.append(grandfathered_long)
					else:
						suspension_list = eval(row[9].strip())
						for suspension, k in zip(suspension_list[::-1], np.arange(len(suspension_list[::-1]))):
							suspension_type, suspension_start, suspension_end = suspension
							# Consider the periods before or after any suspensions
							if k == 0:
								grandfathered_names_list.append(grandfathered_name)
								grandfathered_startdates_list.append(broughtintouse_date)
								tier3a_enddates_list.append(datetime.strptime(suspension_start, '%Y-%m-%d'))
								if grandfathered_long < -180:
									grandfathered_long += 360
									grandfathered_longs_list.append(grandfathered_long)
								else:
									grandfathered_longs_list.append(grandfathered_long) 
							if k == len(suspension_list) - 1:
								if suspension_end != 'n/a':
									grandfathered_names_list.append(grandfathered_name)
									grandfathered_startdates_list.append(datetime.strptime(suspension_end, '%Y-%m-%d'))
									grandfathered_enddates_list.append(datetime.strptime(dates[-1], '%m/%d/%y'))
									if grandfathered_long < -180:
										grandfathered_long += 360
										grandfathered_longs_list.append(grandfathered_long)
									else:
										grandfathered_longs_list.append(grandfathered_long)
							# Consider the period between suspensions
							if (k != 0 and suspension_start > last_suspension_end and suspension_start != 'n/a'):
								grandfathered_names_list.append(tier3_name)
								grandfathered_startdates_list.append(datetime.strptime(last_suspension_end, '%Y-%m-%d'))
								grandfathered_enddates_list.append(datetime.strptime(suspension_start, '%Y-%m-%d'))
								if grandfathered_long < -180:
									grandfathered_long += 360
									grandfathered_longs_list.append(grandfathered_long)
								else:
									grandfathered_longs_list.append(grandfathered_long)
							last_suspension_end = suspension_end

	# Read in compliance results
	hardstartdate = '2016-11-03'
	firstlongitudeindex = 0
	longitudecalculated = False
	plotdates = []
	plotlongs = []
	compliance_results = []
	rownumber = -1
	with open('../Data/Historical Analysis/' + assessmentdate + '/Historical Compliance Assessments/compliance_' + satcat + '_' + assessmentdate + '.csv') as f:
		reader = csv.reader(f, delimiter=",")
		for row in reader:
			if row[0] != 'Date':
				rownumber += 1
				if (row[2].strip() != 'n/a' and longitudecalculated == False):
					longitudecalculated = True
					firstlongitudeindex = rownumber
				if longitudecalculated:
					if datetime.strptime(row[0].strip(), '%Y-%m-%d') >= datetime.strptime(hardstartdate, '%Y-%m-%d'):
						plotdates.append(matplotlib.dates.date2num(datetime.strptime(row[0].strip(), '%Y-%m-%d'))-firstdate)
						plotlongs.append(float(row[1]))
						compliance_results.append(row[2].strip())
	# Count occurrences:
	result_names = ['n/a', 'Yes', 'Maybe', 'No']
	result_breakdown = [
		str(round(compliance_results.count('n/a')/len(compliance_results)*100,1))+'%',
		str(round(compliance_results.count('Yes')/len(compliance_results)*100,1))+'%',
		str(round(compliance_results.count('Maybe')/len(compliance_results)*100,1))+'%',
		str(round(compliance_results.count('No')/len(compliance_results)*100,1))+'%']

	nonplanned_bandwidth = 0.5
	planned_bandwidth = 0.1
	grandfathered_bandwidth = 1
	f, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [20, 1]}, figsize=(13, 6))
	ax1.set_xticks(ticks, labels=tickyears)
	ax1.set_xlim(left=plotdates[0], right=matplotlib.dates.date2num(datetime.strptime(str(2022) + '-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")) - firstdate)
	ax1.set_ylim(-180, 180)
	# ax1.grid(True)
	# Red background
	ax1.add_patch(patches.Rectangle(
		(0, -180), # Bottom left corner of rectangle
		matplotlib.dates.date2num(datetime.strptime(str(2022) + '-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")) - firstdate
		, # Width of rectangle
		360, # Height of rectanlge
		color = color_dictionary['No']))
	# Plot the Non-Planned regions
	for i in np.arange(len(nonplanned_longs_list)):
		ax1.add_patch(patches.Rectangle(
			(max(matplotlib.dates.date2num(nonplanned_startdates_list[i]) - firstdate, 0), nonplanned_longs_list[i]-nonplanned_bandwidth/2), # Bottom left corner of rectangle
			min(matplotlib.dates.date2num(nonplanned_enddates_list[i]) - matplotlib.dates.date2num(nonplanned_startdates_list[i]), matplotlib.dates.date2num(datetime.strptime(str(2022) + '-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")) - max(matplotlib.dates.date2num(nonplanned_startdates_list[i]), 0)), # Width of rectangle
			nonplanned_bandwidth, # Height of rectanlge
			color = color_dictionary['Yes']))
	# Plot the Planned regions
	for i in np.arange(len(planned_longs_list)):
		ax1.add_patch(patches.Rectangle(
		(max(matplotlib.dates.date2num(planned_startdates_list[i]) - firstdate, 0), planned_longs_list[i]-planned_bandwidth/2),
		min(matplotlib.dates.date2num(planned_enddates_list[i]) - matplotlib.dates.date2num(planned_startdates_list[i]), matplotlib.dates.date2num(datetime.strptime(str(2022) + '-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")) - max(matplotlib.dates.date2num(planned_startdates_list[i]), 0)),
		planned_bandwidth,
		color = color_dictionary['Yes']))
	# Plot the Grandfathered regions
	for i in np.arange(len(grandfathered_longs_list)):
		ax1.add_patch(patches.Rectangle(
		(max(matplotlib.dates.date2num(grandfathered_startdates_list[i]) - firstdate, 0), grandfathered_longs_list[i]-grandfathered_bandwidth/2),
		min(matplotlib.dates.date2num(grandfathered_enddates_list[i]) - matplotlib.dates.date2num(grandfathered_startdates_list[i]), matplotlib.dates.date2num(datetime.strptime(str(2022) + '-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")) - max(matplotlib.dates.date2num(grandfathered_startdates_list[i]), 0)),
		grandfathered_bandwidth,
		color = color_dictionary['Yes']))
	# Plot the satellites' path
	dates_sections = [[] for _ in range(1000)]
	longitudes_sections = [[] for _ in range(1000)]
	section = 0
	lastlongitude = plotlongs[0]
	for date, longitude, assessment in zip(plotdates, plotlongs, compliance_results):
		if abs(longitude - lastlongitude) > 300:
			section += 1
		if assessment == 'n/a':
			section += 1
		else:
			dates_sections[section].append(date)
			longitudes_sections[section].append(longitude)
			lastlongitude = longitude
	for date, longitude in zip(dates_sections, longitudes_sections):
		if longitude != []:
			ax1.plot(date, longitude, linewidth = 2, color = 'k')
	# ax1.plot(plotdates, plotlongs, linewidth = 2, color = 'k')
	# Make the mini-plot
	ax2.set_xticks([])
	ax2.set_yticks([])
	ax2.set_xlim(left=plotdates[0], right=matplotlib.dates.date2num(datetime.strptime(str(2022) + '-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")) - firstdate)
	ax2.set_ylim(bottom = 0, top = 1)
	# Plot heat squares
	for i in np.arange(len(compliance_results)):
		plotdate = plotdates[i]
		compliance_result = compliance_results[i]
		ax2.add_patch(patches.Rectangle(
		(plotdate, 0),
		0.08333333333212067,
		1,
		color = color_dictionary[compliance_result]))
	# Add a heat square legend
	patch0 = patches.Patch(color = color_dictionary['n/a'], label = "n/a" + '\n' + '(' + result_breakdown[0] + ')')
	patch1 = patches.Patch(color = color_dictionary['Yes'], label = "Yes" + '\n' + '(' + result_breakdown[1] + ')')
	patch2 = patches.Patch(color = color_dictionary['Maybe'], label = "Maybe" + '\n' + '(' + result_breakdown[2] + ')')
	patch3 = patches.Patch(color = color_dictionary['No'], label = "No" + '\n' + '(' + result_breakdown[3] + ')')

	all_handles = (patch0, patch1, patch2, patch3)

	ax2.legend(handles = all_handles, loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=False, shadow=False, ncol=6, frameon=False, fontsize='small')
	ax1.set_title(satname +"\'s Positions in GEO vs. " + spacetrackcountry + "\'s Corresponding ITU Space Networks", va='bottom')
	f.subplots_adjust(bottom=0.15)
	# plt.show()
	plt.savefig('../Data/Figures/Historical Compliance Figures/' + satcat + '_' + assessmentdate + '.png')
	print('Plot saved for satcat #:', satcat)
	plt.clf()