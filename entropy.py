from math import log2
import util

def instant(track, p):
    noteH = [] * util.MAX_LEVEL_COND
    durationH = []
    deltaH = [] * util.MAX_LEVEL_DELTA

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
        pdr = p.durationP(dur)
        durationH.append(pdr * log2(pdr))

        # Notes
        for lv in range(util.MAX_LEVEL_COND):
            cur = util.getNoteSequency(note, prev_notes, lv)
            pn = p.noteP(cur, lv)
            noteH[lv].append(pn * log2(pn))

        # Deltas
        for lv in range(1, util.MAX_LEVEL_DELTA):
            delta = util.getDelta(midi, prev_midi, lv)
            pd = p.deltaP(delta, lv)
            deltaH[lv].append(pd * log2(pd))

        # Update previous
        prev_notes = prev_notes[1:] + [note]
        prev_midi = prev_midi[1:] + [midi]

    return {
        util.NOTE: noteH,
        util.DURATION: durationH,
        util.DELTA: deltaH
    }

def main():
    pass

if __name__ == '__main__':
    main()
