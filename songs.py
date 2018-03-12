# index
FILE = 0
YEAR = 1
TRACK = 2
NOTES = 3

# artist index
BEATTLES = 'Beattles'
PINK_FLOYD = 'Pink Floyd'
MOZART = 'Wolfgang Mozart'
TAYLOR = 'Taylor Swift'
DREAM_THEATER = 'Dream Theater'
JOBIM = "Tom Jobim"
ELVIS = "Elvis Presley"
RACHMANINOFF = "S. Rachmaninoff"
CHOPIN = "Frédéric Chopin"
PAGANINI = "Niccolò Paganini"
JOPLIN = "Scott Joplin"
ELLINGTON = "Duke Ellington "

ARTISTS = [MOZART,
           PAGANINI,
           CHOPIN,
        #    RACHMANINOFF,
           JOPLIN,
           ELLINGTON,
           ELVIS,
           JOBIM,
           BEATTLES,
           PINK_FLOYD,
           DREAM_THEATER,
           TAYLOR]

class Song():
    def __init__(self, name, year, *tracks):
        self.name = name
        self.year = year
        self.tracks = tracks

LIST = {
    BEATTLES: [ # midiworld.com
        Song('i_want_to_hold_your_hand', 1964, 4, 331),
        Song('come_together', 1969, 3, 700, 4, 268),
        Song('here_comes_the_sun', 1969, 3, 414, 10, 120), # 3
        Song('hey_jude', 1970, 1, 362),
        Song('let_it_be', 1970, 3, 700, 8, 334),
    ],
    PINK_FLOYD: [ # midiworld.com
        Song('brain_damage', 1973, 1, 296),
        Song('money', 1973, 4, 212, 11, 132, 6, 188),
        Song('wish_you_were_here', 1975, 2, 380),
        Song('hey_you', 1979, 3, 219),
    ],
    MOZART: [ # midiworld.com
        Song('sonata_11a', 1784, 1, 3884),
        Song('sonata_11b', 1784, 1, 1689),
        Song('alla_turca', 1784, 1, 1488),
        Song('krebsgang', 1785, 1, 826),
        Song('eine_kleine_nachtmusik', 1787, 1, 3024),
    ],
    TAYLOR: [ # freemidi.org
        Song('you_belong_with_me', 2008, 1, 1034),
        Song('22', 2012, 1, 1054),
        Song('knew_you_were_trouble', 2012, 7, 1226), # 2
        Song('blank_space', 2014, 4, 652), # 2
        Song('shake_it_off', 2014, 10, 360),
    ],
    DREAM_THEATER: [ # freemidi.org
        Song('pull_me_under', 1992, 1, 339, 2, 1446),
        Song('overture_1928', 1999, 9, 245),
        Song('the_dance_of_eternity', 1999, 5, 1781),
        Song('panic_attack', 2005, 4, 262, 7, 340),
        Song('forsaken', 2007, 8, 228, 5, 376), # 2
    ],
    JOBIM: [ # http://www.wersi-orgelstudio.de/midiecke.html
        Song('chega_de_saudade', 1958, 1, 216),
        Song('desafinado', 1959, 1, 626),
        Song('samba_de_uma_nota_so', 1960, 1, 332),
        Song('garota_de_ipanema', 1962, 1, 127),
        Song('wave', 1967, 1, 686),
    ],
    ELVIS: [ # midiworld.com
        Song('hound_dog', 1956, 2, 263, 4, 79),
        Song('all_shook_up', 1957, 4, 568),
        Song('jailhouse_rock', 1957, 6, 802),
        Song('teddy_bear', 1957, 4, 418),
        Song('are_you_lonesome_tonight', 1969, 9, 218),
    ],
    RACHMANINOFF: [ # midiworld.com
        Song('concerto_1_1', 1890, 1, 8199),
        Song('concerto_1_3', 1890, 1, 5409),
        Song('russian_rhapsody', 1891, 4, 3024, 2, 2781),
        Song('prelude_23_5', 1903, 1, 3734),
        Song('prelude_32_3', 1910, 1, 1958),
    ],
    CHOPIN: [ # midiworld.com
        Song('waltze_70_2', 1832, 1, 1242), # Cmin
        Song('nocturne_37_2', 1839, 1, 2698), # G
        Song('fantasie_49', 1841, 1, 3276), # F#m
        Song('nocturne_48_1', 1841, 1, 3414), # Cmin
    ],
    PAGANINI: [ # http://en.midimelody.ru/paganini-nicolo/
        Song('caprice_1', 1817, 1, 1241),
        Song('caprice_2', 1817, 1, 992),
        Song('caprice_5', 1817, 1, 715),
        Song('caprice_16', 1817, 1, 715),
        Song('caprice_24', 1817, 1, 1718),
    ],
    JOPLIN: [ # http://www.trachtman.org/ragtime/
        Song('maple_leaf_rag', 1899, 1, 2380),
        Song('peacherine_rag', 1901, 1, 2512),
        Song('the_easy_winners', 1901, 1, 2530),
        Song('a_breeze_from_alabama', 1902, 1, 3372),
    ],
    ELLINGTON: [ # http://en.midimelody.ru/ellington-duke/
        Song('black_beauty', 1928, 2, 1124),
        Song('mood_indigo', 1930, 1, 544),
        Song('in_a_sentimental_mood', 1935, 1, 123),
        Song('take_the_a_train', 1939, 1, 269),
        Song('satin_doll', 1953, 1, 203),
    ],
}

# musescore.com
DESPACITO = Song('despacito', 2017, 0, 936)
SHAPE_OF_YOU = Song('shape_of_you', 2017, 0, 1552)
UPTOWN_FUNK = Song('uptown_funk', 2014, 0, 920)

def main():
    import matplotlib.pyplot as plt
    l = []
    for a in ARTISTS:
        for s in LIST[a]:
            l.append(s[YEAR])
    l.sort()
    plt.plot(l)
    plt.show()

if __name__ == '__main__':
    main()
