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

def computeItemType(x):
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
    }.get(x, '')
    
def computeItemMaterial(x):
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
        
def computeBonusID(set,quality):
    if set == "" or set == "T21":
        if set == "" and quality == 5: #legendaries
            return "3630"
        else: #T21
            return "3612/1502"
    if set == "T20": #T20
        return "1512/3563"

def computeLegClass(classmask):
    return {
        1: 'warrior',
        2: 'paladin',
        4: 'hunter',
        8: 'rogue',
        16: 'priest',
        32: 'death_knight',
        35: 'warrior/paladin/death_knight',
        64: 'shaman',
        68: 'hunter/shaman',
        128: 'mage',
        256: 'warlock',
        400: 'priest/mage/warlock',
        512: 'monk',
        1024: 'druid',
        2048: 'demon_hunter',
        3592: 'rogue/monk/druid/demon_hunter',
        65535: 'All'
    }.get(classmask, '')

with open(os.path.join(generatedDir, 'ItemSparse.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    ValidItemsRows = []
    ValidLegendariesRows = {}
    ValidLegendariesRows["warrior"] = []
    ValidLegendariesRows["paladin"] = []
    ValidLegendariesRows["hunter"] = []
    ValidLegendariesRows["rogue"] = []
    ValidLegendariesRows["priest"] = []
    ValidLegendariesRows["death_knight"] = []
    ValidLegendariesRows["shaman"] = []
    ValidLegendariesRows["mage"] = []
    ValidLegendariesRows["warlock"] = []
    ValidLegendariesRows["monk"] = []
    ValidLegendariesRows["druid"] = []
    ValidLegendariesRows["demon_hunter"] = []
    for row in reader:
        if not row['inv_type'] == '0' and (row['ilevel'] == '930' or row['ilevel'] == '940' or row['ilevel'] == '1000' or (row['ilevel'] == '890' and not row['item_set'] == '0')):
            ValidItemsRows.append(row)
        if row['ilevel'] == '910' and int(row['quality']) == 5:
            mask = computeLegClass(int(row['class_mask']))
            if "/" in mask:
                t = mask.split('/')
                for i in range(len(t)):
                    ValidLegendariesRows[t[i]].append(row)
            elif mask == "All":
                for key in ValidLegendariesRows:
                    ValidLegendariesRows[key].append(row)
            else:
                ValidLegendariesRows[mask].append(row)
    with open(os.path.join(parsedDir, 'ItemData.json'), 'w', encoding='utf-8') as file:
        file.write('{\n')
        file.write('\t"Items": [\n')
        iMax = len(ValidItemsRows)-1
        for i, row in enumerate(ValidItemsRows):
            set = computeSet(int(row['item_set']),int(row['ilevel']))
            if i == iMax:
                file.write('\t\t{"id":' + row['id'] + ', "name":"' + row['name'] + '", "level":' + row['ilevel'] + ', "type":"' + computeItemType(int(row['inv_type'])) + '", "material":"' + computeItemMaterial(int(row['material'])) + '", "set":"' + set + '", "bonus_id":"' + computeBonusID(set,int(row['quality'])) + '"}\n')
            else:
                file.write('\t\t{"id":' + row['id'] + ', "name":"' + row['name'] + '", "level":' + row['ilevel'] + ', "type":"' + computeItemType(int(row['inv_type'])) + '", "material":"' + computeItemMaterial(int(row['material'])) + '", "set":"' + set + '", "bonus_id":"' + computeBonusID(set,int(row['quality'])) + '"},\n')
        file.write('\t],\n')
        file.write('\t"legendaries": [\n')
        
        for key in ValidLegendariesRows:
            jMax = len(ValidLegendariesRows[key])-1
            file.write('\t\t"'+key+'": [\n')
            for j, row in enumerate(ValidLegendariesRows[key]):
                set = computeSet(int(row['item_set']),int(row['ilevel']))
                if j == jMax:
                    file.write('\t\t\t{"id":' + row['id'] + ', "name": "' + row['name'] + '", "enable":false,"level":' + row['ilevel'] + ', "type":"' + computeItemType(int(row['inv_type'])) + '", "material":"' + computeItemMaterial(int(row['material'])) + '", "bonus_id":"' + computeBonusID(set,int(row['quality'])) + '"}\n')
                else:
                    file.write('\t\t\t{"id":' + row['id'] + ', "name": "' + row['name'] + '", "enable":false, "level":' + row['ilevel'] + ', "type":"' + computeItemType(int(row['inv_type'])) + '", "material":"' + computeItemMaterial(int(row['material'])) + '", "bonus_id":"' + computeBonusID(set,int(row['quality'])) + '"},\n')
            file.write('\t\t],\n')
        file.write('\t]\n')
        file.write('}\n')
