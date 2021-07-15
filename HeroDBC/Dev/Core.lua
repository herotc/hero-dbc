--- ============================ HEADER ============================
--- ======= LOCALIZE =======
-- Addon
local addonName, HDBC = ...
-- File Locals
local Dev = {
  Lib = {},
  Filter = {},
  Utils = {},
}
local Utils = Dev.Utils

--- ======= GLOBALIZE =======
HDBC.Dev = Dev


--- ============================ CONTENT ============================

if not _G.HeroDBCDB then _G.HeroDBCDB = {} end
if not _G.HeroDBCDB.Filtered then _G.HeroDBCDB.Filtered = {} end

-- Print with HeroDBC Prefix
function Utils.Print(...)
    print("[|cFFFF6600Hero DBC|r]", ...)
end

function Utils.ValueIsInTable(Table, SearchValue)
  for _, Value in pairs(Table) do
    if Value == SearchValue then
      return true
    end
  end

  return false
end
