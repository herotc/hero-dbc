#!/usr/bin/env python3

import argparse
import platform
from os import path

# Try to determine wow directory.
wowDirName = 'World of Warcraft'
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
elif platformSystem == 'Linux': # We assume we are using WSL.
    wowDirWindowsCommonPlaces = [
        '/mnt/{}/{}',
        '/mnt/{}/Program Files/{}',
        '/mnt/{}/Program Files (x86)/{}',
        '/mnt/{}/Games/{}'
    ]
    driveLetters = [chr(x) for x in range(97, 122) if path.exists('/mnt/' + chr(x))]
    for driveLetter in driveLetters:
        for wowDirWindowsCommonPlace in wowDirWindowsCommonPlaces:
            guessedWowDirPath = wowDirWindowsCommonPlace.format(driveLetter, wowDirName)
            if path.isdir(guessedWowDirPath):
                wowDirPath = path.normcase(guessedWowDirPath)

if wowDirPath is not None:
    print(wowDirPath)
else:
    print('False')
