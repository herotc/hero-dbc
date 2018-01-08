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
ItemDataList = ""
LegendaryDataList = ""

classTable = {}
relicTypeTable = {}
itemEncounterTable = {}

checkLeg = False

os.chdir(os.path.join(os.path.dirname(sys.path[0]), 'AethysDBC'))

def computeItemType(x):
    return {
        0: 'relic',
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
    
def computeRelicType(x):
    return {
        64: 'iron',
        128:'blood',
        256:'shadow',
        512: 'fel',
        1024: 'arcane',
        2048: 'frost',
        4096: 'fire',
        16384: 'life',
        32768: 'storm',
        65536: 'holy'
    }.get(x,'')

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
    
def createRelicTypeTable():
    global relicTypeTable
    with open(os.path.join(generatedDir, 'GemProperties.csv')) as csvfile:
        reader = csv.DictReader(csvfile, escapechar='\\')
        for row in reader:
            
            relicType = computeRelicType(int(row['color']))
            if not relicType == '':
                relicTypeTable[int(row['id'])] = relicType

def createItemEncounterTable():
    global itemEncounterTable
    with open(os.path.join(generatedDir, 'JournalEncounterItem.csv')) as csvfile:
        reader = csv.DictReader(csvfile, escapechar='\\')
        for row in reader:
            itemEncounterTable[int(row['id_item'])] = int(row['id_encounter'])                
                
def computeSet(set,ilvl):
    if set == 0:
        return ""
    if ilvl == 890:
        return "T20"
    if ilvl == 930 or ilvl == 940:
        return "T21"
        
def computeBonusID(set,quality,id,type):
    if type == 'relic':
        if id in itemEncounterTable and itemEncounterTable[id] == 2031:
            return "3612/1512"
        else:
            return "3612/1502"
    if set == "" or set == "T21":
        if set == "" and quality == 5: #legendaries
            if id == 154172: #Amanthul specific
                return "4213"
            else:
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
        65535: 'warrior/paladin/hunter/rogue/priest/death_knight/shaman/mage/warlock/monk/druid/demon_hunter'
    }.get(classmask, '')
    
def checkLegStatus(legClass,legSpec,itemType,id):
    if checkLeg:
        if legClass in LegendaryDataList and legSpec in LegendaryDataList[legClass] and itemType in LegendaryDataList[legClass][legSpec]:
            for item in LegendaryDataList[legClass][legSpec][itemType]:
                if int(item['id']) == id:
                    return item['enable']
    return False

