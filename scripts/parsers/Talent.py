# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0301

"""
@author: Quentin Giraud <dev@aethys.io>
"""

import sys
import os
import csv
import json

generatedDir = os.path.join('scripts', 'DBC', 'generated')
parsedDir = os.path.join('scripts', 'DBC', 'parsed')

os.chdir(os.path.join(os.path.dirname(sys.path[0]), '..', '..', 'hero-dbc'))

# Parse every csv files into dict
db = {}
dbFiles = ['Talent', 'SpellName']
for dbFile in dbFiles:
    with open(os.path.join(generatedDir, f'{dbFile}.csv')) as csvfile:
        reader = csv.DictReader(csvfile, escapechar='\\')
        db[dbFile] = {}
        for row in reader:
            db[dbFile][row['id']] = row

talents = {}
for entryId, entry in db['Talent'].items():
    classId = entry['class_id']
    if classId not in talents:
        talents[classId] = {}
    specId = entry['spec_id']
    if specId not in talents[classId]:
        talents[classId][specId] = {}
    row = entry['row']
    if row not in talents[classId][specId]:
        talents[classId][specId][row] = {}
    spellId = entry['id_spell']
    talents[classId][specId][row][entry['col']] = {
        'talentId': int(entry['id']),
        'spellId': int(spellId),
        'spellName': db['SpellName'][spellId]['name']
    }

# Full output
with open(os.path.join(parsedDir, 'Talent.json'), 'w') as jsonFile:
    json.dump(talents, jsonFile, indent=4, sort_keys=True)
