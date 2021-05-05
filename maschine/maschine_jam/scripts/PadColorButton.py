# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/PadColorButton.py
# Compiled at: 2021-05-04 12:11:01
# Size of source mod 2**32: 7147 bytes
import _Framework.ButtonElement as ButtonElement
from _Framework.InputControlElement import InputControlElement, MIDI_NOTE_TYPE, MIDI_NOTE_ON_STATUS
from .MidiMap import MATRIX_NOTE_NR, NON_FEEDBACK_CHANNEL, COLOR_BLACK

class PadColorButton(ButtonElement):
    __doc__ = ' Colored Maschine Pads '
    __module__ = __name__

    def __init__(self, is_momentary, channel, row_index, column_index, color_source):
        ButtonElement.__init__(self, is_momentary, MIDI_NOTE_TYPE, channel, MATRIX_NOTE_NR + row_index * 8 + column_index)
        self._is_enabled = True
        self._color_source = color_source
        self._row_index = row_index
        self._column_index = column_index
        self.last_value = None
        self.set_channel(NON_FEEDBACK_CHANNEL)
        self.state = 0
        self._PadColorButton__cc_enabled = True

    def infox(self):
        return 'PC R=' + str(self._row_index) + ' C=' + str(self._column_index)

    def enable_cc_midi(self):
        self._PadColorButton__cc_enabled = True

    def disable_cc_midi(self):
        self._PadColorButton__cc_enabled = False

    def get_identifier(self):
        return self._msg_identifier

    def get_position(self):
        return (
         self._column_index, self._row_index)

    def reset(self):
        self.last_value = None

    def turn_off(self):
        self.last_value = COLOR_BLACK
        if self._PadColorButton__cc_enabled:
            self.send_midi((MIDI_NOTE_ON_STATUS, self._original_identifier, COLOR_BLACK))

    def turn_on(self):
        self.send_value(1, True)

    def refresh(self):
        self.send_value(self.last_value, True)

    def set_send_note(self, note):
        if note in range(128):
            self._msg_identifier = int(note)
            if not self._is_enabled:
                self.canonical_parent._translate_message(self._msg_type, int(self._original_identifier), int(self._original_channel), int(note), int(self._msg_channel))

    def set_to_notemode(self, notemode):
        if self._is_enabled != notemode:
            return
        self._is_enabled = not notemode
        if notemode:
            self.set_channel(0)
            self._is_being_forwarded = False
            self.suppress_script_forwarding = True
        else:
            self.set_channel(NON_FEEDBACK_CHANNEL)
            self._is_being_forwarded = True
            self.suppress_script_forwarding = False
            self._msg_identifier = self._original_identifier

    def send_value(self, value, force_send=False):
        if force_send or self._is_being_forwarded:
            self.send_color(value)

    def send_color(self, value):
        color = self._color_source.get_color(value, self._column_index, self._row_index)
        if color != self.last_value:
            self.last_value = color
            if self._PadColorButton__cc_enabled:
                if color is None:
                    self.send_midi((MIDI_NOTE_ON_STATUS, self._original_identifier, COLOR_BLACK))
                else:
                    self.send_midi((MIDI_NOTE_ON_STATUS, self._original_identifier, color))

    def send_color_direct(self, color):
        self.last_value = color
        if self._PadColorButton__cc_enabled:
            if color is None:
                self.send_midi((MIDI_NOTE_ON_STATUS, self._original_identifier, COLOR_BLACK))
            else:
                self.send_midi((MIDI_NOTE_ON_STATUS, self._original_identifier, color))

    def brighten(self, sat, bright):
        pass

    def switch_off(self):
        self.last_value = COLOR_BLACK
        if self._PadColorButton__cc_enabled:
            self.send_midi((MIDI_NOTE_ON_STATUS, self._original_identifier, COLOR_BLACK))

    def color_value(self):
        return self.last_value or 0

    def set_color_value(self, color):
        self.last_value = color

    def disconnect(self):
        ButtonElement.disconnect(self)
        self._is_enabled = None
        self._color_source = None
        self._report_input = None
        self._column_index = None
        self._row_index = None


class IndexedButton(ButtonElement):
    __doc__ = ' Special button class that has on, off, color an can also be a None Color Button '
    __module__ = __name__

    def __init__(self, is_momentary, midi_type, identifier, channel, color_list):
        ButtonElement.__init__(self, is_momentary, midi_type, channel, identifier)
        self._msg_identifier = identifier
        self._color_list = color_list
        self._last_color = None
        self._last_index = 0
        self._midi_type = midi_type
        self._IndexedButton__note_on_code = MIDI_NOTE_ON_STATUS | channel
        self._IndexedButton__grabbed = False
        self._IndexedButton__resource_hander = None

    @property
    def grabbed(self):
        return self._IndexedButton__grabbed

    def __send_midi(self, color):
        if not self.grabbed:
            self.send_midi((self._IndexedButton__note_on_code, self._original_identifier, color))

    def send_index(self, index):
        if self._color_list is None:
            self._last_color = COLOR_BLACK
            self._IndexedButton__send_midi(COLOR_BLACK)
        else:
            if index < len(self._color_list):
                if self._color_list[index] != self._last_color:
                    self._last_color = self._color_list[index]
                    self._IndexedButton__send_midi(self._last_color)
            else:
                icolor = self._color_list[0] + 1
                if icolor != self._last_color:
                    self._last_color = icolor
                    self._IndexedButton__send_midi(self._last_color)
        self._last_index = index

    def set_resource_handler(self, handler):
        self._IndexedButton__resource_hander = handler

    def set_color(self, color_list):
        self._color_list = color_list
        if not self._IndexedButton__grabbed:
            self.update()

    def reset(self):
        self._last_color = None
        self._last_index = 0

    def update_grab(self, grabbed):
        self._IndexedButton__grabbed = grabbed
        if self._IndexedButton__resource_hander:
            self._IndexedButton__resource_hander(self._IndexedButton__grabbed)

    def send_color(self, color, force=True):
        if color != self._last_color or force:
            self.send_midi((self._IndexedButton__note_on_code, self._original_identifier, color))
            self._last_color = color

    def color_value(self):
        return self._last_color or 0

    def set_color_value(self, color):
        self._last_color = color

    def refresh(self):
        self.send_midi((self._IndexedButton__note_on_code, self._original_identifier, self._last_color))

    def update(self):
        if self._last_index >= len(self._color_list):
            self._last_index = 0
        self.send_index(self._last_index)

    def set_to_black(self):
        self._last_color = COLOR_BLACK

    def unlight(self, force=False):
        if force or self._last_color != COLOR_BLACK:
            self._last_color = COLOR_BLACK
            self.send_midi((self._IndexedButton__note_on_code, self._original_identifier, COLOR_BLACK))

    def turn_on(self):
        self.send_index(1)

    def turn_off(self):
        self.send_index(0)

    def disconnect(self):
        InputControlElement.disconnect(self)
# okay decompiling src/PadColorButton.pyc
