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

os.chdir(os.path.join(os.path.dirname(sys.path[0]), 'hero-dbc'))

with open(os.path.join(generatedDir, 'SpellCooldowns.csv')) as csvfile:
    reader = list(csv.DictReader(csvfile, escapechar='\\'))
    with open(os.path.join(parsedDir, 'TriggerGCD.lua'), 'w', encoding='utf-8') as file:
        file.write('HeroLib.Enum.TriggerGCD = {\n')
        iMax = len(reader)-1
        for i, row in enumerate(reader):
            if i == iMax:
                file.write('  [' + row['id_parent'] + '] = ' + row['gcd_cooldown'] + '\n')
            else:
                file.write('  [' + row['id_parent'] + '] = ' + row['gcd_cooldown'] + ',\n')
        file.write('}\n')
