# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_Studio/GatedColorButton.py
# Compiled at: 2021-04-30 12:12:38
# Size of source mod 2**32: 5151 bytes
import Live
from _Framework.ButtonElement import *
from _Framework.InputControlElement import *

class GatedColorButton(ButtonElement):
    __doc__ = ' Special button class that has on, off, color an can also be a None Color Button '
    __module__ = __name__

    def __init__(self, is_momentary, midi_type, identifier, hue):
        ButtonElement.__init__(self, is_momentary, midi_type, 0, identifier)
        self._msg_identifier = identifier
        self.hue = hue
        self.last_value = 0

    def send_value(self, value, force_send=False):
        assert value is not None
        assert isinstance(value, int)
        assert value in range(128)
        if force_send or self._is_being_forwarded:
            self.send_color(value)

    def set_color(self, hue):
        self.hue = hue
        self.send_color(127)

    def send_color(self, value):
        data_byte1 = self._msg_identifier
        self.last_value = value
        self.send_midi((MIDI_CC_STATUS + 0, data_byte1, self.hue))
        self.send_midi((MIDI_CC_STATUS + 2, data_byte1, value == 0 and 25 or 127))
        self.send_midi((MIDI_CC_STATUS + 1, data_byte1, 127))

    def switch_off(self):
        data_byte = self._msg_identifier
        self.send_midi((MIDI_CC_STATUS + 2, data_byte, 0))
        self.send_midi((MIDI_CC_STATUS + 1, data_byte, 0))
        self.send_midi((MIDI_CC_STATUS + 0, data_byte, 0))

    def activate(self):
        self.send_value(0)

    def update(self):
        self.state_init = False
        self.send_value(self.last_value, True)

    def turn_on(self):
        self.send_value(127, True)

    def turn_off(self):
        self.send_value(0, True)

    def disconnect(self):
        InputControlElement.disconnect(self)


class DualColorButton(ButtonElement):
    __doc__ = ' Special button class that has on, off, color an can also be a None Color Button '
    __module__ = __name__

    def __init__(self, is_momentary, midi_type, identifier, color):
        ButtonElement.__init__(self, is_momentary, midi_type, 0, identifier)
        self._msg_identifier = identifier
        self.last_color = [None, None, None]
        self.oncolor = color[0]
        self.offcolor = color[1]
        self.last_value = 0

    def send_value(self, value, force_send=False):
        assert value is not None
        assert isinstance(value, int)
        assert value in range(128)
        if force_send or self._is_being_forwarded:
            self.send_color(value)

    def set_color(self, hue):
        self.hue = hue
        self.send_color(127)

    def reset(self):
        self.last_color = [
         None, None, None]

    def send_color(self, value):
        data_byte1 = self._msg_identifier
        self.last_value = value
        col = value != 0 and self.oncolor or self.offcolor
        self.send_c_midi(0, col[0])
        self.send_c_midi(1, col[1])
        self.send_c_midi(2, col[2])

    def switch_off(self):
        data_byte = self._msg_identifier
        self.send_c_midi(0, 0)
        self.send_c_midi(1, 0)
        self.send_c_midi(2, 0)

    def activate(self):
        self.send_value(0)

    def update(self):
        self.state_init = False
        self.send_value(self.last_value, True)

    def turn_on(self):
        self.send_value(127, True)

    def turn_off(self):
        self.send_value(0, True)

    def disconnect(self):
        InputControlElement.disconnect(self)

    def send_c_midi(self, channel, colorvalue):
        prevColor = self.last_color[int(channel)]
        if prevColor != colorvalue:
            stat = MIDI_CC_STATUS + channel
            self.last_color[channel] = colorvalue
            self.send_midi((stat, self._original_identifier, colorvalue))


class TwinButton(ButtonElement):
    __doc__ = ' Special button class that can be configured with custom on- and off-values '
    __module__ = __name__

    def __init__(self, is_momentary, channel, partner):
        assert isinstance(partner, ButtonElement)
        ButtonElement.__init__(self, is_momentary, MIDI_NOTE_TYPE, channel, partner._original_identifier)
        self._partner = partner

    def fire(self, value):
        self._partner.send_value(value, True)

    def install_connections(self, install_translation, install_mapping, install_forwarding):
        self._send_delayed_messages_task.kill()
        self._is_mapped = False
        self._is_being_forwarded = False
        if self._msg_channel != self._original_channel or self._msg_identifier != self._original_identifier:
            install_translation(self._msg_type, self._original_identifier, self._original_channel, int(self._msg_identifier), self._msg_channel)
        self._is_mapped = install_mapping(self, self._parameter_to_map_to, self._mapping_feedback_delay, self._mapping_feedback_values())
        if self.script_wants_forwarding():
            self._is_being_forwarded = install_forwarding(self)
            if self._is_being_forwarded:
                if self.send_depends_on_forwarding:
                    self._send_delayed_messages_task.restart()
# okay decompiling src/GatedColorButton.pyc
