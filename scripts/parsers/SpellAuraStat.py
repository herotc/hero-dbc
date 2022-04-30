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
addonEnumDir = os.path.join('HeroDBC', 'DBC')

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
                # Attribute (29)
                # Modify Total Stat% (137)
                # Modify Rating (189) with misc values mapping to stats
                # Modify All Haste% (193)
                # Modify Critical Strike% (290)
                # Modify Mastery% (318)
                # Modify Versatility% (471)
                if (int(row['sub_type']) == 29 or
                    int(row['sub_type']) == 137 or
                    int(row['sub_type']) == 193 or
                    int(row['sub_type']) == 290 or
                    int(row['sub_type']) == 318 or
                    int(row['sub_type']) == 471 or
                    int(row['sub_type']) == 189 and (int(row['misc_value_1']) == 1792 or int(row['misc_value_1']) == 917504 or int(row['misc_value_1']) == 33554432 or int(row['misc_value_1']) == 1879048192)):
                    file.write('  [' + row['id_parent'] + '] = true,\n')
                else:
                    file.write('  [' + row['id_parent'] + '] = false,\n')
        file.write('}\n')
