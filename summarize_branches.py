"""
Create one file combining info from all branch data sheets (except census)
"""

import csv

branches = {}

with open('Branch_General_Profile.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        branches[row['ID']] = row

with open('Catchment_Population.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        branches[row['ID']]['Population'] = row['2011']

# Note - no 'Comp_Learn_Ctr' key if not in file (not set as False)
with open('Computer_Learning_Centres.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        branches[row['ID']]['Comp_Learn_Ctr'] = True

# same comment as for as previous file
with open('Digital_Innovation_Hubs.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        branches[row['ID']]['Dig_Innov_Hubs'] = True

# same comment as for previous
with open('Neighbourhood_Improvement_Area_Branches.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        branches[row['ID']]['NIA'] = True if row['TSNS 2020 NIA'] == \
                                             'Yes' else False
        branches[row['ID']]['NIA_Branch'] = True if \
            row ['TSNS 2020 Branch'] == 'Yes' else False

with open('Programs_by_Type.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        for col in row:
            if col not in ['ID', 'Branch Name', 'Tier']:
                try:
                    branches[row['ID']][col] = row[col]
                except KeyError:
                    pass

with open('Workstation.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        branches[row['ID']]['Workstations'] = row['2015']

with open('Workstation_Users.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            branches[row['ID']]["WS_Users_2015"] = row['2015']
            branches[row['ID']]['WS_Users_2014'] = row['2014']
            branches[row['ID']]['WS_Users_2013'] = row['2013']
        except KeyError:
            pass

with open('Youth_Hubs_Locations.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            branches[row['ID']]['Youth_Hub'] = True
        except KeyError:
            pass

with open('Annual_visits.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['ID'] in branches:
            branches[row['ID']]['visits_2015'] = row['2015']
            branches[row['ID']]['visits_2014'] = row['2014']
            branches[row['ID']]['visits_2013'] = row['2013']

with open('Circulation.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['ID'] in branches:
            branches[row['ID']]['circulation_2015'] = row['2015']
            branches[row['ID']]['circulation_2014'] = row['2014']
            branches[row['ID']]['circulation_2013'] = row['2013']

with open('Collection_size.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['ID'] in branches:
            branches[row['ID']]['collection_size'] = row['2015']

with open('Branches_amalgamated.csv', 'w') as f:
    fieldnames = ['ID',
                  'Branch Name',
                  'Tier',
                  'Address',
                  'Telephone ',
                  'Postal Code',
                  'FSA',
                  'NBHD Number',
                  'NBHD Name',
                  'Ward Number',
                  'Ward Region',
                  'Population',
                  'Comp_Learn_Ctr',
                  'Dig_Innov_Hubs',
                  'NIA',
                  'NIA_Branch',
                  'Programs_Cultural_2015',
                  'Attendance_Cultural_2015',
                  'Programs_ESL_2015',
                  'Attendance_ESL_2015',
                  'Program_Info_Current_Issues_2015',
                  'Attendance_Info_Current_Issues_2015',
                  'Programs_Literacy_2015',
                  'Attendance_Literacy_2015',
                  'Programs_Literary_2015',
                  'Attendance_Literary_2015',
                  'Programs_User_Ed_2015',
                  'Attendance_User_Ed_2015',
                  'Programs_Cultural_2014',
                  'Attendance_Cultural_2014',
                  'Programs_ESL_2014',
                  'Attendance_ESL_2014',
                  'Programs_Info_Current_Issues_2014',
                  'Attendance_Info_Current_Issues_2014',
                  'Programs_Literacy_2014',
                  'Attendance_Literacy_2014',
                  'Programs_Literary_2014',
                  'Attendance_Literary_2014',
                  'Programs_User_Ed_2014',
                  'Attendance_User_Ed_2014',
                  'Workstations',
                  'WS_Users_2015',
                  'WS_Users_2014',
                  'WS_Users_2013',
                  'visits_2015',
                  'visits_2014',
                  'visits_2013',
                  'circulation_2015',
                  'circulation_2014',
                  'circulation_2013',
                  'collection_size',
                  'Youth_Hub']
    writer = csv.DictWriter(f, fieldnames=fieldnames, restval=False)
    writer.writeheader()
    for branch in branches:
        writer.writerow(branches[branch])
