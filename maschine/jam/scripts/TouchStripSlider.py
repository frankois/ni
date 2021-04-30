# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/TouchStripSlider.py
# Compiled at: 2021-04-29 13:54:08
# Size of source mod 2**32: 3265 bytes
import _Framework.SliderElement as SliderElement
from _Framework.InputControlElement import MIDI_NOTE_TYPE

class TouchStripSlider(SliderElement):
    __doc__ = ' Class representing a slider on the controller '

    def __init__(self, msg_type, channel, identifier, index, handler, *a, **k):
        assert msg_type is not MIDI_NOTE_TYPE
        (super(TouchStripSlider, self).__init__)(msg_type, channel, identifier, *a, **k)
        self._TouchStripSlider__grabbed = False
        self._TouchStripSlider__buffered_value = None
        self._TouchStripSlider__led_value = None
        self._TouchStripSlider__index = index
        self._TouchStripSlider__cfg = (0, 0)
        self._TouchStripSlider__cfg_over = (0, 2)
        self._TouchStripSlider__sysexhandler = handler
        self.resource.on_received = self.grab_control
        self.resource.on_lost = self.release_control

    @property
    def is_grabbed(self):
        return self._TouchStripSlider__grabbed

    @property
    def led_value(self):
        return self._TouchStripSlider__led_value

    @led_value.setter
    def led_value(self, value):
        self._TouchStripSlider__led_value = value

    def _set_cfg(self, mode, color):
        self._TouchStripSlider__cfg = (
         mode, color)

    def set_cfg(self, mode, color):
        self._TouchStripSlider__cfg_over = (
         mode, color)
        if self._TouchStripSlider__grabbed:
            self._TouchStripSlider__sysexhandler.update_bar_config()

    def get_strip_cfg(self):
        if self.is_grabbed:
            return self._TouchStripSlider__cfg_over
        return self._TouchStripSlider__cfg

    def remove_value_listener(self, *a, **k):
        (super(self.__class__, self).remove_value_listener)(*a, **k)
        if self.is_grabbed:
            self.resource.release_all()

    def set_display_value(self, value, force=False, channel=None):
        self._TouchStripSlider__buffered_value = value
        if not self._TouchStripSlider__grabbed:
            super(TouchStripSlider, self).send_value(value, force, channel)

    def send_value(self, value, force=False, channel=None):
        super(TouchStripSlider, self).send_value(value, True, channel)

    def grab_control(self, client):
        self._TouchStripSlider__grabbed = True
        self._TouchStripSlider__sysexhandler.update_bar_config()
        super(TouchStripSlider, self).send_value(0, True)

    def release_control(self, client):
        self._TouchStripSlider__grabbed = False
        self._TouchStripSlider__sysexhandler.reset_led()
        self._TouchStripSlider__sysexhandler.set_led_value(self._TouchStripSlider__index, self._TouchStripSlider__led_value or 0)
        self._TouchStripSlider__sysexhandler.update_led()
        self._TouchStripSlider__sysexhandler.update_bar_config()
        self.set_display_value(self._TouchStripSlider__buffered_value or 0, True)


class GrabEncoder(SliderElement):
    __doc__ = ' Class representing Stateless Encoder that can be grabbed '

    def __init__(self, msg_type, channel, identifier, *a, **k):
        assert msg_type is not MIDI_NOTE_TYPE
        (super(GrabEncoder, self).__init__)(msg_type, channel, identifier, *a, **k)
        self._GrabEncoder__grabbed = False
        self.resource.on_received = self.grab_control
        self.resource.on_lost = self.release_control

    @property
    def is_grabbed(self):
        return self._GrabEncoder__grabbed

    def grab_control(self, client):
        self._GrabEncoder__grabbed = True

    def release_control(self, client):
        self._GrabEncoder__grabbed = False

    def remove_value_listener(self, *a, **k):
        (super(self.__class__, self).remove_value_listener)(*a, **k)
        if self._GrabEncoder__grabbed:
            self.resource.release_all()
# okay decompiling scripts/TouchStripSlider.pyc
