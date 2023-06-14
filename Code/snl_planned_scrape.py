"""
Name:           snl_planned_scrape.py
Description:    Scrapes and saves just the planned portion of the ITU's Space Network List. Run using snl.py.
Author:         Thomas G. Roberts (thomasgr@mit.edu / thomasgroberts.com)
Date:           June 8, 2023

Inputs:         n/a
Outputs:        ../Data/SNL Archives/[Today's Date]/snl_planned_[Today's Date].csv
"""

from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request
import csv
import sys
from importlib import reload

#Scrape planned filings
source = urllib.request.urlopen('https://www.itu.int/online/snl/freqrnge_snlplan.sh?plan=plan&lblfreq1=Frequency+%5BMHz%5D%3A+&lblfreq11=+from+&freq_low=0&lblfreq2=+to+&freq_hi=10000000000&lblemi0=Emission%2FReception%3A+&lblemi1=Emission+&lblemi2=Reception+&emi=&lblemi3=All+&lbllong1=Longitude%3A+&lbllong2=+from+&long_from=-180&lbllong3=+%A0+%A0+to++&long_to=180&lblplan=BSS+Plans+%26+Lists+%28AP30%2F30A%29%3A&lblplan1=Regions+1%263+Downlink%28AP30%29&lblplan2=Regions+1%263+feeder-link+%28AP30A%29&lblplan3=Region+2%28AP30%2F30A%29&plan_id=A&lblplan4=All&lblprov1=Article+4+%28Seeking+agreement%29&lblprov2=Article+5+%28Notification%29&lblprov3=Due+Diligence+%28Res.49%29&lblprov4=PLAN%2FList&bss_list=A&lblprov5=All&lblsof=Guardbands&gb_type=C&lblprovsof1=Article+2A+%28Coordination%29&lblprovsof2=Article+11+%28Notification%29&lblprovsof3=All&lblsof2=%28Space+Operation+Functions%29&fss=on&lblfss=FSS+Plan+%28AP30B%29&lblprovfss1=Article+6+%28Seeking+agreement%29&lblprovfss2=Article+8+%28Notification%29&lblprovfss21=Due+Diligence+%28Res.49%29&lblprovfss3=PLAN%2FList&fss_type=A&lblprovfss4=All&sub2=Select&ie=y').read()
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
  
with open('../Data/SNL Archives/' + datetime.today().strftime('%Y%m%d') +'/snl_planned_' + datetime.today().strftime('%Y%m%d') + '.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(output_rows[2:len(output_rows)-2])
