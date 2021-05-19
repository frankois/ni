# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_Studio/NoteRepeatComponent.py
# Compiled at: 2021-04-30 12:12:38
# Size of source mod 2**32: 10521 bytes
import Live
from _Framework.SubjectSlot import subject_slot
from .MIDI_Map import *
from _Framework.InputControlElement import *
import _Framework.SliderElement as SliderElement
from _Framework.ButtonElement import ButtonElement, ON_VALUE, OFF_VALUE
import _Framework.CompoundComponent as CompoundComponent
t = 1.5
NOTE_REPEAT_FREQUENCIES = [32 * t,
 32,
 16 * t,
 16,
 8 * t,
 8,
 4 * t,
 4]
CFG_REPEAT_FREQUENCIES = [2, 2 * t, 4, 4 * t, 8, 8 * t, 16, 16 * t, 32, 32 * t, 64]
CFG_REPEAT_DISPLAY = ['1/2', '1/2T', '1/4', '1/4T', '1/8', '1/8T', '1/16', '1/16T', '1/32', '1/32T', '1/64']
CTRL_TO_FREQ = (
 (40, 4),
 (
  45, 4 * t),
 (41, 8),
 (
  46, 8 * t),
 (42, 16),
 (
  47, 16 * t),
 (43, 32),
 (
  48, 32 * t),
 (44, 64))
CTRL_CFG_TO_FREQ = ((100, 1), (101, 2), (102, 3), (103, 4))
del t

