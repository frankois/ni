# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_Mk2/MaschineDeviceComponent.py
# Compiled at: 2021-04-30 12:04:50
# Size of source mod 2**32: 6295 bytes
import Live
from _Generic.Devices import *
import _Framework.DeviceComponent as DeviceComponent
import _Framework.ButtonElement as ButtonElement
import _Framework.ChannelTranslationSelector as ChannelTranslationSelector
from _Framework.InputControlElement import *

class MaschineDeviceComponent(DeviceComponent):
    __doc__ = ' Class representing a device in Live '

    def __init__(self):
        DeviceComponent.__init__(self)
        self.device_listener = None
        self.device_parm_listener = None
        self._control_translation_selector = ChannelTranslationSelector(8)
        self.clear_mode = True
        self.touch_mode = False
        self.del_parm_map = {}
        self.del_clip_map = {}
        self.del_touch_buttons = []

    def _on_device_name_changed(self):
        if self._device is not None:
            self.canonical_parent.send_to_display('Device: ' + self._device.name, 1)
        else:
            self.canonical_parent.send_to_display('<No Device>', 1)

    def update(self):
        if self.is_enabled() and self._device is not None:
            self._device_bank_registry.set_device_bank(self._device, self._bank_index)
            if self._parameter_controls is not None:
                old_bank_name = self._bank_name
                self._assign_parameters()
                if self._bank_name != old_bank_name:
                    self._show_msg_callback(self._device.name + ' Bank: ' + self._bank_name)
                    self.canonical_parent.update_bank_display()
            if self._bank_up_button is not None:
                if self._bank_down_button is not None:
                    can_bank_up = self._bank_index is None or self._number_of_parameter_banks() > self._bank_index + 1
                    can_bank_down = self._bank_index is None or self._bank_index > 0
                    self._bank_up_button.set_light(can_bank_up)
                    self._bank_down_button.set_light(can_bank_down)
            if self._bank_buttons is not None:
                for index, button in enumerate(self._bank_buttons):
                    button.set_light(index == self._bank_index)

        else:
            if self._lock_button is not None:
                self._lock_button.turn_off()
            if self._bank_up_button is not None:
                self._bank_up_button.turn_off()
            if self._bank_down_button is not None:
                self._bank_down_button.turn_off()
            if self._bank_buttons is not None:
                for button in self._bank_buttons:
                    button.turn_off()

            if self._parameter_controls is not None:
                self._release_parameters(self._parameter_controls)

    def set_touch_mode(self, touchchannel):
        self.touch_mode = True
        nr_dev_ctrl = len(self._parameter_controls)
        for ctrl in self._parameter_controls:
            touch_button = ButtonElement(False, MIDI_CC_TYPE, touchchannel, ctrl.message_identifier())
            self.del_touch_buttons.append(touch_button)
            touch_button.add_value_listener(self._clear_param, True)

    def enter_clear_mode(self):
        self.clear_mode = True
        self.del_parm_map = {}
        self.del_clip_map = {}
        for control in self._parameter_controls:
            key = control.message_identifier()
            self.del_parm_map[key] = control.mapped_parameter()
            self.touch_mode or control.add_value_listener(self._clear_param, True)

        self.touch_mode or self.set_enabled(False)

    def exit_clear_mode(self):
        self.clear_mode = False
        self.touch_mode or self.set_enabled(True)
        for control in self._parameter_controls:
            self.touch_mode or control.remove_value_listener(self._clear_param)

    def _get_track_of_device(self, obj):
        if obj is not None:
            parent = obj.canonical_parent
            if isinstance(parent, Live.Track.Track):
                return parent
            return self._get_track_of_device(parent)

    def _get_clip_of_device(self):
        track = self._get_track_of_device(self._device)
        if track:
            if track.can_be_armed:
                for clip_slot in track.clip_slots:
                    if clip_slot.has_clip and clip_slot.is_playing:
                        return clip_slot.clip

    def _clear_param(self, value, control):
        key = control.message_identifier()
        if self._device:
            if key in self.del_parm_map:
                prev_clip = key in self.del_clip_map and self.del_clip_map[key] or None
                clip = self._get_clip_of_device()
                if clip:
                    if clip != prev_clip:
                        clip.clear_envelope(self.del_parm_map[key])
                        self.del_clip_map[key] = clip

    def set_device(self, device):
        DeviceComponent.set_device(self, device)
        if self.device_listener is not None:
            self.device_listener(device)

    def set_parameter_controls(self, controls):
        DeviceComponent.set_parameter_controls(self, controls)
        self._control_translation_selector.set_controls_to_translate(controls)
        self._control_translation_selector.set_mode(self._bank_index)

    def _on_parameters_changed(self):
        DeviceComponent._on_parameters_changed(self)
        if self.device_parm_listener is not None:
            self.device_parm_listener()

    def set_device_changed_listener(self, listener):
        self.device_listener = listener

    def set_device_parm_listener(self, listener):
        self.device_parm_listener = listener

    def show_message(self, message):
        self.canonical_parent.show_message(message)

    def disconnect(self):
        self._control_translation_selector.disconnect()
        self.device_listener = None
        self.device_parm_listener = None
        self.del_parm_map = None
        self.del_clip_map = None
        for touch_button in self.del_touch_buttons:
            touch_button.remove_value_listener(self._clear_param)

        if self.clear_mode:
            if not self.touch_mode:
                for control in self._parameter_controls:
                    self.touch_mode and control.remove_value_listener(self._clear_param)

        DeviceComponent.disconnect(self)
# okay decompiling src/MaschineDeviceComponent.pyc
