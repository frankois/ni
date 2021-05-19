# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_Mikro_Mk2/MaschineChannelStripComponent.py
# Compiled at: 2021-04-30 12:09:45
# Size of source mod 2**32: 5430 bytes
import Live
import _Framework.ChannelStripComponent as ChannelStripComponent
import _Framework.ButtonElement as ButtonElement
from _Framework.InputControlElement import *

class MaschineChannelStripComponent(ChannelStripComponent):

    def __init__(self):
        ChannelStripComponent.__init__(self)
        self.deleted = {}
        self.clear_mode = False
        self.touch_mode = False
        self.send_control = None
        self.clear_vol_button = None
        self.clear_pan_button = None
        self.clear_send_button = None

    def set_touch_mode(self, touchchannel):
        self.touch_mode = True
        id_vol = self._volume_control.message_identifier()
        id_pan = self._pan_control.message_identifier()
        id_send = None
        for send in self._send_controls:
            if send:
                id_send = send.message_identifier()

        self.clear_vol_button = ButtonElement(False, MIDI_CC_TYPE, touchchannel, id_vol)
        self.clear_vol_button.add_value_listener(self._do_clear_vol)
        self.clear_pan_button = ButtonElement(False, MIDI_CC_TYPE, touchchannel, id_pan)
        self.clear_pan_button.add_value_listener(self._do_clear_pan)
        self.clear_send_button = ButtonElement(False, MIDI_CC_TYPE, touchchannel, id_send)
        self.clear_send_button.add_value_listener(self._do_clear_send)
        for send in self._send_controls:
            if send:
                self.send_control = send

    def enter_clear(self):
        self.clear_mode = True
        self.deleted = {}
        if not self.touch_mode:
            self.set_enabled(False)
            self._volume_control.add_value_listener(self._do_clear_vol)
            self._pan_control.add_value_listener(self._do_clear_pan)
            for send in self._send_controls:
                if send:
                    self.send_control = send
                    send.add_value_listener(self._do_clear_send)

    def exit_clear(self):
        self.clear_mode = False
        if not self.touch_mode:
            self._volume_control.remove_value_listener(self._do_clear_vol)
            self._pan_control.remove_value_listener(self._do_clear_pan)
            for send in self._send_controls:
                if send:
                    send.remove_value_listener(self._do_clear_send)

            self.set_enabled(True)

    def _do_clear_vol(self, value):
        key = self._volume_control.message_identifier()
        if self.clear_mode:
            if key not in self.deleted:
                self.deleted[key] = True
                playing_clip = self._get_playing_clip()
                if playing_clip:
                    playing_clip.clear_envelope(self._track.mixer_device.volume)

    def _do_clear_pan(self, value):
        key = self._pan_control.message_identifier()
        if self.clear_mode:
            if key not in self.deleted:
                self.deleted[key] = True
                playing_clip = self._get_playing_clip()
                if playing_clip:
                    playing_clip.clear_envelope(self._track.mixer_device.panning)

    def _do_clear_send(self, value):
        key = self.send_control.message_identifier()
        if self.clear_mode:
            if key not in self.deleted:
                send_index = len(self._send_controls) - 1
                self.deleted[key] = True
                playing_clip = self._get_playing_clip()
                if playing_clip:
                    if send_index in range(len(self._track.mixer_device.sends)):
                        playing_clip.clear_envelope(self._track.mixer_device.sends[send_index])

    def _mute_value(self, value):
        super(MaschineChannelStripComponent, self)._mute_value(value)
        key = self._mute_button.message_identifier()
        if self.clear_mode:
            if key not in self.deleted:
                self.deleted[key] = True
                playing_clip = self._get_playing_clip()
                if playing_clip:
                    playing_clip.clear_envelope(self._track.mixer_device.track_activator)

    def _get_playing_clip(self):
        if self._track == None:
            return
        clips_slots = self._track.clip_slots
        for cs in clips_slots:
            if cs.has_clip and cs.is_playing:
                return cs.clip

        return

    def disconnect(self):
        self.clear_pan_button = None
        self.clear_send_button = None
        if self.clear_vol_button != None:
            self.clear_vol_button.remove_value_listener(self._do_clear_vol)
            self.clear_vol_button = None
        elif self.clear_pan_button != None:
            self.clear_pan_button.remove_value_listener(self._do_clear_pan)
            self.clear_pan_button = None
        else:
            if self.clear_send_button != None:
                self.clear_send_button.remove_value_listener(self._do_clear_send)
                self.clear_send_button = None
            if not self.touch_mode:
                if self.clear_mode:
                    if self.send_control != None:
                        self.send_control.remove_value_listener(self._do_clear_send)
                        self.send_control = None
                    if self._volume_control != None:
                        self._volume_control.remove_value_listener(self._do_clear_vol)
                        self._volume_control = None
                    if self._pan_control != None:
                        self._pan_control.remove_value_listener(self._do_clear_pan)
                        self._pan_control = None
        super(MaschineChannelStripComponent, self).disconnect()
# okay decompiling src/MaschineChannelStripComponent.pyc
