cd C:\Users\Aethys\Documents\GitHub\AethysDBC
cd ..\simc\casc_extract
call py -3 casc_extract.py -m batch --cdn -o ..\..\AethysDBC\CDN

cd ..\dbc_extract3
set OUTPATH=..\..\AethysDBC\DBC\generated
set RUNFILE=dbc_extract.py
REM Escaped by "" due to spaces
set CACHEDIR="C:\Program Files (x86)\World of Warcraft\Cache\ADB\enUS"

set BUILD=24015
set INPATH=..\..\AethysDBC\CDN\7.2.0.%BUILD%\DBFilesClient
set GTINPATH=..\..\AethysDBC\CDN\7.2.0.%BUILD%\GameTables

py -3 %RUNFILE% -p %INPATH% -b %BUILD% --cache %CACHEDIR% -t csv SpellCooldowns > %OUTPATH%\SpellCooldowns.csv
