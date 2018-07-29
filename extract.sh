#!/usr/bin/env bash

HERODBCPATH=$(pwd)
SIMCPATH=$(dirname ${HERODBCPATH})/simc

cd ${SIMCPATH}/casc_extract
python3 casc_extract.py -m batch --cdn -o ${HERODBCPATH}/CDN

cd ${SIMCPATH}/dbc_extract3
OUTPATH=${HERODBCPATH}/DBC/generated
RUNFILE=dbc_extract.py
CACHEDIR="/Applications/World of Warcraft/Cache/ADB/enUS/DBCache.bin"

PATCH=8.0.1
BUILD=27178
INPATH=${HERODBCPATH}/CDN/${PATCH}.${BUILD}/DBFilesClient
GTINPATH=${HERODBCPATH}/CDN/${PATCH}.${BUILD}/GameTables

python3 ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv ItemEffect > ${OUTPATH}/ItemEffect.csv
python3 ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv Spell > ${OUTPATH}/Spell.csv
python3 ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv SpellCooldowns > ${OUTPATH}/SpellCooldowns.csv
python3 ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv SpellRange > ${OUTPATH}/SpellRange.csv
python3 ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv SpellMisc > ${OUTPATH}/SpellMisc.csv
python3 ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv SpellEffect > ${OUTPATH}/SpellEffect.csv
python3 ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv SpellDuration > ${OUTPATH}/SpellDuration.csv
python3 ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv ItemSparse > ${OUTPATH}/ItemSparse.csv
python3 ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv GemProperties > ${OUTPATH}/GemProperties.csv
python3 ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv JournalEncounterItem > ${OUTPATH}/JournalEncounterItem.csv
python3 ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv SpellAuraOptions > ${OUTPATH}/SpellAuraOptions.csv
python3 ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv SpellProcsPerMinute > ${OUTPATH}/SpellProcsPerMinute.csv
python3 ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv SpellProcsPerMinuteMod > ${OUTPATH}/SpellProcsPerMinuteMod.csv
python3 ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv AzeriteEmpoweredItem > ${OUTPATH}/AzeriteEmpoweredItem.csv
python3 ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv AzeriteItem > ${OUTPATH}/AzeriteItem.csv
python3 ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv AzeritePower > ${OUTPATH}/AzeritePower.csv
python3 ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv AzeritePowerSetMember > ${OUTPATH}/AzeritePowerSetMember.csv
python3 ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv AzeriteTierUnlock > ${OUTPATH}/AzeriteTierUnlock.csv
python3 ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv SpecSetMember > ${OUTPATH}/SpecSetMember.csv

cd ${HERODBCPATH}
python3 parser/TriggerGCD.py
python3 parser/ProjectileSpeed.py
python3 parser/ItemRangeUnfiltered.py
python3 parser/ItemRangeFiltered.py
python3 parser/SpellMeleeRange.py
python3 parser/SpellTickTime.py
python3 parser/SpellDuration.py
python3 parser/ItemData.py
python3 parser/ItemSpell.py
python3 parser/RPPM.py
