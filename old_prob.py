"""
blablabla
"""

from music21 import converter
from music21 import midi

def getNote(pitch):
    return (pitch - 21) % 12

def getSongKey(filename):
    score = converter.parse(filename)
    key = score.analyze('key')
    scale = key.getScale()
    print('Scale:', scale.tonic.name)
    # print(key.tonic.name, key.mode)

def main():
    """
    blablabla
    """
    track = 'bwv539.mid'
    getSongKey(track)
    
    
    file = midi.MidiFile()
    file.open(track)
    file.read()

    count = {}
    pairs_count = {}

    prev_note = None
    for i, track in enumerate(file.tracks):
        if not i: continue # track 0 = header values

        aggregate = False
        for event in track.events():
            if event.isNoteOn():
                note = getNote(event.pitch)
                count[note] += 1
                if prev_note:
                    pairs_count[(prev_note, note)] += 1
                prev_note = note
            elif event.isNoteOff():
                pass
            elif event.isDeltaTime():
                if event.time > 0:
                    pass
                    


    # for track in file.tracks:
    #     print()
    #     for i in range(3):
    #         print(track.events[i])

    # print(file)

if __name__ == '__main__':
    main()
