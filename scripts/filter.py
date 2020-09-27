#!/usr/bin/env python3

from argparse import ArgumentParser
import datetime
import json
import math
import subprocess
from os import path, chdir, system, getcwd

filterStartTime = math.floor(datetime.datetime.now().timestamp())

topLevelWorkingDir = path.dirname(getcwd())
heroDbcDirPath = path.join(topLevelWorkingDir, 'hero-dbc')
simcDirPath = path.normpath(path.join(topLevelWorkingDir, '../simulationcraft/simc'))

cdnDirPath = path.join(heroDbcDirPath, 'CDN')

# Load tasks information (from hero-dbc/scripts/tasks.json)
with open(path.join(heroDbcDirPath, 'scripts', 'tasks.json')) as tasksFile:
    tasks = json.load(tasksFile)

# Find the wow version (using hero-dbc/scripts/tools/wowVersion.py)
chdir(path.join(heroDbcDirPath, 'scripts', 'tools'))
wowVersionProc = subprocess.Popen([f'python3 wowVersion.py --cdnDirPath={cdnDirPath}'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
version = wowVersionProc.communicate()[0].decode().rstrip()

# Parsers (using hero-dbc/scripts/filters)
chdir(path.join(heroDbcDirPath, 'scripts', 'filters'))
print('Parsing client data from CSV...')
for filter in tasks['filters']:
    print(f'Filtering {filter}...')
    system(f'python3 {filter}.py')

# Update .lua meta info (using hero-dbc/scripts/tools/luaMeta.py)
chdir(path.join(heroDbcDirPath, 'scripts', 'tools'))
system(f'python3 luaMeta.py --mtime={filterStartTime} --version={version}')
