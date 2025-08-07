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

generatedDir = os.path.join('scripts', 'DBC', 'generated')
parsedDir = os.path.join('scripts', 'DBC', 'parsed')
ItemDataList = ""
LegendaryDataList = ""

classTable = {}
encounterTable = {}

checkLeg = False

os.chdir(os.path.join(os.path.dirname(sys.path[0]), '..', '..', 'hero-dbc'))

def computeItemType(x):
    return {
        1: 'head',
        2: 'neck',
        3: 'shoulders',
        5: 'chest',
        6: 'waist',
        7: 'legs',
        8: 'feet',
        9: 'wrists',
        10: 'hands',
        11: 'finger',
        12: 'trinket',
        13: 'weapon',
        14: 'shield',
        15: 'ranged',
        16: 'back',
        17: '2hweapon',
        20: 'chest'
    }.get(x, '')

def computeItemMaterial(x):
    return {
        6: 'plate',
        5: 'mail',
        8: 'leather',
        7: 'cloth'
    }.get(x, '')

def createSpecTable():
    global classTable

    # Death Knight
    classTable['death_knight'] = {}
    classTable['death_knight'][0] = 'blood'
    classTable['death_knight'][1] = 'frost'
    classTable['death_knight'][2] = 'unholy'
    # Demon Hunter
    classTable['demon_hunter'] = {}
    classTable['demon_hunter'][0] = 'havoc'
    classTable['demon_hunter'][1] = 'vengeance'
    # Druid                    
    classTable['druid'] = {}
    classTable['druid'][0] = 'balance'
    classTable['druid'][1] = 'feral'
    classTable['druid'][2] = 'guardian'
    classTable['druid'][3] = 'restoration'
    # Hunter 
    classTable['hunter'] = {}
    classTable['hunter'][0] = 'beast_mastery'
    classTable['hunter'][1] = 'marksmanship'
    classTable['hunter'][2] = 'survival'
    # Mage 
    classTable['mage'] = {}
    classTable['mage'][0] = 'arcane'
    classTable['mage'][1] = 'fire'
    classTable['mage'][2] = 'frost'
    # Monk 
    classTable['monk'] = {}
    classTable['monk'][0] = 'brewmaster'
    classTable['monk'][1] = 'windwalker'
    classTable['monk'][2] = 'mistweaver'
    # Paladin 
    classTable['paladin'] = {}
    classTable['paladin'][0] = 'holy'
    classTable['paladin'][1] = 'protection'
    classTable['paladin'][2] = 'retribution'
    # Priest 
    classTable['priest'] = {}
    classTable['priest'][0] = 'discipline'
    classTable['priest'][1] = 'holy'
    classTable['priest'][2] = 'shadow'
    # Rogue 
    classTable['rogue'] = {}
    classTable['rogue'][0] = 'assassination'
    classTable['rogue'][1] = 'outlaw'
    classTable['rogue'][2] = 'subtlety'
    # Shaman 
    classTable['shaman'] = {}
    classTable['shaman'][0] = 'elemental'
    classTable['shaman'][1] = 'enhancement'
    classTable['shaman'][2] = 'restoration'
    # Warlock 
    classTable['warlock'] = {}
    classTable['warlock'][0] = 'affliction'
    classTable['warlock'][1] = 'demonology'
    classTable['warlock'][2] = 'destruction'
    # Warrior 
    classTable['warrior'] = {}
    classTable['warrior'][0] = 'arms'
    classTable['warrior'][1] = 'fury'
    classTable['warrior'][2] = 'protection'

def computeSet(set, ilvl):
    if set == 0:
        return ""
    else:
        print("unknown set:"+str(ilvl))
        return ""

def computeSource(set, quality, id, type, ilvl):
    if ilvl == 158 :
        if id not in encounterTable:
            return "pvp"
        else:
            return "dungeon"
    if ilvl == 200 :
        if id not in encounterTable:
            return "other" #todo : craft / pvp / boe
        else:
            return "castle_nathria"
    if ilvl == 226 or ilvl == 233 :
        return "sanctum_of_domination"

    print("unknown source:"+str(id))
    return ""

