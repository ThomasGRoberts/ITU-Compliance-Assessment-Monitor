# Convert list of lists string into actual list of lists:

list_string = '[[1, 4, 5], [4, 6, 8]]'

print(list_string)
list_list = eval(list_string)

print(list_list)

for i in list_list:
	print(i)
	for j in i:
		print(j)

# # Write that references all the longtudinal data from ../../../PoL Characterization Algorithm/Data/OEs and LLAs/[satcat].csv files and saves it in one place

# from os import listdir
# from os.path import isfile, join
# from datetime import datetime, timedelta
# import pandas as pd
# import numpy as np
# import csv

# # Get a list of all satcats for which an OE exists
# onlyfiles = [f for f in listdir('../../../PoL Characterization Algorithm/Data/OEs and LLAs/') if isfile(join('../../../PoL Characterization Algorithm/Data/OEs and LLAs/', f))]
# satcats = []
# for file in onlyfiles:
# 	try:
# 		satcats.append(int(file[:-4]))
# 	except ValueError:
# 		pass
# satcats.sort()

# # Make a list of dates
# startdate = datetime.strptime('2010-01-01', '%Y-%m-%d')
# enddate = datetime.strptime('2021-12-31', '%Y-%m-%d')
# dates = []
# while startdate <= enddate:
# 	dates.append(str(startdate)[0:10])
# 	startdate += timedelta(days=1)

# # Make a dataframe to hold the results
# df_longitudes = pd.DataFrame(0, columns = ['Date'] + satcats, index = np.arange(len(dates)))

# for i in np.arange(len(df_longitudes)):
# 	date = dates[i]
# 	df_longitudes.at[i, 'Date'] = date

# for s in np.arange(len(satcats)):
# 	satcat = satcats[s]
# 	print('Pulling longitudinal data for', satcat, '...')
# 	alltimesteps = []
# 	alllongitudes = []
# 	with open('../../../PoL Characterization Algorithm/Data/OEs and LLAs/' + str(satcat) + '.csv') as f:
# 		reader = csv.reader(f, delimiter=",")
# 		for row in reader:
# 			if row[0] != 'Time step':
# 				alltimesteps.append(row[0][0:10])
# 				alllongitudes.append(row[10])
# 	# Just include one time step per day
# 	for i in np.arange(len(df_longitudes)):
# 		date = dates[i]
# 		found = False 
# 		for a, b in zip(alltimesteps, alllongitudes):
# 			if (a == date and found == False):
# 				longitude = b
# 				found = True
# 		if not found:
# 			longitude = 'n/a'
# 		df_longitudes.at[i, satcat] = longitude
# 		print('Satellite', s+1, 'of', len(satcats), '(' + str(satcat) + ')', date, '...', longitude)

# # Save the file		
# df_longitudes.to_csv('../Data/Longitude Inputs/longitudes_historical.csv', index = None)



