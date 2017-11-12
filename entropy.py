from math import log2, isnan
from util import *

def instant(track, p):
    noteH = [] * MAX_LEVEL_COND
    durationH = []
    deltaH = [] * MAX_LEVEL_DELTA

    prev_notes = [REST] * MAX_LEVEL_COND
    prev_midi = [REST] * MAX_LEVEL_DELTA
    for event in track.flat.notesAndRests:
        dur = event.duration.quarterLength
        if event.isNote:
            note = NOTES[event.name]
            midi = event.pitch.midi
        if event.isRest:
            note = REST
            midi = REST
        elif event.isChord: # get root note
            note = NOTES[event.root().name]
            midi = event.root().midi

        # Duration
        pdr = p.durationP(dur)
        durationH.append(pdr * log2(pdr))

        # Notes
        for lv in range(MAX_LEVEL_COND):
            cur = getNoteSequency(note, prev_notes, lv)
            pn = p.noteP(cur, lv)
            noteH[lv].append(pn * log2(pn))

        # Deltas
        for lv in range(1, MAX_LEVEL_DELTA):
            delta = getDelta(midi, prev_midi, lv)
            pd = p.deltaP(delta, lv)
            deltaH[lv].append(pd * log2(pd))

        # Update previous
        prev_notes = prev_notes[1:] + [note]
        prev_midi = prev_midi[1:] + [midi]

    return {
        NOTE: noteH,
        DURATION: durationH,
        DELTA: deltaH
    }

def main():
    pass

if __name__ == '__main__':
    main()