def computeItemStat(mask):
    return {
        3: 'agi',
        4: 'str',
        5: 'int',
        7: 'stam',
        32: 'crit',
        36: 'haste',
        40: 'vers',
        49: 'mastery',
        50: 'bonus_armor',
        62: 'leech',
        63: 'avoidance',
        71: 'agi/str/int',
        72: 'agi/str',
        73: 'agi/int',
        74: 'str/int',
    }.get(mask, '')


def getItemStats(row):
    stats = []
    computed = computeItemStat(int(row['stat_type_1']))
    if computed != '':
        stats.append(computed)
    computed = computeItemStat(int(row['stat_type_2']))
    if computed != '':
        stats.append(computed)
    computed = computeItemStat(int(row['stat_type_3']))
    if computed != '':
        stats.append(computed)
    computed = computeItemStat(int(row['stat_type_4']))
    if computed != '':
        stats.append(computed)
    computed = computeItemStat(int(row['stat_type_5']))
    if computed != '':
        stats.append(computed)
    return stats

def computeGemNumber(row):
    gemnb = 0
    if not int(row['socket_color_1']) == 0:
        gemnb = gemnb + 1
        if not int(row['socket_color_2']) == 0:
            gemnb = gemnb + 1
            if not int(row['socket_color_3']) == 0:
                gemnb = gemnb + 1
    return gemnb


def PrepareRow(row, rowClass="", rowSpec=""):
    preparedRow = {}
    preparedRow["id"] = int(row['id'])
    preparedRow["name"] = row['name']
    preparedRow["ilevel"] = int(row['ilevel'])
    preparedRow["type"] = computeItemType(int(row['inv_type']))
    preparedRow["material"] = computeItemMaterial(int(row['material']))
    preparedRow["stats"] = getItemStats(row)

    # set = computeSet(int(row['item_set']), int(row['ilevel']))
    # preparedRow["set"] = computeSet(int(row['item_set']), int(row['ilevel']))
    preparedRow["gems"] = computeGemNumber(row)
    preparedRow["source"] = computeSource(set, int(row['quality']), int(row['id']), preparedRow["type"], int(row['ilevel']))

    return preparedRow


# Program Start
createSpecTable()

with open(os.path.join(generatedDir, f'JournalEncounterItem.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    for row in reader:
        encounterTable[int(row['id_item'])] = int(row['id_encounter'])

with open(os.path.join(generatedDir, 'ItemSparse.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    reader = sorted(reader, key=lambda d: int(d['id']))
    ValidItemsRows = {}

    # Read rows and order them with each inventory type, class and material
    for row in reader:
        # ilvl : 158 = dungeon, 200 = castle nathria, 226/233 = Sanctum of domination
        if int(row['ilevel']) == 158 or int(row['ilevel']) == 200 or int(row['ilevel']) == 226 or int(row['ilevel']) == 233:
            itemType = computeItemType(int(row['inv_type']))
            itemMaterial = computeItemMaterial(int(row['material']))
            if not itemType == "trinket" and not itemType == "neck" and not itemType == "finger" and not itemType == "back":  # handle no material separatly
                if itemType not in ValidItemsRows:
                    ValidItemsRows[itemType] = {}
                if itemMaterial not in ValidItemsRows[itemType]:
                    ValidItemsRows[itemType][itemMaterial] = []
                ValidItemsRows[itemType][itemMaterial].append(PrepareRow(row))
            else:
                if itemType not in ValidItemsRows:
                    ValidItemsRows[itemType] = []
                ValidItemsRows[itemType].append(PrepareRow(row))


    # Prints everything to the files
    with open(os.path.join(parsedDir, 'ItemData.json'), 'w', encoding='utf-8') as file:
        json.dump(ValidItemsRows, file, indent=4)
