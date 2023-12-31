"""
Name:           snl_broughtintouse_download.py
Description:    Downloads the ITU space networks that have been brought into use. Run using snl.py.
Author:         Thomas G. Roberts (thomasgr@mit.edu / thomasgroberts.com)
Date:           August 4, 2023

Inputs:         n/a
Outputs:        ../Data/SNL Downloads/[YYYYMMDD]/snl_broughtintouse_[YYYYMMDD].csv
"""

# The ITU publishes information about when both planned and non-planned space networks are brought into use. The brought-into-use list is available online (https://www.itu.int/net/ITU-R/space/snl/listinuse/index.asp) and updated approximately every two weeks.

# The abbreviations in the "Status" column have the following meanings:
"""
    N : Not yet confirmed, the date in the column "Date of bringing into use" is the foreseen date
    I : Initial information on bringing into use
    C : Confirmed brought into use, No. 11.44B/11.44C/11.44D/11.44E conditions (as applicable) fulfilled.
"""
# In this repository, the phrase "brought into use" is only used when a space network license appears with a "C" in the "Status" column and the date in the "Date of bringing into use" column is equal or less than the date at which compliance is asessessed.

from datetime import datetime
import urllib.request

# Choose a date to run the assessment
assessmentdate = datetime.today().strftime('%Y%m%d')

# Download and save the brought into use list
urllib.request.urlretrieve('https://www.itu.int/net/ITU-R/space/snl/listinuse/index-txt.asp?sel_satname=&sel_orbit_from=&sel_orbit_to=&sel_adm=&sel_org=&sel_date_from=&sel_date_to=&sel_sns_id=&sel_prov=&sel_rec=&order=&mod=', '../Data/SNL Downloads/' + assessmentdate + '/snl_broughtintouse_' + assessmentdate + '.csv')
