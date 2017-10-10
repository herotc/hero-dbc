# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0301

"""
@author: Aethys256
"""

import sys
import os
import csv

generatedDir = os.path.join('DBC', 'generated')
parsedDir = os.path.join('DBC', 'parsed')

os.chdir(os.path.join(os.path.dirname(sys.path[0]), 'AethysDBC'))

## Mapping
# id_spell & id_misc from Spell
# id_misc & proj_speed from SpellMisc

# Get every misc id associated to every spell id
Spells = {}
with open(os.path.join(generatedDir, 'Spell.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    for row in reader:
        Spells[row['id_misc']] = row['id']
# Get every 'valid' ranges for our parser.
# We ignore the '_2' ranges (friendly) and only considers the '_1' ones (hostile)
# We also considers only the range with the flag '1' that identify them as melee.
Ranges = {}
with open(os.path.join(generatedDir, 'SpellRange.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    for row in reader:
        # Every ranges are 6 digits float
        min_range = float(row['min_range_1'])
        max_range = float(row['max_range_1'])
        if max_range > 0 and max_range <= 100:
            Ranges[row['id']] = [str(int(min_range)), str(int(max_range)), int(row['flags'])]

with open(os.path.join(generatedDir, 'SpellMisc.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    ValidRows = []
    for row in reader:
        if row['id'] in Spells and row['id_range'] in Ranges:
            ValidRows.append(row)
    with open(os.path.join(parsedDir, 'SpellMeleeRange.lua'), 'w', encoding='utf-8') as file:
        file.write('AethysCore.Enum.SpellMeleeRange = {\n')
        iMax = len(ValidRows)-1
        for i, row in enumerate(ValidRows):
            if i == iMax:
                file.write('  [' + Spells[row['id']] + '] = {' + ('true' if Ranges[row['id_range']][2] == 1 else 'false') + ', ' + Ranges[row['id_range']][0] + ', ' + Ranges[row['id_range']][1] +'}\n')
            else:
                file.write('  [' + Spells[row['id']] + '] = {' + ('true' if Ranges[row['id_range']][2] == 1 else 'false') + ', ' + Ranges[row['id_range']][0] + ', ' + Ranges[row['id_range']][1] +'},\n')
        file.write('}\n')
