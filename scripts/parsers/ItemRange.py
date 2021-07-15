# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0301

"""
@author: Quentin Giraud <dev@aethys.io>
"""

import sys
import os
import csv
import operator

generatedDir = os.path.join('scripts', 'DBC', 'generated')
addonDevDir = os.path.join('HeroDBC', 'Dev')

os.chdir(os.path.join(os.path.dirname(sys.path[0]), '..', '..', 'hero-dbc'))

## Mapping
# id_item & id_parent from ItemEffect
# id_misc & id_range from SpellMisc
# id_range & min_range/max_range from SpellRange

# Get every spell id associated to an item effect
Items = {}
with open(os.path.join(generatedDir, 'ItemEffect.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    for row in reader:
        Items[row['id_spell']] = row['id']
# Get every 'valid' ranges for our parser, those that aren't a range but a single value.
# We only take values with a min_range of 0 and a max_range between 0 and 100 (WoW limit for range check))
Ranges = {}
with open(os.path.join(generatedDir, 'SpellRange.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    for row in reader:
        # Every ranges are 6 digits float
        # Hostile
        min_range = float(row['min_range_1'])
        max_range = float(row['max_range_1'])
        if min_range == 0 and max_range >= 5 and max_range <= 100:
            Ranges[row['id']] = [max_range, int(row['flag'])]
        # Friendly
        min_range = float(row['min_range_2'])
        max_range = float(row['max_range_2'])
        if min_range == 0 and max_range >= 5 and max_range <= 100:
            Ranges[row['id']] = [max_range, int(row['flag'])]

# Make a table for each range computation (melee, ranged) containing all possible items for a given range
ItemRange = {
    'Melee': {},
    'Ranged': {}
}

with open(os.path.join(generatedDir, 'SpellMisc.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    for row in reader:
        id_misc = row['id_parent']
        if id_misc in Items:
            id_range = row['id_range']
            if id_range in Ranges:
                max_range = Ranges[id_range][0]
                flag = Ranges[id_range][1]
                if flag == 1:
                    ItemRangeT = ItemRange['Melee']
                else:
                    ItemRangeT = ItemRange['Ranged']
                if not max_range in ItemRangeT:
                    ItemRangeT[max_range] = []
                # Convert it to int for later sorting
                ItemRangeT[max_range].append(int(Items[id_misc]))

# For nice output we sort the dict into a list of tuples [ (range1, [items]), (range2, [items]), ... ]
ItemRange['Melee'] = sorted(ItemRange['Melee'].items(), key=operator.itemgetter(0))
ItemRange['Ranged'] = sorted(ItemRange['Ranged'].items(), key=operator.itemgetter(0))

with open(os.path.join(addonDevDir, 'Unfiltered', 'ItemRange.lua'), 'w', encoding='utf-8') as file:
    file.write('-- { [Type] = { [Range] = { [1] = ItemID, [2] = ItemId, [3] = ... } } }\n')
    file.write('HeroDBC.DBC.ItemRangeUnfiltered = {\n')
    for key, value in ItemRange.items():
        file.write('  ' + key + ' = {\n')
        for _, itemRange in enumerate(value):
            # Write the range without the trailing 0 using format ('{' string need to be escaped in this case)
            file.write('    [{0:g}] = {{\n'.format(itemRange[0]))
            for _, itemID in enumerate(sorted(itemRange[1])):
                file.write('      ' + str(itemID) + ',\n')
            file.write('    },\n')
        file.write('  },\n')
    file.write('}\n')
