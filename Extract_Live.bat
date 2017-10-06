cd C:\Users\Aethys\Documents\GitHub\AethysDBC
cd ..\simc\casc_extract
call py -3 casc_extract.py -m batch --cdn -o ..\..\AethysDBC\CDN

cd ..\dbc_extract3
set OUTPATH=..\..\AethysDBC\DBC\generated
set RUNFILE=dbc_extract.py
REM Escaped by "" due to spaces
set CACHEDIR="C:\Program Files (x86)\World of Warcraft\Cache\ADB\enUS"

set PATCH=7.3.0
set BUILD=25195
set INPATH=..\..\AethysDBC\CDN\%PATCH%.%BUILD%\DBFilesClient
set GTINPATH=..\..\AethysDBC\CDN\%PATCH%.%BUILD%\GameTables

py -3 %RUNFILE% -p %INPATH% -b %BUILD% --cache %CACHEDIR% -t csv ItemEffect > %OUTPATH%\ItemEffect.csv
py -3 %RUNFILE% -p %INPATH% -b %BUILD% --cache %CACHEDIR% -t csv Spell > %OUTPATH%\Spell.csv
py -3 %RUNFILE% -p %INPATH% -b %BUILD% --cache %CACHEDIR% -t csv SpellCooldowns > %OUTPATH%\SpellCooldowns.csv
py -3 %RUNFILE% -p %INPATH% -b %BUILD% --cache %CACHEDIR% -t csv SpellRange > %OUTPATH%\SpellRange.csv
py -3 %RUNFILE% -p %INPATH% -b %BUILD% --cache %CACHEDIR% -t csv SpellMisc > %OUTPATH%\SpellMisc.csv
