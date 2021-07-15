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

with open(os.path.join(generatedDir, 'SpellCooldowns.csv')) as csvfile:
    reader = list(csv.DictReader(csvfile, escapechar='\\'))
    reader = sorted(reader, key=lambda d: int(d['id_parent']))
    with open(os.path.join(addonEnumDir, 'SpellGCD.lua'), 'w', encoding='utf-8') as file:
        file.write('HeroDBC.DBC.SpellGCD = {\n')
        for _, row in enumerate(reader):
            if int(row['id_parent']) > 0:
                file.write('  [' + row['id_parent'] + '] = ' + row['gcd_cooldown'] + ',\n')
        file.write('}\n')
