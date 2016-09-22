"""
Exploratory Data Analysis
"""

import pandas as pd
from sklearn.linear_model import LinearRegression

branches = pd.read_csv('Branches_with_demographics.csv')
# remove reference library because it's not a normal branch
branches = branches[branches.ID != 'TRL']

# convert text columns to floats
numeric_columns = ['Programs_Cultural_2015', 'Attendance_Cultural_2015',
                   'Programs_ESL_2015', 'Attendance_ESL_2015',
                   'Program_Info_Current_Issues_2015',
                   'Attendance_Info_Current_Issues_2015',
                   'Programs_Literacy_2015', 'Attendance_Literacy_2015',
                   'Programs_Literary_2015', 'Attendance_Literary_2015',
                   'Programs_User_Ed_2015', 'Attendance_User_Ed_2015',
                   'Programs_Cultural_2014', 'Attendance_Cultural_2014',
                   'Programs_ESL_2014', 'Attendance_ESL_2014',
                   'Programs_Info_Current_Issues_2014',
                   'Attendance_Info_Current_Issues_2014',
                   'Programs_Literacy_2014', 'Attendance_Literacy_2014',
                   'Programs_Literary_2014', 'Attendance_Literary_2014',
                   'Programs_User_Ed_2014', 'Attendance_User_Ed_2014',
                   'Workstations', 'WS_Users_2015', 'WS_Users_2014',
                   'WS_Users_2013', 'visits_2015', 'visits_2014', 'visits_2013',
                   'circulation_2015', 'circulation_2014', 'circulation_2013',
                   'collection_size', 'census_population', 'NPS_population',
                   'citizens', 'non_citizens', 'recent_immigrants',
                   'visible_minority', 'non_official_languages',
                   'in_labour_force', 'employed', 'unemployed',
                   'not_in_labour_force', 'low_income']
for col in numeric_columns:
    if branches[col].dtype == 'O':
        branches[col] = branches[col].astype('float')

# Calculate a couple of values
branches['sessions_per_ws'] = branches['WS_Users_2015'] / \
                              branches['Workstations']
branches['pct_low_income'] = branches['low_income'] / \
                             branches['census_population']
branches['ws_use_per_visit'] = branches['WS_Users_2015'] / \
                               branches['visits_2015']
branches['pct_recent_immigrants'] = branches['recent_immigrants'] / \
                                    branches['census_population']
branches['pct_vis_minority'] = branches['visible_minority'] / \
                               branches['census_population']
branches['pct_labor_force_unemployed'] = branches['unemployed'] / \
                                         branches['in_labour_force']
branches['pct_not_in_labour_force'] = branches['not_in_labour_force'] / \
                                      branches['census_population']


mod1 = LinearRegression()
mod1.fit(branches[['pct_low_income', 'Workstations', 'collection_size',
                   'visits_2015', ]])


