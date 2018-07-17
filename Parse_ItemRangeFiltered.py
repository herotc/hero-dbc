# source: https://github.com/NiftyManiac/slpp/tree/py3

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
import json
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Lib'))
from slpp import slpp as lua

generatedDir = os.path.join('DBC', 'generated')
parsedDir = os.path.join('DBC', 'parsed')

os.chdir(os.path.join(os.path.dirname(sys.path[0]), 'AethysDBC'))

with open(os.path.join(generatedDir, 'ItemRangeFiltered.lua')) as luafile:
    data = luafile.read().replace('\n', '')
    ItemRangeFiltered = lua.decode(data)

ItemRange = {}
for key, value in ItemRangeFiltered.items():
    ItemRange[key] = {}
    for key2, value2 in value.items():
        value2 = json.loads(value2)
        if isinstance(value2, list):
            ItemRangeString = []
            ItemRangeInt = []
            for i, value3 in enumerate(value2):
                if value3 == "Melee":
                    ItemRangeString.append(value3)
                else:
                    ItemRangeInt.append(int(value3))
            ItemRangeString = sorted(ItemRangeString)
            ItemRangeInt = sorted(ItemRangeInt)
            ItemRange[key][key2] = ItemRangeString + ItemRangeInt
        elif isinstance(value2, dict):
            ItemRangeString = {}
            ItemRangeInt = {}
            for key3, value3 in value2.items():
                if key3 == "Melee":
                    ItemRangeString[key3] = value3
                else:
                    key3 = int(key3)
                    ItemRangeInt[key3] = sorted(value3)
            ItemRangeString = dict(sorted(ItemRangeString.items(), key=operator.itemgetter(0)))
            ItemRangeInt = dict(sorted(ItemRangeInt.items(), key=operator.itemgetter(0)))
            ItemRange[key][key2] = {**ItemRangeString, **ItemRangeInt}

with open(os.path.join(parsedDir, 'ItemRange.lua'), 'w', encoding='utf-8') as file:
    file.write('HeroLib.Enum.ItemRange = {\n')
    i, iMax = 0, len(ItemRange)
    for key, value in ItemRange.items():
        i += 1
        file.write('  ' + key + ' = {\n')
        j, jMax = 0, len(value)
        for key2, value2 in value.items():
            j += 1
            k, kMax = 0, len(value2)
            if isinstance(value2, list):
                file.write('    ' + key2 +' = {')
                for _, value3 in enumerate(value2):
                    k += 1
                    if isinstance(value3, str):
                        value3 = '"' + value3 + '"'
                    if k == kMax:
                        file.write(str(value3))
                    else:
                        file.write(str(value3) + ', ')
                if j == jMax:
                    file.write('}\n')
                else:
                    file.write('},\n')
            elif isinstance(value2, dict):
                file.write('    ' + key2 +' = {\n')
                for key3, value3 in value2.items():
                    k += 1
                    if isinstance(key3, str):
                        file.write('      ' + str(key3) +' = {\n')
                    else:
                        file.write('      [' + str(key3) +'] = {\n')
                    l, lMax = 0, len(value3)
                    for _, value4 in enumerate(value3):
                        l += 1
                        if l == lMax:
                            file.write('        ' + str(value4) + '\n')
                        else:
                            file.write('        ' + str(value4) + ',\n')
                    if k == kMax:
                        file.write('      }\n')
                    else:
                        file.write('      },\n')
                if j == jMax:
                    file.write('    }\n')
                else:
                    file.write('    },\n')
        if i == iMax:
            file.write('  }\n')
        else:
            file.write('  },\n')
    file.write('}\n')
