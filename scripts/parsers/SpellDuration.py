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
# id_parent & proj_speed from SpellMisc

Durations = {}
with open(os.path.join(generatedDir, 'SpellDuration.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    for row in reader:
        if int(row['duration_1']) > 0:
            Durations[row['id']] = {}
            Durations[row['id']][1] = row['duration_1']
            Durations[row['id']][2] = row['duration_2']

with open(os.path.join(generatedDir, 'SpellMisc.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    reader = sorted(reader, key=lambda d: int(d['id_parent']))
    current_id = 0
    ValidRows = []
    for row in reader:
        if int(row['id_duration']) > 0 and row['id_duration'] in Durations and current_id != int(row['id_parent']):
            current_id = int(row['id_parent'])
            ValidRows.append(row)
    with open(os.path.join(addonEnumDir, 'SpellDuration.lua'), 'w', encoding='utf-8') as file:
        file.write('HeroDBC.DBC.SpellDuration = {\n')
        for _, row in enumerate(ValidRows):
            baseDuration = int(Durations[row['id_duration']][1])
            pandemic = int(float(Durations[row['id_duration']][1]) * 0.3)
            maxDuration = baseDuration + pandemic
            file.write('  [' + row['id_parent'] + '] = {' + Durations[row['id_duration']][1] + ', ' + str(
                int(maxDuration)) + '},\n')
        file.write('}\n')
