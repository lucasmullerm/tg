import logging as log
import os
from prob import generate

import operator

log.basicConfig(filename='out.txt', filemode='w', level=log.DEBUG)

SONGS_FOLDER = 'songs'

def sorted_dict(d):
    return sorted(d.items(), key=operator.itemgetter(1))

def main():
    p = generate(SONGS_FOLDER)
    for x in sorted_dict(p.eventCount[0][0]):
        log.debug(x)
    log.debug('------------------ total minor: ' + str(p.total[0]))
    for x in sorted_dict(p.eventCount[1][0]):
        log.debug(x)
    log.debug('------------------ total major: ' + str(p.total[1]))

if __name__ == '__main__':
    main()
