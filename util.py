# Constants
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

def getNoteNumber(tonic, note):
    num = NOTES[note] - NOTES[tonic] + 1
    return num if num > 0 else num + NOTES_TOTAL

class Event: # Note Rest or Chord
    """
    Event is a note, chord or rest, with values relative to tonic.
    """
    def __init__(self, *args):
        if len(args) == 1:
            self.value = args[0]
            return
        fargs = tuple(sorted(set(args)))
        if len(fargs) == 1:
            self.value = fargs[0]
            return
        self.value = fargs

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()
