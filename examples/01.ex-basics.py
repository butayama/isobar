#!/usr/bin/env python3

#------------------------------------------------------------------------
# isobar: ex-basics
# 
# Example of some basic functionality: Pattern transformations,
# sequences, randomness, scheduling and parameter mapping.
#------------------------------------------------------------------------

import isobar as iso

import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")

#------------------------------------------------------------------------
# Create a geometric series on a minor scale.
# PingPong plays the series forward then backward. PLoop loops forever.
#------------------------------------------------------------------------
arpeggio = iso.PSeries(0, 2, 6)
arpeggio = iso.PDegree(arpeggio, iso.Scale.minor) + 72
arpeggio = iso.PPingPong(arpeggio)
arpeggio = iso.PLoop(arpeggio)

#------------------------------------------------------------------------
# Create a velocity sequence, with emphasis every 4th note,
# plus a random walk to create gradual dynamic changes.
# Amplitudes are in the MIDI velocity range (0..127).
#------------------------------------------------------------------------
amplitude = iso.PSequence([50, 35, 25, 35]) + iso.PBrown(0, 1, -20, 20)

#------------------------------------------------------------------------
# Create a repeating sequence with scalar transposition:
# [ 36, 38, 43, 39, 36, 38, 43, 39, ... ]
#------------------------------------------------------------------------
bassline = iso.PSequence([0, 2, 7, 3]) + 36

#------------------------------------------------------------------------
# Repeat each note 3 times, and transpose each into a different octave
# [ 36, 48, 60, 38, 50, 62, ... ]
#------------------------------------------------------------------------
bassline = iso.PStutter(bassline, 3) + iso.PSequence([0, 12, 24])

#------------------------------------------------------------------------
# A Timeline schedules events at a given BPM.
# by default, send these over the first MIDI output.
#------------------------------------------------------------------------
output = iso.io.midi.MidiOut()
timeline = iso.Timeline(120, output)

#------------------------------------------------------------------------
# Schedule events, with properties mapped to the Pattern objects.
#------------------------------------------------------------------------
timeline.schedule({
    iso.EVENT_NOTE: arpeggio,
    iso.EVENT_DURATION: 0.25,
    iso.EVENT_AMPLITUDE: amplitude
})
timeline.schedule({
    iso.EVENT_NOTE: bassline,
    iso.EVENT_DURATION: 1
})

timeline.run()