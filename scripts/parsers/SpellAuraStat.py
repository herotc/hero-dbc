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
    # group by id_parent
    effects_by_parent = {}
    for row in reader:
        parent_id = int(row['id_parent'])
        if parent_id > 0 and int(row['type']) == 6:
            effects_by_parent.setdefault(parent_id, []).append(row)
            
    # iterate through effects_by_parent and check for wanted sub-types
    with open(os.path.join(addonEnumDir, 'SpellAuraStat.lua'), 'w', encoding='utf-8') as file:
        file.write('HeroDBC.DBC.SpellAuraStat = {\n')
        for parent_id, rows in sorted(effects_by_parent.items()):
            match_found = False
            for row in rows:
                subtype = int(row['sub_type'])
                if (subtype in (29, 137, 193, 290, 318, 471) or
                    (subtype == 189 and int(row['misc_value_1']) in (1792, 917504, 33554432, 1879048192))):
                    match_found = True
                    break
            file.write(f'  [{parent_id}] = {"true" if match_found else "false"},\n')
        file.write('}\n')
