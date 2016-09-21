"""
Pull Toronto census data out of Ontario file to make processing faster
"""
import csv

toronto = []

with open('99-004-XWE2011001-401-ONT.csv', 'r', encoding='cp437') as f:
    reader = csv.DictReader(f)
    n = 0
    for row in reader:
        n += 1
        if row['Geo_Code'][:3] == '535':
            toronto.append(row)

with open('toronto_census.csv', 'w') as f:
    fieldnames = ['Geo_Code',
                  'Prov_Name',
                  'CMA_CA_Name',
                  'CT_Name',
                  'GNR',
                  'Topic',
                  'Characteristic',
                  'Note',
                  'Total',
                  'Flag_Total',
                  'Male',
                  'Flag_Male',
                  'Female',
                  'Flag_Female']
    writer = csv.DictWriter(f, fieldnames=fieldnames, restval=False)
    writer.writeheader()
    for district in toronto:
        writer.writerow(district)
