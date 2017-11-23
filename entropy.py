import logging as log
from math import log2
import sys
from music21 import converter
from probability import Probability
import util

def mean(p):
    noteH = [0] * util.MAX_LEVEL_COND
    durationH = 0
    deltaH = [0] * util.MAX_LEVEL_DELTA

    # single probability
    for note in p.notes[0]:
        pn = p.noteP(note)
        noteH[0] -= pn * log2(pn)

    # conditional
    for x in p.notes[0]:
        x = x[0]
        for y in p.notes[0]:
            y = y[0]
            pxy = p.noteP((x,y), 1)
            px = p.noteP((x,))
            noteH[1] -= pxy * log2(pxy / px)

    for lv in range(util.MAX_LEVEL_DELTA):
        for note in p.deltas[lv]:
            pd = p.deltaP(note, lv)
            deltaH[lv] -= pd * log2(pd)

    for dur in p.duration:
        pd = p.durationP(dur)
        durationH -= pd * log2(pd)

    return {
        util.NOTE: noteH,
        util.DURATION: durationH,
        util.DELTA: deltaH
    }

def calculate(track, p, tonic, mode):
    noteH = [[] for i in range(util.MAX_LEVEL_COND)]
    durationH = []
    deltaH = [[] for i in range(util.MAX_LEVEL_DELTA)]

    midiMap = util.getMidiScaleMap(tonic, mode)

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
            if lv == 1:
                pe = pe / p.noteP(cur[0])
            noteH[lv].append(-log2(pe))

        # Deltas
        for lv in range(1, util.MAX_LEVEL_DELTA):
            delta = util.getDelta(midi, prev_midi, lv, midiMap)
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

def fromSong(song, cut=util.CUT, p=None):
    p = Probability()
    p.addSong(song, cut)
    h = []
    for part in song.parts:
        if len(part.flat) > cut:
            h.append(calculate(part, p))
    return h

def fromFile(filename, cut=util.CUT):
    song = converter.parse(filename)
    return fromSong(song, cut)

def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else util.FAKE_FILE
    song = converter.parse(filename)
    p = Probability()
    p.addSong(song)

    h = fromSong(song, p=p)
    print(h)
    log.info("%d parts.", len(h))

    h = mean(p)
    print(h)

if __name__ == '__main__':
    main()
