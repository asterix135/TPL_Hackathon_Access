# TPL Hackathon Challenge 1

## Data Analysis to attempt to understand how well the TPL is serving needy communities

### Data Sources:
- Library data from http://opendata.tplcs.ca
- NHS Data from: https://www12.statcan.gc.ca/nhs-enm/2011/dp-pd/prof/details/download-telecharger/comprehensive/comp-csv-tab-nhs-enm.cfm?Lang=E
- Census information from: https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/prof/details/download-telecharger/comprehensive/comp-csv-tab-dwnld-tlchrgr.cfm?Lang=E#tabs2011

### Code
- summarize_branches.py - amalgamates all the TPL branch data into one file
- census_extract.py - extracts only City of Toronto information from broader
2011 National Household Survey Census Data (for faster processing down the line)
- branch_census.py - attributes demographic data to branch based on census tract values
for branch catchment area
