# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Trial.app/Contents/App-Resources/MIDI Remote Scripts/Komplete_Kontrol_Mk1/FocusControl.py
# Compiled at: 2021-04-28 16:44:03
# Size of source mod 2**32: 18340 bytes
import socket, Live
from _Framework.SubjectSlot import subject_slot
from .SimpleDeviceComponent import SimpleDeviceComponent
from .GUtil import debug_out, register_sender
import _Framework.ControlSurface as ControlSurface
from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement, ON_VALUE, OFF_VALUE
import _Framework.TransportComponent as TransportComponent
BUTTON_STATE_OFF = 0
BUTTON_STATE_ON = 127
BUTTON_PRESSED = 1
BUTTON_RELEASED = 0
SID_FIRST = 0
SID_NAV_LEFT = 20
SID_NAV_RIGHT = 21
SID_TRANSPORT_LOOP = 86
SID_TRANSPORT_REWIND = 91
SID_TRANSPORT_FAST_FORWARD = 92
SID_TRANSPORT_STOP = 93
SID_TRANSPORT_PLAY = 94
SID_TRANSPORT_RECORD = 95
transport_control_switch_ids = list(range(SID_TRANSPORT_REWIND, SID_TRANSPORT_RECORD + 1))
SID_LAST = 112
PARAM_PREFIX = 'NIKB'
PLUGIN_PREFIX = 'Komplete Kontrol'
PLUGIN_CLASS_NAME_VST = 'PluginDevice'
PLUGIN_CLASS_NAME_AU = 'AuPluginDevice'

def device_info(device):
    if device:
        debug_out('  # ' + str(device.name) + ' Class: ' + str(device.class_name) + ' DisplayName: ' + str(device.class_display_name) + ' Type: ' + str(device.type))


def vindexof(alist, element):
    index = 0
    for ele in alist:
        if ele == element:
            return index
        index = index + 1


def arm_exclusive(song, track=None):
    if not track:
        track = song.view.selected_track
    if track:
        if track.can_be_armed:
            if not track.arm:
                tracks = song.tracks
                for songtrack in tracks:
                    if songtrack != track and songtrack and songtrack.can_be_armed and songtrack.arm:
                        songtrack.arm = False

                track.arm = True


class TrackElement:
    arm = False

    def __init__(self, index, track, receiver, *a, **k):
        self.index = index
        self.track = track
        if track.can_be_armed:
            self.arm = track.arm
            track.add_arm_listener(self._changed_arming)
        track.add_devices_listener(self._changed_devices)
        self.receiver = receiver

    def _changed_arming(self):
        if self.arm != self.track.arm:
            self.arm = self.track.arm
            if self.track.arm:
                self.receiver.activate_track(self.index, self.track)
            else:
                self.receiver.deactivate_track(self.index, self.track)

    def _changed_devices(self):
        if self.arm:
            self.receiver.devices_changed(self.index, self.track)

    def release(self):
        if self.track:
            if self.track.can_be_armed:
                self.track.remove_arm_listener(self._changed_arming)
        if self.track:
            self.track.remove_devices_listener(self._changed_devices)
        self.receiver = None
        self.track = None


