"""
Name:           snl_suspended_download.py
Description:    Downloads the ITU space networks that have been suspended. Run using snl.py.
Author:         Thomas G. Roberts (thomasgr@mit.edu / thomasgroberts.com)
Date:           June 19, 2023

Inputs:         n/a
Outputs:        ../Data/SNL Archives/[Today's Date]/snl_broughtintouse_[Today's Date].csv
"""

# The ITU publishes information about when ITU administrations submit requests for suspension (and resumption of operation). The suspension list is available online (https://www.itu.int/net/ITU-R/space/snl/list1149/index.asp).

# The abbreviations in the "Status" column have the following meanings:
"""
    S: Suspended
    J: Initial confirmation of resumption of use
    R: Confirmed resumption of use, No. 11.49.1 or § 5.2.10 conditions fulfilled
"""

# The abbreviations in the "Type" column have the following meanings:
"""
    P: Partial suspension of the network
    T: Total suspension of the network
"""

from datetime import datetime
import urllib.request

# The brought-into-use list should be saved in ../Data/SNL Archives/[Today's Date]/snl_broughtintouse_[Today's Date].csv.
urllib.request.urlretrieve('https://www.itu.int/net/ITU-R/space/snl/list1149/index-txt.asp?sel_satname=&sel_orbit_from=&sel_orbit_to=&sel_adm=&sel_org=&sel_suspension_from=&sel_suspension_to=&sel_resumption_from=&sel_resumption_to=&sel_sns_id=&sel_resumption_yes=&sel_resumption_no=&order=&mod=', '../Data/SNL Archives/' + datetime.today().strftime('%Y%m%d') +'/snl_suspended_' + datetime.today().strftime('%Y%m%d') + '.csv')
