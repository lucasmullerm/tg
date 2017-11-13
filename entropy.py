import logging as log
from math import log2
import sys
from music21 import converter
from probability import Probability
import util

def calculate(track, p):
    noteH = [list()] * util.MAX_LEVEL_COND
    durationH = []
    deltaH = [list()] * util.MAX_LEVEL_DELTA

    prev_notes = [util.REST] * util.MAX_LEVEL_COND
    prev_midi = [util.REST] * util.MAX_LEVEL_DELTA
    for event in track.flat.notesAndRests:
        dur = event.duration.quarterLength
        if event.isNote:
            note = util.NOTES[event.name]
            midi = event.pitch.midi
        if event.isRest:
            note = util.REST
            midi = util.REST
        elif event.isChord: # get root note
            note = util.NOTES[event.root().name]
            midi = event.root().midi

        # Duration
        pe = p.durationP(dur)
        durationH.append(-log2(pe))

        # Notes
        for lv in range(util.MAX_LEVEL_COND):
            cur = util.getNoteSequency(note, prev_notes, lv)
            pe = p.noteP(cur, lv)
            noteH[lv].append(-log2(pe))

        # Deltas
        for lv in range(1, util.MAX_LEVEL_DELTA):
            delta = util.getDelta(midi, prev_midi, lv)
            pe = p.deltaP(delta, lv)
            deltaH[lv].append(-log2(pe))

        # Update previous
        prev_notes = prev_notes[1:] + [note]
        prev_midi = prev_midi[1:] + [midi]

    return {
        util.NOTE: noteH,
        util.DURATION: durationH,
        util.DELTA: deltaH
    }

def calculateFromSong(song, cut=250):
    p = Probability()
    p.addSong(song)
    h = []
    for part in song.parts:
        if len(part.flat) > cut:
            h.append(calculate(part, p))
    return h

def calculateFromFile(filename, cut=250):
    song = converter.parse(filename)
    return calculateFromSong(song, cut)

def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else util.FAKE_FILE
    h = calculateFromFile(filename)
    print(h)
    log.info("%d parts.", len(h))

if __name__ == '__main__':
    main()
