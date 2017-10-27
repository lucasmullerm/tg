from collections import defaultdict as ddict
import logging as log
import os

from util import Event, getNoteNumber
from music21 import converter

### CONSTANTS
MAJOR = 'major'
MINOR = 'minor'
MODES = [MAJOR, MINOR]
SONGS_FOLDER = 'songs'
THRESHOLD = 2
LEVEL_MAX = 3

class Probability:
    """
    Holds probability for events.
    Can add information from midi files.
    """
    def __init__(self):
        # eventCount = [MAJOR, MINOR]
        self.eventCount = {m: [ddict(int) for l in range(LEVEL_MAX)] for m in MODES}
        self.total = {m: [0] * LEVEL_MAX for m in MODES}

    def filter(self):
        for mode in MODES:
            for level in range(LEVEL_MAX):
                oldSize = len(self.eventCount[mode][level])
                self.eventCount[mode][level] = ddict(int, {k: v for k, v in self.eventCount[mode][level].items() if v > THRESHOLD})
                self.total[mode][level] -= oldSize - len(self.eventCount[mode][level])

    # event holds prev and prev2 if the case
    # level = notes before used to predict
    def P(self, event, mode=MAJOR, level=0):
        assert not level or len(event) == level + 1
        return self.eventCount[mode][level][event] / self.total[mode][level]

    def __include_part(self, part, key):
        tonic = key.tonic.name
        mode = key.type
        # update total number of events
        for level in range(LEVEL_MAX):
            self.total[mode][level] += len(part.flat.notes)

        prev = Event(0)
        prev2 = Event(0) #2nd previous

        # mapping from Note/Chord/Rest object to integers
        for event in part.flat.notesAndRests:
            if event.isNote:
                num = Event(getNoteNumber(tonic, event.name))
            elif event.isChord:
                num = Event(*map(lambda n: getNoteNumber(tonic, n.name), event.pitches))
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
