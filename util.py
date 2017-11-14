import math
import logging as log
import sys

log.basicConfig(level=log.INFO)

# Constants
MAJOR = 'major'
MINOR = 'minor'
MODES = [MAJOR, MINOR]
NOTES_TOTAL = 12
NOTES = {'A' : 1,
         'A#': 2, 'B-': 2,
         'B' : 3,
         'C' : 4,
         'C#': 5, 'D-': 5,
         'D' : 6,
         'D#': 7, 'E-': 7,
         'E' : 8,
         'F' : 9,
         'F#': 10, 'G-': 10,
         'G' : 11,
         'G#': 12, 'A-': 12}
NOTE = 'note'
DURATION = 'duration'
DELTA = 'delta'
MEASURES = [NOTE, DURATION, DELTA]
REST = -math.inf
MAX_LEVEL_COND = 3
MAX_LEVEL_DELTA = 3
FAKE_FILE = 'songs/bwv653.mid'
CUT = 250 # minimum of notes for the track to be considered
USE_CHORD = len(sys.argv) > 2 and sys.argv == 'chord'

def getNoteSequency(note, prev_notes, level):
    return tuple(prev_notes[MAX_LEVEL_COND-level:]) + (note,)

def getDelta(midi, prev_midi, level):
    delta = midi - prev_midi[-level]
    if math.isnan(delta):
        return 0
    return delta

def simplifyChord(chord):
    notes = map(lambda p: p.name, chord.pitches)
    unique_notes = set(notes)
    numbers = map(lambda n: NOTES[n], unique_notes)
    simplified = sorted(numbers)
    if len(simplified) == 1:
        return simplified[0]
    return tuple(simplified)
