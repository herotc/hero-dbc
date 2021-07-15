# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0301

"""
@author: Kutikuti
"""

import sys
import os
import csv

generatedDir = os.path.join('scripts', 'DBC', 'generated')
addonEnumDir = os.path.join('HeroDBC', 'DBC')

os.chdir(os.path.join(os.path.dirname(sys.path[0]), '..', '..', 'hero-dbc'))

with open(os.path.join(generatedDir, 'SpellEffect.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    reader = sorted(reader, key=lambda d: int(d['id_parent']))
    current_id = 0
    ValidRows = []
    for row in reader:
        if not int(row['amplitude']) == 0 and current_id != int(row['id_parent']):
            current_id = int(row['id_parent'])
            ValidRows.append(row)
    with open(os.path.join(addonEnumDir, 'SpellTickTime.lua'), 'w', encoding='utf-8') as file:
        file.write('HeroDBC.DBC.SpellTickTime = {\n')
        for _, row in enumerate(ValidRows):
            file.write('  [' + row['id_parent'] + '] = { ' + str(int(row['amplitude'])) + ', ' + (
                'false' if row['id_mechanic'] == "15" else 'true') + ' },\n')
        file.write('}\n')
