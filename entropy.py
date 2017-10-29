from math import log2
from util import Event
import logging as log
import pickle

from prob import Probability

from music21 import converter

def calculate(key, track, prob):
    h = [0] * 3

    tonic = key.tonic.name
    mode = key.type

    prev = Event.Rest()
    prev2 = Event.Rest()
    for event in track:
        if event.isNote:
            cur = Event.Note(tonic, event.name)
        elif event.isChord:
            cur = Event.Chord(tonic, map(lambda n: n.name, event.pitches))
        elif event.isRest:
            cur = Event.Rest()
        else:
            raise 'Invalid Type: ' + str(event)

        # event probability
        p = [0] * 3
        p[0] = prob.P(cur, mode)
        p[1] = prob.P((prev, cur), mode, 1)
        p[2] = prob.P((prev2, prev, cur), mode, 2)

        # update entropy
        for l in range(3):
            h[l] += p[l] * log2(p[l])

        # update previous
        prev2 = prev
        prev = cur

    return h

def calculate_from_file(filename, probability):
    song = converter.parse(filename)
    key = song.analyze('key')
    log.info(key)
    parts = list(song.parts)
    return calculate(key, parts[0].flat.notesAndRests, probability)

def main():
    with open('prob', 'rb') as input_file:
        p = pickle.load(input_file)

    h = calculate_from_file('songs/bwv537.mid', p)
    print(h)

if __name__ == '__main__':
    main()
