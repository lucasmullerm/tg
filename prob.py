from collections import defaultdict
import logging as log

import config
from music21 import converter

log.basicConfig(level=log.INFO)

### CONSTANTS
FILE = config.files[0] + '.' + config.extension
MAJOR = 'major'
MINOR = 'minor'
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

class Event: # Note or Chord
    """
    Event is a note, chord or rest, with values relative to tonic.
    """
    def __init__(self, *args):
        self.value = args[0] if len(args) < 2 else tuple(sorted(args))

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other.value

class Probability:
    """
    Holds probability for events.
    Can add information from midi files.
    """
    def __init__(self):
        self.majorCount = [defaultdict(int) for i in range(3)]
        self.minorCount = [defaultdict(int) for i in range(3)]
        self.total = 0

    # event holds prev and prev2 if the case
    # level = notes before used to predict
    def P(self, event, mode, level):
        assert not level or len(event) == level + 1
        if mode == MAJOR:
            return self.majorCount[level][event] / self.total
        elif mode == MINOR:
            return self.minorCount[level][event] / self.total
        else:
            raise "Invalid mode: " + str(mode)

    def __getNoteNumber(self, tonic, note):
        noteSymbol = note.name
        num = NOTES[noteSymbol] - NOTES[tonic] + 1
        return num if num > 0 else num + 12

    def __include_part(self, part, key):
        tonic = key.tonic.name
        # Choose count dictionary
        if key.type == MAJOR:
            count = self.majorCount
        elif key.type == MINOR:
            count = self.minorCount
        else:
            raise 'did not recognize key'

        prev = 0
        prev2 = 0 #2nd previous
        for event in part.flat.notes:
            if event.isNote:
                num = self.__getNoteNumber(tonic, event)
            elif event.isChord:
                num = tuple(map(lambda x: self.__getNoteNumber(tonic, x), event.pitches))
            elif event.isRest:
                num = 0
            else:
                raise 'Invalid Type: ' + str(event)

            self.total += 1
            count[0][num] += 1
            count[1][(prev, num)] += 1
            count[2][(prev2, prev, num)] += 1

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

def main():
    p = Probability()
    p.include_file(FILE)
    print('end')

if __name__ == '__main__':
    main()
