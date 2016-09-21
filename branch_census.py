"""
Summarize Census data per branch and update amalgamated branch info
"""

import csv


def import_values(census_dict):
    """
    Checks to see if census data is something we're looking for
    :param census_dict - line from NHS in dict form
    :returns Boolean, characteristic v
    """
    ok_topics = {
        'Citizenship': [
            'Total population in private households by citizenship',
            'Canadian citizens',
            'Not Canadian citizens'
        ],
        'Recent immigrants by selected place of birth': [
            'Total recent immigrant population in private households by selected places of birth'
        ],
        'Visible minority population': [
            'Total visible minority population'
        ],
        'Non-official languages spoken': [
            'Total population in private households by non-official languages spoken'
        ],
        'Labour force status': [
            'In the labour force',
            'Employed',
            'Unemployed',
            'Not in the labour force'
        ],
        'Shelter costs': [
            '% of tenant households in subsidized housing'
        ],
        'Income of individuals in 2010': [
            'In low income in 2010 based on after-tax low-income measure (LIM-AT)'
        ]
    }
    topic = census_dict['Topic'].strip()
    characteristic = census_dict['Characteristic'].strip()
    if topic in ok_topics and characteristic in ok_topics[topic]:
        try:
            char_value = float(census_dict['Total'])
        except ValueError:
            char_value = 0
        return True, characteristic, char_value
    else:
        return False, characteristic, census_dict['Total']


# import branch info to dict
branches = {}
with open('Branches_amalgamated.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        branches[row['ID']] = row

# create list per branch with census tract(s)
with open('Branch_Census_Tracts.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['ID'] not in branches:
            pass
        elif 'census_tract' not in branches[row['ID']]:
            branches[row['ID']]['census_tract'] = [float(row['Census Tract'])]
        else:
            branches[row['ID']]['census_tract'].append(float(row['Census Tract']))

# import Toronto Census Data
census_data = {}
with open('toronto_census.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        ok_to_import, charateristic, characteristic_value = import_values(row)
        if ok_to_import:
            if float(row['CT_Name']) not in census_data:
                census_data[float(row['CT_Name'])] = \
                    {charateristic: characteristic_value}
            else:
                census_data[float(row['CT_Name'])][charateristic] = \
                    characteristic_value

# Import total census population data
with open('98-316-XWE2011001-401.CSV', 'r', encoding='cp437') as f:
    reader = csv.DictReader(f)
    for row in reader:

        try:
            total_val = float(row['Total'])
        except ValueError:
            total_val = 0

        if row['Geo_Code'].strip()[:3] == '535':
            if row['Characteristic'].strip() == 'Population in 2011':
                if float(row['CT_Name']) not in census_data:
                    census_data[float(row['CT_Name'])] = \
                        {'Census_Population': total_val,
                         'Total population in private households by citizenship': 0,
                         'Canadian citizens': 0,
                         'Not Canadian citizens': 0,
                         'Total recent immigrant population in private households by selected places of birth': 0,
                         'Total visible minority population': 0,
                         'Total population in private households by non-official languages spoken': 0,
                         'In the labour force': 0,
                         'Employed': 0,
                         'Unemployed': 0,
                         'Not in the labour force': 0,
                         'In low income in 2010 based on after-tax low-income measure (LIM-AT)': 0}
                else:
                    census_data[float(row['CT_Name'])]['Census_Population'] = total_val

# calculate various measures of need
no_tract_branches = []
for branch in branches:
    if 'census_tract' not in branches[branch]:
        no_tract_branches.append(branches[branch]['ID'])
    else:
        demographics = {
            'census_population': 0.0,
            'NPS_population': 0.0,
            'citizens': 0.0,
            'non_citizens': 0.0,
            'recent_immigrants': 0.0,
            'visible_minority': 0.0,
            'non_official_languages': 0.0,
            'in_labour_force': 0.0,
            'employed': 0.0,
            'unemployed': 0.0,
            'not_in_labour_force': 0.0,
            'low_income': 0.0
        }
        for census_tract in branches[branch]['census_tract']:
            if census_tract in census_data:
                demographics['census_population'] += census_data[census_tract]\
                    ['Census_Population']
                demographics['NPS_population'] += census_data[census_tract]\
                    ['Total population in private households by citizenship']
                demographics['citizens'] += census_data[census_tract]\
                    ['Canadian citizens']
                demographics['non_citizens'] += census_data[census_tract] \
                    ['Not Canadian citizens']
                demographics['recent_immigrants'] += census_data[census_tract] \
                    ['Total recent immigrant population in private households by selected places of birth']
                demographics['visible_minority'] += census_data[census_tract] \
                    ['Total visible minority population']
                demographics['non_official_languages'] += census_data[census_tract] \
                    ['Total population in private households by non-official languages spoken']
                demographics['in_labour_force'] += census_data[census_tract] \
                    ['In the labour force']
                demographics['employed'] += census_data[census_tract] \
                    ['Employed']
                demographics['unemployed'] += census_data[census_tract] \
                    ['Unemployed']
                demographics['not_in_labour_force'] += census_data[census_tract] \
                    ['Not in the labour force']
                demographics['low_income'] += census_data[census_tract] \
                    ['In low income in 2010 based on after-tax low-income measure (LIM-AT)']
        branches[branch]['census_population'] = demographics['census_population']
        branches[branch]['NPS_population'] = demographics['NPS_population']
        branches[branch]['citizens'] = demographics['citizens']
        branches[branch]['non_citizens'] = demographics['non_citizens']
        branches[branch]['recent_immigrants'] = demographics['recent_immigrants']
        branches[branch]['visible_minority'] = demographics['visible_minority']
        branches[branch]['non_official_languages'] = demographics['non_official_languages']
        branches[branch]['in_labour_force'] = demographics['in_labour_force']
        branches[branch]['employed'] = demographics['employed']
        branches[branch]['unemployed'] = demographics['unemployed']
        branches[branch]['not_in_labour_force'] = demographics['not_in_labour_force']
        branches[branch]['low_income'] = demographics['low_income']

with open('Branches_with_demographics.csv', 'w') as f:
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
                  'Youth_Hub',
                  'census_population',
                  'NPS_population',
                  'citizens',
                  'non_citizens',
                  'recent_immigrants',
                  'visible_minority',
                  'non_official_languages',
                  'in_labour_force',
                  'employed',
                  'unemployed',
                  'not_in_labour_force',
                  'low_income'
                  ]
    writer = csv.DictWriter(f, fieldnames=fieldnames, restval=False,
                            extrasaction='ignore')
    writer.writeheader()
    for branch in branches:
        writer.writerow(branches[branch])


"""
Useful codes:
    Topic - Characteristic
Citizenship
    Total population in private households by citizenship (this is total pop)
    Canadian citizens
    Not Canadian citizens
Recent immigrants by selected place of birth
    Recent immigrants by selected place of birth
Visible minority population
    Total visible minority population
Non-official languages spoken
    Total population in private households by non-official languages spoken
Labour force status
    In the labour force
    Employed
    Unemployed
    Not in the labour force
Shelter costs
    % of tenant households in subsidized housing
Income of individuals in 2010
    Median family income ($)  ## need to look at
    Average family income ($)  ## need to look at
    In low income in 2010 based on after-tax low-income measure (LIM-AT)
"""