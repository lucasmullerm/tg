import logging as log
import os
import pickle
from prob import generate, MAJOR, MINOR
import entropy
from prob import Probability
import sys
from music21 import converter
import matplotlib.pyplot as plt

import operator
    # p = Probability()
    # for filename in os.listdir(directory):
    #     filepath = os.path.join(directory, filename)
    #     log.info(filepath)
    #     p.include_file(filepath)
    # # p.filter()
    # return p

# log.basicConfig(filename='out.txt', filemode='w', level=log.DEBUG)
log.basicConfig(level=log.DEBUG)

SONGS_FOLDER = 'songs'

def sorted_dict(d):
    return sorted(d.items(), key=operator.itemgetter(1))

def main(option, filename):
    # p = generate(SONGS_FOLDER)
    # for x in sorted_dict(p.eventCount[MAJOR][2]):
    #     log.debug(x)
    # log.debug('------------------ total major: ' + str(p.total[MAJOR]))
    # for x in sorted_dict(p.eventCount[MINOR][2]):
    #     log.debug(x)
    # log.debug('------------------ total minor: ' + str(p.total[MINOR]))

    # with open('prob', 'rb') as input_file:
    #     p = pickle.load(input_file)

    p = Probability()
    filepath = os.path.join('songs', filename)
    p.include_file(filepath)

    song = converter.parse(filepath)
    key = song.analyze('key')
    log.info(key)
    parts = list(song.parts)

    if option == 'duration':
        instH = entropy.calculate_inst_duration(key, parts[2].notesAndRests, p)
        h = entropy.calculate_all_duration(p)
        log.info(h)
        log.info(instH)
        plt.plot(instH)
        plt.savefig('duration/'+ filename[:-3] + 'jpg')
    elif option == 'diff':
        log.info(len(parts[2]))
        instH = entropy.calculate_inst_diff(key, parts[2].notesAndRests, p)
        h = entropy.calculate_all_diff(p)
        log.info(h)
        log.info(instH)
        plt.plot(instH)
        plt.savefig('diff/'+ filename[:-3] + 'jpg')


    # h = entropy.calculate_from_file('songs/bwv537.mid', p)
    # log.debug(h)

if __name__ == '__main__':
    option = sys.argv[1]
    filename = sys.argv[2][6:]
    log.info('option: ')
    log.info(option)
    log.info('filename: ')
    log.info(filename)
    main(option, filename)
