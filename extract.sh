#!/usr/bin/env bash

HERODBCPATH=$(pwd)
SIMCPATH=$(dirname ${HERODBCPATH})/simc

cd ${SIMCPATH}/casc_extract
python casc_extract.py -m batch --cdn -o ${HERODBCPATH}/CDN

cd ${SIMCPATH}/dbc_extract3
OUTPATH=${HERODBCPATH}/DBC/generated
RUNFILE=dbc_extract.py
CACHEDIR="/Applications/World of Warcraft/Cache/ADB/enUS/DBCache.bin"

PATCH=8.0.1
BUILD=27178
INPATH=${HERODBCPATH}/CDN/${PATCH}.${BUILD}/DBFilesClient

python ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv ItemEffect > ${OUTPATH}/ItemEffect.csv
python ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv Spell > ${OUTPATH}/Spell.csv
python ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv SpellCooldowns > ${OUTPATH}/SpellCooldowns.csv
python ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv SpellRange > ${OUTPATH}/SpellRange.csv
python ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv SpellMisc > ${OUTPATH}/SpellMisc.csv
python ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv SpellEffect > ${OUTPATH}/SpellEffect.csv
python ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv SpellDuration > ${OUTPATH}/SpellDuration.csv
python ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv ItemSparse > ${OUTPATH}/ItemSparse.csv
python ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv GemProperties > ${OUTPATH}/GemProperties.csv
python ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv JournalEncounterItem > ${OUTPATH}/JournalEncounterItem.csv
python ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv SpellAuraOptions > ${OUTPATH}/SpellAuraOptions.csv
python ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv SpellProcsPerMinute > ${OUTPATH}/SpellProcsPerMinute.csv
python ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv SpellProcsPerMinuteMod > ${OUTPATH}/SpellProcsPerMinuteMod.csv
python ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv AzeriteEmpoweredItem > ${OUTPATH}/AzeriteEmpoweredItem.csv
python ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv AzeriteItem > ${OUTPATH}/AzeriteItem.csv
python ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv AzeritePower > ${OUTPATH}/AzeritePower.csv
python ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv AzeritePowerSetMember > ${OUTPATH}/AzeritePowerSetMember.csv
python ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv AzeriteTierUnlock > ${OUTPATH}/AzeriteTierUnlock.csv
python ${RUNFILE} -p ${INPATH} -b ${BUILD} --hotfix "${CACHEDIR}" -t csv SpecSetMember > ${OUTPATH}/SpecSetMember.csv

cd ${HERODBCPATH}
python parser/TriggerGCD.py
python parser/ProjectileSpeed.py
python parser/ItemRangeUnfiltered.py
python parser/ItemRangeFiltered.py
python parser/SpellMeleeRange.py
python parser/SpellTickTime.py
python parser/SpellDuration.py
python parser/ItemData.py
python parser/ItemSpell.py
python parser/RPPM.py
