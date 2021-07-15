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

generatedDir = os.path.join('scripts', 'DBC', 'generated')
addonEnumDir = os.path.join('HeroDBC', 'DBC')

os.chdir(os.path.join(os.path.dirname(sys.path[0]), '..', '..', 'hero-dbc'))

## Mapping
#SpellEffect.misc_value_1 = SpellItemEnchantment.id
#SpellItemEnchantment.id_property_1 = Spell.id


# Get every spell id associated to an item effect
Enchants = []
with open(os.path.join(generatedDir, 'SpellItemEnchantment.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    reader = sorted(reader, key=lambda d: int(d['id']))
    for row in reader:
        if int(row['id_property_1']) > 0:
            Enchants.append(row)
    with open(os.path.join(addonEnumDir, 'SpellEnchants.lua'), 'w', encoding='utf-8') as file:
        file.write('HeroDBC.DBC.SpellEnchants = {\n')
        for _, row in enumerate(Enchants):
            file.write('  [' + row['id'] + '] = ' + row['id_property_1'] + ',\n')
        file.write('}\n')