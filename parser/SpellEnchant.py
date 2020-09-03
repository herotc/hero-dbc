# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0301

"""
@author: Kutikuti
"""

import sys
import os
import csv
import operator
from collections import OrderedDict

generatedDir = os.path.join('DBC', 'generated')
parsedDir = os.path.join('DBC', 'parsed')

os.chdir(os.path.join(os.path.dirname(sys.path[0]), '..', 'hero-dbc'))

## Mapping
#SpellEffect.misc_value_1 = SpellItemEnchantment.id
#SpellItemEnchantment.id_property_1 = Spell.id


# Get every spell id associated to an item effect
Enchants = []
with open(os.path.join(generatedDir, 'SpellItemEnchantment.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    for row in reader:
        if int(row['id_property_1']) > 0:
            Enchants.append(row)
    with open(os.path.join(parsedDir, 'SpellEnchants.lua'), 'w', encoding='utf-8') as file:
        file.write('MoreTooltipInfo.Enum.SpellEnchants = {\n')
        iMax = len(Enchants) - 1
        for i, row in enumerate(Enchants):
            if i == iMax:
                file.write('  [' + row['id'] + '] = ' + row['id_property_1'] + '\n')
            else:
                file.write('  [' + row['id'] + '] = ' + row['id_property_1'] + ',\n')
        file.write('}\n')