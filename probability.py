from math import log2
from collections import defaultdict
from util import NOTES

# Constants
MAX_LEVEL_COND = 2
MAX_LEVEL_DELTA = 2

class Probability(object):
    def __init__(self):
        self.total = 0
        self.duration = defaultdict(int) # log2
        self.notes = [defaultdict(int) for i in range(MAX_LEVEL_COND + 1)]
        self.delta = [defaultdict(int) for i in range(MAX_LEVEL_DELTA + 1)]

    def noteP(self, note, level=0): # note(index) or tuple [conditional]
        assert self.total
        return self.notes[level][note] / self.total

    def durationP(self, duration): # duration in quarterLength
        assert self.total
        return self.duration[note] / self.total

    def deltaP(self, delta, level=1): # delta in pitch
        assert self.total
        assert self.level
        return self.delta[level][note] / self.total
