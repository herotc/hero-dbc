#!/usr/bin/env python3
import argparse
import datetime
import json
import subprocess
from os import path, chdir, system, getcwd, scandir

parser = argparse.ArgumentParser()
parser.add_argument("--wowdir", dest="wowDir", help="Path to World of Warcraft directory.")
parser.add_argument("--wowrealm", dest="wowRealm", default='live', choices=['live', 'ptr', 'alpha', 'beta'],
                    help="World of Warcraft realm type (live, ptr, alpha, beta).")
parser.add_argument("--simc", action='store_true', dest='updateSimc', default=False,
                    help='Use it to also update simc data.')
args = parser.parse_args()

topLevelWorkingDir = path.dirname(getcwd())
heroDbcDirPath = path.join(topLevelWorkingDir, 'hero-dbc')
simcDirPath = path.normpath(path.join(topLevelWorkingDir, '../simulationcraft/simc'))

realm = args.wowRealm
cdnDirPath = path.join(heroDbcDirPath, 'CDN')

# Get wow directory path
wowDirPath = None
if args.wowDir is not None:
    wowDirPath = args.wowDir
    print(f'WoW directory passed as arg, using: "{wowDirPath}"')
else:
    wowDirFinderProc = subprocess.Popen([f'python wowDirFinder.py --realm={realm}'], stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT, shell=True)
    wowDirFinderResult = wowDirFinderProc.communicate()[0].decode().rstrip()
    if wowDirFinderResult == 'False':
        print('WoW directory not passed as arg and not found using wowDirFinder.')
    else:
        wowDirPath = wowDirFinderResult
        print(f'WoW directory not passed as arg, found using wowDirFinder: "{wowDirPath}"')

# Load extract information (from hero-dbc/extract.json)
with open(path.join(heroDbcDirPath, 'extract.json')) as extractFile:
    extract = json.load(extractFile)

# CDN (using simc/casc_extract)
cascExtractCmd = f'python casc_extract.py -m batch --cdn -o {cdnDirPath}'
if realm != 'live':
    cascExtractCmd += f' --{realm}'
chdir(path.join(simcDirPath, 'casc_extract'))
system(cascExtractCmd)

patch, build = '1.0', '0'
with scandir(cdnDirPath) as iterator:
    for entry in iterator:
        entryName = entry.name
        if not entryName.startswith('.') and entry.is_dir():
            dirPartitions = entryName.rpartition('.')
            dirPatch, dirBuild = dirPartitions[0], dirPartitions[2]
            if int(dirBuild) > int(build):
                patch, build = dirPatch, dirBuild
version = f'{patch}.{build}'
print(f'Using {version} client data from the CDN.')

# DBC (using simc/dbc_extract3)
chdir(path.join(simcDirPath, 'dbc_extract3'))

gameTablesInPath = path.normcase(f'{cdnDirPath}/{version}/GameTables')
clientDataInPath = path.normcase(f'{cdnDirPath}/{version}/DBFilesClient')

gtExtractCmd = f'python dbc_extract.py -p "{gameTablesInPath}" -b {version}'
dbcExtractCmd = f'python dbc_extract.py -p "{clientDataInPath}" -b {version}'

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
        simcGtExtractCmd += f'{path.join(simcDirPath, "engine/dbc/generated/sc_scale_data_ptr.inc")} --prefix=ptr'
        simcDbcExtractCmd += f'{path.join(simcDirPath, "dbc_extract3/ptr.conf")} --prefix=ptr'
    else:
        simcGtExtractCmd += f'{path.join(simcDirPath, "engine/dbc/generated/sc_scale_data.inc")}'
        simcDbcExtractCmd += f'{path.join(simcDirPath, "dbc_extract3/live.conf")}'
    system(simcGtExtractCmd)
    system(simcDbcExtractCmd)

# hero-dbc
print('Updating hero-dbc data...')
clientDataOutPath = path.join(heroDbcDirPath, 'DBC', 'generated')
for dbfile in extract['dbfiles']:
    print(f'Converting {dbfile} to CSV...')
    system(f'{dbcExtractCmd} -t csv {dbfile} > {path.join(clientDataOutPath, dbfile)}.csv')

# Parsers (using hero-dbc/parser)
chdir(path.join(heroDbcDirPath, 'parser'))
print('Parsing client data from CSV...')
for parser in extract['parsers']:
    print(f'Parsing {parser}...')
    system(f'python {parser}.py')

# Prepend meta infos to every lua parsed files
luaMetas = f'-- Generated using WoW {version} client data on {datetime.datetime.now().isoformat()}.\n'
with scandir(path.join(heroDbcDirPath, 'DBC', 'parsed')) as iterator:
    for entry in iterator:
        entryName = entry.name
        if not entryName.startswith('.') and entryName.endswith('.lua') and entry.is_file():
            with open(entry.path, 'r') as entryFile:
                entryContent = entryFile.read()
            with open(entry.path, 'w') as entryFile:
                entryFile.write(luaMetas)
                entryFile.write(entryContent)
