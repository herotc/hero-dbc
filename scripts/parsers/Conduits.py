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

generatedDir = os.path.join('scripts', 'DBC', 'generated')
parsedDir = os.path.join('scripts', 'DBC', 'parsed')
addonEnumDir = os.path.join('HeroDBC', 'DBC')

os.chdir(os.path.join(os.path.dirname(sys.path[0]), '..', '..', 'hero-dbc'))

## Mapping
#SoulbindConduitRank.id_spell = SpellName.id
#SoulbindConduitRank.id_parent = SoulbindConduit.id
#SoulbindConduit.id_spec_set = SpecSetMember.id_parent

# Parse every csv files into dict
db = {}
dbFiles = ['SpecSetMember','SpellName']
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
    reader = sorted(reader, key=lambda d: int(d['id_parent']))
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

# Get conduits specs
for conduit in Conduits:  
    with open(os.path.join(generatedDir, 'SoulbindConduit.csv')) as csvfile:
        reader = csv.DictReader(csvfile, escapechar='\\')
        for row in reader:
            if int(row['id']) == conduit['conduitId']:
                powerIdSpecSetMember = row['id_spec_set']
                if powerIdSpecSetMember != '0':
                    powerSpecs = []
                    for entryId, entry in db['SpecSetMember'].items():
                        if powerIdSpecSetMember == entry['id_parent']:
                            powerSpecs.append(int(entry['id_spec']))
                    conduit['specs'] = powerSpecs
                    conduit['conduitType'] = int(row['type'])

# json output
with open(os.path.join(parsedDir, 'Conduits.json'), 'w') as jsonFile:
    json.dump(Conduits, jsonFile, indent=4, sort_keys=True)

# lua output
with open(os.path.join(addonEnumDir, 'SpellConduits.lua'), 'w', encoding='utf-8') as file:
    file.write('HeroDBC.DBC.SpellConduits = {\n')
    for conduit in Conduits:
        file.write('  [' + str(conduit['conduitId']) + '] = ' + str(conduit['conduitSpellID']) + ',\n')
    file.write('}\n')
