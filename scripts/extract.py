#!/usr/bin/env python3

from argparse import ArgumentParser
import datetime
import json
import math
import subprocess
from os import path, chdir, system, getcwd

parser = ArgumentParser()
parser.add_argument("--wowdir", dest="wowDir", help="Path to World of Warcraft directory.")
parser.add_argument("--wowrealm", dest="wowRealm", default='live', choices=['live', 'ptr', 'alpha', 'beta'],
                    help="World of Warcraft realm type (live, ptr, alpha, beta).")
parser.add_argument("--simc", action='store_true', dest='updateSimc', default=False,
                    help='Use it to also update simc data.')
args = parser.parse_args()

extractStartTime = math.floor(datetime.datetime.now().timestamp())

topLevelWorkingDir = path.dirname(getcwd())
scriptsDirPath = path.join(topLevelWorkingDir, 'hero-dbc', 'scripts')
cdnDirPath = path.join(scriptsDirPath, 'CDN')
dbcDirPath = path.join(scriptsDirPath, 'DBC')
simcDirPath = path.normpath(path.join(topLevelWorkingDir, '../simulationcraft/simc'))

realm = args.wowRealm

# Get wow directory path
wowDirPath = None
if args.wowDir is not None:
    wowDirPath = args.wowDir
    print(f'WoW directory passed as arg, using: "{wowDirPath}"')
else:
    wowDirFinderPath = path.join(scriptsDirPath, 'tools', 'wowDirFinder.py')
    wowDirFinderProc = subprocess.Popen(f'python3 {wowDirFinderPath}', stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT, shell=True)
    wowDirFinderResult = wowDirFinderProc.communicate()[0].decode().rstrip()
    if wowDirFinderResult == 'False':
        print('WoW directory not passed as arg and not found using wowDirFinder.')
    else:
        wowDirPath = wowDirFinderResult
        print(f'WoW directory not passed as arg, found using wowDirFinder: "{wowDirPath}"')

# Load tasks information (from hero-dbc/scripts/tasks.json)
with open(path.join(scriptsDirPath, 'tasks.json')) as tasksFile:
    tasks = json.load(tasksFile)

# CDN (using simc/casc_extract)
cascExtractCmd = f'python3 casc_extract.py -m batch --cdn -o {cdnDirPath}'
if realm != 'live':
    cascExtractCmd += f' --{realm}'
chdir(path.join(simcDirPath, 'casc_extract'))
system(cascExtractCmd)

# Find the wow version (using hero-dbc/scripts/tools/wowVersion.py)
chdir(path.join(scriptsDirPath, 'tools'))
wowVersionProc = subprocess.Popen(f'python3 wowVersion.py --cdnDirPath={cdnDirPath}', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
version = wowVersionProc.communicate()[0].decode().rstrip()
print(f'Using {version} client data from the CDN.')

# DBC (using simc/dbc_extract3)
chdir(path.join(simcDirPath, 'dbc_extract3'))

gameTablesInPath = path.normcase(f'{cdnDirPath}/{version}/GameTables')
clientDataInPath = path.normcase(f'{cdnDirPath}/{version}/DBFilesClient')

gtExtractCmd = f'python3 dbc_extract.py -p "{gameTablesInPath}" -b {version}'
dbcExtractCmd = f'python3 dbc_extract.py -p "{clientDataInPath}" -b {version}'

if wowDirPath is None:
    print('WoW directory not specified nor found, will not use hotfix file.')
else:
    if realm == 'ptr':
        hotfixFilePath = path.join(wowDirPath, '_ptr_', 'Cache', 'ADB', 'enUS', 'DBCache.bin')
    elif realm == 'beta':
        hotfixFilePath = path.join(wowDirPath, '_beta_', 'Cache', 'ADB', 'enUS', 'DBCache.bin')
    else:
        hotfixFilePath = path.join(wowDirPath, '_retail_', 'Cache', 'ADB', 'enUS', 'DBCache.bin')
    if path.isfile(hotfixFilePath):
        print(f'WoW hotfix file exists, using it from: "{hotfixFilePath}".')
        dbcExtractCmd += f' --hotfix="{hotfixFilePath}"'
    else:
        print('No WoW hotfix file found, will not use it.')

# simc
if args.updateSimc is True:
    print('Updating simc data...')
    simcGtExtractCmd = f'{gtExtractCmd} -t scale -o '
    simcDbcExtractCmd = f'{dbcExtractCmd} -t output '
    if realm == 'ptr':
        simcGtExtractCmd += f'{path.join(simcDirPath, "engine", "dbc", "generated", "sc_scale_data_ptr.inc")} --prefix=ptr'
        simcDbcExtractCmd += f'{path.join(simcDirPath, "dbc_extract3", "ptr.conf")} --prefix=ptr'
    else:
        simcGtExtractCmd += f'{path.join(simcDirPath, "engine", "dbc", "generated", "sc_scale_data.inc")}'
        simcDbcExtractCmd += f'{path.join(simcDirPath, "dbc_extract3", "live.conf")}'
    system(simcGtExtractCmd)
    system(simcDbcExtractCmd)

# hero-dbc
print('Updating hero-dbc data...')
clientDataOutPath = path.join(dbcDirPath, 'generated')
for dbfile in tasks['dbfiles']:
    print(f'Converting {dbfile} to CSV...')
    system(f'{dbcExtractCmd} -t csv {dbfile} > {path.join(clientDataOutPath, dbfile)}.csv')

# Parsers (using hero-dbc/scripts/parsers)
chdir(path.join(scriptsDirPath, 'parsers'))
print('Parsing client data from CSV...')
for parser in tasks['parsers']:
    print(f'Parsing {parser}...')
    system(f'python3 {parser}.py')

# Update .lua meta info (using hero-dbc/scripts/tools/luaMeta.py)
chdir(path.join(scriptsDirPath, 'tools'))
system(f'python3 luaMeta.py --mtime={extractStartTime} --version={version}')
