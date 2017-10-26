from collections import defaultdict
import logging as log
import os

import config
from music21 import converter

### CONSTANTS
MAJOR = 'major'
MINOR = 'minor'
SONGS_FOLDER = 'songs'
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
        self.majorCount = [defaultdict(int) for i in range(3)]
        self.minorCount = [defaultdict(int) for i in range(3)]
        self.majorTotal = [0] * 3
        self.minorTotal = [0] * 3

    def filter(self):
        for i in range(3):
            # major
            oldSize = len(self.majorCount[i])
            self.majorCount[i] = defaultdict(int, {k: v for k, v in self.majorCount[i].items() if v > 1})
            self.majorTotal[i] -= oldSize - len(self.majorCount[i])

            #minor
            oldSize = len(self.minorCount[i])
            self.minorCount[i] = defaultdict(int, {k: v for k, v in self.minorCount[i].items() if v > 1})
            self.minorTotal[i] -= oldSize - len(self.minorCount[i])

    # event holds prev and prev2 if the case
    # level = notes before used to predict
    def P(self, event, mode='major', level=0):
        assert not level or len(event) == level + 1
        if mode == MAJOR:
            return self.majorCount[level][event] / self.majorTotal[level]
        elif mode == MINOR:
            return self.minorCount[level][event] / self.minorTotal[level]
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
            for i in range(3):
                self.majorTotal[i] += len(part.flat.notes)
        elif key.type == MINOR:
            count = self.minorCount
            for i in range(3):
                self.minorTotal[i] += len(part.flat.notes)
        else:
            raise 'did not recognize key'

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
            count[0][num] += 1
            count[1][(prev, num)] += 1
            count[2][(prev2, prev, num)] += 1

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
