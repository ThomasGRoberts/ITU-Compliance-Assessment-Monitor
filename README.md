# ITU Compliance Assessment Monitor

**Author:** Thomas G. Roberts ([thomasgr@mit.edu](mailto:thomasgr@mit.edu) / [thomasgroberts.com](thomasgroberts.com))

**Last Updated:** June 14, 2023

This tool can be used to assess geosynchronous (GEO) satellite operators' compliance with orbital slotting guidelines from the International Telecommunications Union (ITU), a specialized agency of the United Nations.

GEO satellite positions can be measured in longitudinal degrees along the geostationary belt. Member states of the ITU can apply and receive space network licenses that describe an individual physical position within the geostationary belt and a number of frequency bands at which satellites can operate such that they are free from harmful interference in the radio-frequency spectrum with other nearby space systems. Altough this system of GEO satellite spectrum allocation has been in place for decades, many operators choose to [largely ignore](https://amostech.com/TechnicalPapers/2022/SSA-SDA/Roberts.pdf) their orbital slotting guidelines.

This work represents a component of the author's PhD dissertation at MIT's Department of Aeronautics and Astronautics, "Measuring Adherence to the International Telecommunication Union’s Geosynchronous Orbital Slotting Guidelines," which offers a historical assessment of adherence to the physical component of ITU space network licences for more than decade of recent GEO satellite operations.

## Getting Started

The scripts in this repository are designed to produce results assessing adherence _today_, when the code is executed. `[Today's Date]` is always written in the YYYYMMDD format. 

### Prepare the Input File
Before performing an assessment, produce a two-column input file describing the GEO satellites you would like to assess and save it as `./Data/Longitude Inputs/longitudes_[Today's Date].csv`. 

The two columns, 'NORAD ID' and 'Longitude', should describe longitudinal positions for GEO satellites of interest. NORAD IDs should be written with no leading zeros. Longitudinal positions in the western hemisphere should be written as negative numbers between -180 and 0.

### Perform Today's Assessment
1. Run the `snl.py` script.
	* This script downloads the latest space network license data from the ITU's Space Network List (SNL) and nicely organizes it.
2. Run the `compliance.py` script.
	* This script takes the prepared input file and offers a satellite-by-satellite letter-grade assessment of ITU orbital slotting compliance.
	* Letter-grade assessments are saved as `./Data/Compliance Grades/grades_[Today's Date].csv`.
	* A shortlist of nearby space network licenses are saved as `./Data/Nearby Shortlists/[Today's Date]/[NORAD ID]_[Today's Date].csv`.

### A Note on Automation

This tool could be paired with a actively updating satellite catalog dataset to automatically assess adherence to ITU orbital slots on a daily cadence. One formulation might could be to perform the following steps each day at the same time:
1. Append information about new GEO satellites to the local satellite catalog (`./Data/Reference Files/satellitlecatalog.csv`).
2. Create a new longitudes file with the longitudinal position of each active GEO satellite in the catalog. 
3. Run the `snl.py` script.
4. Run the `compliance.py` script.
5. For each satellite:
	* Display the list of nearby licenses (`./Data/Nearby Shortlists/[Today's Date]/[NORAD ID]_[Today's Date].csv`).
	* Display the current letter grade. 
	* Display the rolling average of past letter grades.

## Definitions

Some definitions are helpful to ensure clear understanding of various terms and concepts.

### License Types

There are two types of ITU space network licenses: non-planned and planned.

#### Non-Planned Licenses

“Non-planned” services are those that use frequency bands that have been made available by the ITU on a first-come, first-served basis. Just three countries—the United States, Russia, and China—hold about half of all non-planned space network licenses.

#### Planned Licenses

“Planned” services are those that use frequency bands that have been distributed by the ITU amongst applicant administrations on a more equitable basis—a concept developed over two meetings of the “World Administrative Radio Conference on the Use of Geostationary-Satellite Orbit and the Planning of Space Services Utilizing It” in 1985 and 1988—to ensure future access to the geostationary belt by developing nations that operate few or no satellites at the time of application.

In general, planned licenses are less common than non-planned ones.

### Filing Types

ITU members states (or "ITU Administrations") submit various rounds of filings to the ITU in accordance to the Union's conventions:

#### Advance Public Information (A)

This filing type represents the first public record for a proposed space network. It effectively announces an ITU Administration's interest in particular orbital slots and frequency bands. These filings should come two to seven years before their operator plans to bring it into use, but that is not always the case.

This type of filing is only associated with non-planned licenses. 

#### Coordination Request (C)

The date at which the ITU's Radiocommunication Bureau (BR) receives this type of filing marks the network's place in the queue of proposed filings and the beginning of the coordination process that ensures that the new license would not pose a threat of harmful interference with active licenses or those that come earlier in the coordination queue.

This type of filing is only associated with non-planned licenses. 

#### Planned (P or P/Plan/List)

This type of filing refers to an early-stage planned license that has not yet received protected status. 

This type of filing is only associated with planned licenses. 

#### Notification of Space Station (N)

This type of filing marks a network's transition from an "application" to a "license" in that it grants the network protected status to its prescribed orbital slot and frequency bands.

This type of filing is associated with both non-planned planned licenses. 

#### Due Diligence (U)

ITU conventions require that administrations submit more information about the satellite that will host a space network license once it becomes available. Such information (including the proposed launch date, launch vehicle, launch site, and satellite manufcaturer) is included in what are known as _due diligence_ filings. The information within due diligence filings is not available on the easy-to-access SNL, but rather the harder-to-access Space Network System (SNS). The SNS is also available on the ITU’s website, but is restricted to users with annual subscriptions or who are members of the Union’s Telecommunication Information Exchange Service (TIES). 

The data encoded within due diligence filings are used to match GEO satellites with space network licenses. 

### "Brought into Use"

When the ITU determines that a space network license has been "brought into use" via an assessment of more required filings from ITU administrations, it appears [here](https://www.itu.int/net/ITU-R/space/snl/listinuse/index.asp). For this tool, space network licenses are considered to be brought into use if the the ITU's "Date of bringing into use" is today's date or earlier.

Bringing-into-use information is updated by the ITU approximately every two weeks.

### "Matched Characteristics"

A GEO satellite is said to "match" a space network license if its mission characteristics resemble those encoded in the license's due diligence filings. For this tool, a match requires that:
* The center of the launch window described in the due diligence filings is less than one year away from the satellite's actual launch;
* The ITU Administration corresponds to the satellite's operating country or organization (see Table A2.1 [here](https://amostech.com/TechnicalPapers/2022/SSA-SDA/Roberts.pdf) for more information);
* Two of the following three characteristics match:
	* Launch vehicle family;
	* Launch site;
	* Satellite manufacturer.

Note that this definition does not consider the prescribed longitude of a space network license. Doing so inherently assumes some level of adherence, which should be considered inappropriate for an adherence assessment.

Match information is prepared by the author.

### "Corresponding ITU Administration"

Since the many space object catalogs, including the one used for this tool (`./Data/Reference Files/satellitlecatalog.csv`), allows countries, groups of countries, and non-state organizations to be listed as satellite operators while the ITU considers only ITU member states as space network administrations, a crossreference scheme must be established to match satellite operators to space network administrators. GEO satellite
operators are considered a match with a space network filing’s administration if the administration’s ITU country symbol appears alongside the operator’s abbreviation in Table A2.1 [here](https://amostech.com/TechnicalPapers/2022/SSA-SDA/Roberts.pdf).
 
### Compliance Letter Grades

Letter grades are used to describe GEO satellites's compliance. 
* An **"A" letter grade** means there there exists a space network license within 0.1 degrees longitude held by a corresponding ITU administration that has been brought into use and features matching characteristics.
* A **"B" letter grade** means that there exists a space network license within 0.1 degrees longitude held by a corresponding ITU administration that has been brought into use, but its features do not match those of the satellite.
* A **"C" letter grade** means that there exists an early-stage space network filing (i.e. 'A', 'C', 'P', or 'P/Plan/List', meaning protected access is not yet granted) within 0.1 degrees longitude held by a corresponding ITU administration.
* A **"D" letter grade** means that there are no filings of any kind held by _any_ ITU administration within 0.1 degrees longitude.
* A **"F" letter grade** means that there are no filings of any kind held by a corresponding ITU administration within 0.1 degrees longitude, but another ITU administration _does_ have a nearby filing.

This letter grade scheme was modeled after the U.S. collegiate 4.0 scale, such that historical compliance can be measured using a traditional grade-point average.

## Scripts

Performing today's assessment requires running just two scripts (`snl.py` and `compliance.py`). This section describes those two scripts as well as the others that support them. 

### `snl.py`

The ITU Space Network List includes relevant information about space network filings in three places. [One place](https://www.itu.int/online/snl/freqrnge_snl.sh?plan=&lblfreq1=Frequency+%5BMHz%5D%3A+&lblfreq11=+from+&freq_low=0&lblfreq2=+to+&freq_hi=10000000000&lblemi0=Emission%2FReception%3A+&lblemi1=Emission+&lblemi2=Reception+&emi=&lblemi3=All+&lbllong1=Longitude%3A+&lbllong2=+from+&long_from=-180&lbllong3=+%A0+%A0+to++&long_to=180&lblstn=Space+or+Earth%3A+&categ=G&lblcateg1=Geostationary&lblcateg2=Non-geostationary&lblcateg3=Earth+station&lblsub=Submission+reason%3A+&lblsub1=API&lblsub2=Coordination&lblsub3=Notification&ntf=&lblsub4=All&sub0=Select&ie=y) has filing data associated with unplanned space network licenses, [another](https://www.itu.int/online/snl/freqrnge_snlplan.sh?plan=plan&lblfreq1=Frequency+%5BMHz%5D%3A+&lblfreq11=+from+&freq_low=0&lblfreq2=+to+&freq_hi=10000000000&lblemi0=Emission%2FReception%3A+&lblemi1=Emission+&lblemi2=Reception+&emi=&lblemi3=All+&lbllong1=Longitude%3A+&lbllong2=+from+&long_from=-180&lbllong3=+%A0+%A0+to++&long_to=180&lblplan=BSS+Plans+%26+Lists+%28AP30%2F30A%29%3A&lblplan1=Regions+1%263+Downlink%28AP30%29&lblplan2=Regions+1%263+feeder-link+%28AP30A%29&lblplan3=Region+2%28AP30%2F30A%29&plan_id=A&lblplan4=All&lblprov1=Article+4+%28Seeking+agreement%29&lblprov2=Article+5+%28Notification%29&lblprov3=Due+Diligence+%28Res.49%29&lblprov4=PLAN%2FList&bss_list=A&lblprov5=All&lblsof=Guardbands&gb_type=C&lblprovsof1=Article+2A+%28Coordination%29&lblprovsof2=Article+11+%28Notification%29&lblprovsof3=All&lblsof2=%28Space+Operation+Functions%29&fss=on&lblfss=FSS+Plan+%28AP30B%29&lblprovfss1=Article+6+%28Seeking+agreement%29&lblprovfss2=Article+8+%28Notification%29&lblprovfss21=Due+Diligence+%28Res.49%29&lblprovfss3=PLAN%2FList&fss_type=A&lblprovfss4=All&sub2=Select&ie=y) has filing data planned space network licenses, and [a third](https://www.itu.int/net/ITU-R/space/snl/listinuse/index.asp) has information describes whether both the unplanned and planned licenses have been brought into use. This script downloads those three datasets and organizes them into one easy-to-read file (`./Data/SNL Archives/[Today's Date]/licenses_[Today's Date].csv`). 

#### `snl_unplanned_scrape.py`

This script scrapes information about _non-planned_ space network licenses (`./Data/SNL Archives/[Today's Date]/snl_unplanned_[Today's Date].csv`).

#### `snl_planned_scrape.py`

This script scrapes information about _planned_ space network licenses (`./Data/SNL Archives/[Today's Date]/snl_planned_[Today's Date].csv`).

#### `snl_broughtintouse_download.py`

This script downloads information relating to when space network licesnes were _brought into use_ (`./Data/SNL Archives/[Today's Date]/snl_broughtintouse_[Today's Date].csv`).

### `compliance.py`

This script issues a letter-grade compliance rating for GEO satellites given their NORAD ID and longitudinal position (`./Data/Compliance Grades/grades_[Today's Date].csv`). A shortlist of nearby filings is also produced for each GEO satellite (`./Data/Nearby Shortlists/[Today's Date]/[NORAD ID]_[Today's Date].csv`).


## Data

Interesting products within the `./Data/` directory are described in more detail here.

### Nearby Shortlists

For each GEO satellite included in the input file, a shortlist of space network licenses within 1.0 degrees is produced. As an example, a short list of nearby licenses for the _Luch (Olymp)_ satellite (NORAD ID: 40258) on June 14, 2023, is reproduced below. On this date, _Luch_ was located at approximately -18.07 degrees, or 18.07°W.

| License          | ITU Administration            | Longitude | License Type | Filing Type                       | Brought into Use | Matched Characteristics |
|------------------|-------------------------------|-----------|--------------|-----------------------------------|------------------|-------------------------|
| YAHSAT-FSS-18W   | United Arab Emirates 🇦🇪 | 18.0°W   | Planned      | Planned (P)                       | n/a              | n/a                     |
| INTELSAT7 342E   | United States 🇺🇸        | 18.0°W   | Non-Planned  | Due Diligence (U)                 | Yes              | No                      |
| INTELSAT9 342E   | United States 🇺🇸        | 18.0°W   | Non-Planned  | Due Diligence (U)                 | Yes              | No                      |
| INTELSAT8 342E   | United States 🇺🇸        | 18.0°W   | Non-Planned  | Due Diligence (U)                 | Yes              | No                      |
| USASAT-71Q       | United States 🇺🇸        | 18.0°W   | Non-Planned  | Coordination Request (C)          | n/a              | n/a                     |
| INMARSAT-7-18W   | Switzerland 🇨🇭          | 18.0°W   | Non-Planned  | Coordination Request (C)          | n/a              | n/a                     |
| UKNETSAT-18W     | United Kingdom 🇬🇧       | 18.0°W   | Non-Planned  | Due Diligence (U)                 | Yes              | No                      |
| SIGNSAT-18W      | China 🇨🇳                | 18.0°W   | Non-Planned  | Coordination Request (C)          | n/a              | n/a                     |
| USASAT-101E      | United States 🇺🇸        | 18.0°W   | Planned      | Planned (P)                       | n/a              | n/a                     |
| UKFSS-18W-A      | United Kingdom 🇬🇧       | 18.0°W   | Planned      | Due Diligence (U)                 | Yes              | No                      |
| UKFSS-18W        | United Kingdom 🇬🇧       | 18.0°W   | Planned      | Due Diligence (U)                 | Yes              | No                      |
| SKYNET-5E        | United Kingdom 🇬🇧       | 17.8°W   | Non-Planned  | Due Diligence (U)                 | Yes              | No                      |
| SKYNET-5E-KA3    | United Kingdom 🇬🇧       | 17.8°W   | Non-Planned  | Coordination Request (C)          | n/a              | n/a                     |
| INMARSAT-6-17.5W | United Kingdom 🇬🇧       | 17.5°W   | Non-Planned  | Coordination Request (C)          | n/a              | n/a                     |
| YAHSAT-G6-17.5W  | United Arab Emirates 🇦🇪 | 17.5°W   | Non-Planned  | Due Diligence (U)                 | Yes              | No                      |
| DJI00000         | Djibouti 🇩🇯             | 17.46°W  | Planned      | Planned (P/Plan/List)             | n/a              | n/a                     |
| USMB-3           | United States 🇺🇸        | 19.0°W   | Non-Planned  | Notification of Space Station (N) | Yes              | n/a                     |
| LIE00000         | Liechtenstein 🇱🇮        | 17.1°W   | Planned      | Planned (P/Plan/List)             | n/a              | n/a                     |

The country names in the "ITU Administration" appear as they do in the [ITU's list of member states](https://www.itu.int/en/ITU-R/terrestrial/fmd/Pages/administrations_members.aspx).

Such a list of is particularly insightful for satellites that perpetually violate ITU orbital slotting guidelines. When a satellite is operating somewhere it is not licensed to be, who _is_ entitled to be in that very spot? 

### Due Diligence Matches

Because most users do not have TIES access, the process of matching satellite characteristics and ITU space network license due diligence information is performed offline and results are saved in `./Data/Due Diligence Matches/[NORAD ID].csv`. These files do not reproduce the data stored in the ITU's SNS, but rather the results of a matching algorithm that compares the information from the SNS with publicly available satellite catalog information. 
