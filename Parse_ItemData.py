# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0301

"""
@author: Kutikuti
"""

import sys
import os
import csv
import json

generatedDir = os.path.join('DBC', 'generated')
parsedDir = os.path.join('DBC', 'parsed')

os.chdir(os.path.join(os.path.dirname(sys.path[0]), 'AethysDBC'))

def itemType(x):
    return {
        1: 'head',
        2: 'neck',
        3: 'shoulder',
        5: 'chest',
        6: 'waist',
        7: 'legs',
        8: 'feet',
        9: 'wrist',
        10: 'hands',
        11: 'finger',
        12: 'trinket',
        16: 'back',
        20: 'chest'
    }.get(x, 'unknown')
    
def itemMaterial(x):
    return {
        6: 'plate',
        5: 'mail',
        8: 'leather',
        7: 'cloth'
    }.get(x, '')
    
def computeSet(set,ilvl):
    if set == 0:
        return ""
    if ilvl == 890:
        return "T20"
    if ilvl == 930 or ilvl == 940:
        return "T21"
        
def computeBonusID(set):
    if set == "" or set == "T21":
        return "3612/1502"
    if set == "T20":
        return "1512/3563"

with open(os.path.join(generatedDir, 'ItemSparse.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    ValidRows = []
    for row in reader:
        if not row['inv_type'] == '0' and (row['ilevel'] == '930' or row['ilevel'] == '940' or row['ilevel'] == '1000' or (row['ilevel'] == '890' and not row['item_set'] == '0')):
            ValidRows.append(row)
    with open(os.path.join(parsedDir, 'ItemData.json'), 'w', encoding='utf-8') as file:
        file.write('{\n')
        iMax = len(ValidRows)-1
        for i, row in enumerate(ValidRows):
            set = computeSet(int(row['item_set']),int(row['ilevel']))
            if i == iMax:
                file.write('  { "id":' + row['id'] + ', "name": "' + row['name'] + '", "level": ' + row['ilevel'] + ', "type": "' + itemType(int(row['inv_type'])) + '", "material": "' + itemMaterial(int(row['material'])) + '", "set": "' + set + '", "bonus_id": "' + computeBonusID(set) + '"}\n')
            else:
                file.write('  { "id":' + row['id'] + ', "name": "' + row['name'] + '", "level": ' + row['ilevel'] + ', "type": "' + itemType(int(row['inv_type'])) + '", "material": "' + itemMaterial(int(row['material'])) + '", "set": "' + set + '", "bonus_id": "' + computeBonusID(set) + '"},\n')
        file.write('}\n')
