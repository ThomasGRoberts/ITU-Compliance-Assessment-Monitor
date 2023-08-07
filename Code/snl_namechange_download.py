"""
Name:           snl_namechange_download.py
Description:    Downloads the ITU space networks that have had their names changed over time.
Author:         Thomas G. Roberts (thomasgr@mit.edu / thomasgroberts.com)
Date:           August 4, 2023

Inputs:         n/a
Outputs:        ../Data/SNL Downloads/[YYYYMMDD]/snl_namechange_[YYYYMMDD].csv
"""

# The ITU publishes information about which ITU satellite networks' names have chang. The name-change list is available online (https://www.itu.int/net/ITU-R/space/snl/name_change/index.asp).

import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import csv

# Choose a date to run the assessment
assessmentdate = datetime.today().strftime('%Y%m%d')

with open('../Data/SNL Downloads/' + assessmentdate + '/snl_namechange_' + assessmentdate + '.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['New Name', 'Old Name'])

url = 'https://www.itu.int/net/ITU-R/space/snl/name_change/index.asp'

source = urllib.request.urlopen(url).read()
soup = BeautifulSoup(source,'html.parser')
tables = soup.find_all('table')

table_rows = tables[0].find_all('tr')

data = False
for table_row in table_rows:
    columns = table_row.findAll('td')
    output_row = []
    for column in columns:
        output_row.append(column.text)
    if data:
        with open('../Data/SNL Downloads/' + assessmentdate + '/snl_namechange_' + assessmentdate + '.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(output_row)
    if output_row == ['down - up', 'down - up']:
        data = True
