# ITU Compliance Assessment Monitor

**Author:** Thomas G. Roberts ([thomasgr@mit.edu](mailto:thomasgr@mit.edu) / [thomasgroberts.com](thomasgroberts.com))

**Last Updated:** August 9, 2023

This tool can be used to assess geosynchronous (GEO) satellite operators' compliance with orbital allocations from the International Telecommunications Union (ITU), a specialized agency of the United Nations.

After an international coordination process, ITU member states receive space network assignments that describe individual physical positions within the geostationary belt (*orbital* allocations) and frequency bands (*frequency* allocations) at which satellites can operate such that they are free from harmful interference with other nearby space systems. Altough this system of GEO satellite spectrum allocation has been in place for decades, many operators choose to [largely ignore](https://amostech.com/TechnicalPapers/2022/SSA-SDA/Roberts.pdf) their orbital allocations and instead operate wherever they choose.

This work represents a component of the author's doctoral thesis at [MIT's Department of Aeronautics and Astronautics](https://aeroastro.mit.edu/), "Assessing Compliance with Geosynchronous Orbital Allocations from the International Telecommunication Union," which offers a historical assessment of compliance to the physical component of ITU space networks for more than decade of recent GEO satellite operations.

## Getting Started

To run a compliance assessment:
1. [Download](https://github.com/ThomasGRoberts/ITU-Compliance-Assessment-Monitor/archive/refs/heads/main.zip) or [clone](https://github.com/ThomasGRoberts/ITU-Compliance-Assessment-Monitor.git) this GitHub repository.
2. Download the latest ITU space network data by running the `./Code/snl.py` script.
3. Produce a formatted input file describing the longitudinal positions of GEO satellites of interest and add it to the appropriate sub-directory.
	* Note: single- and multi-date compliance assessments require differently formatted input files saved in different sub-directories, as described in the following subsections.
4. Assess compliance for a single date or multiple dates by running `compliance_daily.py` or `compliance_historical.py`, respectively.

The following subections describe each of these four steps in greater detail. 

### Step 1: Organize local directories

Downloading this GitHub repository results in the following file organization:
```
📁 .
├── 📁 Data
│   ├── 📁 Reference Files	
│   ├── 📁 SNL Downloads
│   ├── 📁 Daily Analysis
│   └── 📁 Historical Analysis
└── 📁 Code
```

All data associated with single- and multi-date compliance assessments are organized in the `./Data/Daily Analysis/` and `./Data/Historical Analysis/` sub-directories, respectively, including the user-generated input files. Both variants of the compliance assessment scripts reference data in the `./Data/Reference Files/` and `./Data/SNL Downloads/` sub-directories. 

### Step 2: Download the latest ITU data from the SNL

Running `./Code/snl.py` produces a sub-directory in `./Data/SNL Downloads/` named with today's date in the `YYYYMMDD` format. Inside that sub-directory you'll find a file called `networks_[Today's Date].csv`, with columns that describe each network's:
- Name ('Network Name');
- Prescribed longitude ('Longitude');
- An abbreviation for the ITU administration that submits filings for that network ('ITU Administration');
- The previous name for the network, if its name has changed since its earliest filing ('Previous Name');
- Whether the network offers planned or non-planned services ('Planned or Non-Planned');
- The highest-maturity notification reason of all filings received for the network ('Highest Maturity');
- The date when the network was brought into use, if applicable ('Brought-into-Use Date');
- The date when the network was first eligible for protections from harmful interference, if applicable ('Late-Stage Filing Date');
- The date when the first filing of any kind was received for the network ('Early-Stage Filing Date'); and
- Information describing any time periods during which the network was suspended ('Suspensions').  

### Step 3: Produce input files

For both single- and multi-date compliance assessments, users must create an input file of GEO satellites' longitudinal positions and save it in an appropriate directory. The two variants described below are formatted differently, such that they are both row-rich instead of column-rich. 

#### Single-date assessment input file format
Input files for single-date assessments have one row per GEO satellite of interest.

The two columns, 'NORAD ID' and 'Longitude', describe the catalog ID number and longitudinal position for each satellite. NORAD IDs should be written with no leading zeros. Longitudinal positions in the western hemisphere should be written as negative numbers between -180 and 0. If no longitudinal position is available for an object of interest, write 'n/a' in the longitude column.

An input file for a single-date assessment on August 7, 2023, should be called `longitudes_20230807.csv` and stored in a sub-directory called `./Data/Daily Analysis/20230807/`. Its format looks like the example below.

| <center>NORAD ID</center> | <center>Longitudes</center> |
|:------------------:|:-------------------------------:|
|      38978         |        -177.042        |
|         ⋮          |             ⋮             |
|      37834         |         179.996        |


The order of the entries in this file doesn't matter. Because compliance assessments can be based on the behavior of nearby neighbors, it is critical to be as comprehensive as possible when creating input files: the more GEO objects included in this input file, the more accurate the resulting compliance assessments will be.

#### Multi-date assessment input file format

Input files for multi-date assessments have one *column* per GEO satellite of interest and one *row* per evaluation date.

The first column stores evaluation dates in the `YYYY-MM-DD` format. The next columns store longitudinal data for GEO satellites of interest, with their NORAD ID as the column header. NORAD IDs should be written with no leading zeros. Longitudinal positions in the western hemisphere should be written as negative numbers between -180 and 0. If no longitudinal position is available for an object of interest at a particular evaluation date, write 'n/a' in the longitude column.

An input file for a multi-date assessment run on August 7, 2023, should be called `longitudes_20230807.csv` and stored in a sub-directory called `./Data/Historical Analysis/20230807/`. Its format looks like the example below.

| <center>Date</center> |<center>27632</center> | <center>40258</center> |... |<center>41838</center> |
|:---------------------:|:---------------------:|:----------------------:|:--:|:---------------------:|
|      2010-01-01       |    -91.010       |    n/a        |... |   n/a        |
|      2010-01-02       |   -91.010       |    n/a        |... |   n/a        |
|      2010-01-03       |    -91.012       |    n/a        |... |   n/a        |
|         ⋮             |             ⋮          |             ⋮          |... |             ⋮          |
| 2021-12-29 |   -46.131    |   59.958      |  ... |117.553     |
| 2021-12-30 |   -47.062    |   59.947      |  ... |117.557     |
| 2021-12-31 |   -47.990    |   59.948      |  ... |117.561     |

The rows in this file should be ordered chronologically. The order of the non-date columns doesn't matter. Because compliance assessments are based on the behavior of nearby neighbors, it is critical to be as comprehensive as possible when creating input files: the more GEO objects included in this input file, the more accurate the resulting compliance assessments will be.

### Step 4: Assess compliance

Assess single- or multi-date compliance by running `./Code/compliance_daily.py` or `./Code/compliance_daily.py`, respectively. 

For both single- and multi-date assessments, the algorithm produces two products: compliance results and shortlists of space networks with prescribed longitudinal positions near the assessed satellites (called *nearby neighbors*). These various types of output files are described below.

#### Compliance results
Compliance results are stored in `./Data/Daily Analysis/[Today's Date]/compliance_[Today's Date].csv` and `./Data/Historical Analysis/[Today's Date]/Historical Compliance Assessments/compliance_[NORAD ID]_[Today's Date].csv`, respectively. The two variants of compliance assessment results are described below.

##### Single-date assessment output

Running a single-date compliance assessment produces one output file, stored in `./Data/Daily Analysis/[Today's Date]/compliance_[Today's Date].csv`, with four columns:
- The catalog number of the GEO object of interest ('NORAD ID');
- The longitudinal position at which it was assessed ('Longitude');
- The 'Yes', 'No', or 'Maybe' compliance assessment ('Compliance Assessment'); and
- A note further describing how the satellite is or is not in compliance with the ITU Radio Regulations ('Note').

##### Multi-date assessment output

Running a multi-date compliance assessment produces one output file per satelite assessed, stored in `./Data/Historical Analysis/[Today's Date]/Historical Compliance Assessments/compliance_[NORAD ID]_[Today's Date].csv`, with four columns:
- The date for which compliance was assessed ('Date');
- The longitudinal position at which the satellite was assessed ('Longitude');
- The 'Yes', 'No', or 'Maybe' compliance assessment ('Compliance Assessment'); and
- A note further describing how the satellite is or is not in compliance with the ITU Radio Regulations ('Note').

#### Shortlists of nearby neighbors

For each GEO satellite evaluated, a shortlist of space networks within 1.0 degrees is produced for each assessment date. Shortlists for single- and multi-date assessments are stored in `./Data/Daily Analysis/[Today's Date]/Daily Nearby Shortlists/nearbyshortlist_[NORAD ID]_[Today's Date].csv` and `./Data/Historical Analysis/Historical Nearby Shortlists/[Assessment Date]/nearbyshortlist_[NORAD ID]_[Assessment Date].csv`, respectively.

As an example, a shortlist of nearby networks for the *Luch (Olymp)* satellite (NORAD ID: 40258) on October 24, 2017, is reproduced below. On this date, Luch was located at approximately 38.12 degrees, or 38.12°E.

|           Network           | ITU Administration | Longitude | Network Type | Filing Maturity | Brought into Use | Suspended | Longitudinal Distance |
|:---------------------------:|:------------------:|:---------:|:------------:|:--------------:|:----------------:|:---------:|:---------------------:|
|         UKR00001            |   Ukraine 🇺🇦     |  38.2°E  |   Planned    |  Early-Stage   |        No        |    No     |        0.08°         |
| PAKSAT-MM1-38.2E            |  Pakistan 🇵🇰   |  38.2°E  |  Non-Planned |  Early-Stage   |        No        |    No     |        0.08°         |
| PAKSAT-MM1-38.2E-KA         |  Pakistan 🇵🇰   |  38.2°E  |  Non-Planned |  Early-Stage   |        No        |    No     |        0.08°         |
| PAKSAT-MM1-38.2E-KA1        |  Pakistan 🇵🇰   |  38.2°E  |  Non-Planned |  Early-Stage   |        No        |    No     |        0.08°         |
| PAKSAT-MM1-38.2E-30B        |  Pakistan 🇵🇰   |  38.2°E  |   Planned    |  Early-Stage   |        No        |    No     |        0.08°         |
| PAKSAT-MM1-38.2E-FSS        |  Pakistan 🇵🇰   |  38.2°E  |   Planned    |  Early-Stage   |        No        |    No     |        0.08°         |
|      ATHENA-FIDUS-38E       |   France 🇫🇷    |  38.0°E  |  Non-Planned |  Late-Stage    |       Yes        |    No     |        0.12°         |
|        PAKSAT-1R1           |  Pakistan 🇵🇰   |  38.0°E  |  Non-Planned |  Late-Stage    |       Yes        |    No     |        0.12°         |
|         PAKSAT-1            |  Pakistan 🇵🇰   |  38.0°E  |  Non-Planned |  Late-Stage    |       Yes        |    No     |        0.12°         |
|        ITS-38E-N            |    China 🇨🇳    |  38.0°E  |  Non-Planned |  Early-Stage   |        No        |    No     |        0.12°         |
|        PAKSAT-1R            |  Pakistan 🇵🇰   |  38.0°E  |  Non-Planned |  Late-Stage    |       Yes        |    No     |        0.12°         |
|         FMS5-37.5E          |   France 🇫🇷    |  37.5°E  |  Non-Planned |  Early-Stage   |        No        |    No     |        0.62°         |
|      HELLAS-SAT-2G          |   Greece 🇬🇷    |  39.0°E  |  Non-Planned |  Late-Stage    |       Yes        |  Partial  |        0.88°         |
|        HELLAS-SAT-C         |   Greece 🇬🇷    |  39.0°E  |  Non-Planned |  Early-Stage   |        No        |    No     |        0.88°         |
|      INMARSAT-S4-R          | United Kingdom 🇬🇧 |  39.0°E  |  Non-Planned |  Early-Stage   |       Yes        |    No     |        0.88°         |
|       KYPROS-SAT-7          |   Cyprus 🇨🇾    |  39.0°E  |  Non-Planned |  Early-Stage   |        No        |    No     |        0.88°         |
|        HELLAS-SAT           |   Greece 🇬🇷    |  39.0°E  |  Non-Planned |  Late-Stage    |       Yes        |    No     |        0.88°         |
|       KYPROS-SAT-5          |   Cyprus 🇨🇾    |  39.0°E  |  Non-Planned |  Late-Stage    |       Yes        |  Partial  |        0.88°         |
|       KYPROS-SAT-C          |   Cyprus 🇨🇾    |  39.0°E  |  Non-Planned |  Late-Stage    |       Yes        |    No     |        0.88°         |
|       KYPROS-SAT-3          |   Cyprus 🇨🇾    |  39.0°E  |   Planned    |  Late-Stage    |       Yes        |    No     |        0.88°         |
|       KYPROS-SAT-6          |   Cyprus 🇨🇾    |  39.0°E  |   Planned    |  Early-Stage   |        No        |    No     |        0.88°         |
|    HELLAS-SAT-4G            |   Greece 🇬🇷    |  39.0°E  |   Planned    |  Early-Stage   |        No        |    No     |        0.88°         |
|    HELLAS-SAT-3G            |   Greece 🇬🇷    |  39.0°E  |   Planned    |  Late-Stage    |       Yes        |   Total   |        0.88°         |
|    KYPROS-SAT-L4            |   Cyprus 🇨🇾    |  39.0°E  |  Non-Planned |  Late-Stage    |       Yes        |    No     |        0.88°         |
|        GAB00000             |    Gabon 🇬🇦    |  39.0°E  |   Planned    |  Early-Stage   |        No        |    No     |        0.88°         |
|        CANGYU-2             |    China 🇨🇳    |  37.2°E  |  Non-Planned |  Early-Stage   |        No        |    No     |        0.92°         |
|        D  00002             |  Germany 🇩🇪    |  37.2°E  |   Planned    |  Early-Stage   |        No        |    No     |        0.92°         |


These tables also include a 'Link' column, not shown in the example above, which points towards the relevant queried result of Part-B of the Space Network List online.


## Notes on Automating Daily Compliance Assessments

The scripts in this tool could be used as part of an automated process that assesses compliance for the entire GEO satellite population on a daily basis and appends results to a series of historical assessments. One implementation of such a concept takes the following steps:
1. Choose a date on which to begin historical assessments.
	* The study period for the author's doctoral thesis begins on January 1, 2010.
2. Produce a satellite catalog for all satellites that spent at least one day in the [IADC-defined GEO protected region](https://orbitaldebris.jsc.nasa.gov/library/iadc-space-debris-guidelines-revision-2.pdf) since the start date.
	* Save the satellite catalog in `./Data/Reference Files/satellitecatalog.csv` with the following columns:
		* International COSPAR number ('COSPAR');
		* NORAD ID with no leading zeros ('NORAD');
		* Name ('SATNAME');
		* The Space-Track.org abbreviation used to describe the satellite's operator ('COUNTRY'); and
		* Launch date, in `m/d/yy` format ('LAUNCH').
3. Develop a script that collates the most recent data from both single- and multi-date compliance assessments and stores them in a series of new documents (one per satellite in the satellite catalog).
	* Format this new document with rows and columns such that it matches the multi-date assessment results documents stored in `./Data/Historical Analysis/[Today's Date]/Historical Compliance Assessments/`.
	* Add two additional columns describing:
		* Whether the data was collected from a single- or multi-date compliance assessment ('Assessment Type'); and
		* The date on which the single- or multi-date compliance assessment was run ('Assessment Run Date').
	* When a compliance assessment for a satellite on a particular date is available in both the most-recent single-date run and the most-recent multi-date run, choose to referfence the multi-date result.
4. On a daily basis:
	1. Refresh the satellite catalog to ensure it is up to date with the newest GEO satellites.
	2. Run `./Code/snl.py`.
	3. Produce an input file in the single-date format with today's longitudinal data, ensuring all satellites in the satellite catalog are included.
		* When satellites are not in GEO during a particular evaluation date (either because they have yet to reach the geostationary belt or they have retired to a higher-altitude gragveyard orbit), use the 'n/a' symbol to describe their longitudinal position.
	4. Run `./Code/compliance_daily.py`.
	5. Run the new script developed in Step 3.
5. Every two weeks:
	1. Produce an input file in the multi-date format with longitudinal data for all satellites in the satellite catalog and all dates between the start date selected in Step 1 and today.
		* Use the 'n/a' symbol for missing longitudinal positions.
	2. Run `./Code/compliance_historical.py`

## Notes on Visualizing Compliance Assessment Data

The products from the ITU Compliance Assessment Monitor are well-suited for display on a web-based space object database.

On each GEO satellite's page of a web-based space object database, relevant information to display could be:
- Today's compliance assessment;
- Today's note;
	* The longest note is 334 characters and may be better suited in a tooltip.
- A chart displaying the satellite's historical compliance with two subplots:
	* The top subplot (the larger of the two) should display the satellite's longitudinal position overlaid on top of its corresponding ITU administation(s) regions of protections from harmful interference;
		* The data for the background charts can be derived from `./Data/SNL Downloads/[Today's Date]/networks_[Today's Date]`; please consult the author for details.
	* The bottom subplot should display a heatmap of historical compliance assessments.
		* Green for 'Yes', red for 'No', yellow for 'Maybe', and gray for 'n/a'.
	* These charts should begin at the satellite's launch and end on either its last day in the GEO region or today (whichever is earlier). 
- Today's shortlist of nearest neighbor networks.
	* The table can be miniaturized by removing some data; please consult the author for details. 
- A tool to display past shortslist of nearest neighbor networks.
- A link to a landing page on more information about the compliance asesesment tool, including its methodology and some key definitions. 
