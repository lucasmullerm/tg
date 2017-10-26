from collections import defaultdict as ddict
import logging as log
import os

import config
from music21 import converter

### CONSTANTS
MAJOR = 'major'
MINOR = 'minor'
INDEX = {MAJOR: 0, MINOR: 1}
MODE_MAX = len(INDEX)
SONGS_FOLDER = 'songs'
THRESHOLD = 2
LEVEL_MAX = 3
NOTES_TOTAL = 12
NOTES = {'A' : 1,
         'A#': 2, 'B-': 2,
         'B' : 3,
         'C' : 4,
         'C#': 5, 'D-': 5,
         'D' : 6,
         'D-': 7, 'E-': 7,
         'E' : 8,
         'F' : 9,
         'F#': 10, 'G-': 10,
         'G' : 11,
         'G#': 12, 'A-': 12}

class Event: # Note Rest or Chord
    """
    Event is a note, chord or rest, with values relative to tonic.
    """
    def __init__(self, *args):
        self.value = args[0] if len(args) < 2 else tuple(sorted(set(args)))

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()

class Probability:
    """
    Holds probability for events.
    Can add information from midi files.
    """
    def __init__(self):
        # eventCount = [MAJOR, MINOR]
        self.eventCount = [[ddict(int) for l in range(LEVEL_MAX)] for m in range(MODE_MAX)]
        self.total = [[0] * LEVEL_MAX, [0] * LEVEL_MAX]

    def filter(self):
        for mode in range(MODE_MAX): # major, minor
            for level in range(LEVEL_MAX):
                oldSize = len(self.eventCount[mode][level])
                self.eventCount[mode][level] = ddict(int, {k: v for k, v in self.eventCount[mode][level].items() if v > THRESHOLD})
                self.total[mode][level] -= oldSize - len(self.eventCount[mode][level])

    # event holds prev and prev2 if the case
    # level = notes before used to predict
    def P(self, event, mode='major', level=0):
        assert not level or len(event) == level + 1
        mode = INDEX[mode]
        return self.eventCount[mode][level][event] / self.total[mode][level]

    def __getNoteNumber(self, tonic, note):
        noteSymbol = note.name
        num = NOTES[noteSymbol] - NOTES[tonic] + 1
        return num if num > 0 else num + NOTES_TOTAL

    def __include_part(self, part, key):
        tonic = key.tonic.name
        mode = INDEX[key.type]
        # update total number of events
        for level in range(LEVEL_MAX):
            self.total[mode][level] += len(part.flat.notes)

        prev = Event(0)
        prev2 = Event(0) #2nd previous

        # mapping from Note/Chord/Rest object to integers
        for event in part.flat.notes:
            if event.isNote:
                num = Event(self.__getNoteNumber(tonic, event))
            elif event.isChord:
                num = Event(*map(lambda x: self.__getNoteNumber(tonic, x), event.pitches))
            elif event.isRest:
                num = Event(0)
            else:
                raise 'Invalid Type: ' + str(event)

            # update counter for probabilities
            self.eventCount[mode][0][num] += 1
            self.eventCount[mode][1][(prev, num)] += 1
            self.eventCount[mode][2][(prev2, prev, num)] += 1

            # update previous
            prev2 = prev
            prev = num

    def include_file(self, filename):
        song = converter.parse(filename)
        key = song.analyze('key')
        log.info(key)
        parts = list(song.parts)
        self.__include_part(parts[0], key)
        if len(parts) > 1:
            self.__include_part(parts[1], key)

def generate(directory):
    p = Probability()
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        log.info(filepath)
        p.include_file(filepath)
    p.filter()
    return p

def main():
    generate(SONGS_FOLDER)
    log.info('end')

if __name__ == '__main__':
    main()
