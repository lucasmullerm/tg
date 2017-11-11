from math import log2, inf
from collections import defaultdict
from util import NOTES

# Constants
MAX_LEVEL_COND = 2
MAX_LEVEL_DELTA = 2
REST_MIDI = -inf
class Probability(object):
    def __init__(self):
        self.total = 0
        self.duration = defaultdict(int) # log2
        self.notes = [defaultdict(int) for i in range(MAX_LEVEL_COND)]
        self.deltas = [defaultdict(int) for i in range(MAX_LEVEL_DELTA)]

    def noteP(self, note, level=0): # note(index) or tuple [conditional]
        assert self.total
        return self.notes[level][note] / self.total

    def durationP(self, duration): # duration in quarterLength
        assert self.total
        return self.duration[note] / self.total

    def deltaP(self, delta, level=1): # delta in pitch
        assert self.total
        assert self.level
        return self.deltas[level][delta] / self.total

    def add_track(self, track):
        store_total = self.total
        prev_notes = [REST_MIDI] * MAX_LEVEL_COND
        prev_midi = [REST_MIDI] * MAX_LEVEL_DELTA
        for event in track:
            self.total += 1
            dur = event.duration.quarterLength
            assert dur
            if event.isNote:
                note = NOTES[event.name]
                midi = event.pitch.midi
            if event.isRest:
                note = REST_MIDI
                midi = REST_MIDI
            elif event.isChord: # get root note
                note = NOTES[event.root().name]
                midi = event.root().midi

            # Add duration
            self.duration[dur] += 1

            # Add notes
            for l in range(MAX_LEVEL_COND):
                cur = tuple(notes[MAX_LEVEL_COND-1:]) + (note,)
                self.notes[l][cur] += 1

            # Add deltas
            for l in range(1, MAX_LEVEL_DELTA):
                delta = midi - prev_midi[-l]
                self.deltas[l][delta] += 1

            # Update previous
            prev_notes = prev_notes[1:] + [note]
            prev_midi = prev_midi[1:] + [midi]

        log.info("adding track with %d notes.".format(self.total - store_total))