# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/_NativeInstruments/NIController.py
# Compiled at: 2021-05-26 13:27:36
# Size of source mod 2**32: 39133 bytes
"""
This script is based off the Ableton Live supplied MIDI Remote Scripts, customised
for OSC request delivery and response. This script can be run without any extra
Python libraries out of the box.

This is the third file that is loaded, by way of being instantiated through
__init__.py

"""
import Live, sys
from _NativeInstruments import NIControllerCallbacks, OSC, Helpers, Messages
from _NativeInstruments.Types import TrackType
from _NativeInstruments.Logger import log

class NIController:
    __module__ = __name__
    __doc__ = 'Main class that establishes the NI Controller Component'

    def __init__(self, c_instance, oscEndpoint):
        self.prlisten = {}
        self.plisten = {}
        self.dlisten = {}
        self.clisten = {}
        self.slisten = {}
        self.pplisten = {}
        self.cnlisten = {}
        self.cclisten = {}
        self.wlisten = {}
        self.llisten = {}
        _send_pos = {}
        self.mlisten = {'solo':{},  'mute':{},  'arm':{},  'panning':{},  'volume':{},  'sends':{},  'name':{},  'oml':{},  'omr':{}}
        self.rlisten = {'solo':{},  'mute':{},  'panning':{},  'volume':{},  'sends':{},  'name':{}}
        self.masterlisten = {'panning':{},  'volume':{},  'crossfader':{}}
        self.scenelisten = {}
        self.scene = 0
        self.track = 0
        self._NIController__c_instance = c_instance
        self.oscEndpoint = oscEndpoint
        self.basicAPI = 0
        self.oscEndpoint.send('/remix/oscserver/startup', 1)
        if self.song().visible_tracks_has_listener(self.refresh_state) != 1:
            self.song().add_visible_tracks_listener(self.refresh_state)

    def connect_script_instances(self, instanciated_scripts):
        """
        Called by the Application as soon as all scripts are initialized.
        You can connect yourself to other running scripts here, as we do it
        connect the extension modules
        """
        pass

    def is_extension(self):
        return False

    def request_rebuild_midi_map(self):
        """
        To be called from any components, as soon as their internal state changed in a
        way, that we do need to remap the mappings that are processed directly by the
        Live engine.
        Dont assume that the request will immediately result in a call to
        your build_midi_map function. For performance reasons this is only
        called once per GUI frame.
        """
        pass

    def update_display(self):
        """
        This function is run every 100ms, so we use it to initiate our Song.current_song_time
        listener to allow us to process incoming OSC commands as quickly as possible under
        the current listener scheme.
        """
        if self.basicAPI == 0:
            try:
                doc = self.song()
            except:
                log('could not get song handle')
                return

            try:
                self.basicAPI = NIControllerCallbacks.NIControllerCallbacks(self._NIController__c_instance, self.oscEndpoint)
                self.time = 0
                doc.add_current_song_time_listener(self.current_song_time_changed)
            except ConnectionError:
                self.oscEndpoint.send('/remix/echo', 'setting up basicAPI failed')
                log('setting up basicAPI failed')
                return

        if self.oscEndpoint:
            try:
                self.oscEndpoint.process_incoming_udp()
            except ConnectionError:
                log('error processing incoming UDP packets:', sys.exc_info())

    def current_song_time_changed(self):
        time = self.song().current_song_time
        if int(time) != self.time:
            self.time = int(time)
            self.oscEndpoint.send('/live/beat', self.time)

    def send_midi(self, midi_event_bytes):
        """
        Use this function to send MIDI events through Live to the _real_ MIDI devices
        that this script is assigned to.
        """
        pass

    def receive_midi(self, midi_bytes):
        pass

    def can_lock_to_devices(self):
        return False

    def suggest_input_port(self):
        return ''

    def suggest_output_port(self):
        return ''

    def __handle_display_switch_ids(self, switch_id, value):
        pass

    def application(self):
        """returns a reference to the application that we are running in"""
        return Live.Application.get_application()

    def song(self):
        """returns a reference to the Live Song that we do interact with"""
        return self._NIController__c_instance.song()

    def handle(self):
        """returns a handle to the c_interface that is needed when forwarding MIDI events via the MIDI map"""
        return self._NIController__c_instance.handle()

    def getslots(self):
        tracks = self.song().visible_tracks
        clipSlots = []
        for track in tracks:
            clipSlots.append(track.clip_slots)

        return clipSlots

    def trBlock(self, trackOffset):
        tracks = Helpers.visibleTracks()
        tracksCount = len(tracks)
        block = []
        for trackIndex in range(0, tracksCount):
            if trackOffset + trackIndex < tracksCount:
                block.extend([str(tracks[(trackOffset + trackIndex)].name)])

        self.oscEndpoint.send('/live/name/trackblock', block)

    def disconnect(self):
        self.rem_clip_listeners()
        self.rem_mixer_listeners()
        self.rem_scene_listeners()
        self.rem_tempo_listener()
        self.rem_overdub_listener()
        self.rem_tracks_listener()
        self.rem_device_listeners()
        self.rem_transport_listener()
        self.rem_record_listener()
        self.rem_loop_listener()
        self.rem_metronome_listener()
        self.rem_session_automation_record_listener()
        self.song().remove_visible_tracks_listener(self.refresh_state)
        self.oscEndpoint.send('/script/shutdown', 1)
        self.oscEndpoint.shutdown()

    def build_midi_map(self, midi_map_handle):
        self.refresh_state()

    def refresh_state(self):
        self.add_clip_listeners()
        self.add_mixer_listeners()
        self.add_scene_listeners()
        self.add_tempo_listener()
        self.add_overdub_listener()
        self.add_tracks_listener()
        self.add_device_listeners()
        self.add_transport_listener()
        self.add_record_listener()
        self.add_loop_listener()
        self.add_metronome_listener()
        self.add_session_automation_record_listener()
        trackNumber = 0
        clipNumber = 0
        self.tracks_change()
        for track in self.song().visible_tracks:
            bundle = OSC.OSCBundle()
            for clipSlot in track.clip_slots:
                if clipSlot.clip is not None:
                    bundle.append(Messages.clipInfo(trackNumber, clipNumber))
                clipNumber = clipNumber + 1

            clipNumber = 0
            trackNumber = trackNumber + 1
            self.oscEndpoint.send_message(bundle)

        self.trBlock(0)

    def add_scene_listeners(self):
        self.rem_scene_listeners()
        if self.song().view.selected_scene_has_listener(self.scene_change) != 1:
            self.song().view.add_selected_scene_listener(self.scene_change)
        if self.song().view.selected_track_has_listener(self.track_change) != 1:
            self.song().view.add_selected_track_listener(self.track_change)

    def rem_scene_listeners(self):
        if self.song().view.selected_scene_has_listener(self.scene_change) == 1:
            self.song().view.remove_selected_scene_listener(self.scene_change)
        if self.song().view.selected_track_has_listener(self.track_change) == 1:
            self.song().view.remove_selected_track_listener(self.track_change)

    def track_change(self):
        self.oscEndpoint.send_message(Messages.currentTrackIndex())

    def scene_change(self):
        self.oscEndpoint.send_message(Messages.currentSceneIndex())

    def add_tempo_listener(self):
        self.rem_tempo_listener()
        if self.song().tempo_has_listener(self.tempo_change) != 1:
            self.song().add_tempo_listener(self.tempo_change)

    def rem_tempo_listener(self):
        if self.song().tempo_has_listener(self.tempo_change) == 1:
            self.song().remove_tempo_listener(self.tempo_change)

    def tempo_change(self):
        self.oscEndpoint.send_message(Messages.tempo())

    def add_transport_listener(self):
        self.rem_transport_listener()
        if self.song().is_playing_has_listener(self.transport_change) != 1:
            self.song().add_is_playing_listener(self.transport_change)

    def rem_transport_listener(self):
        if self.song().is_playing_has_listener(self.transport_change) == 1:
            self.song().remove_is_playing_listener(self.transport_change)

    def transport_change(self):
        self.oscEndpoint.send('/live/play', self.song().is_playing and 2 or 1)

    def add_record_listener(self):
        self.rem_record_listener()
        if self.song().record_mode_has_listener(self.record_change) != 1:
            self.song().add_record_mode_listener(self.record_change)
        if self.song().session_record_has_listener(self.record_change) != 1:
            self.song().add_session_record_listener(self.record_change)

    def rem_record_listener(self):
        if self.song().record_mode_has_listener(self.record_change) == 1:
            self.song().remove_record_mode_listener(self.record_change)
        if self.song().session_record_has_listener(self.record_change) == 1:
            self.song().remove_session_record_listener(self.record_change)

    def record_change(self):
        self.oscEndpoint.send('/live/record', self.song().record_mode and 2 or 1)
        self.oscEndpoint.send('/live/session_record', self.song().session_record and 2 or 1)

    def add_loop_listener(self):
        self.rem_loop_listener()
        if self.song().loop_has_listener(self.loop_change) != 1:
            self.song().add_loop_listener(self.loop_change)

    def rem_loop_listener(self):
        try:
            if self.song().loop_has_listener(self.loop_change):
                self.song().remove_loop_listener(self.loop_change)
        except TypeError as te:
            try:
                log('Type error: {}'.format(te))
            finally:
                te = None
                del te

    def loop_change(self):
        self.oscEndpoint.send_message(Messages.loop())

    def add_metronome_listener(self):
        self.rem_metronome_listener()
        if self.song().metronome_has_listener(self.metronome_change) != 1:
            self.song().add_metronome_listener(self.metronome_change)

    def rem_metronome_listener(self):
        try:
            if self.song().metronome_has_listener(self.metronome_change):
                self.song().remove_metronome_listener(self.metronome_change)
        except TypeError as te:
            try:
                log('Type error: {}'.format(te))
            finally:
                te = None
                del te

    def metronome_change(self):
        metronome = Helpers.song().metronome
        self.oscEndpoint.send('/live/metronome', int(metronome) + 1)

    def add_session_automation_record_listener(self):
        self.rem_session_automation_record_listener()
        if self.song().session_automation_record_has_listener(self.session_automation_record_change) != 1:
            self.song().add_session_automation_record_listener(self.session_automation_record_change)

    def rem_session_automation_record_listener(self):
        try:
            if self.song().session_automation_record_has_listener(self.session_automation_record_change):
                self.song().remove_session_automation_record_listener(self.session_automation_record_change)
        except TypeError as te:
            try:
                log('Type error: {}'.format(te))
            finally:
                te = None
                del te

    def session_automation_record_change(self):
        session_automation_record = Helpers.song().session_automation_record
        self.oscEndpoint.send('/live/session_automation_record', int(session_automation_record))

    def add_overdub_listener(self):
        self.rem_overdub_listener()
        if self.song().overdub_has_listener(self.overdub_change) != 1:
            self.song().add_overdub_listener(self.overdub_change)

    def rem_overdub_listener(self):
        try:
            if self.song().overdub_has_listener(self.overdub_change):
                self.song().remove_overdub_listener(self.overdub_change)
        except TypeError as te:
            try:
                log('Type error: {}'.format(te))
            finally:
                te = None
                del te

    def overdub_change(self):
        overdub = Helpers.song().overdub
        self.oscEndpoint.send('/live/overdub', int(overdub) + 1)

    def add_tracks_listener(self):
        self.rem_tracks_listener()
        if not self.song().tracks_has_listener(self.tracks_change):
            self.song().add_tracks_listener(self.tracks_change)

    def rem_tracks_listener(self):
        try:
            if self.song().tracks_has_listener(self.tempo_change):
                self.song().remove_tracks_listener(self.tracks_change)
        except TypeError as te:
            try:
                log('Type error: {}'.format(te))
            finally:
                te = None
                del te

    def tracks_change(self):
        self.oscEndpoint.send_message(Messages.sizeInfo())
        self.oscEndpoint.send_message(Messages.currentTrackIndex())
        self.oscEndpoint.send_message(Messages.currentSceneIndex())

    def rem_clip_listeners(self):
        for slot in self.slisten:
            if slot is not None:
                cb = self.slisten.get(slot)
                try:
                    tmp = slot.has_clip_has_listener(cb)
                    if tmp:
                        slot.remove_has_clip_listener(cb)
                except TypeError as te:
                    try:
                        log('Type error: {}'.format(te))
                    finally:
                        te = None
                        del te

        self.slisten = {}
        for clip in self.clisten:
            if clip is not None:
                try:
                    if clip.playing_status_has_listener(self.clisten.get(clip)):
                        clip.remove_playing_status_listener(self.clisten.get(clip))
                except TypeError:
                    log()

        self.clisten = {}
        for clip in self.pplisten:
            if clip is not None:
                try:
                    if clip.playing_position_has_listener(self.pplisten.get(clip)):
                        clip.remove_playing_position_listener(self.pplisten.get(clip))
                except TypeError as te:
                    try:
                        log('Type error: {}'.format(te))
                    finally:
                        te = None
                        del te

        self.pplisten = {}
        for clip in self.cnlisten:
            if clip is not None:
                try:
                    if clip.name_has_listener(self.cnlisten.get(clip)):
                        clip.remove_name_listener(self.cnlisten.get(clip))
                except TypeError as te:
                    try:
                        log('Type error: {}'.format(te))
                    finally:
                        te = None
                        del te

        self.cnlisten = {}
        for clip in self.cclisten:
            if clip is not None:
                try:
                    if clip.color_has_listener(self.cclisten.get(clip)):
                        clip.remove_color_listener(self.cclisten.get(clip))
                except TypeError as te:
                    try:
                        log('Type error: {}'.format(te))
                    finally:
                        te = None
                        del te

        self.cclisten = {}
        for clip in self.wlisten:
            if clip is not None and clip.is_audio_clip:
                try:
                    if clip.warping_has_listener(self.wlisten.get(clip)):
                        clip.remove_warping_listener(self.wlisten.get(clip))
                except TypeError as te:
                    try:
                        log('Type error: {}'.format(te))
                    finally:
                        te = None
                        del te

        self.wlisten = {}
        for clip in self.llisten:
            if clip is not None:
                try:
                    if clip.looping_has_listener(self.llisten.get(clip)):
                        clip.remove_looping_listener(self.llisten.get(clip))
                except TypeError as te:
                    try:
                        log('Type error: {}'.format(te))
                    finally:
                        te = None
                        del te

        self.llisten = {}

    def add_clip_listeners(self):
        self.rem_clip_listeners()
        tracks = self.getslots()
        for track in range(len(tracks)):
            for clip in range(len(tracks[track])):
                c = tracks[track][clip]
                if c.clip is not None:
                    self.add_cliplistener(c.clip, track, clip)
                    log('ClipLauncher: added clip listener tr: ' + str(track) + ' clip: ' + str(clip))
                self.add_slotlistener(c, track, clip)

    def add_cliplistener(self, clip, tid, cid):
        cb = lambda : self.clip_changestate(clip, tid, cid)
        if (clip in self.clisten) != 1:
            clip.add_playing_status_listener(cb)
            self.clisten[clip] = cb
        cb3 = lambda : self.clip_name(clip, tid, cid)
        if (clip in self.cnlisten) != 1:
            clip.add_name_listener(cb3)
            self.cnlisten[clip] = cb3
        if (clip in self.cclisten) != 1:
            clip.add_color_listener(cb3)
            self.cclisten[clip] = cb3
        if clip.is_audio_clip:
            cb4 = lambda : self.clip_warping(clip, tid, cid)
            if (clip in self.wlisten) != 1:
                clip.add_warping_listener(cb4)
                self.wlisten[clip] = cb4
        cb5 = lambda : self.clip_looping(clip, tid, cid)
        if (clip in self.llisten) != 1:
            clip.add_looping_listener(cb5)
            self.llisten[clip] = cb5

    def add_slotlistener(self, slot, tid, cid):
        cb = lambda : self.slot_changestate(slot, tid, cid)
        if (slot in self.slisten) != 1:
            slot.add_has_clip_listener(cb)
            self.slisten[slot] = cb

    def rem_mixer_listeners(self):
        for type in ('volume', 'panning', 'crossfader'):
            for tr in self.masterlisten[type]:
                if tr is not None:
                    cb = self.masterlisten[type][tr]
                    test = eval('tr.mixer_device.' + type + '.value_has_listener(cb)')
                    if test == 1:
                        eval('tr.mixer_device.' + type + '.remove_value_listener(cb)')

        for type in ('arm', 'solo', 'mute'):
            for tr in self.mlisten[type]:
                if tr is not None:
                    cb = self.mlisten[type].get(tr)
                if cb:
                    if type == 'arm':
                        if tr is not None:
                            try:
                                tmp = tr.can_be_armed
                                if tmp:
                                    if tr.arm_has_listener(cb):
                                        tr.remove_arm_listener(cb)
                            except TypeError as te:
                                try:
                                    log('Type error: {}'.format(te))
                                finally:
                                    te = None
                                    del te

                    try:
                        test = eval('tr.' + type + '_has_listener(cb)')
                        if test:
                            eval('tr.remove_' + type + '_listener(cb)')
                    except TypeError as te:
                        try:
                            log('Type error: {}'.format(te))
                        finally:
                            te = None
                            del te

        for type in ('volume', 'panning'):
            for tr in self.mlisten[type]:
                if tr is not None:
                    cb = self.mlisten[type].get(tr)
                    if cb:
                        try:
                            test = eval('tr.mixer_device.' + type + '.value_has_listener(cb)')
                            if test == 1:
                                eval('tr.mixer_device.' + type + '.remove_value_listener(cb)')
                        except TypeError as te:
                            try:
                                log('Type error: {}'.format(te))
                            finally:
                                te = None
                                del te

        for tr in self.mlisten['sends']:
            if tr is not None:
                sends = self.mlisten['sends'].get(tr)
                if sends:
                    for send in sends:
                        if send is not None:
                            try:
                                cb = sends.get(send)
                                if send.value_has_listener(cb):
                                    send.remove_value_listener(cb)
                            except TypeError as te:
                                try:
                                    log('Type error: {}'.format(te))
                                finally:
                                    te = None
                                    del te

        for tr in self.mlisten['name']:
            if tr is not None:
                cb = self.mlisten['name'].get(tr)
                if cb and cb is not None:
                    try:
                        if tr.name_has_listener(cb):
                            tr.remove_name_listener(cb)
                    except TypeError as te:
                        try:
                            log('Type error: {}'.format(te))
                        finally:
                            te = None
                            del te

        for tr in self.mlisten['oml']:
            if tr is not None:
                cb = self.mlisten['oml'].get(tr)
                if cb and cb is not None:
                    try:
                        if tr.output_meter_left_has_listener(cb):
                            tr.remove_output_meter_left_listener(cb)
                    except TypeError as te:
                        try:
                            log('Type error: {}'.format(te))
                        finally:
                            te = None
                            del te

        for tr in self.mlisten['omr']:
            if tr is not None:
                cb = self.mlisten['omr'].get(tr)
                if cb:
                    try:
                        tmp = tr.output_meter_right_has_listener(cb)
                        if tmp:
                            tr.remove_output_meter_right_listener(cb)
                    except TypeError as te:
                        try:
                            log('Type error: {}'.format(te))
                        finally:
                            te = None
                            del te

        for type in ('solo', 'mute'):
            for tr in self.rlisten[type]:
                if tr is not None:
                    cb = self.rlisten[type].get(tr)
                    if cb:
                        try:
                            test = eval('tr.' + type + '_has_listener(cb)')
                            if test == 1:
                                eval('tr.remove_' + type + '_listener(cb)')
                        except TypeError as te:
                            try:
                                log('Type error: {}'.format(te))
                            finally:
                                te = None
                                del te

        for type in ('volume', 'panning'):
            for tr in self.rlisten[type]:
                if tr is not None:
                    cb = self.rlisten[type].get(tr)
                    if cb:
                        try:
                            test = eval('tr.mixer_device.' + type + '.value_has_listener(cb)')
                            if test == 1:
                                eval('tr.mixer_device.' + type + '.remove_value_listener(cb)')
                        except TypeError as te:
                            try:
                                log('Type error: {}'.format(te))
                            finally:
                                te = None
                                del te

        for tr in self.rlisten['sends']:
            if tr is not None:
                sends = self.rlisten['sends'].get(tr)
                if sends:
                    for send in sends:
                        if send is not None:
                            try:
                                cb = sends.get(send)
                                if send.value_has_listener(cb):
                                    send.remove_value_listener(cb)
                            except TypeError as te:
                                try:
                                    log('Type error: {}'.format(te))
                                finally:
                                    te = None
                                    del te

        for tr in self.rlisten['name']:
            if tr is not None:
                cb = self.rlisten['name'].get(tr)
                if cb:
                    try:
                        if tr.name_has_listener(cb):
                            tr.remove_name_listener(cb)
                    except TypeError as te:
                        try:
                            log('Type error: {}'.format(te))
                        finally:
                            te = None
                            del te

        self.mlisten = {'solo':{},  'mute':{},  'arm':{},  'panning':{},  'volume':{},  'sends':{},  'name':{},  'oml':{},  'omr':{}}
        self.rlisten = {'solo':{},  'mute':{},  'panning':{},  'volume':{},  'sends':{},  'name':{}}
        self.masterlisten = {'panning':{},  'volume':{},  'crossfader':{}}

    def add_mixer_listeners(self):
        print('adding mixer listeners')
        self.rem_mixer_listeners()
        tr = self.song().master_track
        for type in ('volume', 'panning', 'crossfader'):
            self.add_master_listener(0, type, tr)

        self.add_meter_listener(0, tr, 2)
        tracks = self.song().visible_tracks
        for track in range(len(tracks)):
            tr = tracks[track]
            self.add_trname_listener(track, tr, 0)
            if tr.has_audio_output:
                self.add_meter_listener(track, tr)
            if tr.can_be_armed:
                self.add_mixert_listener(track, 'arm', tr)
            for type in ('solo', 'mute'):
                self.add_mixert_listener(track, type, tr)

            for type in ('volume', 'panning'):
                self.add_mixerv_listener(track, type, tr)

            for sid in range(len(tr.mixer_device.sends)):
                self.add_send_listener(track, tr, sid, tr.mixer_device.sends[sid])

        tracks = self.song().return_tracks
        for track in range(len(tracks)):
            tr = tracks[track]
            self.add_trname_listener(track, tr, 1)
            self.add_meter_listener(track, tr, 1)
            for type in ('solo', 'mute'):
                self.add_retmixert_listener(track, type, tr)

            for type in ('volume', 'panning'):
                self.add_retmixerv_listener(track, type, tr)

            for sid in range(len(tr.mixer_device.sends)):
                self.add_retsend_listener(track, tr, sid, tr.mixer_device.sends[sid])

    def add_send_listener(self, tid, track, sid, send):
        if (track in self.mlisten['sends']) != 1:
            self.mlisten['sends'][track] = {}
        if (send in self.mlisten['sends'][track]) != 1:
            cb = lambda : self.send_changestate(tid, track, sid, send)
            self.mlisten['sends'][track][send] = cb
            send.add_value_listener(cb)

    def add_mixert_listener(self, tid, type, track):
        if (track in self.mlisten[type]) != 1:
            cb = lambda : self.mixert_changestate(type, tid, track)
            self.mlisten[type][track] = cb
            eval('track.add_' + type + '_listener(cb)')

    def add_mixerv_listener(self, tid, type, track):
        if (track in self.mlisten[type]) != 1:
            cb = lambda : self.mixerv_changestate(type, tid, track)
            self.mlisten[type][track] = cb
            eval('track.mixer_device.' + type + '.add_value_listener(cb)')

    def add_master_listener(self, tid, type, track):
        if (track in self.masterlisten[type]) != 1:
            cb = lambda : self.mixerv_changestate(type, tid, track, 2)
            self.masterlisten[type][track] = cb
            eval('track.mixer_device.' + type + '.add_value_listener(cb)')

    def add_retsend_listener(self, tid, track, sid, send):
        if (track in self.rlisten['sends']) != 1:
            self.rlisten['sends'][track] = {}
        if (send in self.rlisten['sends'][track]) != 1:
            cb = lambda : self.send_changestate(tid, track, sid, send, 1)
            self.rlisten['sends'][track][send] = cb
            send.add_value_listener(cb)

    def add_retmixert_listener(self, tid, type, track):
        if (track in self.rlisten[type]) != 1:
            cb = lambda : self.mixert_changestate(type, tid, track, 1)
            self.rlisten[type][track] = cb
            eval('track.add_' + type + '_listener(cb)')

    def add_retmixerv_listener(self, tid, type, track):
        if (track in self.rlisten[type]) != 1:
            cb = lambda : self.mixerv_changestate(type, tid, track, 1)
            self.rlisten[type][track] = cb
            eval('track.mixer_device.' + type + '.add_value_listener(cb)')

    def add_trname_listener(self, tid, track, ret=0):
        cb = lambda : self.trname_changestate(tid, track, ret)
        if ret == 1:
            if (track in self.rlisten['name']) != 1:
                self.rlisten['name'][track] = cb
        elif (track in self.mlisten['name']) != 1:
            self.mlisten['name'][track] = cb
        track.add_name_listener(cb)

    def add_meter_listener(self, tid, track, r=0):
        cb = lambda : self.meter_changestate(tid, track, 0, r)
        if track in self.mlisten['oml']:
            self.mlisten['oml'][track] = cb
        track.add_output_meter_left_listener(cb)
        cb = lambda : self.meter_changestate(tid, track, 1, r)
        if (track in self.mlisten['omr']) != 1:
            self.mlisten['omr'][track] = cb
        track.add_output_meter_right_listener(cb)

    def clip_warping(self, clip, x, y):
        log('clip_warping[' + str(x) + ', ' + str(y) + ']')
        self.oscEndpoint.send_message(Messages.clipStatus(x, y))

    def clip_looping(self, clip, x, y):
        log('clip_looping[' + str(x) + ', ' + str(y) + ']')
        self.oscEndpoint.send_message(Messages.clipStatus(x, y))

    def clip_name(self, clip, x, y):
        log('clip_name[' + str(x) + ', ' + str(y) + ']')
        self.oscEndpoint.send_message(Messages.clipInfo(x, y))

    def slot_changestate(self, slot, x, y):
        tmptrack = Helpers.genericTrack(x)
        if tmptrack is None:
            return
        if slot.clip is not None:
            log('slot_changestate[' + str(x) + ', ' + str(y) + ']: added clip')
            self.add_cliplistener(slot.clip, x, y)
            self.oscEndpoint.send_message(Messages.clipInfo(x, y))
            self.oscEndpoint.send_message(Messages.clipStatus(x, y))
        else:
            log('slot_changestate[' + str(x) + ', ' + str(y) + ']: removed clip')
            if slot.clip in self.clisten:
                slot.clip.remove_playing_status_listener(self.clisten[slot.clip])
            if slot.clip in self.pplisten:
                slot.clip.remove_playing_position_listener(self.pplisten[slot.clip])
            if slot.clip in self.cnlisten:
                slot.clip.remove_name_listener(self.cnlisten[slot.clip])
            if slot.clip in self.cclisten:
                slot.clip.remove_color_listener(self.cclisten[slot.clip])
            self.oscEndpoint.send_message(Messages.clipRemoved(x, y))

    def clip_changestate(self, clip, x, y):
        log('clip_changestate[' + str(x) + ', ' + str(y) + ']')
        self.oscEndpoint.send_message(Messages.clipStatus(x, y))

    def mixerv_changestate(self, type, tid, track, r=0):
        val = eval('track.mixer_device.' + type + '.value')
        types = {'panning':'pan',  'volume':'volume',  'crossfader':'crossfader'}
        trackType = track.has_audio_input and TrackType.AUDIO or TrackType.MIDI
        if track.is_foldable:
            trackType = TrackType.GROUP
        elif r == 2:
            trackType = TrackType.MASTER
        else:
            if r == 1:
                trackType = TrackType.RETURN
        self.oscEndpoint.send('/live/' + types[type], (trackType, tid, float(val)))

    def mixert_changestate(self, type, tid, track, r=0):
        val = eval('track.' + type)
        trackType = track.has_audio_input and TrackType.AUDIO or TrackType.MIDI
        if track.is_foldable:
            trackType = TrackType.GROUP
        if r == 1:
            trackType = TrackType.RETURN
        self.oscEndpoint.send('/live/' + type, (trackType, tid, int(val)))

    def send_changestate(self, tid, track, sid, send, r=0):
        val = send.value
        if r == 1:
            self.oscEndpoint.send('/live/return/send', (tid, sid, float(val)))
        else:
            self.oscEndpoint.send('/live/send', (tid, sid, float(val)))

    def trname_changestate(self, tid, track, r=0):
        if r == 1:
            self.oscEndpoint.send_message(Messages.trackInfo(TrackType.RETURN, tid))
        else:
            self.oscEndpoint.send_message(Messages.trackInfo(TrackType.GENERIC, tid))
            self.trBlock(0)

    def meter_changestate(self, tid, track, lr, r=0):
        if r == 2:
            if lr == 0:
                self.oscEndpoint.send('/live/meter', (tid, 4, 0, float(track.output_meter_left)))
            else:
                self.oscEndpoint.send('/live/meter', (tid, 4, 1, float(track.output_meter_right)))
        elif r == 1:
            if lr == 0:
                self.oscEndpoint.send('/live/meter', (tid, 3, 0, float(track.output_meter_left)))
            else:
                self.oscEndpoint.send('/live/meter', (tid, 3, 1, float(track.output_meter_right)))
        else:
            trackType = track.has_audio_input and 1 or 0
            if track.is_foldable:
                trackType = 2
            elif lr == 0:
                self.oscEndpoint.send('/live/meter', (tid, trackType, 0, float(track.output_meter_left)))
            else:
                self.oscEndpoint.send('/live/meter', (tid, trackType, 1, float(track.output_meter_right)))

    def add_device_listeners(self):
        self.rem_device_listeners()
        self.do_add_device_listeners(self.song().tracks, 0)
        self.do_add_device_listeners(self.song().return_tracks, 1)
        self.do_add_device_listeners([self.song().master_track], 2)

    def do_add_device_listeners(self, tracks, type):
        for i in range(len(tracks)):
            self.add_devicelistener(tracks[i], i, type)
            if len(tracks[i].devices) >= 1:
                for j in range(len(tracks[i].devices)):
                    self.add_devpmlistener(tracks[i].devices[j])
                    if len(tracks[i].devices[j].parameters) >= 1:
                        for k in range(len(tracks[i].devices[j].parameters)):
                            par = tracks[i].devices[j].parameters[k]
                            self.add_paramlistener(par, i, j, k, type)

    def rem_device_listeners(self):
        for pr in self.prlisten:
            if pr is not None:
                try:
                    ocb = self.prlisten[pr]
                    if pr.value_has_listener(ocb):
                        pr.remove_value_listener(ocb)
                except TypeError as te:
                    try:
                        log('Type error: {}'.format(te))
                    finally:
                        te = None
                        del te

        self.prlisten = {}
        for tr in self.dlisten:
            if tr is not None:
                ocb = self.dlisten.get(tr)
                if ocb:
                    try:
                        if tr.view.selected_device_has_listener(ocb):
                            tr.view.remove_selected_device_listener(ocb)
                    except TypeError as te:
                        try:
                            log('Type error: {}'.format(te))
                        finally:
                            te = None
                            del te

        self.dlisten = {}
        for de in self.plisten:
            if de is not None:
                ocb = self.plisten[de]
                if de.parameters_has_listener(ocb):
                    de.remove_parameters_listener(ocb)

        self.plisten = {}

    def add_devpmlistener(self, device):
        cb = lambda : self.devpm_change()
        if (device in self.plisten) != 1:
            device.add_parameters_listener(cb)
            self.plisten[device] = cb

    def devpm_change(self):
        self.refresh_state()

    def add_paramlistener(self, param, tid, did, pid, type):
        cb = lambda : self.param_changestate(param, tid, did, pid, type)
        if (param in self.prlisten) != 1:
            param.add_value_listener(cb)
            self.prlisten[param] = cb

    def param_changestate(self, param, tid, did, pid, type):
        if type == 2:
            self.oscEndpoint.send('/live/master/device/param', (did, pid, param.value, str(param.name)))
        else:
            if type == 1:
                self.oscEndpoint.send('/live/return/device/param', (tid, did, pid, param.value, str(param.name)))
            else:
                self.oscEndpoint.send('/live/device/param', (tid, did, pid, param.value, str(param.name)))

    def add_devicelistener(self, track, tid, type):
        cb = lambda : self.device_changestate(track, tid, type)
        if (track in self.dlisten) != 1:
            track.view.add_selected_device_listener(cb)
            self.dlisten[track] = cb

    def device_changestate(self, track, tid, type):
        did = self.tuple_idx(track.devices, track.view.selected_device)
        if type == 2:
            self.oscEndpoint.send('/live/master/devices/selected', did)
        else:
            if type == 1:
                self.oscEndpoint.send('/live/return/device/selected', (tid, did))
            else:
                self.oscEndpoint.send('/live/device/selected', (tid, did))
        self.oscEndpoint.send('/track/device/instance-name', str(Helpers.checkForKKInstance(tid)))

    def tuple_idx(self, tuple, obj):
        for i in range(0, len(tuple)):
            if tuple[i] == obj:
                return i
# okay decompiling src/_NativeInstruments/NIController.pyc
