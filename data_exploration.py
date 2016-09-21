"""
Exploratory Data Analysis
"""

import pandas as pd
import matplotlib.pyplot as plt

branches = pd.read_csv('Branches_with_demographics.csv')
# remove reference library because it's not a normal branch
branches = branches[branches.ID != 'TRL']

plt.scatter(branches['Workstations'], branches['WS_Users_2015'])
plt.show()

plt.scatter(branches['visits_2015'], branches['WS_Users_2015'])
plt.show()

plt.scatter(branches['low_income'], branches['WS_Users_2015'])

plt.show()