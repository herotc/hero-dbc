#!/usr/bin/env python3

from argparse import ArgumentParser
from os import scandir

parser = ArgumentParser()
parser.add_argument("--cdnDirPath", dest="cdnDirPath", help="Path to the CDN folder.")
args = parser.parse_args()

cdnDirPath = args.cdnDirPath

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
print(version)