class FocusControl(ControlSurface):
    controlled_track = None

    def __init__(self, c_instance):
        super().__init__(c_instance)
        self.song().add_is_playing_listener(self._FocusControl__update_play_button_led)
        register_sender(self)
        self._active = False
        self._tracks = []
        self.rewind_button_down = False
        self.forward_button_down = False
        with self.component_guard():
            self._set_suppress_rebuild_requests(True)
            self._suppress_send_midi = True
            device = SimpleDeviceComponent()
            self.set_device_component(device)
            self._on_selected_track_changed()
            self.set_up_controls()
            self.request_rebuild_midi_map()
            self._set_suppress_rebuild_requests(False)
            self._active = True
            self._suppress_send_midi = False
            self.transport = TransportComponent()
            self.transport.set_play_button(ButtonElement(False, MIDI_NOTE_TYPE, 0, SID_TRANSPORT_PLAY))
            self.transport.set_record_button(ButtonElement(False, MIDI_NOTE_TYPE, 0, SID_TRANSPORT_RECORD))
            self.transport.set_seek_buttons(ButtonElement(True, MIDI_NOTE_TYPE, 0, SID_TRANSPORT_FAST_FORWARD), ButtonElement(True, MIDI_NOTE_TYPE, 0, SID_TRANSPORT_REWIND))
            self.transport.set_loop_button(ButtonElement(False, MIDI_NOTE_TYPE, 0, SID_TRANSPORT_LOOP))
        self._assign_tracks()
        ctrack = self.get_controlled_track()
        if ctrack:
            track = ctrack[0]
            instr = ctrack[1]
            self.controlled_track = track
            index = list(self.song().tracks).index(track)
            self.update_status_midi(index, track, instr, 1)
        self.refresh_state()

    def refresh_state(self):
        self._FocusControl__update_play_button_led()

    def receive_midi(self, midi_bytes):
        if midi_bytes[0] & 240 == MIDI_NOTE_ON_STATUS or midi_bytes[0] & 240 == MIDI_NOTE_OFF_STATUS:
            note = midi_bytes[1]
            value = BUTTON_PRESSED if midi_bytes[2] > 0 else BUTTON_RELEASED
            if note in transport_control_switch_ids:
                self.handle_transport_switch_ids(note, value)
        super().receive_midi(midi_bytes)

    def handle_transport_switch_ids(self, switch_id, value):
        if switch_id == SID_TRANSPORT_REWIND:
            if value == BUTTON_PRESSED:
                self.rewind_button_down = True
            else:
                if value == BUTTON_RELEASED:
                    self.rewind_button_down = False
            self._FocusControl__update_forward_rewind_leds()
        else:
            if switch_id == SID_TRANSPORT_FAST_FORWARD:
                if value == BUTTON_PRESSED:
                    self.forward_button_down = True
                else:
                    if value == BUTTON_RELEASED:
                        self.forward_button_down = False
                self._FocusControl__update_forward_rewind_leds()
            else:
                if switch_id == SID_TRANSPORT_STOP:
                    if value == BUTTON_PRESSED:
                        self._FocusControl__stop_song()

    def __stop_song(self):
        self.song().stop_playing()
        self._FocusControl__update_play_button_led()

    def __update_play_button_led(self):
        if self.song().is_playing:
            self._send_midi((MIDI_NOTE_ON_STATUS, SID_TRANSPORT_PLAY, BUTTON_STATE_ON))
            self._send_midi((MIDI_NOTE_ON_STATUS, SID_TRANSPORT_STOP, BUTTON_STATE_OFF))
        else:
            self._send_midi((MIDI_NOTE_ON_STATUS, SID_TRANSPORT_PLAY, BUTTON_STATE_OFF))
            self._send_midi((MIDI_NOTE_ON_STATUS, SID_TRANSPORT_STOP, BUTTON_STATE_ON))

    def __update_forward_rewind_leds(self):
        if self.forward_button_down:
            self._send_midi((MIDI_NOTE_ON_STATUS, SID_TRANSPORT_FAST_FORWARD, BUTTON_STATE_ON))
        else:
            self._send_midi((MIDI_NOTE_ON_STATUS, SID_TRANSPORT_FAST_FORWARD, BUTTON_STATE_OFF))
        if self.rewind_button_down:
            self._send_midi((MIDI_NOTE_ON_STATUS, SID_TRANSPORT_REWIND, BUTTON_STATE_ON))
        else:
            self._send_midi((MIDI_NOTE_ON_STATUS, SID_TRANSPORT_REWIND, BUTTON_STATE_OFF))

    def set_up_controls(self):
        is_momentary = True
        self.left_button = ButtonElement(is_momentary, MIDI_CC_TYPE, 0, SID_NAV_LEFT)
        self.right_button = ButtonElement(is_momentary, MIDI_CC_TYPE, 0, SID_NAV_RIGHT)
        self._do_left.subject = self.left_button
        self._do_right.subject = self.right_button
        self.stop_button = ButtonElement(False, MIDI_NOTE_TYPE, 0, SID_TRANSPORT_STOP)
        self._do_stop.subject = self.stop_button

    @subject_slot('value')
    def _do_stop(self, value):
        self._FocusControl__stop_song()

    @subject_slot('value')
    def _do_left(self, value):
        assert value in range(128)
        if value != 0:
            self.navigate_midi_track(-1)

    @subject_slot('value')
    def _do_right(self, value):
        assert value in range(128)
        if value != 0:
            self.navigate_midi_track(1)

    def navigate_midi_track(self, direction):
        tracks = self.song().tracks
        seltrack = self.song().view.selected_track
        index = vindexof(tracks, seltrack)
        nxttrack = self.get_next_track(direction, index, tracks)
        if nxttrack:
            self.song().view.selected_track = nxttrack
            arm_exclusive(self.song(), nxttrack)

    def get_next_track(self, direction, index, tracks):
        pos = index
        if pos is None:
            pos = len(tracks)
        pos = pos + direction
        while 0 <= pos < len(tracks):
            track = tracks[pos]
            if track.can_be_armed:
                return track
            pos = pos + direction

    def get_next_midi_track(self, direction, index, tracks):
        pos = index
        if pos is None:
            pos = len(tracks)
        pos = pos + direction
        while 0 <= pos < len(tracks):
            track = tracks[pos]
            if track.can_be_armed:
                if track.has_midi_input:
                    return track
            pos = pos + direction

    def get_controlled_track(self):
        armed_tracks = []
        tracks = self.song().tracks
        for track in tracks:
            if track.can_be_armed and track.arm:
                armed_tracks.append(track)

        if len(armed_tracks) == 1:
            return (
             armed_tracks[0], self.find_instrument_list(armed_tracks[0].devices))
        if len(armed_tracks) > 1:
            instr = self.find_instrument_ni(armed_tracks)
            if instr:
                return instr
            return self.find_instrument_any(armed_tracks)

    def find_instrument_ni(self, tracks):
        for track in tracks:
            instr = self.find_instrument_list(track.devices)
            if instr and instr[1] is not None:
                return (
                 track, instr)

    def find_instrument_any(self, tracks):
        for track in tracks:
            instr = self.find_instrument_list(track.devices)
            if instr:
                return (
                 track, instr)

    def _assign_tracks(self):
        tracks = self.song().tracks
        for track in self._tracks:
            track.release()

        self._tracks = []
        for index in range(len(tracks)):
            self._tracks.append(TrackElement(index, tracks[index], self))

    def activate_track(self, index, track):
        self.controlled_track = track
        instr = self.find_instrument_list(track.devices)
        self.update_status_midi(index, track, instr, 1)

    def deactivate_track(self, index, track):
        pass

    def devices_changed(self, index, track):
        instr = self.find_instrument_list(track.devices)
        self.update_status_midi(index, track, instr, 1)

    def _on_track_list_changed(self):
        super()._on_track_list_changed()
        self._assign_tracks()
        ctrack = self.get_controlled_track()
        if ctrack:
            track = ctrack[0]
            instr = ctrack[1]
            if track != self.controlled_track:
                self.controlled_track = track
                index = list(self.song().tracks).index(track)
        elif self.controlled_track:
            self.controlled_track = None

    def _on_selected_track_changed(self):
        super()._on_selected_track_changed()
        self.set_controlled_track(self.song().view.selected_track)

    def broadcast(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not s:
            debug_out(' Could Not open Socket ')
        else:
            try:
                s.connect(('localhost', 60090))
                s.sendall('Hello, world'.encode('utf-8'))
                s.close()
            except ConnectionError:
                debug_out(' No Server ')

    @subject_slot('devices')
    def _on_devices_changed(self):
        self.scan_devices()

    def find_instrument_list(self, devicelist):
        for device in devicelist:
            instr = self.find_instrument(device)
            if instr:
                return instr

    def find_in_chain(self, chain):
        for device in chain.devices:
            instr = self.find_instrument(device)
            if instr:
                return instr

    def find_instrument(self, device):
        if device.type == 1:
            if device.can_have_chains:
                chains = device.chains
                for chain in chains:
                    instr = self.find_in_chain(chain)
                    if instr:
                        return instr

            else:
                if device.class_name == PLUGIN_CLASS_NAME_VST or device.class_name == PLUGIN_CLASS_NAME_AU:
                    if device.class_display_name.startswith(PLUGIN_PREFIX):
                        parms = device.parameters
                        if parms:
                            if len(parms) > 1:
                                pn = parms[1].name
                                pnLen = len(pn)
                                if pn.startswith(PARAM_PREFIX):
                                    return (str(device.class_display_name), str(pn[4:pnLen]))
            return (
             device.class_display_name, None)

    def scan_chain(self, chain):
        for device in chain.devices:
            self.scan_device(device)

    def scan_device(self, device):
        if device.class_name == 'PluginDevice' and device.class_display_name == 'FocusTester1':
            parms = device.parameters
        else:
            if device.can_have_chains:
                chains = device.chains
                for chain in chains:
                    self.scan_chain(chain)

    def update_status_midi(self, index, track, instrument, value):
        msgsysex = [
         240, 0, 0, 102, 20, 18, 0]
        tr_name = track.name
        for c in tr_name:
            msgsysex.append(ord(c))

        msgsysex.append(25)
        ind_str = str(index)
        for c in ind_str:
            msgsysex.append(ord(c))

        if instrument is not None:
            msgsysex.append(25)
            for c in instrument[0]:
                msgsysex.append(ord(c))

            if instrument[1] is not None:
                msgsysex.append(25)
                for c in instrument[1]:
                    msgsysex.append(ord(c))

        msgsysex.append(247)
        self._send_midi(tuple(msgsysex))

    def send_to_display(self, text, grid=0):
        if len(text) > 28:
            text = text[:27]
        msgsysex = [240, 0, 0, 102, 23, 18, min(grid, 3) * 28]
        filled = text.ljust(28)
        for c in filled:
            msgsysex.append(ord(c))

        msgsysex.append(247)
        self._send_midi(tuple(msgsysex))

    def scan_devices(self):
        song = self.song()
        for track in song.tracks:
            for device in track.devices:
                self.scan_device(device)

    def disconnect(self):
        self._active = False
        self._suppress_send_midi = True
        self.song().remove_is_playing_listener(self._FocusControl__update_play_button_led)
        super().disconnect()
# okay decompiling src/FocusControl.pyc
