import logging as log
import os
from prob import generate

import operator

log.basicConfig(filename='out.txt', level=log.DEBUG)

SONGS_FOLDER = 'songs'

def sorted_dict(d):
    return sorted(d.items(), key=operator.itemgetter(1))

def main():
    p = generate(SONGS_FOLDER)
    for x in sorted_dict(p.minorCount[2]):
        log.debug(x)
    log.debug('------------------ total minor: ' + str(p.minorTotal))
    for x in sorted_dict(p.majorCount[2]):
        log.debug(x)
    log.debug('------------------ total major: ' + str(p.majorTotal))
        # log.info(str(x) + ': ' + str(p.minorCount[2][x]))

if __name__ == '__main__':
    main()
