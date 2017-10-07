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

# Variables to compute the Projectile Speed Mean, for fun =)
PrjSpeedRawValue = 0
PrjSpeedNbValue = 0

with open(os.path.join(generatedDir, 'SpellMisc.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    ValidRows = []
    for row in reader:
        if float(row['proj_speed']) > 0 and row['id'] in Spells:
            ValidRows.append(row)
    with open(os.path.join(parsedDir, 'ProjectileSpeed.lua'), 'w', encoding='utf-8') as file:
        file.write('AethysCore.Enum.ProjectileSpeed = {\n')
        iMax = len(ValidRows)-1
        for i, row in enumerate(ValidRows):
            prj_speed_int = int(float(row['proj_speed']))
            PrjSpeedRawValue += prj_speed_int
            PrjSpeedNbValue += 1
            if i == iMax:
                file.write('  [' + Spells[row['id']] + '] = ' + str(prj_speed_int) + '\n')
            else:
                file.write('  [' + Spells[row['id']] + '] = ' + str(prj_speed_int) + ',\n')
        file.write('}\n')

# Fun print
print('Projectile Speed Mean : ' + str(PrjSpeedRawValue/PrjSpeedNbValue))
