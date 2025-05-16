# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0301

"""
@author: Quentin Giraud <dev@aethys.io>
"""

import sys
import os
import operator
import json
from slpp import slpp as lua  # SLPP-23 package: https://pypi.org/project/SLPP-23

generatedDir = os.path.join('scripts', 'DBC', 'generated')
addonDevDir = os.path.join('HeroDBC', 'Dev')
addonEnumDir = os.path.join('HeroDBC', 'DBC')

os.chdir(os.path.join(os.path.dirname(sys.path[0]), '..', '..', 'hero-dbc'))

with open(os.path.join(addonDevDir, 'Filtered', 'ItemRange.lua')) as luafile:
    data = luafile.read()
    # Strip leading 'return' from Lua file for proper decoding
    brace_index = data.find('{')
    if brace_index != -1:
        data = data[brace_index:]
    ItemRangeFiltered = lua.decode(data)

ItemRange = {}
for type, value in ItemRangeFiltered.items():
    ItemRange[type] = {}
    for reaction, value2 in value.items():
        ItemRange[type][reaction] = {}
        for key3, value3 in value2.items():
            value3 = json.loads(value3)
            if isinstance(value3, list):
                ItemRangeInt = []
                for i, value4 in enumerate(value3):
                    ItemRangeInt.append(float(value4))
                ItemRange[type][reaction][key3] = sorted(ItemRangeInt)
            elif isinstance(value3, dict):
                ItemRangeInt = {}
                for key4, value4 in value3.items():
                    ItemRangeInt[float(key4)] = sorted(value4)
                ItemRangeInt = dict(sorted(ItemRangeInt.items(), key=operator.itemgetter(0)))
                ItemRange[type][reaction][key3] = {**ItemRangeInt}

with open(os.path.join(addonEnumDir, 'ItemRange.lua'), 'w', encoding='utf-8') as file:
    file.write('HeroDBC.DBC.ItemRange = {\n')
    for key, value in ItemRange.items():
        file.write('  ' + key + ' = {\n')
        for key2, value2 in value.items():
            file.write('    ' + key2 + ' = {\n')
            for key3, value3 in value2.items():
                if isinstance(value3, list):
                    file.write('      ' + key3 + ' = {\n')
                    for _, value4 in enumerate(value3):
                        if isinstance(value4, str):
                            value4 = '"' + value4 + '"'
                        file.write('        ' + f'{float(value4):g}' + ',\n')
                    file.write('      },\n')
                elif isinstance(value3, dict):
                    file.write('      ' + key3 + ' = {\n')
                    for key4, value4 in value3.items():
                        if isinstance(key4, str):
                            file.write('        ' + f'{float(key4):g}' + ' = {\n')
                        else:
                            file.write('        [' + f'{float(key4):g}' + '] = {\n')
                        for _, value4 in enumerate(value4):
                            file.write('          ' + f'{float(value4):g}' + ',\n')
                        file.write('        },\n')
                    file.write('      },\n')
            file.write('    },\n')
        file.write('  },\n')
    file.write('}\n')
