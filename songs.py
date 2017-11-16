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
RACHMANINOFF = "Sergei Rachmaninoff"
CHOPIN = "Frédéric Chopin"
PAGANINI = "Niccolò Paganini"
JOPLIN = "Scott Joplin"
ELLINGTON = "Duke Ellington "

ARTISTS = [MOZART,
           PAGANINI,
           CHOPIN,
           JOPLIN,
           ELLINGTON,
           ELVIS,
           JOBIM,
           BEATTLES,
           PINK_FLOYD,
           DREAM_THEATER,
           TAYLOR]

LIST = {
    BEATTLES: [ # midiworld.com
        ['let_it_be', 1970, 3, 700, 8, 334],
        ['come_together', 1969, 3, 700, 4, 268],
        ['here_comes_the_sun', 1969, 3, 414, 10, 120], # 3
        ['i_want_to_hold_your_hand', 1964, 4, 331],
        ['hey_jude', 1970, 1, 362],
    ],
    PINK_FLOYD: [ # midiworld.com
        ['wish_you_were_here', 1975, 2, 380],
        ['money', 1973, 4, 212, 11, 132, 6, 188],
        ['hey_you', 1979, 3, 219],
        ['brain_damage', 1973, 1, 296],
    ],
    MOZART: [ # midiworld.com
        ['sonata_11a', 1784, 1, 3884],
        ['sonata_11b', 1784, 1, 1689],
        ['alla_turca', 1784, 1, 1488],
        ['eine_kleine_nachtmusik', 1787, 1, 3024],
        ['krebsgang', 1785, 1, 826],
    ],
    TAYLOR: [ # freemidi.org
        ['blank_space', 2014, 4, 652], # 2
        ['shake_it_off', 2014, 10, 360],
        ['knew_you_were_trouble', 2012, 7, 1226], # 2
        ['you_belong_with_me', 2008, 1, 1034],
        ['22', 2012, 1, 1054],
    ],
    DREAM_THEATER: [ # freemidi.org
        ['pull_me_under', 1992, 1, 339, 2, 1446],
        ['the_dance_of_eternity', 1999, 5, 1781],
        ['panic_attack', 2005, 4, 262, 7, 340],
        ['overture_1928', 1999, 9, 245],
        ['forsaken', 2007, 8, 228, 5, 376], # 2
    ],
    JOBIM: [ # http://www.wersi-orgelstudio.de/midiecke.html
        ['wave', 1967, 1, 686],
        ['garota_de_ipanema', 1962, 1, 127],
        ['chega_de_saudade', 1958, 1, 216],
        ['desafinado', 1959, 1, 626],
        ['samba_de_uma_nota_so', 1960, 1, 332],
    ],
    ELVIS: [ # midiworld.com
        ['jailhouse_rock', 1957, 6, 802],
        ['hound_dog', 1956, 2, 263, 4, 79],
        ['all_shook_up', 1957, 4, 568],
        ['are_you_lonesome_tonight', 1969, 9, 218],
        ['teddy_bear', 1957, 4, 418],
    ],
    RACHMANINOFF: [ # midiworld.com
        ['concerto_1_1', 1890, 1, 8199],
        ['concerto_1_3', 1890, 1, 5409],
        ['russian_rhapsody', 1891, 4, 3024, 2, 2781],
        ['prelude_23_5', 1903, 1, 3734],
        ['prelude_32_3', 1910, 1, 1958],
    ],
    CHOPIN: [ # midiworld.com
        ['fantasie_49', 1841, 1, 3276], # F#m
        ['nocturne_37_2', 1839, 1, 2698], # G
        ['nocturne_48_1', 1841, 1, 3414], # Cmin
        ['waltze_70_2', 1832, 1, 1242], # Cmin
    ],
    PAGANINI: [ # http://en.midimelody.ru/paganini-nicolo/
        ['caprice_24', 1817, 1, 1718],
        ['caprice_1', 1817, 1, 1241],
        ['caprice_2', 1817, 1, 992],
        ['caprice_16', 1817, 1, 715],
        ['caprice_5', 1817, 1, 715],
    ],
    JOPLIN: [ # http://www.trachtman.org/ragtime/
        ['a_breeze_from_alabama', 1902, 1, 3372],
        ['the_easy_winners', 1901, 1, 2530],
        ['maple_leaf_rag', 1899, 1, 2380],
        ['peacherine_rag', 1901, 1, 2512],
    ],
    ELLINGTON: [ # http://en.midimelody.ru/ellington-duke/
        ['satin_doll', 1953, 1, 203],
        ['black_beauty', 1928, 2, 1124],
        ['take_the_a_train', 1939, 1, 269],
        ['mood_indigo', 1930, 1, 544],
        ['in_a_sentimental_mood', 1935, 1, 123],
    ],
}

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
