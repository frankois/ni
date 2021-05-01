# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_Studio/MaschineStudio.py
# Compiled at: 2021-04-30 12:12:38
# Size of source mod 2**32: 2865 bytes
import Live, time
from .Maschine import Maschine
from .JogWheelSection import JogWheelSection
from .MIDI_Map import debug_out
from .PadColorButton import PadColorButton
from .GatedColorButton import GatedColorButton
from _Framework.SubjectSlot import subject_slot
from _Framework.InputControlElement import *
import _Framework.SliderElement as SliderElement

class MaschineStudio(Maschine):
    __doc__ = 'Control Script for Maschine Studio'
    __module__ = __name__
    _gated_buttons = []

    def __init__(self, c_instance):
        super().__init__(c_instance)

    def create_pad_button(self, scene_index, track_index, color_source):
        return PadColorButton(True, 0, scene_index, track_index, color_source)

    def create_gated_button(self, identifier, hue):
        button = GatedColorButton(True, MIDI_CC_TYPE, identifier, hue)
        self._gated_buttons.append(button)
        return button

    def _init_maschine(self):
        self._jogwheel = JogWheelSection(self._modeselect, self._editsection)
        self.prehear_knob = SliderElement(MIDI_CC_TYPE, 0, 41)
        self.prehear_knob.connect_to(self.song().master_track.mixer_device.cue_volume)
        self._device_component.set_touch_mode(2)

    def _final_init(self):
        debug_out('########## LIVE 9 MASCHINE STUDIO V 2.02 ############# ')

    def _click_measure(self):
        pass

    def preferences_name(self):
        return 'MaschineStudio'

    def apply_preferences(self):
        super().apply_preferences()
        pref_dict = self._pref_dict
        if 'use_scrub' in pref_dict:
            self._jogwheel.set_scrub_mode(pref_dict['use_scrub'])
        else:
            self._jogwheel.set_scrub_mode(True)
        if 'color_mode' in pref_dict:
            value = pref_dict['color_mode']
            self._session.set_color_mode(value)
            self._session._c_mode_button.send_value(value == True and 127 or 0, True)
        else:
            self._session.set_color_mode(False)
            self._session._c_mode_button.send_value(0, True)

    def _send_midi(self, midi_bytes, **keys):
        self._c_ref.send_midi(midi_bytes)
        time.sleep(0.001)
        return True

    def store_preferences(self):
        super().store_preferences()
        self._pref_dict['use_scrub'] = self._jogwheel.use_scrub_mode()
        self._pref_dict['color_mode'] = self._session.is_color_mode()

    @subject_slot('value')
    def _do_stop_all(self, value):
        if value != 0:
            if self.isShiftDown():
                self.song().stop_all_clips(0)
            else:
                self.song().stop_all_clips(1)

    def to_color_edit_mode(self, active):
        if self._editsection.is_color_edit() != active:
            self._editsection.set_color_edit(active)

    def cleanup(self):
        for button in self._gated_buttons:
            button.switch_off()
# okay decompiling src/MaschineStudio.pyc