def computeItemStat(mask):
    return {
        3 : 'agi',
        4 : 'str',
        5 : 'int',
        7 : 'stam',
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
    statString = ""
    if not int(row['stat_type_1']) == -1:
        statString = computeItemStat(int(row['stat_type_1']))
        if not int(row['stat_type_2']) == -1:
            statString = statString + "/" + computeItemStat(int(row['stat_type_2']))
            if not int(row['stat_type_3']) == -1:
                statString = statString + "/" + computeItemStat(int(row['stat_type_3']))
                if not int(row['stat_type_4']) == -1:
                    statString = statString + "/" + computeItemStat(int(row['stat_type_4']))
                    if not int(row['stat_type_5']) == -1:
                        statString = statString + "/" + computeItemStat(int(row['stat_type_5']))
    return statString

def computeGemNumber(row):
    gemnb = 0
    if not int(row['socket_color_1']) == 0:
        gemnb = gemnb + 1
        if not int(row['socket_color_2']) == 0:
            gemnb = gemnb + 1
            if not int(row['socket_color_3']) == 0:
                gemnb = gemnb + 1
    return gemnb
  
def PrepareRow(row,rowClass="",rowSpec=""):
    preparedRow = {}
    preparedRow["id"] = int(row['id'])
    preparedRow["name"] = row['name']
    preparedRow["level"] = int(row['ilevel'])
    preparedRow["type"] = computeItemType(int(row['inv_type']))
    
    if preparedRow["type"] == 'relic':
        preparedRow["relicType"] = relicTypeTable[int(row['gem_props'])]
        preparedRow["bonus_id"] = computeBonusID("","",preparedRow["id"],preparedRow["type"])
    else:
        preparedRow["material"] = computeItemMaterial(int(row['material']))
        preparedRow["stats"] = getItemStats(row)

        set = computeSet(int(row['item_set']),int(row['ilevel']))

        if int(row['ilevel']) == 910 and int(row['quality']) == 5:
            preparedRow["enable"] = checkLegStatus(rowClass,rowSpec,preparedRow["type"],preparedRow["id"])
        else:   
            preparedRow["set"] = computeSet(int(row['item_set']),int(row['ilevel']))
            if not set == "":
                preparedRow["class"] = computeLegClass(int(row['class_mask']))
        preparedRow["gems"] = computeGemNumber(row)
        preparedRow["bonus_id"] = computeBonusID(set,int(row['quality']),int(row['id']),preparedRow["type"])

    return preparedRow
    
# Program Start
createSpecTable()
createRelicTypeTable()
createItemEncounterTable()

if os.path.isfile('../AutoSimC/generatorItemData.json') and os.path.isfile('../AutoSimC/generatorLegendaryData.json'): 
    with open('../AutoSimC/generatorItemData.json') as existingitemDataFile:
        with open('../AutoSimC/generatorLegendaryData.json') as existinglegendaryDataFile: 
            ItemDataList = json.load(existingitemDataFile)
            LegendaryDataList = json.load(existinglegendaryDataFile)
            checkLeg = True
    
with open(os.path.join(generatedDir, 'ItemSparse.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    ValidItemsRows = {}
    ValidLegendariesRows = {}
    
    #Read rows and order them with each inventory type, class and material
    for row in reader:
        #ilvl : 930/940/1000 = argus, 890, only T20 
        if int(row['ilevel']) == 930 or int(row['ilevel']) == 940 or int(row['ilevel']) == 1000 or (int(row['ilevel']) == 890 and not int(row['item_set']) == 0):
            itemType = computeItemType(int(row['inv_type']))
            if itemType == 'relic' and int(row['gem_props']) != 0:
                if itemType not in ValidItemsRows:
                    ValidItemsRows[itemType] = {}
                relictype = relicTypeTable[int(row['gem_props'])]
                if relictype not in ValidItemsRows[itemType]:
                    ValidItemsRows[itemType][relictype] = []
                ValidItemsRows[itemType][relictype].append(PrepareRow(row))
            elif not itemType == 'relic':
                itemMaterial = computeItemMaterial(int(row['material']))
                if not itemType == "trinket" and not itemType == "neck" and not itemType == "finger" and not itemType == "back": #handle no materal separatly
                    if itemType not in ValidItemsRows:
                        ValidItemsRows[itemType] = {} 
                    if itemMaterial not in ValidItemsRows[itemType]:
                        ValidItemsRows[itemType][itemMaterial] = [] 
                    ValidItemsRows[itemType][itemMaterial].append(PrepareRow(row))
                else:
                    if itemType not in ValidItemsRows:
                        ValidItemsRows[itemType] = []
                    ValidItemsRows[itemType].append(PrepareRow(row))
        
        #Legendaries : baseilvl = 910  
        if int(row['ilevel']) == 910 and int(row['quality']) == 5: 
            mask = computeLegClass(int(row['class_mask']))
            itemType = computeItemType(int(row['inv_type']))
            itemMaterial = computeItemMaterial(int(row['material']))
            if "/" in mask: # cut the multiple spec legendaries and handle them separatly
                t = mask.split('/')
                for i in range(len(t)):
                    if t[i] not in ValidLegendariesRows:
                        ValidLegendariesRows[t[i]] = {}
                    for j in range(len(classTable[t[i]])):  
                        if classTable[t[i]][j] not in ValidLegendariesRows[t[i]]:
                            ValidLegendariesRows[t[i]][classTable[t[i]][j]] = {}    
                        if itemType not in ValidLegendariesRows[t[i]][classTable[t[i]][j]]:
                            ValidLegendariesRows[t[i]][classTable[t[i]][j]][itemType] = [] 
                        ValidLegendariesRows[t[i]][classTable[t[i]][j]][itemType].append(PrepareRow(row,t[i],classTable[t[i]][j]))
            else: 
                if mask not in ValidLegendariesRows:
                        ValidLegendariesRows[mask] = {}
                for j in range(len(classTable[mask])):
                    if classTable[mask][j] not in ValidLegendariesRows[mask]:
                        ValidLegendariesRows[mask][classTable[mask][j]] = {}
                    if itemType not in ValidLegendariesRows[mask][classTable[mask][j]]:
                        ValidLegendariesRows[mask][classTable[mask][j]][itemType] = [] 
                    ValidLegendariesRows[mask][classTable[mask][j]][itemType].append(PrepareRow(row,mask,classTable[mask][j]))
  
    #Prints everything to the files  
    with open(os.path.join(parsedDir, 'generatorItemData.json'), 'w', encoding='utf-8') as file:
        json.dump(ValidItemsRows, file, indent=4)
    with open(os.path.join(parsedDir, 'generatorLegendaryData.json'), 'w', encoding='utf-8') as fileLegendary:
        json.dump(ValidLegendariesRows, fileLegendary, indent=4)
