"""
Name:           snl_broughtintouse_download.py
Description:    Downloads the ITU space network licenses that have been brought into use. Run using snl.py.
Author:         Thomas G. Roberts (thomasgr@mit.edu / thomasgroberts.com)
Date:           June 8, 2023

Inputs:         n/a
Outputs:        ../Data/SNL Archives/[Today's Date]/snl_broughtintouse_[Today's Date].csv
"""

# The ITU publishes information about when both planned and non-planned space network licenses are brought into use. The brought-into-use list is available online (https://www.itu.int/net/ITU-R/space/snl/listinuse/index.asp) and updated approximately every two weeks.

# The abbreviations in the "Status" column have the following meanings:
"""
    N : Not yet confirmed, the date in the column "Date of bringing into use" is the foreseen date
    I : Initial information on bringing into use
    C : Confirmed brought into use, No. 11.44B/11.44C/11.44D/11.44E conditions (as applicable) fulfilled.
"""
# In this repository, the phrase "brought into use" is only used when a space network license appears with a "C" in the "Status" column and the date in the "Date of bringing into use" column is equal or less than the date at which compliance is asessessed.

from datetime import datetime
import urllib.request

# The brought-into-use list should be saved in ../Data/SNL Archives/[Today's Date]/snl_broughtintouse_[Today's Date].csv.
urllib.request.urlretrieve('https://www.itu.int/net/ITU-R/space/snl/listinuse/index-txt.asp?sel_satname=&sel_orbit_from=&sel_orbit_to=&sel_adm=&sel_org=&sel_date_from=&sel_date_to=&sel_sns_id=&sel_prov=&sel_rec=&order=&mod=', '../Data/SNL Archives/' + datetime.today().strftime('%Y%m%d') +'/snl_broughtintouse_' + datetime.today().strftime('%Y%m%d') + '.csv')
