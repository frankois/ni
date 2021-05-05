# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/EncoderHandler.py
# Compiled at: 2021-05-04 12:11:01
# Size of source mod 2**32: 10088 bytes
from _Framework.SubjectSlot import subject_slot
import _Framework.CompoundComponent as CompoundComponent
N_PARM_RANGE = 200

class EncoderHandler(CompoundComponent):
    _parameter = None
    _track = None
    _grid_control = None
    _edit_active = False
    _parm_to_midi = None
    _midi_to_parm = None
    _touch_handle = None
    _slider_handle = None
    _confirmed_type = False
    _has_audio = False
    _use_metering = False

    def __init__(self, index, encoder, touchbutton, control, *a, **k):
        (super().__init__)(*a, **k)
        self._index = index
        self._touchbutton = touchbutton
        self._handle_touch.subject = touchbutton
        self._handle_encoder_value.subject = encoder
        self._encoder_control = control
        self._encoder = encoder
        self._laster_meter_val = -1
        self._parm_change = self._handle_parm_change
        self._last_touch_val = None
        self._is_quantized = False
        self._parm_raster_value = 1

    def assign_parameter(self, parameter, track=None, disable_grid=True, use_metering=False):
        """
        Assign parameter to encoder.
    
        parameter:
            the parameter to assign
        track:
            the associated track 
        disable_grid:
            reset the basic display, only needed for metering tracks
        use_metering:
            track shows current output value
        """
        self._use_metering = use_metering
        if self._parameter is not None:
            self._handle_value_changed.subject = None
        self._parameter = parameter
        if parameter is not None:
            self._handle_value_changed.subject = parameter
            self._grid_control = None
            self._is_quantized = False
            if self._parameter.is_quantized:
                self._parm_to_midi = self._int_parm_to_value
                self._midi_to_parm = self._convert_int
                self._confirmed_type = True
                self._is_quantized = True
            else:
                self._parm_to_midi = self._parameter_to_value
                self._midi_to_parm = self._convert_range
                self._confirmed_float = False
                parm_range = parameter.max - parameter.min
                self._parm_raster_value = int((parameter.value - parameter.min) / parm_range * N_PARM_RANGE + 0.1)
            use_metering or self._encoder.set_display_value(self._parm_to_midi(), True)
        else:
            if disable_grid:
                self._encoder.set_display_value(0, True)
                self._grid_control = None
            else:
                if track:
                    self._track = track
                    self._device_change.subject = self._track
                    self._color_changed.subject = self._track
                    self._output_meter_changed.subject = None
                    self._output_meter_changed_left.subject = None
                else:
                    self._track = None
                    self._output_meter_changed.subject = None
                    self._output_meter_changed_left.subject = None
                    self._color_changed.subject = None
                    self._device_change.subject = None
                if track and use_metering:
                    if self._track.has_audio_output:
                        self._output_meter_changed_left.subject = self._track
                        self._output_meter_changed.subject = None
                        self._has_audio = True
                    else:
                        self._output_meter_changed.subject = self._track
                        self._output_meter_changed_left.subject = None
                        self._has_audio = False
                    self._parm_change = self._handle_level_change
                    if self._parameter:
                        val = max(0, min(127, int((self._parameter.value - self._parameter.min) / (self._parameter.max - self._parameter.min) * 127)))
                        if self._encoder.is_grabbed:
                            self._encoder.led_value = val
                        else:
                            self._encoder.led_value = val
                            self._encoder_control.set_led_value(self._index, val)
                        if self._track.has_audio_output:
                            meterval = int(127 * pow(max(self._track.output_meter_left, self._track.output_meter_right), 2.0))
                            self._encoder.set_display_value(meterval, True)
                else:
                    self._parm_change = self._handle_parm_change
            self._encoder_control.reset_led()

    def _int_parm_to_value(self):
        if self._parameter:
            return max(0, min(127, int((self._parameter.value - self._parameter.min) / (self._parameter.max - self._parameter.min) * 127)))
        return 0

    def _parameter_to_value(self):
        if self._parameter:
            return max(0, min(127, int((self._parameter.value - self._parameter.min) / (self._parameter.max - self._parameter.min) * 127)))
        return 0

    @property
    def index(self):
        return self._index

    @subject_slot('color')
    def _color_changed(self):
        self._encoder_control.update_touchstrip_color()

    @subject_slot('output_meter_level')
    def _output_meter_changed(self):
        if self._track:
            if self._use_metering:
                val = int(127 * self._track.output_meter_level)
                if val != self._laster_meter_val:
                    self._encoder.set_display_value(val, True)
                    self._laster_meter_val = val

    @subject_slot('output_meter_left')
    def _output_meter_changed_left(self):
        if self._track:
            if self._use_metering:
                val = int(127 * pow(max(self._track.output_meter_left, self._track.output_meter_right), 2.0))
                if val != self._laster_meter_val:
                    self._encoder.set_display_value(val, True)
                    self._laster_meter_val = val

    @subject_slot('devices')
    def _device_change(self):
        if self._track.has_audio_output:
            self._output_meter_changed_left.subject = self._track
            self._output_meter_changed.subject = None
        else:
            self._output_meter_changed.subject = self._track
            self._output_meter_changed_left.subject = None
        if (self._has_audio or self._track).has_audio_output:
            self._has_audio = True
        else:
            if self._has_audio:
                if not self._track.has_audio_output:
                    self._has_audio = False

    @subject_slot('value')
    def _handle_value_changed(self):
        self._parm_change()

    def _handle_parm_change(self):
        self._encoder.set_display_value(self._parm_to_midi(), True)

    def _handle_level_change(self):
        if self._parameter:
            val = max(0, min(127, int((self._parameter.value - self._parameter.min) / (self._parameter.max - self._parameter.min) * 127)))
            self._encoder.led_value = val
            if not self._encoder.is_grabbed:
                self._encoder.led_value = val
                self._encoder_control.set_led_value(self._index, val)
                self._encoder_control.update_led()

    def reset_level_led(self):
        if self._encoder.is_grabbed:
            self._encoder.led_value = 0
        else:
            self._encoder_control.set_led_value(self._index, 0)

    def send_value(self, value, force=False):
        self._encoder.set_display_value(value, force)

    def set_grid(self, value, grid_control):
        self._encoder.set_display_value(value, True)
        self._grid_control = grid_control

    def set_encoder_cfg(self, mode, color):
        self._encoder._set_cfg(mode, color)

    def get_strip_cfg(self):
        return self._encoder.get_strip_cfg()

    def refresh(self):
        if self._parameter is not None:
            if self._track is None:
                self._encoder.set_display_value(self._parm_to_midi(), True)

    @subject_slot('value')
    def _handle_touch(self, value):
        if value == 0:
            self._last_touch_val = None
        self._edit_active = value != 0
        if self._parameter:
            if value != 0:
                self._encoder_control.notify_touch(self._parameter)

    def _convert_int(self, midi_value):
        return int((self._parameter.max - self._parameter.min) / 127 * midi_value + 0.5) + self._parameter.min

    def _convert_range(self, midi_value):
        return (self._parameter.max - self._parameter.min) / 127 * midi_value + self._parameter.min

    @subject_slot('value')
    def _handle_encoder_value(self, value):
        if self._encoder.is_grabbed:
            return
            if self._encoder_control.is_shift_down():
                if self._last_touch_val is not None:
                    diff = value - self._last_touch_val
                    if diff != 0:
                        self._parameter.value = self.change_parm(diff, self._parameter, self._is_quantized)
                self._last_touch_val = value
                return
            if self._encoder_control.is_modifier_down():
                return
            if self._parameter:
                nval = self._midi_to_parm(value)
                self._parameter.value = nval
                if not self._confirmed_type:
                    diff = abs(nval - self._parameter.value)
                    if diff > 0.2:
                        self._midi_to_parm = self._convert_int
                        self._confirmed_type = True
                        self._is_quantized = True
        elif self._grid_control:
            self._grid_control.level_change(self._index, value)
        return

    def change_parm(self, diff, parm, is_quant):
        if is_quant:
            delta = diff > 0 and 1 or diff < 0 and -1 or 0
            parm_range = parm.max - parm.min + 1
            new_val = min(parm.max, max(parm.min, parm.value + delta))
            return float(new_val)
        delta = diff
        parm_range = parm.max - parm.min
        self._parm_raster_value = min(N_PARM_RANGE, max(0, self._parm_raster_value + delta))
        return float(self._parm_raster_value) / float(N_PARM_RANGE) * parm_range + parm.min
# okay decompiling src/EncoderHandler.pyc
