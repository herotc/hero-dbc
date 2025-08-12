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

ItemBitMask = [
    {'mask':2, 'slot':'Head'}, 
    {'mask':4, 'slot':'Neck'},
    {'mask':8, 'slot':'Shoulder'}, 
    {'mask':16, 'slot':'Body'}, 
    {'mask':32, 'slot':'Chest'}, 
    {'mask':64, 'slot':'Waist'}, 
    {'mask':128, 'slot':'Legs'},
    {'mask':256, 'slot':'Feet'}, 
    {'mask':512, 'slot':'Wrist'}, 
    {'mask':1024, 'slot':'Hands'},
    {'mask':2048, 'slot':'Finger'}, 
    {'mask':4096, 'slot':'Trinket'}, 
    {'mask':8192, 'slot':'One-Hand'}, 
    {'mask':16384, 'slot':'Off Hand'}, 
    {'mask':32768, 'slot':'Ranged'}, 
    {'mask':65536, 'slot':'Back'}, 
    {'mask':1048576, 'slot':'Robe'}
]

# Parse every csv files into dict
db = {}
dbFiles = ['SpecSetMember','Covenant']
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
    reader = sorted(reader, key=lambda d: int(d['id']))
    for row in reader:
        legendary = {
            'legendaryId': int(row['id']),
            'legendaryName': row['name'],
            'legendarySpellID': int(row['id_spell']),
            'legendaryBonusID': int(row['id_bonus']),
        }

        # Retrieve the items it applies to
        legendarySlot = []
        currentMask = int(row['mask_inv_type']) 
        for i in reversed(ItemBitMask):
            if currentMask / i['mask'] >= 1:
                currentMask = currentMask - i['mask']
                legendarySlot.append(i['slot'])
        legendary['itemSlot'] = legendarySlot

        # Retrieve the specs if the power is allowed only for some specs
        powerIdSpecSetMember = row['id_spec_set']
        if powerIdSpecSetMember != '0':
            powerSpecs = []
            for entryId, entry in db['SpecSetMember'].items():
                if powerIdSpecSetMember == entry['id_parent']:
                    powerSpecs.append(int(entry['id_spec']))
            legendary['specs'] = powerSpecs

        # Retrieve the covenant if the power is allowed only for some covenant
        covenantId = row['id_covenant']
        if covenantId != '0':
            legendary['covenant'] = db['Covenant'][covenantId]['name']

        Legendaries.append(legendary)

# Full output
with open(os.path.join(parsedDir, 'Legendaries.json'), 'w') as jsonFile:
    json.dump(Legendaries, jsonFile, indent=4, sort_keys=True)

# LUA output
with open(os.path.join(parsedDir, 'Legendaries.lua'), 'w', encoding='utf-8') as file:
    for _, row in enumerate(Legendaries):
        file.write('-- ' + str(row['legendaryId']) + ', ' + str(row['legendaryBonusID']) + ', ' + row['legendaryName'] + '\n')