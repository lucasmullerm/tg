from math import isnan
import logging as log
import sys
from collections import defaultdict
from util import *
from music21 import converter

log.basicConfig(level=log.INFO)

# Constants
class Probability(object):
    def __init__(self):
        self.total = 0
        self.duration = defaultdict(int) # log2
        self.notes = [defaultdict(int) for i in range(MAX_LEVEL_COND)]
        self.deltas = [defaultdict(int) for i in range(MAX_LEVEL_DELTA)]

    def noteP(self, note, level=0): # note(index) or tuple [conditional]
        assert self.total
        if not level and not isinstance(note, tuple):
            note = (note,)
        return self.notes[level][note] / self.total

    def durationP(self, duration): # duration in quarterLength
        assert self.total
        return self.duration[duration] / self.total

    def deltaP(self, delta, level=1): # delta in pitch
        assert self.total
        assert level
        return self.deltas[level][delta] / self.total

    def P(self, event, measure=NOTE, level=0):
        if measure == NOTE:
            return self.noteP(event, level)
        elif measure == DURATION:
            return self.durationP(event)
        elif measure == DELTA:
            return self.deltaP(event, level)

    def addSong(self, song, cut=250):
        for part in song.parts:
            if len(part.flat) > cut:
                self.addTrack(part)

    @staticmethod
    def generate(filename):
        song = converter.parse(filename)
        # TODO: song key to be used
        # key = song.analyze('key')
        # log.info(key)
        p = Probability()
        p.addSong(song)
        return p

    def addTrack(self, track):
        store_total = self.total
        prev_notes = [REST] * MAX_LEVEL_COND
        prev_midi = [REST] * MAX_LEVEL_DELTA
        for event in track.flat.notesAndRests:
            self.total += 1
            dur = event.duration.quarterLength
            # TODO: use log or not
            # assert dur
            # dur = log2(dur)
            if event.isNote:
                note = NOTES[event.name]
                midi = event.pitch.midi
            if event.isRest:
                note = REST
                midi = REST
            elif event.isChord: # get root note
                note = NOTES[event.root().name]
                midi = event.root().midi

            # Add durationargs
            self.duration[dur] += 1

            # Add notes
            for lv in range(MAX_LEVEL_COND):
                cur = tuple(prev_notes[MAX_LEVEL_COND-lv:]) + (note,)
                self.notes[lv][cur] += 1

            # Add deltas
            for lv in range(1, MAX_LEVEL_DELTA):
                delta = midi - prev_midi[-lv]
                if isnan(delta):
                    delta = 0
                self.deltas[lv][delta] += 1

            # Update previous
            prev_notes = prev_notes[1:] + [note]
            prev_midi = prev_midi[1:] + [midi]

        log.info("Adding track with %d notes.", self.total - store_total)

def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else FAKE_FILE
    p = Probability.generate(filename)
    print()

if __name__ == '__main__':
    main()
