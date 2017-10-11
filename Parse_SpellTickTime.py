# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0301

"""
@author: Kutikuti
"""

import sys
import os
import csv

generatedDir = os.path.join('DBC', 'generated')
parsedDir = os.path.join('DBC', 'parsed')

os.chdir(os.path.join(os.path.dirname(sys.path[0]), 'AethysDBC'))

with open(os.path.join(generatedDir, 'SpellEffect.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    ValidRows = []
    for row in reader:
        if not row['amplitude'] == '0' and not row['sp_coefficient'] == '0':
            ValidRows.append(row)
    with open(os.path.join(parsedDir, 'TickTime.lua'), 'w', encoding='utf-8') as file:
        file.write('AethysCore.Enum.TickTime = {\n')
        iMax = len(ValidRows)-1
        for i, row in enumerate(ValidRows):
            if i == iMax:
                file.write('  [' + row['id_spell'] + '] = {' + str(int(row['amplitude'])) + ', ' + ('false' if row['id_mechanic'] == "15" else 'true') + '}\n')
            else:
                file.write('  [' + row['id_spell'] + '] = {' + str(int(row['amplitude'])) + ', ' + ('false' if row['id_mechanic'] == "15" else 'true') + '},\n')
        file.write('}\n')
