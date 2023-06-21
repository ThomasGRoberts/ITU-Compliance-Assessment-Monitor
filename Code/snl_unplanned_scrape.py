"""
Name:           snl_unplanned_scrape.py
Description:    Scrapes and saves just the non-planned portion of the ITU's Space Network List. Run using snl.py.
Author:         Thomas G. Roberts (thomasgr@mit.edu / thomasgroberts.com)
Date:           June 20, 2023

Inputs:         n/a
Outputs:        ../Data/SNL Archives/[Today's Date]/snl_unplanned_[Today's Date].csv
"""

from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request
import csv
import sys
from importlib import reload
# reload(sys)
# sys.setdefaultencoding('utf8')

#Scrape unplanned filings
source = urllib.request.urlopen('https://www.itu.int/online/snl/freqrnge_snl.sh?plan=&lblfreq1=Frequency+%5BMHz%5D%3A+&lblfreq11=+from+&freq_low=0&lblfreq2=+to+&freq_hi=10000000000&lblemi0=Emission%2FReception%3A+&lblemi1=Emission+&lblemi2=Reception+&emi=&lblemi3=All+&lbllong1=Longitude%3A+&lbllong2=+from+&long_from=-180&lbllong3=+%A0+%A0+to++&long_to=180&lblstn=Space+or+Earth%3A+&categ=G&lblcateg1=Geostationary&lblcateg2=Non-geostationary&lblcateg3=Earth+station&lblsub=Submission+reason%3A+&lblsub1=API&lblsub2=Coordination&lblsub3=Notification&ntf=&lblsub4=All&sub0=Select&ie=y').read()
soup = BeautifulSoup(source,'html.parser')
tables = soup.find_all('table')
table_rows = tables[1].find_all('tr')

output_rows = []
for table_row in tables[1].findAll('tr'):
    columns = table_row.findAll('td')
    links = table_row.findAll('a')
    output_row = []
    for column in columns:
        output_row.append(column.text)
    for link in links:
    	output_row.append(link.get('href'))
    output_rows.append(output_row)
    
with open('../Data/SNL Archives/' + datetime.today().strftime('%Y%m%d') +'/snl_unplanned_' + datetime.today().strftime('%Y%m%d') + '.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(output_rows[2:len(output_rows)-2])

