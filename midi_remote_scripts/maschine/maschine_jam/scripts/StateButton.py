# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/StateButton.py
# Compiled at: 2021-05-04 12:11:01
# Size of source mod 2**32: 4449 bytes
import _Framework.ButtonElement as ButtonElement
from _Framework.InputControlElement import MIDI_CC_TYPE

class StateButton(ButtonElement):
    __doc__ = ' Special button class that can be configured with custom on- and off-values '
    __module__ = __name__

    def __init__(self, is_momentary, msg_type, channel, identifier, *a, **k):
        (ButtonElement.__init__)(self, is_momentary, msg_type, channel, identifier, *a, **k)
        self._is_enabled = True
        self._is_notifying = False
        self._force_next_value = False
        self._last_value = 0
        self._StateButton__main_listener = None
        self._StateButton__grabbed = False
        self._StateButton__buffered_value = None
        self.resource.on_received = self.grab_control
        self.resource.on_lost = self.release_control

    def turn_off(self):
        self._last_value = 0
        self.set_display_value(0, True)

    def turn_on(self):
        self._last_value = 127
        self.set_display_value(127, True)

    @property
    def grabbed(self):
        return self._StateButton__grabbed

    def set_value(self, value):
        if value != self._last_value:
            self._last_value = value
            self.set_display_value(value, True)

    def set_enabled(self, enabled):
        self._is_enabled = enabled

    def send_value(self, value, force=False, channel=None):
        super().send_value(value, True)

    def reset(self):
        self._last_value = 0
        self.send_value(0, True)

    def set_display_value(self, value, force=False, channel=None):
        self._StateButton__buffered_value = value
        if not self._StateButton__grabbed:
            self.send_value(value, force, channel)

    def grab_control(self, client):
        self._StateButton__grabbed = True
        self.notify_ownership_change(client, True)

    def release_control(self, client):
        self._StateButton__grabbed = False
        self.notify_ownership_change(client, False)
        if self._StateButton__buffered_value >= 0:
            self.send_value(self._StateButton__buffered_value, True)

    def remove_value_listener(self, *a, **k):
        (super().remove_value_listener)(*a, **k)
        if self.grabbed:
            self.resource.release_all()

    def install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback):
        if self._is_enabled:
            ButtonElement.install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback)
        else:
            if self._msg_channel != self._original_channel or self._msg_identifier != self._original_identifier:
                install_translation_callback(self._msg_type, self._original_identifier, self._original_channel, self._msg_identifier, self._msg_channel)


class SysExButton(ButtonElement):
    __doc__ = 'Button that represents Shift Status '
    __module__ = __name__

    def __init__(self, identifier, *a, **k):
        (ButtonElement.__init__)(self, True, MIDI_CC_TYPE, 15, identifier, *a, **k)
        self._SysExButton__main_listener = None
        self._SysExButton__grabbed = False
        self._SysExButton__buffered_value = None

    @property
    def is_grabbed(self):
        return self._SysExButton__grabbed

    def send_value(self, value, opt_value=None):
        pass

    def send_value_ext(self, value, force=False, channel=None):
        pass

    def grab_control(self):
        self._SysExButton__grabbed = True

    def release_control(self):
        self._SysExButton__grabbed = False


class TouchButton(ButtonElement):
    __doc__ = ' Touch '
    __module__ = __name__

    def __init__(self, msg_type, channel, identifier, *a, **k):
        (ButtonElement.__init__)(self, True, msg_type, channel, identifier, *a, **k)
        self._TouchButton__grabbed = False
        self._TouchButton__main_listener = None
        self.resource.on_received = self.grab_control
        self.resource.on_lost = self.release_control

    @property
    def is_grabbed(self):
        return self._TouchButton__grabbed

    def grab_control(self, client):
        self._TouchButton__grabbed = True
        if self._TouchButton__main_listener:
            super().remove_value_listener(self._TouchButton__main_listener)

    def release_control(self, client):
        self._TouchButton__grabbed = False
        if self._TouchButton__main_listener:
            super().add_value_listener(self._TouchButton__main_listener)

    def add_value_listener(self, *a, **k):
        if not self._TouchButton__main_listener:
            self._TouchButton__main_listener = a[0]
        (super().add_value_listener)(*a, **k)
# okay decompiling src/StateButton.pyc
