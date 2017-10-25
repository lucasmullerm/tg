import logging as log
import os
from prob import generate

log.basicConfig(filename='out.txt', level=log.DEBUG)

SONGS_FOLDER = 'songs'

def main():
    p = generate(SONGS_FOLDER)
    for x in p.minorCount[0]:
        log.info(str(x) + ': ' + str(p.minorCount[0][x]))

if __name__ == '__main__':
    main()
