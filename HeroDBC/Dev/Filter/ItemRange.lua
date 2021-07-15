--- ============================ HEADER ============================
--- ======= LOCALIZE =======
-- Addon
local addonName, HDBC = ...
local DBC = HDBC.DBC
local Filter = HDBC.Dev.Filter
local Utils = HDBC.Dev.Utils
-- Lua
local IsItemInRange = IsItemInRange
local tableinsert = table.insert
-- File Locals
local Vars = {
  Iterations = nil, -- { Current, Max }
  ItemRangeFiltered = nil, -- { [Type] = { [Reaction] = { RangeIndex = { [1] = Range, [2] = Range, [3] = ... }, ItemRange = { [Range] = { [1] = ItemID, [2] = ItemId, [3] = ... } } } } }
}


--- ============================ CONTENT ============================

--- USE WHAT IS BELOW ONLY IF YOU KNOW WHAT YOU'RE DOING ---
-- Run ManuallyFilterItemRanges() while standing at less than 1yds from an hostile target and the same for a friendly focus (easy with dummies like the ones in Orgrimmar)
-- Keep running this function until you get the message in the chat saying that the filtering is done.
-- Due to some issues with the Blizzard API we need to do multiple iterations on different frame (ideally do one call each 3-5secs)
function Filter.ItemRange()
  local Iterations = Vars.Iterations

  if not Iterations then
    -- Init
    Iterations = { Current = 0, Max = 15 }
    Vars.Iterations = Iterations

    Vars.ItemRangeFiltered = {
      Melee = {
        Hostile = { RangeIndex = {}, ItemRange = {} },
        Friendly = { RangeIndex = {}, ItemRange = {} },
      },
      Ranged = {
        Hostile = { RangeIndex = {}, ItemRange = {} },
        Friendly = { RangeIndex = {}, ItemRange = {} },
      }
    }
    Utils.Print('ItemRange filter initialized.')
  else
    -- Done
    if Iterations.Current == Iterations.Max then
      Utils.Print('ItemRange filter is done, /reload if you want to do it again.')
      return
    end
  end

  -- Locals
  local ItemRangeFiltered = Vars.ItemRangeFiltered
  local MeleeTable, RangedTable = ItemRangeFiltered.Melee, ItemRangeFiltered.Ranged
  local MHostileTable, MFriendlyTable = MeleeTable.Hostile, MeleeTable.Friendly
  local MHTItemRange, MHTRangeIndex = MHostileTable.ItemRange, MHostileTable.RangeIndex
  local MFTItemRange, MFTRangeIndex = MFriendlyTable.ItemRange, MFriendlyTable.RangeIndex
  local RHostileTable, RFriendlyTable = RangedTable.Hostile, RangedTable.Friendly
  local RHTItemRange, RHTRangeIndex = RHostileTable.ItemRange, RHostileTable.RangeIndex
  local RFTItemRange, RFTRangeIndex = RFriendlyTable.ItemRange, RFriendlyTable.RangeIndex

  -- Inside a given frame, we do 5 iterations.
  for i = 1, 5 do
    -- Filter items that can only be casted on an unit. (i.e. blacklist ground targeted aoe items)
    for Type, Ranges in pairs(DBC.ItemRangeUnfiltered) do
      local HTItemRange = Type == "Melee" and MHTItemRange or RHTItemRange
      local HTRangeIndex = Type == "Melee" and MHTRangeIndex or RHTRangeIndex
      local FTItemRange = Type == "Melee" and MFTItemRange or RFTItemRange
      local FTRangeIndex = Type == "Melee" and MFTRangeIndex or RFTRangeIndex

      for Range, ItemIDs in pairs(Ranges) do
        -- RangeIndex
        Range = tostring(Range) -- The parser assume a string that's why we convert it to a string

        for j = 1, #ItemIDs do
          local ItemID = ItemIDs[j]

          -- Hostile filter
          if IsItemInRange(ItemID, "target") then
            -- Make the Range table if it doesn't exist yet
            if not HTItemRange[Range] then
              HTItemRange[Range] = {}
              tableinsert(HTRangeIndex, Range)
            end
            -- Check if the item isn't already inserted since we do multiple passes then insert it
            if not Utils.ValueIsInTable(HTItemRange[Range], ItemID) then
              tableinsert(HTItemRange[Range], ItemID)
            end
          end

          -- Friendly filter
          if IsItemInRange(ItemID, "focus") then
            -- Make the Range table if it doesn't exist yet
            if not FTItemRange[Range] then
              FTItemRange[Range] = {}
              tableinsert(FTRangeIndex, Range)
            end
            -- Check if the item isn't already inserted since we do multiple passes
            if not Utils.ValueIsInTable(FTItemRange[Range], ItemID) then
              tableinsert(FTItemRange[Range], ItemID)
            end
          end
        end
      end
    end
  end

  -- Increment the pass counter
  Iterations.Current = Iterations.Current + 1

  if Iterations.Current == Iterations.Max then
    -- Encode in JSON the content (JSON is used since it's easier to work with)
    MHostileTable.ItemRange = Utils.JSON.encode(MHTItemRange)
    MHostileTable.RangeIndex = Utils.JSON.encode(MHTRangeIndex)
    MFriendlyTable.ItemRange = Utils.JSON.encode(MFTItemRange)
    MFriendlyTable.RangeIndex = Utils.JSON.encode(MFTRangeIndex)
    RHostileTable.ItemRange = Utils.JSON.encode(RHTItemRange)
    RHostileTable.RangeIndex = Utils.JSON.encode(RHTRangeIndex)
    RFriendlyTable.ItemRange = Utils.JSON.encode(RFTItemRange)
    RFriendlyTable.RangeIndex = Utils.JSON.encode(RFTRangeIndex)

    -- Pass it to SavedVariables
    _G.HeroDBCDB.Filtered.ItemRange = ItemRangeFiltered
    Utils.Print('ManuallyFilterItemRanges done.')
  else
    Utils.Print('ManuallyFilterItemRanges still needs ' .. Iterations.Max - Iterations.Current .. ' iteration(s).')
  end
end
