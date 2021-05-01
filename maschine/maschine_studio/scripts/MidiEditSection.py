# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_Studio/MidiEditSection.py
# Compiled at: 2021-04-30 12:12:38
# Size of source mod 2**32: 13406 bytes
import Live
import _Framework.CompoundComponent as CompoundComponent
from _Framework.InputControlElement import *
import _Framework.ButtonElement as ButtonElement
import _Framework.SliderElement as SliderElement
from .MIDI_Map import *
from _Framework.SubjectSlot import subject_slot
STRECH_INC = 0.125
STRECH_INC_PLS = 0.5
FADE_TIME = 0
FADE_EVENT = 1

class MidiEditSection(CompoundComponent):
    _current_clip = None
    _split_value = 4
    _base_note = None
    _gate = 1.0
    _selected_note = None
    _note_pos = None
    _note_len = 0.0
    _bend_val = 0
    _offset = 0.0
    _transpose = 0
    _vel_fade = 0
    _fade_mode = FADE_TIME
    _note_set = None
    _note_index = 0

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)
        is_momentary = True
        self.split_knob = SliderElement(MIDI_CC_TYPE, 5, 70)
        self.gate_knob = SliderElement(MIDI_CC_TYPE, 5, 71)
        self.bend_knob = SliderElement(MIDI_CC_TYPE, 5, 72)
        self.offset_knob = SliderElement(MIDI_CC_TYPE, 5, 73)
        self.strech_knob = SliderElement(MIDI_CC_TYPE, 5, 74)
        self.fade_knob = SliderElement(MIDI_CC_TYPE, 5, 75)
        self.transpose_knob = SliderElement(MIDI_CC_TYPE, 5, 77)
        self.edit_button = ButtonElement(is_momentary, MIDI_CC_TYPE, 5, 60)
        self.split_button = ButtonElement(is_momentary, MIDI_CC_TYPE, 5, 61)
        self.init_button = ButtonElement(is_momentary, MIDI_CC_TYPE, 5, 62)
        self.delete_button = ButtonElement(is_momentary, MIDI_CC_TYPE, 5, 63)
        self.select_button = ButtonElement(is_momentary, MIDI_CC_TYPE, 5, 64)
        self._do_edit_button.subject = self.edit_button
        self._do_split_button.subject = self.split_button
        self._do_delete.subject = self.delete_button
        self._do_init.subject = self.init_button
        self._do_select.subject = self.select_button
        self._do_split.subject = self.split_knob
        self._do_gate.subject = self.gate_knob
        self._do_bend.subject = self.bend_knob
        self._do_offset.subject = self.offset_knob
        self._do_strech.subject = self.strech_knob
        self._do_fade.subject = self.fade_knob
        self._do_transpose.subject = self.transpose_knob

    def do_message(self, msg, statusbarmsg=None):
        if statusbarmsg is None:
            self.canonical_parent.show_message(msg)
        else:
            self.canonical_parent.show_message(statusbarmsg)
        self.canonical_parent.timed_message(2, msg)

    def _init_value(self):
        self._split_value = 4

    def select_note(self, note):
        if self._current_clip:
            if self._note_set:
                self._note_index = 0
                self.set_notes(tuple(self._note_set[self._note_index]))

    @subject_slot('value')
    def _do_select(self, value):
        if value == 0:
            clip_slot = self.song().view.highlighted_clip_slot
            if clip_slot:
                if clip_slot.has_clip:
                    if clip_slot.clip.is_midi_clip:
                        clip = clip_slot.clip
                        self._notes_changed.subject = clip
                        self._current_clip = clip
                        self._note_set = clip.get_notes(0.0, 0, clip.length, 127)
                        if self._note_index is None:
                            self._note_index = 0
                        else:
                            self._note_index = (self._note_index + 1) % len(self._note_set)
                        ls = []
                        selnote = self._note_set[self._note_index]
                        ls.append(selnote)
                        clip.remove_notes(selnote[1], selnote[0], selnote[2], 1)
                        clip.deselect_all_notes()
                        clip.set_notes(tuple(ls))
                        clip.replace_selected_notes(tuple(ls))

    @subject_slot('value')
    def _do_delete(self, value):
        if value != 0:
            self._selected_note = None
            self.edit_button.send_value(0, True)
            if self._current_clip:
                selected = self._current_clip.get_selected_notes_extended()
                for note in selected:
                    self._current_clip.remove_notes_extended(note.pitch, 1, note.start_time, note.duration)

    @subject_slot('value')
    def _do_init(self, value):
        if value != 0:
            self._transpose = 0
            self._offset = 0.0
            self._bend_val = 0
            self._split_value = 4
            self._vel_fade = 0.0
            self._gate = 1.0
            self.canonical_parent.timed_message(2, 'SPLIT:' + str(self._split_value))

    @subject_slot('value')
    def _do_edit_button(self, value):
        if value > 0:
            note = self.get_selected_note()
            self._transpose = 0
            if note:
                self.edit_button.send_value(127, True)
            else:
                self.edit_button.send_value(0, True)

    def get_selected_note(self):
        clip_slot = self.song().view.highlighted_clip_slot
        if clip_slot:
            if clip_slot.has_clip:
                if clip_slot.clip.is_midi_clip:
                    self._notes_changed.subject = clip_slot.clip
                    self._current_clip = clip_slot.clip
                    notes = self._current_clip.get_selected_notes_extended()
                    if len(notes) == 1:
                        self._selected_note = notes[0]
                        self._base_note = self._selected_note.pitch
                        self._note_len = self._selected_note.duration
                        self._note_pos = self._selected_note.start_time
                        return notes[0]

    def execute_transpose(self, dir):
        clip_slot = self.song().view.highlighted_clip_slot
        if clip_slot:
            if clip_slot.has_clip:
                if clip_slot.clip.is_midi_clip:
                    clip = clip_slot.clip
                    notes = clip.get_selected_notes_extended()
                    if len(notes) > 0:
                        for note in notes:
                            if note.pitch + dir < 128:
                                note.pitch = note.pitch + dir
                            notes.append(note)
                            clip.apply_note_modifications(notes)

    def execute_split(self):
        selected_notes = self._current_clip.get_selected_notes_extended()
        for selected_note in selected_notes:
            if selected_note:
                splited_notes = []
                note_len = selected_note.duration
                note_pitch = min(max(0, selected_note.pitch + self._transpose), 127)
                velocity = selected_note.velocity
                mute = selected_note.mute
                sp = selected_note.start_time
                pos = selected_note.start_time
                test = self._current_clip.get_selected_notes_extended()
                test.extend([selected_note])
                if velocity < 0:
                    endvel = velocity
                    startvel = velocity - velocity * abs(self._vel_fade)
                else:
                    startvel = velocity
                    endvel = velocity - velocity * self._vel_fade
                divList = self.get_interval(note_len, self._split_value, self._bend_val)
                off = int(self._split_value * self._offset)
                velinc = (endvel - startvel) / self._split_value
                velocity = startvel
                for index in range(self._split_value):
                    pcl = int((index + off) % self._split_value)
                    div = divList[pcl]
                    notvlen = div * self._gate
                    if notvlen > 0.0:
                        note_specification = Live.Clip.MidiNoteSpecification(note_pitch, pos, notvlen, velocity, mute, selected_note.probability, selected_note.velocity_deviation, selected_note.release_velocity)
                        splited_notes.append(note_specification)
                    pos += div
                    if self._fade_mode == FADE_EVENT:
                        velocity += velinc
                    else:
                        rp = (pos - sp) / note_len
                        velocity = startvel + (endvel - startvel) * rp

                self._current_clip.add_new_notes(splited_notes)

    @subject_slot('value')
    def _do_transpose(self, value):
        diff = value == REL_KNOB_DOWN and -1 or 1
        self.execute_transpose(diff)

    @subject_slot('value')
    def _do_fade(self, value):
        if self.canonical_parent.isShiftDown():
            diff = value == REL_KNOB_DOWN and -0.01 or 0.01
        else:
            diff = value == REL_KNOB_DOWN and -0.1 or 0.1
        newvale = self._vel_fade + diff
        if newvale >= -1.0:
            if newvale <= 1.0:
                self._vel_fade = newvale
                self.canonical_parent.timed_message(2, 'FADE:' + str(int(round(self._vel_fade * 100, 0))) + '%')
                self.canonical_parent.show_message('Split Fade: ' + str(int(round(self._vel_fade * 100, 0))) + '%')
                self.execute_split()

    @subject_slot('value')
    def _do_strech(self, value):
        diff = value == REL_KNOB_DOWN and -1 or 1
        if self.canonical_parent.isShiftDown():
            newval = self._note_len + diff * STRECH_INC_PLS
        else:
            newval = self._note_len + diff * STRECH_INC
        if newval > 0:
            self._note_len = newval
            self.execute_split()
            self.canonical_parent.timed_message(2, 'LENGTH:' + str(self._note_len) + ' BEATS')
            self.canonical_parent.show_message('Set Length TO : ' + str(self._note_len) + ' beats')

    @subject_slot('value')
    def _do_offset(self, value):
        diff = value == REL_KNOB_DOWN and -0.01 or 0.01
        newval = self._offset + diff
        if newval >= 0.0:
            if newval <= 1.0:
                self._offset = newval
                self.canonical_parent.timed_message(2, 'OFF:' + str(round(self._offset, 2)))
                self.canonical_parent.show_message('Split Offset : ' + str(round(self._offset, 2)))
                self.execute_split()

    @subject_slot('value')
    def _do_split_button(self, value):
        if value != 0:
            self.execute_split()

    @subject_slot('notes')
    def _notes_changed(self):
        pass

    @subject_slot('value')
    def _do_split(self, value):
        diff = value == REL_KNOB_DOWN and -1 or 1
        newval = self._split_value + diff
        if newval > 0:
            if newval <= 128:
                self._split_value = newval
                self.canonical_parent.timed_message(2, 'SPLIT:' + str(self._split_value))
                self.canonical_parent.show_message('Splits : ' + str(self._split_value))
                self.execute_split()

    @subject_slot('value')
    def _do_gate(self, value):
        diff = value == REL_KNOB_DOWN and -0.01 or 0.01
        newval = self._gate + diff
        if newval > 0.1:
            if newval <= 1.0:
                self._gate = newval
                self.canonical_parent.timed_message(2, 'GATE:' + str(int(round(self._gate * 100, 0))) + '%')
                self.canonical_parent.show_message('Split Gate: ' + str(int(round(self._gate * 100, 0))) + '%')
                self.execute_split()

    def get_interval__(self, notelen):
        div = notelen / self._split_value
        n = self._split_value
        ls = []
        sum = 0
        ct = self._split_value
        rl = notelen
        bv = self._bend_val / 100.0
        param = abs(bv) * (self._split_value / 2)
        for i in range(n):
            div = rl / ct
            sz = div * (1.0 + param)
            ls.append(sz)
            ct -= 1
            rl -= sz

        sum = 0
        for v in ls:
            sum += v

        ratio = notelen / sum
        for i in range(len(ls)):
            ls[i] = ls[i] * ratio

        return self._bend_val < 0 and ls.reverse() or ls

    def get_interval(self, notelen, splits, bend_val):
        div = notelen / splits
        n = splits
        ls = []
        param = abs(bend_val / 100.0)
        spl = 2
        for i in range(n):
            sec = notelen / spl
            ls.append(sec)
            if i < n - 2:
                spl *= 1.0 + param

        acc = 0
        for v in ls:
            acc += v

        ratio = notelen / acc
        for i in range(len(ls)):
            ls[i] = ls[i] * ratio

        return bend_val < 0.0 and ls.reverse() or ls

    @subject_slot('value')
    def _do_bend(self, value):
        diff = value == REL_KNOB_DOWN and -1 or 1
        newval = self._bend_val + diff
        if newval >= -100:
            if newval <= 100:
                if self._selected_note:
                    self._bend_val = newval
                    self.canonical_parent.timed_message(2, 'BEND:' + str(self._bend_val) + '%')
                    self.canonical_parent.show_message('Split Bend: ' + str(self._bend_val) + '%')
                    list = self.get_interval(self._selected_note.duration, self._split_value, self._bend_val)
                    self.execute_split()

    def _on_selected_track_changed(self):
        debug_out(' Selected Track Changed ')

    def update(self):
        pass

    def refresh(self):
        pass
# okay decompiling src/MidiEditSection.pyc
