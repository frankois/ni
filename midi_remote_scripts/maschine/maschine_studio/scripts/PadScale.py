# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_Studio/PadScale.py
# Compiled at: 2021-04-30 12:12:38
# Size of source mod 2**32: 814 bytes


class PadScale:
    __doc__ = ' scale '
    __module__ = __name__

    def __init__(self, name, notevalues):
        isinstance(notevalues, tuple)
        self.name = name
        self.notevalues = notevalues
        scale_len = len(self.notevalues)
        rel_range = 16.0 / scale_len
        self.octave_range = int(10 - rel_range + 0.5)
        if self.octave_range < 0:
            self.octave_range = 0

    def to_octave(self, value):
        if self.octave_range == 0:
            return 0
        return int(value * self.octave_range)

    def to_relative(self, value, prev):
        if self.octave_range == 0:
            return prev
        relvalue = value / float(self.octave_range)
        if relvalue > 1.0:
            return 1.0
        if relvalue < 0.0:
            return 0.0
        return relvalue
# okay decompiling src/PadScale.pyc