class NoteRepeatComponent(CompoundComponent):
    __doc__ = ' Noter Repeat Handler'
    __module__ = __name__
    _knob_handler = None

    def __init__(self, note_repeat=None, *a, **k):
        (super().__init__)(*a, **k)
        self._note_repeat = note_repeat
        self._adjust_cfg_value.subject = SliderElement(MIDI_CC_TYPE, 2, 105)
        self._note_repeat_button = ButtonElement(True, MIDI_CC_TYPE, 0, 102)
        self._do_note_repeat.subject = self._note_repeat_button
        self._cfg_adjust_button = ButtonElement(True, MIDI_CC_TYPE, 2, 106)
        self._cfg_adjust_button.add_value_listener(self._do_cfg_button)
        self._cfg_down = False
        self._hold_mode = False
        self.nr_down = False
        self._current_nr_button = None
        self._do_change_nr_1.subject = SliderElement(MIDI_CC_TYPE, 1, 76)
        self._do_change_nr_2.subject = SliderElement(MIDI_CC_TYPE, 1, 77)
        self._do_change_nr_3.subject = SliderElement(MIDI_CC_TYPE, 1, 78)
        self._do_change_nr_4.subject = SliderElement(MIDI_CC_TYPE, 1, 79)

        def createButton(ccindenfier, nr_freq):
            button = ButtonElement(True, MIDI_CC_TYPE, 1, ccindenfier)
            button.add_value_listener(self._select_value, True)
            button.active = False
            button.freq = nr_freq
            button.cfg = False
            button.hold = False
            return button

        def createCfgButton(ccindenfier, nr_freq_idx):
            button = ButtonElement(True, MIDI_CC_TYPE, 2, ccindenfier)
            button.add_value_listener(self._select_value, True)
            button.active = False
            button.fr_idx = nr_freq_idx
            button.freq = CFG_REPEAT_FREQUENCIES[nr_freq_idx]
            button.cfg = True
            button.hold = False
            return button

        self._cfg_buttons = [createCfgButton(assign[0], assign[1]) for assign in CTRL_CFG_TO_FREQ]
        for button in self._cfg_buttons:
            button.send_value(button.active and 1 or 0, True)

        self.nr_frq = CTRL_TO_FREQ[4][1]
        self._note_repeat.repeat_rate = 1.0 / self.nr_frq * 4.0
        self.buttons = [createButton(assign[0], assign[1]) for assign in CTRL_TO_FREQ]
        self.buttons[4].active = True
        self._previous_button = self.buttons[4]
        self._last_active_button = self.buttons[4]
        for button in self.buttons:
            button.send_value(button.active and 1 or 0, True)

    def update(self):
        pass

    def store_values(self, dict):
        for button, idx in zip(self._cfg_buttons, list(range(len(self._cfg_buttons)))):
            dict['cofig-nr-val' + str(idx)] = button.fr_idx

    def recall_values(self, dict):
        for button, idx in zip(self._cfg_buttons, list(range(len(self._cfg_buttons)))):
            key = 'cofig-nr-val' + str(idx)
            if key in dict:
                fqidx = dict[key]
                button.fr_idx = fqidx
                button.freq = CFG_REPEAT_FREQUENCIES[fqidx]

    def registerKnobHandler(self, handler):
        self._knob_handler = handler

    def show_note_rates(self):
        rates = ''
        for button, idx in zip(self._cfg_buttons, list(range(len(self._cfg_buttons)))):
            rates += ' ' + CFG_REPEAT_DISPLAY[button.fr_idx].ljust(5)
            if idx < 3:
                rates += '|'

        self.canonical_parent.timed_message(2, rates)

    def mod_button(self, button, inc, which):
        cindex = button.fr_idx
        maxindex = len(CFG_REPEAT_FREQUENCIES) - 1
        minindex = 0
        if self.canonical_parent.isShiftDown():
            inc *= 2
            maxindex = cindex % 2 == 0 and maxindex or maxindex - 1
            minindex = cindex % 2
        new_idx = max(minindex, min(maxindex, cindex + inc))
        if new_idx != cindex:
            self.canonical_parent.show_message('Note Repeat Button ' + str(which) + ' : ' + CFG_REPEAT_DISPLAY[new_idx])
            button.fr_idx = new_idx
            button.freq = CFG_REPEAT_FREQUENCIES[new_idx]
            if button.active:
                self.nr_frq = CFG_REPEAT_FREQUENCIES[new_idx]
                self._note_repeat.repeat_rate = 1.0 / self.nr_frq * 4.0

    @subject_slot('value')
    def _do_change_nr_1(self, value):
        self.mod_button(self._cfg_buttons[0], value == REL_KNOB_DOWN and -1 or 1, 1)
        self.show_note_rates()

    @subject_slot('value')
    def _do_change_nr_2(self, value):
        self.mod_button(self._cfg_buttons[1], value == REL_KNOB_DOWN and -1 or 1, 2)
        self.show_note_rates()

    @subject_slot('value')
    def _do_change_nr_3(self, value):
        self.mod_button(self._cfg_buttons[2], value == REL_KNOB_DOWN and -1 or 1, 3)
        self.show_note_rates()

    @subject_slot('value')
    def _do_change_nr_4(self, value):
        self.mod_button(self._cfg_buttons[3], value == REL_KNOB_DOWN and -1 or 1, 4)
        self.show_note_rates()

    def _do_cfg_button(self, value):
        if value != 0:
            self._cfg_down = True
            button = self._current_nr_button
            if button and button.cfg and button.fr_idx >= 0:
                self.canonical_parent.show_message('Note Repeat ' + CFG_REPEAT_DISPLAY[button.fr_idx])
        else:
            self._cfg_down = False
        if self._knob_handler:
            self._knob_handler.do_main_push(value)

    @subject_slot('value')
    def _adjust_cfg_value(self, value):
        button = self._current_nr_button
        if button:
            if button.cfg:
                if not (self.nr_down or button.hold or self)._hold_mode or button.active:
                    inc = value == 127 and -1 or 1
                    cindex = button.fr_idx
                    maxindex = len(CFG_REPEAT_FREQUENCIES) - 1
                    minindex = 0
                    if self._cfg_down:
                        inc *= 2
                        maxindex = cindex % 2 == 0 and maxindex or maxindex - 1
                        minindex = cindex % 2
                    new_idx = max(minindex, min(maxindex, cindex + inc))
                    self.canonical_parent.show_message('Note Repeat ' + CFG_REPEAT_DISPLAY[new_idx])
                    button.fr_idx = new_idx
                    button.freq = CFG_REPEAT_FREQUENCIES[new_idx]
                    self.nr_frq = CFG_REPEAT_FREQUENCIES[new_idx]
                    self._note_repeat.repeat_rate = 1.0 / self.nr_frq * 4.0
        elif self._knob_handler:
            self._knob_handler.do_main(value)

    def _select_value(self, value, button):
        if value != 0:
            self._current_nr_button = button
            button.hold = True
            self.show_note_rates()
            if self._hold_mode:
                if self._previous_button == button:
                    button.send_value(0, True)
                    button.active = False
                    self._last_active_button = button
                    button.active = False
                    self._note_repeat.repeat_rate = 32.0
                    self._previous_button = None
                else:
                    if self._previous_button is None or self._previous_button != button:
                        button.send_value(1, True)
                        button.active = True
                        self.nr_frq = button.freq
                        self._note_repeat.repeat_rate = 1.0 / self.nr_frq * 4.0
                        if not self._note_repeat.enabled:
                            self._note_repeat.enabled = True
                        if self._previous_button is not None:
                            self._previous_button.active = False
                            self._previous_button.send_value(0, True)
                        self._previous_button = button
            else:
                button.send_value(1, True)
                button.active = True
                self.nr_frq = button.freq
                self._note_repeat.repeat_rate = 1.0 / self.nr_frq * 4.0
                if self._previous_button is not None:
                    if self._previous_button != button:
                        self._previous_button.active = False
                        self._previous_button.send_value(0, True)
                self._previous_button = button
        else:
            button.hold = False

    @subject_slot('value')
    def _do_note_repeat(self, value):
        self.nr_down = value > 0
        if self._hold_mode:
            if value > 0:
                self._note_repeat_button.send_value(0)
                self._note_repeat.enabled = False
                self._hold_mode = False
                if self._previous_button is None:
                    if self._last_active_button is not None:
                        self._previous_button = self._last_active_button
                        self._last_active_button.send_value(1)
                        self._last_active_button.active = True
                        self.nr_frq = self._last_active_button.freq
                        self._note_repeat.repeat_rate = 1.0 / self.nr_frq * 4.0
        else:
            if self.canonical_parent.isShiftDown() and value > 0:
                self._note_repeat_button.send_value(1)
                self._note_repeat.enabled = True
                self._hold_mode = True
                self._note_repeat.repeat_rate = 1.0 / self.nr_frq * 4.0
            else:
                if value == 0:
                    self._note_repeat.enabled = False
                    self._note_repeat_button.send_value(0)
                else:
                    self._note_repeat_button.send_value(1)
                    self._note_repeat.repeat_rate = 1.0 / self.nr_frq * 4.0
                    self._note_repeat.enabled = True

    def disconnect(self):
        super().disconnect()
# okay decompiling src/NoteRepeatComponent.pyc
