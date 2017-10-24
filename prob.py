from music21 import converter
import music21

FILE = "bwv539.mid"
MAJOR = 'major'
MINOR = 'minor'
NOTES = {'A' : 1,
         'A#': 2, 'B-': 2 ,
         'B' : 3,
         'C' : 4,
         'C#': 5, 'D-': 5, 
         'D' : 6,
         'D-': 7, 'E-': 7,
         'E' : 8,
         'F' : 9,
         'F#': 10, 'G-': 10,  
         'G' : 11,
         'G#': 12, 'A-': 12}

class Event: # Note or Chord
    def __init__(self, *args):
        self.value = args[0] if len(args) < 2 else tuple(sorted(args))

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other.value

class Probability:
    def __init__(self):
        self.majorCount = {}
        self.minorCount = {}
        self.total = 0

    def __getNoteNumber(self, tonic, note):
        # if note is rest
        num = NOTES[note] - NOTES[tonic] + 1
        return num if num > 0 else num + 12

    def __includePart(self, part, key):
        # tonic = key.tonic.name
        # Choose count dictionary
        if key.type == MAJOR:
            count = majorCount        
        elif key.type == MINOR:
            count = minorCount
        else:
            raise 'did not recognize key'

        for event in part.flat.notes:
            if event.isRest or event.isNote:
                num = self.__getNoteNumber()
            elif n is Chord:
                pass
            elif n is SingleNote: # or Rest
                pass
            else:
                raise 'Invalid Type: ' + str(n.type)


    def includeFile(self, filename):
        song = converter.parse(filename)
        key = song.analyze('key')
        parts = list(song.parts)
        self.__includePart(parts[0], key)
        if len(parts) > 1:
            self.__includePart(parts[1], key)



def main():
    pass

if __name__ == '__main__':
    main()