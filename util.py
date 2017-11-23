import math
import logging as log
import sys

LOG_LEVEL = log.WARNING
log.basicConfig(level=LOG_LEVEL)

# Constants
MAJOR = 'major'
MINOR = 'minor'
MODES = [MAJOR, MINOR]
MAJOR_DELTAS = [2, 2, 1, 2, 2, 2, 1]
MINOR_DELTAS = [2, 1, 2, 2, 1, 2, 2]
NOTES_TOTAL = 12
NOTES = {'A' : 10,
         'A#': 11, 'B-': 11,
         'B' : 12,
         'C' : 1,
         'C#': 2, 'D-': 2,
         'D' : 3,
         'D#': 4, 'E-': 4,
         'E' : 5,
         'F' : 6,
         'F#': 7, 'G-': 7,
         'G' : 8,
         'G#': 9, 'A-': 9}
NOTE = 'note'
DURATION = 'duration'
DELTA = 'delta'
MEASURES = [NOTE, DURATION, DELTA]
REST = -math.inf
MAX_LEVEL_COND = 3
MAX_LEVEL_DELTA = 3
FAKE_FILE = 'songs/bwv653.mid'
CUT = 0 # minimum of notes for the track to be considered
USE_CHORD = len(sys.argv) > 2 and sys.argv == 'chord'

def getMidiScaleMap(tonic, mode=MAJOR):
    final_map = [-1] * 130 
    id = NOTES[tonic] - 1
    final_map[id] = 0
    deltas = MAJOR_DELTAS if mode == MAJOR else MINOR_DELTAS
    d_id = 0
    while id < 128:
        id += 1
        if deltas[d_id] == 1:
            prev = final_map[id-1]
            final_map[id] = prev + 2
        elif deltas[d_id] == 2:
            prev = final_map[id-1]
            final_map[id] = prev + 1
            id += 1
            prev = final_map[id-1]
            final_map[id] = prev + 1
        d_id += 1
        d_id %= 7
    return final_map

def getNoteSequency(note, prev_notes, level):
    return tuple(prev_notes[MAX_LEVEL_COND-level:]) + (note,)

def getDelta(midi, prev_midi, level, midiMap):
    delta = midi - prev_midi[-level]
    # # delta = a - b
    # a = REST if midi == REST else midiMap[midi]
    # b = REST if prev_midi[-level] == REST else midiMap[prev_midi[-level]]
    # delta = a - b
    delta = abs(delta)
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
