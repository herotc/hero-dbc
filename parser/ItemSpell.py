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
# id_parent and id_spell itemEffect

# Get every spell id associated to an item effect
Items = {}
with open(os.path.join(generatedDir, 'ItemEffect.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    for row in reader:
        Items[int(row['id_parent'])] = int(row['id_spell'])



with open(os.path.join(parsedDir, 'ItemSpell.lua'), 'w', encoding='utf-8') as file:
    file.write('MoreItemInfo.Enum.ItemSpell = {\n')
    itemRowMax = len(Items) - 1
    for i, itemRow in enumerate(Items):
        file.write('\t[' + str(itemRow) + '] = ' + str(Items[itemRow]))
        if not i == itemRowMax:
            file.write(',')
        file.write('\n')
    file.write('}\n')

