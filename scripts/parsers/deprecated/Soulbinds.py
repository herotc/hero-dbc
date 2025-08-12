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

os.chdir(os.path.join(os.path.dirname(sys.path[0]), '..', '..', 'hero-dbc'))

## Mapping
#Covenant.id = Soulbind.id_covenant
#Soulbind.id_garr_talent_tree = GarrTalent.id_garr_talent_tree
#GarrTalent.id = GarrTalentRank.id
#SpellName.id = GarrTalent.id_spell

db = {}
dbFiles = ['SpellName']
for dbFile in dbFiles:
    with open(os.path.join(generatedDir, f'{dbFile}.csv')) as csvfile:
        reader = csv.DictReader(csvfile, escapechar='\\')
        db[dbFile] = {}
        for row in reader:
            db[dbFile][row['id']] = row

# Get every covenants
Covenants = []
with open(os.path.join(generatedDir, 'Covenant.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    for row in reader:
        covenant = {
            'covenantId': int(row['id']),
            'covenantName': row['name'],
            'soulbinds': []
        }
        Covenants.append(covenant)

TreeSpell = {}
# Parse Soulbind tree spells
with open(os.path.join(generatedDir, 'GarrTalentRank.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    for row in reader:
        if int(row['id_spell']) > 0:
            TreeSpell[int(row['id_parent'])] = int(row['id_spell'])

with open(os.path.join(generatedDir, 'Soulbind.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    reader = sorted(reader, key=lambda d: int(d['id']))
    Soulbinds = []
    for row in reader:
        soulbind = {
            'soulbindId': int(row['id']),
            'soulbindName': row['name'],
            'soulbindTreeID': int(row['id_garr_talent_tree']),
            'soulbindTree': {}
        }

        # Get the soulbind tree
        with open(os.path.join(generatedDir, 'GarrTalent.csv')) as csvfile:
            reader = csv.DictReader(csvfile, escapechar='\\')
            reader = sorted(reader, key=lambda d: int(d['id']))
            for rowTalents in reader:
                if int(rowTalents['id_garr_talent_tree']) == int(row['id_garr_talent_tree']):
                    soulbindAbility = {
                        'soulbindAbilityId': int(rowTalents['id']),
                        'soulbindAbilityName': rowTalents['name']
                    }
                    # assign spell id
                    if int(rowTalents['id']) in TreeSpell:
                        soulbindAbility['soulbindAbilitySpellId'] = TreeSpell[int(rowTalents['id'])]
                        soulbindAbility['soulbindAbilityName'] = db['SpellName'][str(TreeSpell[int(rowTalents['id'])])]['name']
                    if int(rowTalents['conduit_type']) > 0:
                        soulbindAbility['soulbindAbilityConduitType'] = int(rowTalents['conduit_type'])
                    if int(rowTalents['id_garr_talent_prereq']) > 0:
                        soulbindAbility['soulbindAbilityPrereq'] = int(rowTalents['id_garr_talent_prereq'])
                    if not int(rowTalents['tier']) in soulbind['soulbindTree']:
                        soulbind['soulbindTree'][int(rowTalents['tier'])] = {}

                    soulbind['soulbindTree'][int(rowTalents['tier'])][int(rowTalents['ui_order'])] = soulbindAbility

        # Attach soulbind to covenant
        for index in range(len(Covenants)):
            if Covenants[index]['covenantId'] == int(row['id_covenant']):
                Covenants[index]['soulbinds'].append(soulbind)

# Full output
with open(os.path.join(parsedDir, 'Soulbinds.json'), 'w') as jsonFile:
    json.dump(Covenants, jsonFile, indent=4, sort_keys=True)