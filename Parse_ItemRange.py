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
# We ignore the '_2' ranges and only considers the '_1' ones
Ranges = {}
with open(os.path.join(generatedDir, 'SpellRange.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    for row in reader:
        # Every ranges are 6 digits float
        min_range = float(row['min_range_1'])
        max_range = float(row['max_range_1'])
        if min_range == 0 and max_range > 0 and max_range <= 100:
            Ranges[row['id']] = max_range

# Make a table containing all possible items for a given range
ItemRange = {}
with open(os.path.join(generatedDir, 'SpellMisc.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    for row in reader:
        id_misc = row['id']
        if id_misc in Spells:
            id_range = row['id_range']
            if id_range in Ranges:
                max_range = Ranges[id_range]
                if not max_range in ItemRange:
                    ItemRange[max_range] = []
                # Convert it to int for later sorting
                ItemRange[max_range].append(int(Items[Spells[id_misc]]))

# For nice output we sort the dict into a list of tuples [ (range1, [items]), (range2, [items]), ... ]
ItemRangeD = sorted(ItemRange.items(), key=operator.itemgetter(0))

with open(os.path.join(parsedDir, 'ItemRange.lua'), 'w', encoding='utf-8') as file:
    file.write('AethysCore.Enum.ItemRange = {\n')
    for _, itemRange in enumerate(ItemRangeD):
        # Write the range without the trailing 0 using format ('{' string need to be escaped in this case)
        file.write('  [{0:g}] = {{\n'.format(itemRange[0]))
        for _, itemID in enumerate(sorted(itemRange[1])):
            file.write('    ' + str(itemID) + ',\n')
        file.write('  },\n')
    file.write('}\n')
