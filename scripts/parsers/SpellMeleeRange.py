# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0301

"""
@author: Quentin Giraud <dev@aethys.io>
"""

import sys
import os
import csv

generatedDir = os.path.join('scripts', 'DBC', 'generated')
addonEnumDir = os.path.join('HeroDBC', 'DBC')

os.chdir(os.path.join(os.path.dirname(sys.path[0]), '..', '..', 'hero-dbc'))

## Mapping
# id_misc & proj_speed from SpellMisc

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
            Ranges[row['id']] = [str(int(min_range)), str(int(max_range)), int(row['flag'])]

with open(os.path.join(generatedDir, 'SpellMisc.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    reader = sorted(reader, key=lambda d: int(d['id_parent']))
    current_id = 0
    ValidRows = []
    for row in reader:
        if row['id_range'] in Ranges and current_id != int(row['id_parent']):
            current_id = int(row['id_parent'])
            ValidRows.append(row)
    with open(os.path.join(addonEnumDir, 'SpellMeleeRange.lua'), 'w', encoding='utf-8') as file:
        file.write('-- { [SpellID] = { [1] = IsMelee, [2] = MinRange, [3] = MaxRange } }\n')
        file.write('HeroDBC.DBC.SpellMeleeRange = {\n')
        for _, row in enumerate(ValidRows):
            file.write('  [' + row['id_parent'] + '] = { ' + (
                'true' if Ranges[row['id_range']][2] == 1 else 'false') + ', ' + Ranges[row['id_range']][0] + ', ' +
                        Ranges[row['id_range']][1] + ' },\n')
        file.write('}\n')
