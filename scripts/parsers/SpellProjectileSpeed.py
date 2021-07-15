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

# Variables to compute the Projectile Speed Mean, for fun =)
PrjSpeedRawValue = 0
PrjSpeedNbValue = 0

with open(os.path.join(generatedDir, 'SpellMisc.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    reader = sorted(reader, key=lambda d: int(d['id_parent']))
    current_id = 0
    ValidRows = []
    for row in reader:
        if float(row['proj_speed']) > 0 and current_id != int(row['id_parent']):
            current_id = int(row['id_parent'])
            ValidRows.append(row)
    with open(os.path.join(addonEnumDir, 'SpellProjectileSpeed.lua'), 'w', encoding='utf-8') as file:
        file.write('HeroDBC.DBC.SpellProjectileSpeed = {\n')
        for _, row in enumerate(ValidRows):
            prj_speed_int = int(float(row['proj_speed']))
            PrjSpeedRawValue += prj_speed_int
            PrjSpeedNbValue += 1
            file.write('  [' + row['id_parent'] + '] = ' + str(prj_speed_int) + ',\n')
        file.write('}\n')

# Fun print
print('Projectile Speed Mean : ' + str(PrjSpeedRawValue / PrjSpeedNbValue))
