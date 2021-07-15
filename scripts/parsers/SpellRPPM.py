# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0301

"""
@author: Kutikuti
"""

import sys
import os
import csv
import operator
from collections import OrderedDict

generatedDir = os.path.join('scripts', 'DBC', 'generated')
addonEnumDir = os.path.join('HeroDBC', 'DBC')

os.chdir(os.path.join(os.path.dirname(sys.path[0]), '..', '..', 'hero-dbc'))


def computeRPPMType(x):
    return {
        1: 'HASTE',
        2: 'CRIT',
        3: 'CLASS',
        4: 'SPEC',
        5: 'RACE'
    }.get(x, '')


def computeClass(classmask):
    return {
        1: 1,
        2: 2,
        3: 4,
        4: 8,
        5: 16,
        6: 32,
        7: 64,
        8: 128,
        9: 256,
        10: 512,
        11: 1024,
        12: 2048
    }.get(classmask, 0)


def computeRace(racemask):
    return {
        1: 'Human',
        2: 'Orc',
        3: 'Dwarf',
        4: 'NightElf',
        5: 'Scourge',
        6: 'Tauren',
        7: 'Gnome',
        8: 'Troll',
        9: 'Goblin',
        10: 'BloodElf',
        11: 'Draenei',
        24: 'Pandaren',
        25: 'Pandaren',
        26: 'Pandaren',
        27: 'Nightborne',
        28: 'HighmountainTauren',
        29: 'VoidElf',
        30: 'LightforgedDraenei'
    }.get(racemask, '')


## Mapping
# id from itemEffect
# itemEffect.id_spell and SpellAuraOptions.idparent
# SpellAuraOptions.id_ppm and SpellProcsPerMinute.id
# SpellAuraOptions.id_ppm and SpellProcsPerMinuteMod.id_parent

# Get the RPPM list
BasePPM = {}
with open(os.path.join(generatedDir, 'SpellProcsPerMinute.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    for row in reader:
        BasePPM[int(row['id'])] = float(row['ppm'])

# Gets the ppm modifier list
ModPPM = {}
with open(os.path.join(generatedDir, 'SpellProcsPerMinuteMod.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    for row in reader:
        modType = computeRPPMType(int(row['unk_1']))  # Get the type of modifier
        if not computeRPPMType(int(row['unk_1'])) == '':  # If that is a type that we are interested in
            if int(row['id_parent']) not in ModPPM:
                ModPPM[int(row['id_parent'])] = {}
            if modType == 'HASTE' or modType == 'CRIT':  # Haste and crit modifier only have a boolean
                ModPPM[int(row['id_parent'])][int(row['unk_1'])] = True
            if modType == 'CLASS':  # for class mask , we have to iterate through the mask to determine which class it concerns
                racemask = int(row['id_chr_spec'])
                for i in range(12, 0, -1):
                    if racemask - computeClass(i) >= 0:
                        if int(row['unk_1']) not in ModPPM[int(row['id_parent'])]:
                            ModPPM[int(row['id_parent'])][int(row['unk_1'])] = {}
                        if i not in ModPPM[int(row['id_parent'])][int(row['unk_1'])]:
                            ModPPM[int(row['id_parent'])][int(row['unk_1'])][i] = {}
                        ModPPM[int(row['id_parent'])][int(row['unk_1'])][i] = BasePPM[int(row['id_parent'])] * (
                                    1.0 + float(row['coefficient']))  # Calcs the modified ppm
                        racemask = racemask - computeClass(i)
            if modType == 'SPEC' or modType == 'RACE':  # list all spec and give them the coefficient
                if int(row['unk_1']) not in ModPPM[int(row['id_parent'])]:
                    ModPPM[int(row['id_parent'])][int(row['unk_1'])] = {}
                if int(row['id_chr_spec']) not in ModPPM[int(row['id_parent'])][int(row['unk_1'])]:
                    ModPPM[int(row['id_parent'])][int(row['unk_1'])][int(row['id_chr_spec'])] = {}
                ModPPM[int(row['id_parent'])][int(row['unk_1'])][int(row['id_chr_spec'])] = BasePPM[int(
                    row['id_parent'])] * (1.0 + float(row['coefficient']))  # Calcs the modified ppm

# Get all the PPM id from a spell that comes from an item  
PPMID = {}
with open(os.path.join(generatedDir, 'SpellAuraOptions.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    reader = sorted(reader, key=lambda d: int(d['id_parent']))
    for row in reader:
        if not int(row['id_ppm']) == 0:  # Only if spell has a rppm
            PPMID[int(row['id_parent'])] = int(row['id_ppm'])

with open(os.path.join(addonEnumDir, 'SpellRPPM.lua'), 'w', encoding='utf-8') as file:
    file.write('HeroDBC.DBC.SpellRPPM = {\n')
    for _, itemRow in enumerate(PPMID):
        file.write('  [' + str(itemRow) + '] = {\n')

        # Write base RPPM
        file.write('    [0] = ' + str(BasePPM[PPMID[itemRow]]) + ',\n')

        if PPMID[itemRow] in ModPPM:
            # Write RPPM mods
            for _, modRow in enumerate(ModPPM[PPMID[itemRow]]):
                if type(ModPPM[PPMID[itemRow]][modRow]) == bool:
                    file.write('    [' + str(modRow) + '] = ' + ('true' if ModPPM[PPMID[itemRow]][modRow] else 'false') + ',\n')
                if type(ModPPM[PPMID[itemRow]][modRow]) == dict:
                    modDictRowMax = len(ModPPM[PPMID[itemRow]][modRow]) - 1
                    file.write('    [' + str(modRow) + '] = {\n')
                    for k, modDictRow in enumerate(ModPPM[PPMID[itemRow]][modRow]):
                        file.write(
                            '      [' + str(modDictRow) + '] = ' + str(ModPPM[PPMID[itemRow]][modRow][modDictRow]) + ',\n')
                    file.write('    },\n')
        file.write('  },\n')
    file.write('}\n')
