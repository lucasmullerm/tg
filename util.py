# Constants
MAJOR = 'major'
MINOR = 'minor'
MODES = [MAJOR, MINOR]
NOTES_TOTAL = 12
NOTES = {'A' : 1,
         'A#': 2, 'B-': 2,
         'B' : 3,
         'C' : 4,
         'C#': 5, 'D-': 5,
         'D' : 6,
         'D#': 7, 'E-': 7,
         'E' : 8,
         'F' : 9,
         'F#': 10, 'G-': 10,
         'G' : 11,
         'G#': 12, 'A-': 12}
NOTE = 'note'
DURATION = 'duration'
DELTA = 'delta'
MEASURES = [NOTE, DURATION, DELTA]
REST = -inf

def getNoteNumber(tonic, note):
    num = NOTES[note] - NOTES[tonic] + 1
    return num if num > 0 else num + NOTES_TOTAL

def getChordNumbers(tonic, chord): #chord is a iterator of letters
    return map(lambda n: getNoteNumber(tonic, n), chord)

class Event: # Note Rest or Chord
    """
    Event is a note, chord or rest, with values relative to tonic.
    """
    def __init__(self, value):
        self.value = value

    @staticmethod
    def Note(tonic, note): #note is a letter
        return Event(getNoteNumber(tonic, note))

    @staticmethod
    def Rest():
        return Event(0)

    # @staticmethod
    # def Dist(prev, note): # prev and note are midi numbers
    #     return Event(0)

    @staticmethod
    def Chord(tonic, chord): #chord is iterable of letters
        chord_numbers = getChordNumbers(tonic, set(chord))
        chord_final = tuple(sorted(chord_numbers))
        if len(chord_final) == 1: # chord has only the same note
            return Event(chord_final[0])
        return Event(chord_final)

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()
