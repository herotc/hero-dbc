#!/usr/bin/env python3

import argparse
import platform
from os import path

parser = argparse.ArgumentParser()
parser.add_argument("--realm", default='live', choices=['live', 'ptr', 'alpha', 'beta'],
                    help="World of Warcraft realm type (live, ptr, alpha, beta).")
args = parser.parse_args()

wowDirNames = {
    'live': 'World of Warcraft',
    'ptr': 'World of Warcraft Public Test',
    'alpha': 'World of Warcraft Alpha',
    'beta': 'World of Warcraft Beta'
}

realm = args.realm

# Try to determine wow directory
wowDirName = wowDirNames[realm]
wowDirPath = None
platformSystem = platform.system()
if platformSystem == 'Darwin':
    guessedWowDirPath = f'/Applications/{wowDirName}'
    if path.isdir(guessedWowDirPath):
        wowDirPath = path.normcase(guessedWowDirPath)
elif platformSystem == 'Windows':
    wowDirWindowsCommonPlaces = [
        '{}\{}',
        '{}\Program Files\{}',
        '{}\Program Files (x86)\{}',
        '{}\Games\{}'
    ]
    driveLetters = [chr(x) + ':' for x in range(65, 90) if path.exists(chr(x) + ':')]
    for driveLetter in driveLetters:
        for wowDirWindowsCommonPlace in wowDirWindowsCommonPlaces:
            guessedWowDirPath = wowDirWindowsCommonPlace.format(driveLetter, wowDirName)
            if path.isdir(guessedWowDirPath):
                wowDirPath = path.normcase(guessedWowDirPath)

if wowDirPath is not None:
    print(wowDirPath)
else:
    print('False')
