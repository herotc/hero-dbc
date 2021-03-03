# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0301

"""
@author: Kutikuti
"""

import sys
import os
import csv

#List all spell that triggers an aura
#true if the aura gives 'dps' stat (simc has_stat.any_dps)
#flase if the aura gives tertiary stat or something else (simc has_stat.any)

generatedDir = os.path.join('scripts', 'DBC', 'generated')
addonEnumDir = os.path.join('addon', 'DBC')

os.chdir(os.path.join(os.path.dirname(sys.path[0]), '..', '..', 'hero-dbc'))

with open(os.path.join(generatedDir, 'SpellEffect.csv')) as csvfile:
    reader = list(csv.DictReader(csvfile, escapechar='\\'))
    reader = sorted(reader, key=lambda d: int(d['id_parent']))
    with open(os.path.join(addonEnumDir, 'SpellAuraStat.lua'), 'w', encoding='utf-8') as file:
        file.write('HeroDBC.DBC.SpellAuraStat = {\n')
        current = 0
        for _, row in enumerate(reader):
            if int(row['id_parent']) > 0 and current != int(row['id_parent']) and int(row['type']) == 6:
                current = int(row['id_parent'])
                if int(row['sub_type']) == 29:
                    file.write('  [' + row['id_parent'] + '] = true,\n')
                else:
                    file.write('  [' + row['id_parent'] + '] = false,\n')
        file.write('}\n')
