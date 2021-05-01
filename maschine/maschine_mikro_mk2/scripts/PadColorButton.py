# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_Mikro_Mk2/PadColorButton.py
# Compiled at: 2021-04-30 12:09:45
# Size of source mod 2**32: 3225 bytes
import Live
from _Framework.ButtonElement import *
from _Framework.InputControlElement import *
from .MIDI_Map import *

class PadColorButton(ButtonElement):
    __doc__ = ' Colored Maschine Pads '
    __module__ = __name__

    def __init__(self, is_momentary, channel, row_index, column_index, color_source):
        ButtonElement.__init__(self, is_momentary, MIDI_NOTE_TYPE, channel, CLIPNOTEMAP[row_index][column_index])
        self._is_enabled = True
        self._color_source = color_source
        self._row_index = row_index
        self._column_index = column_index
        self.last_value = 0
        self.last_color = [None, None, None]
        self.set_channel(NON_FEEDBACK_CHANNEL)
        self.set_feedback_delay(1)

    def get_identifier(self):
        return self._msg_identifier

    def reset(self):
        self.last_color = [
         None, None, None, 0, 0]

    def blink_value(self):
        return 0

    def turn_off(self):
        self.send_value(0, True)

    def turn_on(self):
        self.send_value(1, True)

    def refresh(self):
        self.send_value(self.last_value, True)

    def set_send_note(self, note):
        if note in range(128):
            self._msg_identifier = note
            if not self._is_enabled:
                self.canonical_parent._translate_message(self._msg_type, self._original_identifier, self._original_channel, self._msg_identifier, self._msg_channel)

    def set_to_notemode(self, notemode):
        self._is_enabled = not notemode
        if notemode:
            self.set_channel(0)
            self._is_being_forwarded = False
        else:
            self.set_channel(NON_FEEDBACK_CHANNEL)
            self._is_being_forwarded = True

    def send_value(self, value, force_send=False):
        if force_send or self._is_being_forwarded:
            self.send_color(value)
            self.last_value = value

    def send_color(self, value):
        data_byte1 = self._original_identifier
        color = self._color_source.get_color(value, self._column_index, self._row_index)
        scolor = color == None and OFF_COLOR or color
        self.send_c_midi(2, scolor[2])
        self.send_c_midi(1, scolor[1])
        self.send_c_midi(0, scolor[0])

    def send_color_direct(self, color):
        scolor = color == None and OFF_COLOR or color
        self.send_c_midi(0, scolor[0])
        self.send_c_midi(1, scolor[1])
        self.send_c_midi(2, scolor[2])

    def switch_off(self):
        self.send_c_midi(2, 0)

    def send_c_midi(self, channel, colorvalue, force=False):
        prevColor = self.last_color[channel]
        if prevColor != colorvalue:
            stat = MIDI_CC_STATUS + channel
            self.last_color[channel] = colorvalue
            self.send_midi((stat, self._original_identifier, colorvalue))

    def disconnect(self):
        ButtonElement.disconnect(self)
        self._is_enabled = None
        self._color_source = None
        self._report_input = None
        self._column_index = None
        self._row_index = None
# okay decompiling src/PadColorButton.pyc
