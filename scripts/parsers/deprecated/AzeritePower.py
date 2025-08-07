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

# Load whitelisted specIds for some powerIds (from parser/AzeritePowerSpecsWhitelist.json)
with open(os.path.join(os.getcwd(), 'scripts', 'parsers', 'AzeritePowerSpecsWhitelist.json')) as specsWhitelistFile:
    specsWhitelist = json.load(specsWhitelistFile)

# Parse every csv files into dict
db = {}
dbFiles = ['AzeritePower', 'AzeritePowerSetMember', 'ItemSparse', 'AzeriteEmpoweredItem', 'SpellName',
           'AzeriteTierUnlock', 'SpecSetMember']
for dbFile in dbFiles:
    with open(os.path.join(generatedDir, f'{dbFile}.csv')) as csvfile:
        reader = csv.DictReader(csvfile, escapechar='\\')
        db[dbFile] = {}
        for row in reader:
            db[dbFile][row['id']] = row

# Add valid azerite power sets (i.e. if there is a corresponding item in game)
validAzeritePowerSets = {}
for entryId, entry in db['AzeriteEmpoweredItem'].items():
    if entry['id_item'] not in db['ItemSparse']:
        continue
    idPowerSet = entry['id_power_set']
    validAzeritePowerSets[idPowerSet] = entry
print(f'Found {len(validAzeritePowerSets)} valid azerite power sets out of {len(db["AzeriteEmpoweredItem"])} possible.')

# Add valid azerite powers
validAzeritePowers = {}
for entryId, entry in db['AzeritePowerSetMember'].items():
    idParent = entry['id_parent']
    if idParent not in validAzeritePowerSets:
        continue

    idPower = entry['id_power']
    if idPower not in db['AzeritePower']:
        continue

    power = db['AzeritePower'][idPower]
    powerIdSpell = power['id_spell']
    if powerIdSpell == '0':
        continue

    if powerIdSpell not in db['SpellName']:
        continue

    validAzeritePowers[idPower] = power
print(f'Found {len(validAzeritePowers)} valid azerite powers out of {len(db["AzeritePower"])} possible.')

azeritePowers = []
for powerId, data in validAzeritePowers.items():
    power = {
        'powerId': int(powerId),
        'spellId': int(data['id_spell']),
        'spellName': db['SpellName'][data['id_spell']]['name']
    }

    powerIdSpecSetMember = data['id_spec_set_member']
    # Retrieve the specs if the power is allowed only for some specs
    if powerIdSpecSetMember != '0':
        powerSpecs = []
        for entryId, entry in db['SpecSetMember'].items():
            if powerIdSpecSetMember == entry['id_parent']:
                powerSpecs.append(int(entry['id_spec']))
        if powerId in specsWhitelist:
            powerSpecs += specsWhitelist[powerId]
        power['specsId'] = powerSpecs

    # Retrieve the other infos by joining from AzeritePowerSetMember
    powerSets = []
    for entryId, entry in db['AzeritePowerSetMember'].items():
        if powerId == entry['id_power']:
            powerSet = {
                'classId': int(entry['class_id']),
                'tier': int(entry['tier']),
                'index': int(entry['index'])
            }

            # Get available items by joining on AzeriteEmpoweredItem
            entryIdParent = entry['id_parent']
            powerItems = []
            for entry2Id, entry2 in db['AzeriteEmpoweredItem'].items():
                if entryIdParent == entry2['id_power_set']:
                    powerItem = {
                        'itemId': int(entry2['id_item'])
                    }

                    # Get how tiers are unlocked per item by joining on AzeriteTierUnlocker
                    powerItemTiers = []
                    entry2IdAzeriteTierUnlock = entry2['id_azerite_tier_unlock']
                    for entry3Id, entry3 in db['AzeriteTierUnlock'].items():
                        if entry2IdAzeriteTierUnlock == entry3['id_parent']:
                            powerItemTier = {
                                'tier': int(entry3['tier']),
                                'azeriteLevel': int(entry3['azerite_level'])
                            }
                            powerItemTiers.append(powerItemTier)

                    powerItem['tiers'] = powerItemTiers
                    powerItems.append(powerItem)

            if len(powerItems) > 0:
                powerSet['items'] = powerItems
                powerSets.append(powerSet)

    power['sets'] = powerSets

    azeritePowers.append(power)

# Full output
with open(os.path.join(parsedDir, 'AzeritePowerWithItems.json'), 'w') as jsonFile:
    json.dump(azeritePowers, jsonFile, indent=4)

# Output a version without items infos
for power in azeritePowers:
    if power['sets']:
        powerClassesId = []

        # Get classes and tier from the powerSet
        for powerSet in power['sets']:
            classId = powerSet['classId']
            if classId not in powerClassesId:
                powerClassesId.append(classId)
            # AFAIK there can be only one tier, so we register the first valid we find
            if 'tier' in powerSet and 'tier' not in power:
                power['tier'] = powerSet['tier']
        power['classesId'] = sorted(powerClassesId)
        del power['sets']

with open(os.path.join(parsedDir, 'AzeritePower.json'), 'w') as jsonFile:
    json.dump(azeritePowers, jsonFile, indent=4)
