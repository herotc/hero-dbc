# hero-dbc

## AddOn

World of Warcraft AddOn to make info from DBC available in-game.

### Usage

```lua
local DBC = HeroDBC.DBC
local ItemRange = DBC.ItemRange

-- Do something with ItemRange.
```

## Extract

Extract infos from the DBC using SimulationCraft dbc_extract.

### Live

`python3 scripts/extract.py --wowrealm=live`

### PTR

`python3 scripts/extract.py --wowrealm=ptr`

### Beta

`python3 scripts/extract.py --wowrealm=beta`

### Alpha

`python3 scripts/extract.py --wowrealm=alpha`

### SimC Update

Update SimC: `python3 scripts/extract.py --wowrealm=xxx --simc`

## Process

In order to have accurate information for `.lua` DBC files, some filtering might be needed.

The first thing to do is to replace the `addon/HeroDBC.toc` with the one from `addon/Dev/HeroDBC.toc`.  
Then check each filter code to see the instructions (inside `addon/Dev/Filter`),  
they use data from `addon/Dev/Unfiltered` and output has to be in `addon/Dev/Filtered` (you need to copy/paste from SavedVariables).

Once finished then you have to run the filter script (`python3 scripts/filter.py`).  
Do not forget to restore the original content of `HeroDBC.toc`file.
