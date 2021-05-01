# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_Mikro_Mk2/MaschineMikroMk2.py
# Compiled at: 2021-04-30 12:09:45
# Size of source mod 2**32: 2541 bytes
import Live, time
from .Maschine import Maschine
from .MIDI_Map import debug_out
from .KnobSection import KnobSection
from .PadColorButton import PadColorButton
from .GatedColorButton import GatedColorButton
from _Framework.InputControlElement import *

class MaschineMikroMk2(Maschine):
    __doc__ = 'Control Script for Maschine Studio'
    __module__ = __name__
    _gated_buttons = []

    def __init__(self, c_instance):
        super(MaschineMikroMk2, self).__init__(c_instance)

    def create_pad_button(self, scene_index, track_index, color_source):
        return PadColorButton(True, 0, scene_index, track_index, color_source)

    def create_gated_button(self, identifier, hue):
        button = GatedColorButton(True, MIDI_CC_TYPE, identifier, hue)
        self._gated_buttons.append(button)
        return button

    def _init_maschine(self):
        self._jogwheel = KnobSection(self._modeselect, self._editsection)
        self._note_repeater.registerKnobHandler(self._jogwheel)
        self._mixer.set_touch_mode(2)
        self._device_component.set_touch_mode(2)

    def to_color_edit_mode(self, active):
        if self._editsection.is_color_edit() != active:
            self._jogwheel.invoke_color_mode(active and 1 or 0)

    def use_layered_buttons(self):
        return True

    def _final_init(self):
        debug_out('########## LIVE 9 MASCHINE Mikro Mk2 V 2.0.0 ############# ')

    def _click_measure(self):
        pass

    def _send_midi(self, midi_bytes, **keys):
        self._c_ref.send_midi(midi_bytes)
        if self._midi_pause_count == 1:
            time.sleep(0.002)
            self._midi_pause_count = 0
        else:
            self._midi_pause_count = self._midi_pause_count + 1
        return True

    def apply_preferences(self):
        super(MaschineMikroMk2, self).apply_preferences()
        pref_dict = self._pref_dict
        if 'color_mode' in pref_dict:
            value = pref_dict['color_mode']
            self._session.set_color_mode(value)
            self._session._c_mode_button.send_value(value == True and 127 or 0, True)
        else:
            self._session.set_color_mode(False)
            self._session._c_mode_button.send_value(0, True)

    def store_preferences(self):
        super(MaschineMikroMk2, self).store_preferences()
        self._pref_dict['color_mode'] = self._session.is_color_mode()

    def preferences_name(self):
        return 'MaschineMikroMk2'

    def cleanup(self):
        for button in self._gated_buttons:
            button.switch_off()
# okay decompiling src/MaschineMikroMk2.pyc
