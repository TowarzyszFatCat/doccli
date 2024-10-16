-- Plik doccli
-- Jeżeli aktywowano opcję pomijania, plik zostanie skopiowany do folderu ze skryptami mpv, jeśli nie to nie :D
-- To jeszcze nic nie robi


local mpv = require('mp')
local mpv_options = require("mp.options")

local options = { opening_start = 0, opening_end = 0, ending_start = 0, ending_end = 0 }
mpv_options.read_options(options, "skip")


local function skip()
    local current_time = mp.get_property_number("time-pos")

    if not current_time then
        return
    end

    if current_time >= options.opening_start + 2 and current_time < options.opening_start + 3 then
        mp.set_property_number("time-pos", options.opening_end - 2)
    end

    if current_time >= options.ending_start + 2 and current_time < options.ending_start + 3 then
        mp.set_property_number("time-pos", options.ending_end)
    end
end

mp.observe_property("time-pos", "number", skip)