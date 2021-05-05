# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/PadScale.py
# Compiled at: 2021-05-04 10:35:59
# Size of source mod 2**32: 3184 bytes
BASE_NOTE_FIX_COLOR = 71

class PadScale:
    __doc__ = ' scale '
    __module__ = __name__

    def __init__(self, name, notevalues, colorconverter=None):
        isinstance(notevalues, tuple)
        self.name = name
        self.notevalues = notevalues
        self._colorconverter = colorconverter
        self._scale_len = len(self.notevalues)
        rel_range = 64.0 / self._scale_len
        self._map = {}
        for idx, val in enumerate(notevalues):
            if val in self._map:
                self._map[val + 12] = idx
            else:
                self._map[val] = idx

        self.octave_range = int(10 - rel_range + 0.5)
        self._chromatic = len(notevalues) == 12
        if self.octave_range < 0:
            self.octave_range = 0
        self._note_to_grid_map = {}
        self._grid_to_note_map = list(range(8))

    def _next_scale_index(self, pitch, base_note, next_pitch_direction=0):
        inc = next_pitch_direction < 0 and -1 or 1
        next_pitch = pitch + inc
        while (next_pitch - base_note) % 12 not in self._map:
            next_pitch += inc

        return next_pitch

    def in_scale(self, note_value):
        return note_value in self.notevalues

    def transpose_by_scale(self, base_note, pitch, amount):
        inc = amount < 0 and -1 or 1
        newpitch = pitch + amount
        if self._chromatic:
            return newpitch
        while (newpitch - base_note) % 12 not in self._map:
            newpitch += inc

        return newpitch

    def inc_steps(self):
        if self._chromatic:
            return 8
        return 12

    def set_grid_map(self, base_note, start_pitch, next_pitch_direction=0):
        self._note_to_grid_map = {}
        base_grid_pitch = start_pitch
        start_pitch_index = (base_grid_pitch - base_note) % 12
        if start_pitch_index not in self._map:
            base_grid_pitch = self._next_scale_index(start_pitch, base_note, next_pitch_direction)
        pitch = base_grid_pitch
        count = 0
        while count < 8:
            index = (pitch - base_note) % 12
            if index in self._map:
                self._note_to_grid_map[pitch] = 7 - count
                self._grid_to_note_map[7 - count] = pitch
                count += 1
            pitch += 1

        return base_grid_pitch

    def convert_color(self, midi_note, base_note, color=(36, 39)):
        if midi_note % 12 != base_note:
            return color[1]
        return BASE_NOTE_FIX_COLOR

    def grid_row_to_note(self, row):
        assert row in range(8)
        return self._grid_to_note_map[row]

    def note_to_gridrow(self, note):
        if note in self._note_to_grid_map:
            return self._note_to_grid_map[note]
        return

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
