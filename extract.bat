cd ..\simc\casc_extract
call py -3 casc_extract.py -m batch --cdn -o ..\..\hero-dbc\CDN

cd ..\dbc_extract3
set OUTPATH=..\..\hero-dbc\DBC\generated
set RUNFILE=dbc_extract.py
REM Escaped by "" due to spaces
set CACHEDIR="C:\Program Files (x86)\World of Warcraft\Cache\ADB\enUS\DBCache.bin"

set PATCH=8.0.1
set BUILD=27178
set INPATH=..\..\hero-dbc\CDN\%PATCH%.%BUILD%\DBFilesClient

py -3 %RUNFILE% -p %INPATH% -b %BUILD% --hotfix %CACHEDIR% -t csv ItemEffect > %OUTPATH%\ItemEffect.csv
py -3 %RUNFILE% -p %INPATH% -b %BUILD% --hotfix %CACHEDIR% -t csv Spell > %OUTPATH%\Spell.csv
py -3 %RUNFILE% -p %INPATH% -b %BUILD% --hotfix %CACHEDIR% -t csv SpellCooldowns > %OUTPATH%\SpellCooldowns.csv
py -3 %RUNFILE% -p %INPATH% -b %BUILD% --hotfix %CACHEDIR% -t csv SpellRange > %OUTPATH%\SpellRange.csv
py -3 %RUNFILE% -p %INPATH% -b %BUILD% --hotfix %CACHEDIR% -t csv SpellMisc > %OUTPATH%\SpellMisc.csv
py -3 %RUNFILE% -p %INPATH% -b %BUILD% --hotfix %CACHEDIR% -t csv SpellEffect > %OUTPATH%\SpellEffect.csv
py -3 %RUNFILE% -p %INPATH% -b %BUILD% --hotfix %CACHEDIR% -t csv SpellDuration > %OUTPATH%\SpellDuration.csv
py -3 %RUNFILE% -p %INPATH% -b %BUILD% --hotfix %CACHEDIR% -t csv ItemSparse > %OUTPATH%\ItemSparse.csv
py -3 %RUNFILE% -p %INPATH% -b %BUILD% --hotfix %CACHEDIR% -t csv GemProperties > %OUTPATH%\GemProperties.csv
py -3 %RUNFILE% -p %INPATH% -b %BUILD% --hotfix %CACHEDIR% -t csv JournalEncounterItem > %OUTPATH%\JournalEncounterItem.csv
py -3 %RUNFILE% -p %INPATH% -b %BUILD% --hotfix %CACHEDIR% -t csv SpellAuraOptions > %OUTPATH%\SpellAuraOptions.csv
py -3 %RUNFILE% -p %INPATH% -b %BUILD% --hotfix %CACHEDIR% -t csv SpellProcsPerMinute > %OUTPATH%\SpellProcsPerMinute.csv
py -3 %RUNFILE% -p %INPATH% -b %BUILD% --hotfix %CACHEDIR% -t csv SpellProcsPerMinuteMod > %OUTPATH%\SpellProcsPerMinuteMod.csv
py -3 %RUNFILE% -p %INPATH% -b %BUILD% --hotfix %CACHEDIR% -t csv AzeriteEmpoweredItem > ${OUTPATH}/AzeriteEmpoweredItem.csv
py -3 %RUNFILE% -p %INPATH% -b %BUILD% --hotfix %CACHEDIR% -t csv AzeriteItem > ${OUTPATH}/AzeriteItem.csv
py -3 %RUNFILE% -p %INPATH% -b %BUILD% --hotfix %CACHEDIR% -t csv AzeritePower > ${OUTPATH}/AzeritePower.csv
py -3 %RUNFILE% -p %INPATH% -b %BUILD% --hotfix %CACHEDIR% -t csv AzeritePowerSetMember > ${OUTPATH}/AzeritePowerSetMember.csv
py -3 %RUNFILE% -p %INPATH% -b %BUILD% --hotfix %CACHEDIR% -t csv AzeriteTierUnlock > ${OUTPATH}/AzeriteTierUnlock.csv
py -3 %RUNFILE% -p %INPATH% -b %BUILD% --hotfix %CACHEDIR% -t csv SpecSetMember > ${OUTPATH}/SpecSetMember.csv

cd ..\..\hero-dbc
py -3 parser/TriggerGCD.py
py -3 parser/ProjectileSpeed.py
py -3 parser/ItemRangeUnfiltered.py
py -3 parser/ItemRangeFiltered.py
py -3 parser/SpellMeleeRange.py
py -3 parser/SpellTickTime.py
py -3 parser/SpellDuration.py
py -3 parser/ItemData.py
py -3 parser/ItemSpell.py
py -3 parser/RPPM.py
