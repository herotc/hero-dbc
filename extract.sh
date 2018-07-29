cd ../simc/casc_extract
python3 casc_extract.py -m batch --cdn -o ../../hero-dbc/CDN

cd ../dbc_extract3
OUTPATH=../../hero-dbc/DBC/generated
RUNFILE=dbc_extract.py
# Escaped by "" due to spaces
CACHEDIR='/Applications/World of Warcraft/Cache/ADB/enUS/DBCache.bin'

PATCH=8.0.1
BUILD=27144
INPATH=../../hero-dbc/CDN/${PATCH}.${BUILD}/DBFilesClient
GTINPATH=../../hero-dbc/CDN/${PATCH}.${BUILD}/GameTables

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

cd ../../hero-dbc
python3 Parse_TriggerGCD.py
python3 Parse_ProjectileSpeed.py
python3 Parse_ItemRangeUnfiltered.py
python3 Parse_ItemRangeFiltered.py
python3 Parse_SpellMeleeRange.py
python3 Parse_SpellTickTime.py
python3 Parse_SpellDuration.py
python3 Parse_ItemData.py
python3 Parse_ItemSpell.py
python3 Parse_RPPM.py
