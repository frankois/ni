# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_Mikro_Mk2/StateButton.py
# Compiled at: 2021-04-30 12:09:45
# Size of source mod 2**32: 2947 bytes
import Live
from _Framework.ButtonElement import *
from _Framework.InputControlElement import *

class StateButton(ButtonElement):
    __doc__ = ' Special button class that can be configured with custom on- and off-values '
    __module__ = __name__

    def __init__(self, is_momentary, msg_type, channel, identifier):
        ButtonElement.__init__(self, is_momentary, msg_type, channel, identifier)
        self._is_enabled = True
        self._is_notifying = False
        self._force_next_value = False

    def turn_off(self):
        self.send_value(0, True)

    def turn_on(self):
        self.send_value(127, True)

    def set_enabled(self, enabled):
        self._is_enabled = enabled

    def reset(self):
        self.send_value(0, True)

    def install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback):
        if self._is_enabled:
            ButtonElement.install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback)
        else:
            if self._msg_channel != self._original_channel or self._msg_identifier != self._original_identifier:
                install_translation_callback(self._msg_type, self._original_identifier, self._original_channel, int(self._msg_identifier), self._msg_channel)


class ToggleButton(ButtonElement):
    __doc__ = '  '
    __module__ = __name__

    def __init__(self, msg_type, channel, identifier):
        ButtonElement.__init__(self, True, msg_type, channel, identifier)
        self._is_enabled = True
        self._is_notifying = False
        self._force_next_value = False
        self._value = 0

    def turn_off(self):
        self._value = 0
        self.send_value(0, True)

    def turn_on(self):
        self._value = 1
        self.send_value(127, True)

    def set_enabled(self, enabled):
        self._is_enabled = enabled

    def reset(self):
        self.send_value(0, True)

    def receive_value(self, value):
        if value > 0:
            if self._value == 0:
                self._value = 1
                InputControlElement.receive_value(self, 127)
            else:
                self._value = 0
                InputControlElement.receive_value(self, 0)

    def install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback):
        if self._is_enabled:
            ButtonElement.install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback)
        else:
            if self._msg_channel != self._original_channel or self._msg_identifier != self._original_identifier:
                install_translation_callback(self._msg_type, self._original_identifier, self._original_channel, int(self._msg_identifier), self._msg_channel)
# okay decompiling src/StateButton.pyc
