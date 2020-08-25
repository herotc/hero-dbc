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

# Parse every csv files into dict
db = {}
dbFiles = ['SpecSetMember']
for dbFile in dbFiles:
    with open(os.path.join(generatedDir, f'{dbFile}.csv')) as csvfile:
        reader = csv.DictReader(csvfile, escapechar='\\')
        db[dbFile] = {}
        for row in reader:
            db[dbFile][row['id']] = row

Legendaries = []
# Parse Soulbind tree spells
with open(os.path.join(generatedDir, 'RuneforgeLegendaryAbility.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    for row in reader:
        legendary = {
            'legendaryId': int(row['id']),
            'legendaryName': row['name'],
            'legendarySpellID': int(row['id_spell']),
            'legendaryBonusID': int(row['id_bonus']),        }
        powerIdSpecSetMember = row['id_spec_set']
        # Retrieve the specs if the power is allowed only for some specs
        if powerIdSpecSetMember != '0':
            powerSpecs = []
            for entryId, entry in db['SpecSetMember'].items():
                if powerIdSpecSetMember == entry['id_parent']:
                    powerSpecs.append(int(entry['id_spec']))
            legendary['specs'] = powerSpecs
        Legendaries.append(legendary)

# Full output
with open(os.path.join(parsedDir, 'Legendaries.json'), 'w') as jsonFile:
    json.dump(Legendaries, jsonFile, indent=4, sort_keys=True)