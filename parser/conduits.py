# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0301

"""
@author: Kutikuti
"""

import sys
import os
import csv
import json
from collections import OrderedDict

generatedDir = os.path.join('DBC', 'generated')
parsedDir = os.path.join('DBC', 'parsed')

os.chdir(os.path.join(os.path.dirname(sys.path[0]), '..', 'hero-dbc'))

## Mapping
#SoulbindConduitRank.id_spell = SpellName.id

# Parse every csv files into dict
db = {}
dbFiles = ['SpellName']
for dbFile in dbFiles:
    with open(os.path.join(generatedDir, f'{dbFile}.csv')) as csvfile:
        reader = csv.DictReader(csvfile, escapechar='\\')
        db[dbFile] = {}
        for row in reader:
            db[dbFile][int(row['id'])] = row

# Get every covenants
Conduits = []
with open(os.path.join(generatedDir, 'SoulbindConduitRank.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    current_id = 0
    for row in reader:
        if int(row['id_spell']) > 0 and current_id != int(row['id_parent']):
            current_id = int(row['id_parent'])

            conduit = {
                'conduitId': int(row['id_parent']),
                'conduitSpellID': int(row['id_spell'])
            }   

            if conduit['conduitSpellID'] not in db['SpellName']:
                continue
            
            conduit['conduitName'] = db['SpellName'][conduit['conduitSpellID']]['name']
            Conduits.append(conduit)
    

# json output
with open(os.path.join(parsedDir, 'Conduits.json'), 'w') as jsonFile:
    json.dump(Conduits, jsonFile, indent=4, sort_keys=True)

# lua output
""" with open(os.path.join(parsedDir, 'Conduits.lua'), 'w', encoding='utf-8') as file:
        file.write('MoreTooltipInfo.Enum.Conduits = {\n')
        iMax = len(ValidRows) - 1
        for i, row in enumerate(ValidRows):
            if i == iMax:
                file.write('  [' + row['id_parent'] + '][] = ' + row['id_spell'] + '\n')
            else:
                file.write('  [' + row['id_parent'] + '][] = ' + row['id_spell'] + ',\n')
        file.write('}\n') """