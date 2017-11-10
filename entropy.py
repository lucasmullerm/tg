from math import log2, inf
from util import Event
import logging as log
import pickle

from prob import Probability
from util import MAJOR, MINOR

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
            h[l] -= p[l] * log2(p[l])

        # update previous
        prev2 = prev
        prev = cur

    return h

def calculate_inst_duration(key, track, prob):
    instH = []

    tonic = key.tonic.name
    mode = key.type

    for event in track:
        dur = event.duration.quarterLength
        dur = -inf if dur == 0 else log2(dur)
        # event probability
        p = prob.durationP(dur)

        # update entropy
        instH.append(-p * log2(p))

    return instH

def calculate_inst_diff(key, track, prob):
    instH = []

    tonic = key.tonic.name
    mode = key.type

    prev = 0

    for event in track:
        if event.isNote:
            midi = event.pitch.midi
        elif event.isChord:
            midi = event.root().midi
        elif event.isRest:
            midi = 0
        else:
            raise 'Invalid Type: ' + str(event)
            
        # event probability
        p = prob.diffP(abs(midi-prev))

        # update entropy
        instH.append(-p * log2(p))

        prev = midi

    return instH

def calculate_from_file(filename, probability):
    song = converter.parse(filename)
    key = song.analyze('key')
    log.info(key)
    parts = list(song.parts)
    return calculate(key, parts[0].flat.notesAndRests, probability)

def calculate_all_duration(p):
    h = 0
    for e in p.eventCount[0]:
        pe = p.durationP(e)
        h -= pe * log2(pe)
    return h

def calculate_all_diff(p):
    h = 0
    for e in p.noteDiffCount:
        pe = p.diffP(e)
        h -= pe * log2(pe)
    return h

def calculate_all(p, mode=MAJOR, level=0, prev=0):
    h = 0
    prev = Event(prev)
    for e in p.eventCount[mode][0]:
        if level:
            ev = (prev, e)
            pe = p.P(ev, mode, 1)
        else:
            pe = p.P(e, mode)
        h -= pe * log2(pe)
    return h

def main():
    with open('prob', 'rb') as input_file:
        p = pickle.load(input_file)

    # h = calculate_from_file('songs/bwv537.mid', p)
    h = calculate_all(p, MAJOR)
    print(MAJOR, h)
    h = calculate_all(p, MINOR)
    print(MINOR, h)
    for prev in range(13):
        h = calculate_all(p, MAJOR, 1, prev)
        print(MAJOR, 'after', prev, h)
    for prev in range(13):
        h = calculate_all(p, MINOR, 1, prev)
        print(MINOR, 'after', prev, h)

if __name__ == '__main__':
    main()
