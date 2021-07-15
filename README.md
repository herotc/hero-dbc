# HeroDBC

[![GitHub license](https://img.shields.io/badge/license-EUPL-blue.svg)](https://raw.githubusercontent.com/herotc/hero-dbc/master/LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/herotc/hero-dbc)](https://github.com/herotc/hero-dbc/graphs/contributors)
[![GitHub forks](https://img.shields.io/github/forks/herotc/hero-dbc.svg)](https://github.com/herotc/hero-dbc/network)
[![GitHub stars](https://img.shields.io/github/stars/herotc/hero-dbc.svg)](https://github.com/herotc/hero-dbc/stargazers)\
[![GitHub issues](https://img.shields.io/github/issues/herotc/hero-dbc.svg)](https://github.com/herotc/hero-dbc/issues?q=is%3Aopen+is%3Aissue)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/herotc/hero-dbc)](https://github.com/herotc/hero-dbc/pulls?q=is%3Aopen+is%3Apr)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/herotc/hero-dbc)](https://github.com/herotc/hero-dbc/issues?q=is%3Aissue+is%3Aclosed)
[![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/herotc/hero-dbc)](https://github.com/herotc/hero-dbc/pulls?q=is%3Apr+is%3Aclosed)\
[![GitHub release](https://img.shields.io/github/v/release/herotc/hero-dbc)](https://github.com/herotc/hero-dbc/releases)
[![GitHub Release Date](https://img.shields.io/github/release-date/herotc/hero-dbc)](https://github.com/herotc/hero-dbc/releases)
[![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/herotc/hero-dbc/latest)](https://github.com/herotc/hero-dbc/commits/master)
[![GitHub last commit](https://img.shields.io/github/last-commit/herotc/hero-dbc)](https://github.com/herotc/hero-dbc/commits/master)

## AddOn

World of Warcraft AddOn to make info from DBC available in-game.\
It is used by [HeroLib](https://github.com/herotc/hero-lib) and [HeroRotation](https://github.com/herotc/hero-rotation).\
The project is hosted on [GitHub](https://github.com/herotc/hero-dbc).\
It is maintained by [Aethys](https://github.com/aethys256/) and the [HeroTC](https://github.com/herotc) team.\
Also, you can find it on [CurseForge](https://www.curseforge.com/wow/addons/herodbc).

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

The first thing to do is to replace the `HeroDBC/HeroDBC.toc` with the one from `HeroDBC/Dev/HeroDBC.toc`.  
Then check each filter code to see the instructions (inside `HeroDBC/Dev/Filter`),  
they use data from `HeroDBC/Dev/Unfiltered` and output has to be in `HeroDBC/Dev/Filtered` (you need to copy/paste from SavedVariables).

Once finished then you have to run the filter script (`python3 scripts/filter.py`).  
Do not forget to restore the original content of `HeroDBC.toc`file.
