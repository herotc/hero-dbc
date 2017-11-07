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
    
def computeSet(set,ilvl):
    if set == 0:
        return ""
    if ilvl == 890:
        return "T20"
    if ilvl == 930 or ilvl == 940:
        return "T21"
        
def computeBonusID(set,quality,id):
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

def addValidRow(dict, index , row, objtype): 
    if index not in dict:
        dict[index] = objtype
    dict[index].append(row)

def computeGemNumber(row):
    gemnb = 0
    if not int(row['socket_color_1']) == 0:
        gemnb = gemnb + 1
        if not int(row['socket_color_2']) == 0:
            gemnb = gemnb + 1
            if not int(row['socket_color_3']) == 0:
                gemnb = gemnb + 1
    return gemnb
    
def printRow(row):
    stringToPrint = ""
    enableString = ""
    setString = ""
    classstring = ""
    gems = ""
    
    set = computeSet(int(row['item_set']),int(row['ilevel']))
    gems = ', "gems":'+ str(computeGemNumber(row))
    
    if row['ilevel'] == '910' and int(row['quality']) == 5:
        enableString = ', "enable":false'
    else:
        setString = ', "set":"' + set + '"'
        if not set == "": 
            classstring = ', "class":"' + computeLegClass(int(row['class_mask'])) + '"'
            
    stringToPrint = '{"id":' + row['id'] + ', "name":"' + row['name'] + '"'+ enableString +', "level":' + row['ilevel'] + ', "type":"' + computeItemType(int(row['inv_type'])) + '", "material":"' + computeItemMaterial(int(row['material'])) + '"'+ setString + classstring + gems + ', "bonus_id":"' + computeBonusID(set,int(row['quality']),int(row['id'])) + '"}'
    
    return stringToPrint


    
    
