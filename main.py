import logging as log
import os
import pickle
from prob import generate, MAJOR, MINOR
import entropy
from prob import Probability

import operator

log.basicConfig(filename='out.txt', filemode='w', level=log.DEBUG)

SONGS_FOLDER = 'songs'

def sorted_dict(d):
    return sorted(d.items(), key=operator.itemgetter(1))

def main():
    # p = generate(SONGS_FOLDER)
    # for x in sorted_dict(p.eventCount[MAJOR][2]):
    #     log.debug(x)
    # log.debug('------------------ total major: ' + str(p.total[MAJOR]))
    # for x in sorted_dict(p.eventCount[MINOR][2]):
    #     log.debug(x)
    # log.debug('------------------ total minor: ' + str(p.total[MINOR]))

    with open('prob', 'rb') as input_file:
        p = pickle.load(input_file)

    h = entropy.calculate_from_file('songs/bwv537.mid', p)
    log.debug(h)

if __name__ == '__main__':
    main()
