-- Plik doccli
-- Jeżeli aktywowano opcję pomijania, plik zostanie skopiowany do folderu ze skryptami mpv, jeśli nie to nie :D
-- To jeszcze nic nie robi


local mpv = require('mp')
local mpv_options = require("mp.options")

local options = { opening_start = -1, opening_end = -1, ending_start = -1, ending_end = -1 }
mpv_options.read_options(options, "doccli_skip")


local function skip()
    local current_time = mp.get_property_number("time-pos")

    if not current_time then
        return
    end

    if current_time >= options.opening_start + 2 and current_time < options.opening_start + 3 and options.opening_end ~= -1 then
        mp.set_property_number("time-pos", options.opening_end - 3)
    end

    if current_time >= options.ending_start + 2 and current_time < options.ending_start + 3 and options.ending_end ~= -1 then
        mp.set_property_number("time-pos", options.ending_end - 3)
    end
end

mp.observe_property("time-pos", "number", skip)