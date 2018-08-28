#!/usr/bin/env python3
import argparse
import datetime
import json
import subprocess
from os import path, chdir, system, getcwd, scandir
from distutils.version import StrictVersion

parser = argparse.ArgumentParser()
parser.add_argument("--wowdir", dest="wowDir", help="Path to World of Warcraft directory.")
parser.add_argument("--wowrealm", dest="wowRealm", default='live', choices=['live', 'ptr', 'alpha', 'beta'],
                    help="World of Warcraft realm type (live, ptr, alpha, beta).")
args = parser.parse_args()

topLevelWorkingDir = path.dirname(getcwd())
heroDbcDirPath = path.join(topLevelWorkingDir, 'hero-dbc')
simcDirPath = path.join(topLevelWorkingDir, 'simc')

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
chdir(path.join(simcDirPath, 'casc_extract'))
system(f'python casc_extract.py -m batch --cdn -o {cdnDirPath}')

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

gtExtractCmd = f'python dbc_extract.py -p "{gameTablesInPath}" -b {build}'
dbcExtractCmd = f'python dbc_extract.py -p "{clientDataInPath}" -b {build}'

if wowDirPath is None:
    print('WoW directory not specified nor found, will not use hotfix file.')
else:
    hotfixFilePath = path.join(wowDirPath, 'Cache', 'ADB', 'enUS', 'DBCache.bin')
    if path.isfile(hotfixFilePath):
        print(f'WoW hotfix file exists, using it from: "{hotfixFilePath}".')
        dbcExtractCmd += f' --hotfix="{hotfixFilePath}"'
    else:
        print('No WoW hotfix file found, will not use it.')

# simc
print('Updating simc data...')
system(f'{gtExtractCmd} -t scale -o {path.join(simcDirPath, "engine/dbc/generated/sc_scale_data.inc")}')
system(f'{dbcExtractCmd} -t output {path.join(simcDirPath, "dbc_extract3/live.conf")}')

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
