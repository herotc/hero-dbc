# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0301

"""
@author: Aethys256
"""

import sys
import os
import csv
import operator

generatedDir = os.path.join('DBC', 'generated')
parsedDir = os.path.join('DBC', 'parsed')

os.chdir(os.path.join(os.path.dirname(sys.path[0]), 'AethysDBC'))

## Mapping
# id_item & id_spell from ItemEffect
# id_spell & id_misc from Spell
# id_misc & id_range from SpellMisc
# id_range & min_range/max_range from SpellRange

# Get every spell id associated to an item effect
Items = {}
with open(os.path.join(generatedDir, 'ItemEffect.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    for row in reader:
        Items[row['id_spell']] = row['id_item']
# Get every misc id associated to every spell id associated to an item effect
Spells = {}
with open(os.path.join(generatedDir, 'Spell.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    for row in reader:
        id_spell = row['id']
        if id_spell in Items:
            Spells[row['id_misc']] = id_spell
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
        id_misc = row['id']
        if id_misc in Spells:
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
                ItemRangeT[max_range].append(int(Items[Spells[id_misc]]))

# For nice output we sort the dict into a list of tuples [ (range1, [items]), (range2, [items]), ... ]
ItemRange['Melee'] = sorted(ItemRange['Melee'].items(), key=operator.itemgetter(0))
ItemRange['Ranged'] = sorted(ItemRange['Ranged'].items(), key=operator.itemgetter(0))

with open(os.path.join(parsedDir, 'ItemRangeUnfiltered.lua'), 'w', encoding='utf-8') as file:
    file.write('AethysCore.Enum.ItemRangeUnfiltered = {\n')
    i, iMax = 0, len(ItemRange)
    for key, value in ItemRange.items():
        i += 1
        file.write('  ' + key + ' = {\n')
        j, jMax = 0, len(value)
        for _, itemRange in enumerate(value):
            j += 1
            # Write the range without the trailing 0 using format ('{' string need to be escaped in this case)
            file.write('    [{0:g}] = {{\n'.format(itemRange[0]))
            k, kMax = 0, len(itemRange[1])
            for _, itemID in enumerate(sorted(itemRange[1])):
                k += 1
                if k == kMax:
                    file.write('      ' + str(itemID) + '\n')
                else:
                    file.write('      ' + str(itemID) + ',\n')
            if j == jMax:
                file.write('    }\n')
            else:
                file.write('    },\n')
        if i == iMax:
            file.write('  }\n')
        else:
            file.write('  },\n')
    file.write('}\n')