with open(os.path.join(generatedDir, 'ItemSparse.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    ValidItemsRows = {}
    ValidLegendariesRows = {}
    
    #Read rows and order them with each inventory type, class and material
    for row in reader:
        #inv_type = 0 : non equipable items
        #ilvl : 930/940/1000 = argus, 890, only T20 
        if not row['inv_type'] == '0' and (row['ilevel'] == '930' or row['ilevel'] == '940' or row['ilevel'] == '1000' or (row['ilevel'] == '890' and not row['item_set'] == '0')):
            itemType = computeItemType(int(row['inv_type']))
            itemMaterial = computeItemMaterial(int(row['material']))
            if not itemType == "trinket" and not itemType == "neck" and not itemType == "finger" and not itemType == "back": #handle no materal separatly
                if itemType not in ValidItemsRows:
                    ValidItemsRows[itemType] = {} #Dictionnary because we need to order more
                if itemMaterial not in ValidItemsRows[itemType]:
                    ValidItemsRows[itemType][itemMaterial] = [] #List of item ordered
                ValidItemsRows[itemType][itemMaterial].append(row)
            else:
                addValidRow(ValidItemsRows,itemType,row,[]) # for non material items, handle them directly
        
        #Legendaries : baseilvl = 910      
        if row['ilevel'] == '910' and int(row['quality']) == 5: 
            mask = computeLegClass(int(row['class_mask']))
            itemType = computeItemType(int(row['inv_type']))
            itemMaterial = computeItemMaterial(int(row['material']))
            if "/" in mask: # cut the multiple spec legendaries and handle them separatly
                t = mask.split('/')
                for i in range(len(t)):
                    if t[i] not in ValidLegendariesRows:
                        ValidLegendariesRows[t[i]] = {}
                    if not itemType == "trinket" and not itemType == "neck" and not itemType == "finger" and not itemType == "back": #handle no materal separatly
                        if itemType not in ValidLegendariesRows[t[i]]:
                            ValidLegendariesRows[t[i]][itemType] = {} #Dictionnary because we need to order more
                        if itemMaterial not in ValidLegendariesRows[t[i]][itemType]:
                            ValidLegendariesRows[t[i]][itemType][itemMaterial] = [] #List of item ordered
                        ValidLegendariesRows[t[i]][itemType][itemMaterial].append(row)
                    else:
                        if itemType not in ValidLegendariesRows[t[i]]:
                            ValidLegendariesRows[t[i]][itemType] = [] #Dictionnary because we need to order more
                        ValidLegendariesRows[t[i]][itemType].append(row)

            else: 
                if mask not in ValidLegendariesRows:
                        ValidLegendariesRows[mask] = {}
                if not itemType == "trinket" and not itemType == "neck" and not itemType == "finger" and not itemType == "back": #handle no materal separatly
                    if itemType not in ValidLegendariesRows[mask]:
                        ValidLegendariesRows[mask][itemType] = {} #Dictionnary because we need to order more
                    if itemMaterial not in ValidLegendariesRows[mask][itemType]:
                        ValidLegendariesRows[mask][itemType][itemMaterial] = [] #List of item ordered
                    ValidLegendariesRows[mask][itemType][itemMaterial].append(row)
                else:
                    if itemType not in ValidLegendariesRows[mask]:
                        ValidLegendariesRows[mask][itemType] = [] #Dictionnary because we need to order more
                    ValidLegendariesRows[mask][itemType].append(row)
          
    #Prints everything to the file in the right order          
    with open(os.path.join(parsedDir, 'generatorItemData.json'), 'w', encoding='utf-8') as file:
        file.write('{\n')
        
        file.write('\t"items": {\n')
        keymax = len(ValidItemsRows)
        keycount = 0
        for key in ValidItemsRows:
            keycount = keycount + 1
            file.write('\t\t"'+key+'": ')
            if not key == "trinket" and not key == "neck" and not key == "finger" and not key == "back": #handle no materal separatly
                file.write('{\n')
                keymax2 = len(ValidItemsRows[key])
                keycount2 = 0
                for key2 in ValidItemsRows[key]:
                    keycount2 = keycount2 + 1
                    iMax = len(ValidItemsRows[key][key2])-1
                    file.write('\t\t\t"'+key2+'": [\n')
                    for i, row in enumerate(ValidItemsRows[key][key2]):
                        set = computeSet(int(row['item_set']),int(row['ilevel']))
                        classstring = ""
                        if not set == "": #Add class when there is an item set
                            classstring =', "class":"' + computeLegClass(int(row['class_mask'])) + '"'
                        file.write('\t\t\t\t'+printRow(row))
                        if not i == iMax:
                            file.write(',')
                        file.write('\n')
                    file.write('\t\t\t]')    
                    if not keycount2 == keymax2:
                        file.write(',')
                    file.write('\n')
                file.write('\t\t}') 
            else:
                file.write('[\n')
                iMax = len(ValidItemsRows[key])-1
                for i, row in enumerate(ValidItemsRows[key]):
                    set = computeSet(int(row['item_set']),int(row['ilevel']))
                    file.write('\t\t\t'+printRow(row))
                    if not i == iMax:
                        file.write(',')
                    file.write('\n')
                file.write('\t\t]')    
            if not keycount == keymax:
                file.write(',')
            file.write('\n')
        file.write('\t},\n')
        
        file.write('\t"legendaries": {\n')
        keyclassmax = len(ValidLegendariesRows)
        keyclasscount = 0
        
        for keyclass in ValidLegendariesRows:
            keyclasscount = keyclasscount + 1
            keytypeMax = len(ValidLegendariesRows[keyclass])
            keytypecount = 0
            file.write('\t\t"'+keyclass+'": {\n')
            
            for keytype in ValidLegendariesRows[keyclass]:
                keytypecount = keytypecount + 1
                file.write('\t\t\t"'+keytype+'": ')
                
                if not keytype == "trinket" and not keytype == "neck" and not keytype == "finger" and not keytype == "back": #handle no materal separatly
                    file.write('{\n')
                    keyMaterialmax = len(ValidLegendariesRows[keyclass][keytype])
                    keyMaterialmaxcount = 0
                    
                    for keyMaterial in ValidLegendariesRows[keyclass][keytype]:
                        keyMaterialmaxcount = keyMaterialmaxcount + 1
                        keyItemsMax = len(ValidLegendariesRows[keyclass][keytype][keyMaterial])-1
                        file.write('\t\t\t\t"'+keyMaterial+'": [\n')
                        
                        for i, row in enumerate(ValidLegendariesRows[keyclass][keytype][keyMaterial]):
                            set = computeSet(int(row['item_set']),int(row['ilevel']))
                            classstring = ""
                            if not set == "": #Add class when there is an item set
                                classstring =', "class":"' + computeLegClass(int(row['class_mask'])) + '"'
                            file.write('\t\t\t\t\t'+printRow(row))
                            if not i == keyItemsMax:
                                file.write(',')
                            file.write('\n')
                        file.write('\t\t\t\t]')    
                        if not keyMaterialmaxcount == keyMaterialmax:
                            file.write(',')
                        file.write('\n')
                    file.write('\t\t\t}') 
                else:
                    file.write('[\n')
                    keyItemsMax = len(ValidLegendariesRows[keyclass][keytype])-1
                    
                    for i, row in enumerate(ValidLegendariesRows[keyclass][keytype]):
                        set = computeSet(int(row['item_set']),int(row['ilevel']))
                        file.write('\t\t\t\t'+printRow(row))
                        if not i == keyItemsMax:
                            file.write(',')
                        file.write('\n')
                    file.write('\t\t\t]')
                    
                if not keytypecount == keytypeMax:
                    file.write(',')
                file.write('\n')
            file.write('\t\t}')    
            if not keyclasscount == keyclassmax:
                    file.write(',')
            file.write('\n')
        file.write('\t}\n')
        file.write('}\n')
