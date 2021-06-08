# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/_NativeInstruments/NIControllerCallbacks.py
# Compiled at: 2021-05-19 16:19:00
# Size of source mod 2**32: 47030 bytes
import Live
from . import OSC
from . import Helpers
from . import Messages
from .Types import TrackType, PlayingStatus
from .Logger import log

class NIControllerCallbacks:

    def __init__(self, c_instance, oscEndpoint):
        self.oscEndpoint = oscEndpoint
        self.callbackManager = oscEndpoint.callbackManager
        self.c_instance = c_instance
        self.callbackManager.add('/script/init', self.initCB)
        self.callbackManager.add('/live/tempo', self.tempoCB)
        self.callbackManager.add('/live/time', self.timeCB)
        self.callbackManager.add('/live/next/cue', self.nextCueCB)
        self.callbackManager.add('/live/prev/cue', self.prevCueCB)
        self.callbackManager.add('/live/play', self.playCB)
        self.callbackManager.add('/live/record', self.recordCB)
        self.callbackManager.add('/live/session_record', self.sessionRecordCB)
        self.callbackManager.add('/live/play/continue', self.playContinueCB)
        self.callbackManager.add('/live/play/selection', self.playSelectionCB)
        self.callbackManager.add('/live/play/clip', self.playClipCB)
        self.callbackManager.add('/live/play/scene', self.playSceneCB)
        self.callbackManager.add('/live/stop', self.stopCB)
        self.callbackManager.add('/live/stop/clip', self.stopClipCB)
        self.callbackManager.add('/live/stop/all_clips', self.stopAllClipsCB)
        self.callbackManager.add('/live/stop/track', self.stopTrackCB)
        self.callbackManager.add('/live/scenes', self.scenesCB)
        self.callbackManager.add('/live/tracks', self.tracksCB)
        self.callbackManager.add('/live/returns', self.returnsCB)
        self.callbackManager.add('/live/name/scene', self.nameSceneCB)
        self.callbackManager.add('/live/scene', self.sceneCB)
        self.callbackManager.add('/live/name/sceneblock', self.nameSceneBlockCB)
        self.callbackManager.add('/live/name/trackblock', self.nameTrackBlockCB)
        self.callbackManager.add('/live/name/clip', self.nameClipCB)
        self.callbackManager.add('/live/name/clipblock', self.nameClipBlockCB)
        self.callbackManager.add('/live/arm', self.armTrackCB)
        self.callbackManager.add('/live/midi_arm_exclusive', self.armExclusiveCB)
        self.callbackManager.add('/live/mute', self.muteTrackCB)
        self.callbackManager.add('/live/solo', self.soloTrackCB)
        self.callbackManager.add('/live/volume', self.volumeCB)
        self.callbackManager.add('/live/pan', self.panCB)
        self.callbackManager.add('/live/send', self.sendCB)
        self.callbackManager.add('/live/track/jump', self.trackJump)
        self.callbackManager.add('/live/track/info', self.trackInfoCB)
        self.callbackManager.add('/live/undo', self.undoCB)
        self.callbackManager.add('/live/redo', self.redoCB)
        self.callbackManager.add('/live/play/clipslot', self.playClipSlotCB)
        self.callbackManager.add('/live/scene/view', self.viewSceneCB)
        self.callbackManager.add('/live/track/view', self.viewTrackCB)
        self.callbackManager.add('/live/return/view', self.viewTrackCB)
        self.callbackManager.add('/live/master/view', self.mviewTrackCB)
        self.callbackManager.add('/live/track/device/view', self.viewDeviceCB)
        self.callbackManager.add('/live/return/device/view', self.viewDeviceCB)
        self.callbackManager.add('/live/master/device/view', self.mviewDeviceCB)
        self.callbackManager.add('/live/clip/view', self.viewClipCB)
        self.callbackManager.add('/live/detail/view', self.detailViewCB)
        self.callbackManager.add('/live/overdub', self.overdubCB)
        self.callbackManager.add('/live/metronome', self.metronomeCB)
        self.callbackManager.add('/live/state', self.stateCB)
        self.callbackManager.add('/live/clip/info', self.clipInfoCB)
        self.callbackManager.add('/live/clip/status', self.clipStatusCB)
        self.callbackManager.add('/live/clip/pitch', self.clipPitchCB)
        self.callbackManager.add('/live/return/send', self.sendCB)
        self.callbackManager.add('/live/devicelist', self.devicelistCB)
        self.callbackManager.add('/live/return/devicelist', self.devicelistCB)
        self.callbackManager.add('/live/master/devicelist', self.mdevicelistCB)
        self.callbackManager.add('/live/device/range', self.devicerangeCB)
        self.callbackManager.add('/live/return/device/range', self.devicerangeCB)
        self.callbackManager.add('/live/master/device/range', self.mdevicerangeCB)
        self.callbackManager.add('/live/device', self.deviceCB)
        self.callbackManager.add('/live/return/device', self.deviceCB)
        self.callbackManager.add('/live/master/device', self.mdeviceCB)
        self.callbackManager.add('/live/clip/loopstate', self.loopStateCB)
        self.callbackManager.add('/live/clip/loopstart', self.loopStartCB)
        self.callbackManager.add('/live/clip/loopend', self.loopEndCB)
        self.callbackManager.add('/live/clip/loopstate_id', self.loopStateCB)
        self.callbackManager.add('/live/clip/loopstart_id', self.loopStartCB)
        self.callbackManager.add('/live/clip/loopend_id', self.loopEndCB)
        self.callbackManager.add('/live/clip/warping', self.warpingCB)
        self.callbackManager.add('/live/clip/signature', self.sigCB)
        self.callbackManager.add('/live/clip/add_note', self.addNoteCB)
        self.callbackManager.add('/live/clip/notes', self.getNotesCB)
        self.callbackManager.add('/live/clip/quantize', self.quantizeClipCB)
        self.callbackManager.add('/live/master/crossfader', self.crossfaderCB)
        self.callbackManager.add('/live/track/crossfader', self.trackxfaderCB)
        self.callbackManager.add('/live/return/crossfader', self.trackxfaderCB)
        self.callbackManager.add('/live/quantization', self.quantizationCB)
        self.callbackManager.add('/live/selection', self.selectionCB)
        self.callbackManager.add('/live/loop', self.loopCB)
        self.callbackManager.add('/live/tap_tempo', self.tapTempoCB)
        self.callbackManager.add('/live/session_automation_record', self.automationRecordCB)
        self.callbackManager.add('/live/scrub', self.scrubByCB)
        self.callbackManager.add('/script/ping', self.pingCB)

    def initCB(self, msg, source):
        """Called when a /live/init message is received.
        """
        self.oscEndpoint.send_message(Messages.sizeInfo())
        self.oscEndpoint.send_message(Messages.currentTrackIndex())
        self.oscEndpoint.send_message(Messages.currentSceneIndex())
        self.oscEndpoint.send_message(Messages.trackVolume(TrackType.MASTER, 0))
        self.oscEndpoint.send_message(Messages.trackPan(TrackType.MASTER, 0))
        self.oscEndpoint.send_message(Messages.sessionAutomationRecord())
        self.oscEndpoint.send_message(Messages.loop())

    def sigCB(self, msg, source):
        """ Called when a /live/clip/signature message is recieved
        """
        track = msg[2]
        clip = msg[3]
        c = Helpers.song().visible_tracks[track].clip_slots[clip].clip
        if len(msg) == 4:
            self.oscEndpoint.send('/live/clip/signature', (track, clip, c.signature_numerator, c.signature_denominator))
        if len(msg) == 6:
            self.oscEndpoint.send('/live/clip/signature', 1)
            c.signature_denominator = msg[5]
            c.signature_numerator = msg[4]

    def warpingCB(self, msg, source):
        """ Called when a /live/clip/warping message is recieved
        """
        track = msg[2]
        clip = msg[3]
        if len(msg) == 4:
            state = Helpers.song().visible_tracks[track].clip_slots[clip].clip.warping
            self.oscEndpoint.send('/live/clip/warping', (track, clip, int(state)))
        else:
            if len(msg) == 5:
                Helpers.song().visible_tracks[track].clip_slots[clip].clip.warping = msg[4]

    def selectionCB(self, msg, source):
        """ Called when a /live/selection message is received
        """
        if len(msg) == 6:
            self.c_instance.set_session_highlight(msg[2], msg[3], msg[4], msg[5], 0)

    def loopCB(self, msg, source):
        """ Called when a /live/loop message is received
        """
        if len(msg) == 2:
            self.oscEndpoint.send_message(Messages.loop())
        else:
            if len(msg) == 3:
                loopActive = msg[2]
                Helpers.song().loop = loopActive != 0

    def tapTempoCB(self, msg, source):
        """ Called when a /live/tap_tempo message is received
        """
        Helpers.song().tap_tempo()

    def automationRecordCB(self, msg, source):
        """ Called when a /live/session_automation_record message is received
        """
        if len(msg) == 3:
            automation = int(msg[2]) > 0 and 1 or 0
            Helpers.song().session_automation_record = automation
        else:
            self.oscEndpoint.send_message(Messages.sessionAutomationRecord())

    def scrubByCB(self, msg, source):
        """ Called when a /live/scrub_by message is received
        """
        if len(msg) == 3:
            value = msg[2]
            Helpers.song().scrub_by(value)

    def pingCB(self, msg, source):
        """ Called when a /script/ping message is received
        """
        self.oscEndpoint.send('/script/pong', 1)

    def trackxfaderCB(self, msg, source):
        """ Called when a /live/track/crossfader or /live/return/crossfader message is received
        """
        ty = msg[0] == '/live/return/crossfader' and 1 or 0
        if len(msg) == 3:
            track = msg[2]
            if ty == 1:
                assign = Helpers.song().return_tracks[track].mixer_device.crossfade_assign
                name = Helpers.song().return_tracks[track].mixer_device.crossfade_assignments.values[assign]
                self.oscEndpoint.send('/live/return/crossfader', (track, str(assign), str(name)))
            else:
                assign = Helpers.song().visible_tracks[track].mixer_device.crossfade_assign
                name = Helpers.song().visible_tracks[track].mixer_device.crossfade_assignments.values[assign]
                self.oscEndpoint.send('/live/track/crossfader', (track, str(assign), str(name)))
        else:
            if len(msg) == 4:
                track = msg[2]
                assign = msg[3]
                if ty == 1:
                    Helpers.song().return_tracks[track].mixer_device.crossfade_assign = assign
                else:
                    Helpers.song().visible_tracks[track].mixer_device.crossfade_assign = assign

    def tempoCB(self, msg, source):
        """Called when a /live/tempo message is received.

        Messages:
        /live/tempo                 Request current tempo, replies with /live/tempo (float tempo)
        /live/tempo (float tempo)   Set the tempo, replies with /live/tempo (float tempo)
        """
        if len(msg) == 2:
            self.oscEndpoint.send_message(Messages.tempo())
        else:
            if len(msg) == 3:
                tempo = msg[2]
                Helpers.setTempo(tempo)

    def timeCB(self, msg, source):
        """Called when a /live/time message is received.

        Messages:
        /live/time                 Request current song time, replies with /live/time (float time)
        /live/time (float time)    Set the time , replies with /live/time (float time)
        """
        if len(msg) == 2:
            self.oscEndpoint.send('/live/time', float(Helpers.currentSongTime()))
        else:
            if len(msg) == 3:
                time = msg[2]
                Helpers.setCurrentSongTime(time)

    def nextCueCB(self, msg, source):
        """Called when a /live/next/cue message is received.

        Messages:
        /live/next/cue              Jumps to the next cue point
        """
        Helpers.song().jump_to_next_cue()

    def prevCueCB(self, msg, source):
        """Called when a /live/prev/cue message is received.

        Messages:
        /live/prev/cue              Jumps to the previous cue point
        """
        Helpers.song().jump_to_prev_cue()

    def playCB(self, msg, source):
        """Called when a /live/play message is received.

        Messages:
        /live/play              Starts the song playing
        """
        Helpers.song().start_playing()

    def recordCB(self, msg, source):
        """Called when a /live/record message is received.

        Messages:
        /live/record     (int on/off)      Enables/disables recording
        """
        if len(msg) == 3:
            record = msg[2]
            Helpers.song().record_mode = record

    def sessionRecordCB(self, msg, source):
        """Called when a /live/record message is received.

        Messages:
        /live/session_record     (int on/off)      Enables/disables session recording
        """
        if len(msg) == 3:
            session_record = msg[2]
            Helpers.song().session_record = session_record

    def playContinueCB(self, msg, source):
        """Called when a /live/play/continue message is received.

        Messages:
        /live/play/continue     Continues playing the song from the current point
        """
        Helpers.song().continue_playing()

    def playSelectionCB(self, msg, source):
        """Called when a /live/play/selection message is received.

        Messages:
        /live/play/selection    Plays the current selection
        """
        Helpers.song().play_selection()

    def playClipCB(self, msg, source):
        """Called when a /live/play/clip message is received.

        Messages:
        /live/play/clip     (int track, int clip)   Launches clip number clip in track number track
        """
        if len(msg) == 4:
            c = Helpers.song().clip(int(msg[2]), int(msg[3]))
            if c is not None:
                c.fire()

    def playSceneCB(self, msg, source):
        """Called when a /live/play/scene message is received.

        Messages:
        /live/play/scene    (int scene)     Launches scene number scene
        """
        if len(msg) == 3:
            s = Helpers.scene(int(msg[2]))
            if s is not None:
                s.fire()

    def stopCB(self, msg, source):
        """Called when a /live/stop message is received.

        Messages:
        /live/stop              Stops playing the song
        """
        Helpers.song().stop_playing()

    def stopClipCB(self, msg, source):
        """Called when a /live/stop/clip message is received.

        Messages:
        /live/stop/clip     (int track, int clip)   Stops clip number clip in track number track
        """
        if len(msg) == 4:
            c = Helpers.song().clip(int(msg[2]), int(msg[3]))
            if c is not None:
                c.stop()

    def stopAllClipsCB(self, msg, source):
        """Called when a /live/stop/all_clips message is received.

        Messages:
        /live/stop/all_clips        Stops all clips
        """
        if len(msg) == 2:
            Helpers.song().stop_all_clips()

    def stopTrackCB(self, msg, source):
        """Called when a /live/stop/track message is received.

        Messages:
        /live/stop/track     (int track)   Stops track number track
        """
        if len(msg) == 3:
            t = Helpers.genericTrack(int(msg[2]))
            if t is not None:
                t.stop_all_clips()

    def scenesCB(self, msg, source):
        """Called when a /live/scenes message is received.

        Messages:
        /live/scenes        no argument  Returns the total number of scenes

        """
        if len(msg) == 2:
            sceneTotal = len(Helpers.scenes())
            self.oscEndpoint.send('/live/scenes', sceneTotal)
            return

    def sceneCB(self, msg, source):
        """Called when a /live/scene message is received.

        Messages:
        /live/scene         no argument  Returns the currently playing scene number
        """
        if len(msg) == 2:
            self.oscEndpoint.send_message(Messages.currentSceneIndex())
        else:
            if len(msg) == 3:
                scene = msg[2]
                Helpers.song().view.selected_scene = Helpers.song().scenes[scene]

    def tracksCB(self, msg, source):
        """Called when a /live/tracks message is received.

        Messages:
        /live/tracks       no argument  Returns the total number of tracks

        """
        if len(msg) == 2:
            trackTotal = len(Helpers.visibleTracks())
            self.oscEndpoint.send('/live/tracks', trackTotal)
            return

    def returnsCB(self, msg, source):
        """Called when a /live/returns message is received.

        Messages:
        /live/returns       no argument  Returns the total number of return tracks

        """
        if len(msg) == 2:
            trackTotal = len(Helpers.song().return_tracks)
            self.oscEndpoint.send('/live/returns', trackTotal)
            return

    def nameSceneCB(self, msg, source):
        """Called when a /live/name/scene message is received.

        Messages:
        /live/name/scene                            Returns a a series of all the scene names in the form /live/name/scene (int scene, string name)
        /live/name/scene    (int scene)             Returns a single scene's name in the form /live/name/scene (int scene, string name)
        /live/name/scene    (int scene, string name)Sets scene number scene's name to name

        """
        if len(msg) == 2:
            bundle = OSC.OSCBundle()
            sceneNumber = 0
            for scene in Helpers.scenes():
                bundle.append('/live/name/scene', (sceneNumber, str(scene.name)))
                sceneNumber = sceneNumber + 1

            self.oscEndpoint.send_message(bundle)
        else:
            if len(msg) == 3:
                sceneNumber = msg[2]
                self.oscEndpoint.send('/live/name/scene', (sceneNumber, str(Helpers.scene(sceneNumber).name)))
            else:
                if len(msg) == 4:
                    sceneNumber = msg[2]
                    name = msg[3]
                    Helpers.scene(sceneNumber).name = name

    def nameSceneBlockCB(self, msg, source):
        """Called when a /live/name/sceneblock message is received.

        /live/name/clipblock    (int offset, int blocksize) Returns a list of blocksize scene names starting at offset
        """
        if len(msg) == 4:
            block = []
            sceneOffset = msg[2]
            blocksize = msg[3]
            for scene in range(0, blocksize):
                block.extend([str(Helpers.scene(sceneOffset + scene).name)])

            self.oscEndpoint.send('/live/name/sceneblock', block)

    def nameTrackBlockCB(self, msg, source):
        """Called when a /live/name/trackblock message is received.

        /live/name/trackblock    (int offset, int blocksize) Returns a list of blocksize track names starting at offset
        """
        if len(msg) == 4:
            block = []
            trackOffset = msg[2]
            blocksize = msg[3]
            for track in range(0, blocksize):
                block.extend([str(Helpers.genericTrack(trackOffset + track).name)])

            self.oscEndpoint.send('/live/name/trackblock', block)

    def nameClipBlockCB(self, msg, source):
        """Called when a /live/name/clipblock message is received.

        /live/name/clipblock    (int track, int clip, blocksize x/tracks, blocksize y/clipslots) Returns a list of clip names for a block of clips (int blockX, int blockY, clipname)

        """
        if len(msg) == 6:
            block = []
            trackOffset = msg[2]
            clipOffset = msg[3]
            blocksizeX = msg[4]
            blocksizeY = msg[5]
            for clip in range(0, blocksizeY):
                for track in range(0, blocksizeX):
                    trackNumber = trackOffset + track
                    clipNumber = clipOffset + clip
                    block.extend([Helpers.clipName(trackNumber, clipNumber)])

            self.oscEndpoint.send('/live/name/clipblock', block)

    def nameClipCB(self, msg, source):
        """Called when a /live/name/clip message is received.

        Messages:
        /live/name/clip                                      Returns a a series of all the clip names in the form /live/name/clip (int track, int clip, string name)
        /live/name/clip    (int track, int clip)             Returns a single clip's name in the form /live/name/clip (int clip, string name)
        /live/name/clip    (int track, int clip, string name)Sets clip number clip in track number track's name to name

        """
        if len(msg) == 2:
            trackNumber = 0
            clipNumber = 0
            for track in Helpers.visibleTracks():
                bundle = OSC.OSCBundle()
                for clipSlot in track.clip_slots:
                    if clipSlot.clip is not None:
                        bundle.append('/live/name/clip', (
                         trackNumber, clipNumber, str(clipSlot.clip.name), clipSlot.clip.color))
                    clipNumber = clipNumber + 1

                self.oscEndpoint.send_message(bundle)
                clipNumber = 0
                trackNumber = trackNumber + 1

            return
        if len(msg) == 4:
            trackNumber = msg[2]
            clipNumber = msg[3]
            self.oscEndpoint.send('/live/name/clip', (
             trackNumber, clipNumber, Helpers.clipName(trackNumber, clipNumber),
             Helpers.clip(trackNumber, clipNumber).color))
            return
        if len(msg) >= 5:
            trackNumber = msg[2]
            clipNumber = msg[3]
            name = msg[4]
            Helpers.clip(trackNumber, clipNumber).name = name
        if len(msg) >= 6:
            trackNumber = msg[2]
            clipNumber = msg[3]
            color = msg[5]
            Helpers.clip(trackNumber, clipNumber).color = color

    def addNoteCB(self, msg, source):
        """Called when a /live/clip/add_note message is received

        Messages:
        /live/clip/add_note (int pitch) (double time) (double duration) (int velocity) (bool muted)    Add the given note to the clip
        """
        selected_notes = self._current_clip.get_selected_notes_extended()
        trackNumber = msg[2]
        clipNumber = msg[3]
        pitch = msg[4]
        time = msg[5]
        duration = msg[6]
        velocity = msg[7]
        muted = msg[8]
        Helpers.clip(trackNumber, clipNumber).deselect_all_notes()
        for selected_note in selected_notes:
            selected_note.pitch = pitch
            selected_note.start_time = time
            selected_note.duration = duration
            selected_note.velocity = velocity
            selected_note.muted = muted

        Helpers.clip(trackNumber, clipNumber).apply_note_modifications(selected_notes)
        self.oscEndpoint.send('/live/clip/note', (trackNumber, clipNumber, pitch, time, duration, velocity, muted))

    def getNotesCB(self, msg, source):
        """Called when a /live/clip/notes message is received

        Messages:
        /live/clip/notes    Return all notes in the clip in /live/clip/note messages.  Each note is sent in the format
                            (int trackNumber) (int clipNumber) (int pitch) (double time) (double duration) (int velocity) (int muted)
        """
        trackNumber = msg[2]
        clipNumber = msg[3]
        Helpers.clip(trackNumber, clipNumber).select_all_notes()
        bundle = OSC.OSCBundle()
        for note in Helpers.clip(trackNumber, clipNumber).get_selected_notes():
            pitch = note[0]
            time = note[1]
            duration = note[2]
            velocity = note[3]
            muted = 0
            if note[4]:
                muted = 1
            bundle.append('/live/clip/note', (trackNumber, clipNumber, pitch, time, duration, velocity, muted))

        self.oscEndpoint.send_message(bundle)

    def quantizeClipCB(self, msg, source):
        """Called when a /live/clip/quantize message is received.

        Messages:
        /live/clip/quantize                               Quantize current clip
        """
        Helpers.quantizeCurrentClip()

    def armTrackCB(self, msg, source):
        """Called when a /live/arm message is received.

        Messages:
        /live/arm     (int track)   (int armed/disarmed)     Arms track number track
        """
        if len(msg) == 3:
            self.oscEndpoint.send_message(Messages.trackArm(int(msg[2])))
        else:
            if len(msg) == 4:
                Helpers.armTrack(int(msg[2]), int(msg[3]) > 0 and 1 or 0)

    def armExclusiveCB(self, msg, source):
        """Called when a /live/midi_arm_exclusive message is received.

        Messages:
        /live/midi_arm_exclusive
        """
        if len(msg) == 2:
            focusedTrack = Helpers.song().view.selected_track
            shouldArm = focusedTrack is not None and not focusedTrack.is_foldable and not focusedTrack.has_audio_input
            for index, track in enumerate(Helpers.visibleTracks()):
                shouldDisarm = track is not None and not track.is_foldable and not track.has_audio_input
                if track == focusedTrack:
                    if shouldArm:
                        Helpers.armTrack(index, 1)
                if shouldDisarm:
                    Helpers.armTrack(index, 0)

    def muteTrackCB(self, msg, source):
        """Called when a /live/mute message is received.

        Messages:
        /live/mute     (int trackType, int track)  Returns the mute state for the selected track
        /live/mute     (int trackType, int track, int state)   Mutes the selected track
        """
        if len(msg) < 4:
            return
        else:
            trackType = int(msg[2])
            trackIndex = int(msg[3])
            if len(msg) == 4:
                self.oscEndpoint.send_message(Messages.trackMute(trackType, trackIndex))
            else:
                if len(msg) == 5:
                    Helpers.muteTrack(trackType, trackIndex, int(msg[4]) > 0 and 1 or 0)

    def soloTrackCB(self, msg, source):
        """Called when a /live/solo message is received.

        Messages:
        /live/solo     (int trackType, int track)   Returns the solo state for the selected track
        /live/solo     (int trackType, int track, int state)   Soloes the selected track
        """
        if len(msg) < 4:
            return
        else:
            trackType = int(msg[2])
            trackIndex = int(msg[3])
            if len(msg) == 4:
                self.oscEndpoint.send_message(Messages.trackSolo(trackType, trackIndex))
            else:
                if len(msg) == 5:
                    Helpers.soloTrack(trackType, trackIndex, int(msg[4]) > 0 and 1 or 0)

    def volumeCB(self, msg, source):
        """Called when a /live/volume message is received.

        Messages:
        /live/volume     (int trackType, int track)                            Returns the current volume of track number track as: /live/volume (int track, float volume(0.0 to 1.0))
        /live/volume     (int trackType, int track, float volume(0.0 to 1.0))  Sets track number track's volume to volume
        """
        if len(msg) < 4:
            return
        trackType = int(msg[2])
        trackIndex = int(msg[3])
        if len(msg) == 4:
            self.oscEndpoint.send_message(Messages.trackVolume(trackType, trackIndex))
        else:
            if len(msg) == 5:
                volume = msg[4]
                track = Helpers.track(trackType, trackIndex)
                if track is not None:
                    if volume >= 0.0:
                        if volume <= 1.0:
                            track.mixer_device.volume.value = volume

    def panCB(self, msg, source):
        """Called when a /live/pan message is received.

        Messages:
        /live/pan     (int trackType, int track)                            Returns the pan of track number track as: /live/pan (int track, float pan(-1.0 to 1.0))
        /live/pan     (int trackType, int track, float pan(-1.0 to 1.0))    Sets track number track's pan to pan

        """
        if len(msg) < 4:
            return
        trackType = int(msg[2])
        trackIndex = int(msg[3])
        if len(msg) == 4:
            self.oscEndpoint.send_message(Messages.trackPan(trackType, trackIndex))
        else:
            if len(msg) == 5:
                panning = msg[4]
                track = Helpers.track(trackType, trackIndex)
                if track is not None:
                    if panning >= -1.0:
                        if panning <= 1.0:
                            track.mixer_device.panning.value = panning

    def sendCB(self, msg, source):
        """Called when a /live/send message is received.

        Messages:
        /live/send     (int trackType, int track)                                        Returns the send level of all sends on track number track as: /live/send (int track, int send, float level(0.0 to 1.0))
        /live/send     (int trackType, int track, int send)                              Returns the send level of send (send) on track number track as: /live/send (int track, int send, float level(0.0 to 1.0))
        /live/send     (int trackType, int track, int send, float level(0.0 to 1.0))     Sets the send (send) of track number (track)'s level to (level)

        """
        if len(msg) < 4:
            return
        trackType = int(msg[2])
        trackIndex = int(msg[3])
        if len(msg) == 4:
            self.oscEndpoint.send_message(Messages.trackSends(trackType, trackIndex))
        if len(msg) == 5:
            self.oscEndpoint.send_message(Messages.trackSend(trackType, trackIndex, int(msg[4])))
        else:
            if len(msg) == 6:
                sendIndex = int(msg[4])
                sendValue = msg[5]
                track = Helpers.track(trackType, trackIndex)
                if track is not None:
                    if len(track.mixer_device.sends) > sendIndex:
                        if 0.0 <= sendValue <= 1.0:
                            track.mixer_device.sends[sendIndex].value = sendValue

    def trackJump(self, msg, source):
        """Called when a /live/track/jump message is received.

        Messages:
        /live/track/jump     (int track, float beats)   Jumps in track's currently running session clip by beats
        """
        if len(msg) == 4:
            track = msg[2]
            beats = msg[3]
            track = Helpers.genericTrack(track)
            track.jump_in_running_session_clip(beats)

    def trackInfoCB(self, msg, source):
        """Called when a /live/track/info message is received.

        Messages:
        /live/track/info     (int track)   Returns trackType, trackIndex, name, color, arm, solo, mute, volume, panning
        """
        if len(msg) < 4:
            return
        trackType = int(msg[2])
        trackIndex = int(msg[3])
        self.oscEndpoint.send_message(Messages.trackInfo(trackType, trackIndex))

    def undoCB(self, msg, source):
        """Called when a /live/undo message is received.

        Messages:
        /live/undo      Requests the song to undo the last action
        """
        Helpers.song().undo()
        can_undo = Helpers.song().can_undo and 1 or 0
        can_redo = Helpers.song().can_redo and 1 or 0
        self.oscEndpoint.send('/live/undo_redo', (can_undo, can_redo))

    def redoCB(self, msg, source):
        """Called when a /live/redo message is received.

        Messages:
        /live/redo      Requests the song to redo the last action
        """
        Helpers.song().redo()
        can_undo = Helpers.song().can_undo and 1 or 0
        can_redo = Helpers.song().can_redo and 1 or 0
        self.oscEndpoint.send('/live/undo_redo', (can_undo, can_redo))

    def playClipSlotCB(self, msg, source):
        """Called when a /live/play/clipslot message is received.

        Messages:
        /live/play/clipslot     (int track, int clip)   Launches clip number clip in track number track
        """
        if len(msg) == 4:
            track_num = msg[2]
            clip_num = msg[3]
            if track_num < len(Helpers.visibleTracks()):
                track = Helpers.genericTrack(track_num)
                clipslot = track.clip_slots[clip_num]
                clipslot.fire()
            else:
                scene = Helpers.scene(clip_num)
                scene.fire()

    def viewSceneCB(self, msg, source):
        """Called when a /live/scene/view message is received.

        Messages:
        /live/scene/view     (int track)      Selects a track to view
        """
        if len(msg) == 3:
            scene = msg[2]
            Helpers.song().view.selected_scene = Helpers.song().scenes[scene]

    def viewTrackCB(self, msg, source):
        """Called when a /live/track/view message is received.

        Messages:
        /live/track/view     (int track)      Selects a track to view
        """
        ty = msg[0] == '/live/return/view' and 1 or 0
        track_num = msg[2]
        if len(msg) == 3:
            if ty == 1:
                track = Helpers.song().return_tracks[track_num]
            else:
                track = Helpers.song().visible_tracks[track_num]
            Helpers.song().view.selected_track = track
            Live.Application.get_application().view.show_view('Detail/DeviceChain')

    def mviewTrackCB(self, msg, source):
        """Called when a /live/master/view message is received.

        Messages:
        /live/track/view     (int track)      Selects a track to view
        """
        track = Helpers.song().master_track
        Helpers.song().view.selected_track = track
        Live.Application.get_application().view.show_view('Detail/DeviceChain')

    def viewClipCB(self, msg, source):
        """Called when a /live/clip/view message is received.

        Messages:
        /live/clip/view     (int track, int clip)      Selects a track to view
        """
        track = Helpers.song().visible_tracks[msg[2]]
        if len(msg) == 4:
            clip = msg[3]
        else:
            clip = 0
        Helpers.song().view.selected_track = track
        Helpers.song().view.detail_clip = track.clip_slots[clip].clip
        Live.Application.get_application().view.show_view('Detail/Clip')

    def detailViewCB(self, msg, source):
        """Called when a /live/detail/view message is received. Used to switch between clip/track detail

        Messages:
        /live/detail/view (int) Selects view where 0=clip detail, 1=track detail
        """
        if len(msg) == 3:
            if msg[2] == 0:
                Live.Application.get_application().view.show_view('Detail/Clip')
            else:
                if msg[2] == 1:
                    Live.Application.get_application().view.show_view('Detail/DeviceChain')

    def viewDeviceCB(self, msg, source):
        """Called when a /live/track/device/view message is received.

        Messages:
        /live/track/device/view     (int track)      Selects a track to view
        """
        ty = msg[0] == '/live/return/device/view' and 1 or 0
        track_num = msg[2]
        if len(msg) == 4:
            if ty == 1:
                track = Helpers.song().return_tracks[track_num]
            else:
                track = Helpers.song().visible_tracks[track_num]
            Helpers.song().view.selected_track = track
            Helpers.song().view.select_device(track.devices[msg[3]])
            Live.Application.get_application().view.show_view('Detail/DeviceChain')

    def mviewDeviceCB(self, msg, source):
        track = Helpers.song().master_track
        if len(msg) == 3:
            Helpers.song().view.selected_track = track
            Helpers.song().view.select_device(track.devices[msg[2]])
            Live.Application.get_application().view.show_view('Detail/DeviceChain')

    def overdubCB(self, msg, source):
        """Called when a /live/overdub message is received.

        Messages:
        /live/overdub     (int on/off)      Enables/disables overdub
        """
        if len(msg) == 3:
            overdub = msg[2]
            Helpers.song().overdub = overdub

    def metronomeCB(self, msg, source):
        """Called when a /live/metronome message is received.

        Messages:
        /live/metronome     (int on/off)      Enables/disables metronome
        """
        if len(msg) == 2:
            self.oscEndpoint.send('/live/metronome', int(Helpers.song().metronome) + 1)
        if len(msg) == 3:
            metronome = msg[2]
            Helpers.song().metronome = metronome

    def stateCB(self, msg, source):
        """Called when a /live/state is received.

        Messages:
        /live/state                    Returns the current tempo and overdub status
        """
        if len(msg) == 2:
            tempo = Helpers.tempo()
            overdub = Helpers.song().overdub
            self.oscEndpoint.send('/live/state', (tempo, int(overdub)))

    def clipInfoCB(self, msg, source):
        """Called when a /live/clip/info message is received.

        Messages:
        /live/clip/info     (int track, int clip)      Gets the info of a single clip
        """
        if len(msg) == 4:
            self.oscEndpoint.send_message(Messages.clipInfo(int(msg[2]), int(msg[3])))

    def clipStatusCB(self, msg, source):
        """Called when a /live/clip/status message is received.

        Messages:
        /live/clip/status     (int track, int clip)      Gets the status of a single clip
        """
        if len(msg) == 4:
            self.oscEndpoint.send_message(Messages.clipStatus(int(msg[2]), int(msg[3])))

    def clipPitchCB(self, msg, source):
        """Called when a /live/clip/pitch message is received.

        Messages:
        /live/clip/pitch     (int track, int clip)                                               Returns the pan of track number track as: /live/pan (int track, int clip, int coarse(-48 to 48), int fine (-50 to 50))
        /live/clip/pitch     (int track, int clip, int coarse(-48 to 48), int fine (-50 to 50))  Sets clip number clip in track number track's pitch to coarse / fine

        """
        if len(msg) >= 5:
            c = clip(int(msg[2]), int(msg[3]))
            if c is not None:
                c.pitch_coarse = msg[4]
                if len(msg) == 6:
                    c.pitch_fine = msg[5]
        elif len(msg) == 4:
            self.oscEndpoint.send_message(Messages.clipPitch(int(msg[2]), int(msg[3])))

    def deviceCB(self, msg, source):
        ty = msg[0] == '/live/return/device' and 1 or 0
        track = msg[2]
        if len(msg) == 4:
            device = msg[3]
            po = [track, device]
            if ty == 1:
                params = Helpers.song().return_tracks[track].devices[device].parameters
            else:
                params = Helpers.song().visible_tracks[track].devices[device].parameters
            for i in range(len(params)):
                po.append(i)
                po.append(float(params[i].value))
                po.append(str(params[i].name))

            self.oscEndpoint.send(ty == 1 and '/live/return/device/allparam' or '/live/device/allparam', tuple(po))
        else:
            if len(msg) == 5:
                device = msg[3]
                param = msg[4]
                if ty == 1:
                    p = Helpers.song().return_tracks[track].devices[device].parameters[param]
                else:
                    p = Helpers.song().visible_tracks[track].devices[device].parameters[param]
                self.oscEndpoint.send(ty == 1 and '/live/return/device/param' or '/live/device/param', (
                 track, device, param, p.value, str(p.name)))
            else:
                if len(msg) == 6:
                    device = msg[3]
                    param = msg[4]
                    value = msg[5]
                    if ty == 1:
                        Helpers.song().return_tracks[track].devices[device].parameters[param].value = value
                    else:
                        Helpers.song().visible_tracks[track].devices[device].parameters[param].value = value

    def devicerangeCB(self, msg, source):
        ty = msg[0] == '/live/return/device/range' and 1 or 0
        track = msg[2]
        if len(msg) == 4:
            device = msg[3]
            po = [track, device]
            if ty == 1:
                params = Helpers.song().return_tracks[track].devices[device].parameters
            else:
                params = Helpers.song().visible_tracks[track].devices[device].parameters
            for i in range(len(params)):
                po.append(i)
                po.append(params[i].min)
                po.append(params[i].max)

            self.oscEndpoint.send(ty == 1 and '/live/return/device/range' or '/live/device/range', tuple(po))
        else:
            if len(msg) == 5:
                device = msg[3]
                param = msg[4]
                if ty == 1:
                    p = Helpers.song().return_tracks[track].devices[device].parameters[param]
                else:
                    p = Helpers.song().visible_tracks[track].devices[device].parameters[param]
                self.oscEndpoint.send(ty == 1 and '/live/return/device/range' or '/live/device/range', (
                 track, device, param, p.min, p.max))

    def devicelistCB(self, msg, source):
        ty = msg[0] == '/live/return/devicelist' and 1 or 0
        track = msg[2]
        if len(msg) == 3:
            do = [
             track]
            if ty == 1:
                devices = Helpers.song().return_tracks[track].devices
            else:
                devices = Helpers.song().visible_tracks[track].devices
            for i in range(len(devices)):
                do.append(i)
                do.append(str(devices[i].name))

            self.oscEndpoint.send(ty == 1 and '/live/return/devicelist' or '/live/devicelist', tuple(do))

    def mdeviceCB(self, msg, source):
        if len(msg) == 3:
            device = msg[2]
            po = [device]
            params = Helpers.song().master_track.devices[device].parameters
            for i in range(len(params)):
                po.append(i)
                po.append(float(params[i].value))
                po.append(str(params[i].name))

            self.oscEndpoint.send('/live/master/device', tuple(po))
        else:
            if len(msg) == 4:
                device = msg[2]
                param = msg[3]
                p = Helpers.song().master_track.devices[device].parameters[param]
                self.oscEndpoint.send('/live/master/device', (device, param, p.value, str(p.name)))
            else:
                if len(msg) == 5:
                    device = msg[2]
                    param = msg[3]
                    value = msg[4]
                    Helpers.song().master_track.devices[device].parameters[param].value = value

    def mdevicerangeCB(self, msg, source):
        if len(msg) == 3:
            device = msg[2]
            po = [device]
            params = Helpers.song().master_track.devices[device].parameters
            for i in range(len(params)):
                po.append(i)
                po.append(params[i].max)
                po.append(params[i].min)

            self.oscEndpoint.send('/live/master/device/range', tuple(po))
        else:
            if len(msg) == 4:
                device = msg[2]
                param = msg[3]
                p = Helpers.song().master_track.devices[device].parameters[param]
                self.oscEndpoint.send('/live/master/device/range', (device, param, p.min, p.max))

    def mdevicelistCB(self, msg, source):
        if len(msg) == 2:
            do = []
            devices = Helpers.song().master_track.devices
            for i in range(len(devices)):
                do.append(i)
                do.append(str(devices[i].name))

            self.oscEndpoint.send('/live/master/devicelist', tuple(do))

    def crossfaderCB(self, msg, source):
        if len(msg) == 2:
            self.oscEndpoint.send('/live/master/crossfader', float(Helpers.song().master_track.mixer_device.crossfader.value))
        else:
            if len(msg) == 3:
                val = msg[2]
                Helpers.song().master_track.mixer_device.crossfader.value = val

    def loopStateCB(self, msg, source):
        type = msg[0] == '/live/clip/loopstate_id' and 1 or 0
        trackNumber = msg[2]
        clipNumber = msg[3]
        if len(msg) == 4:
            if type == 1:
                self.oscEndpoint.send('/live/clip/loopstate', (
                 trackNumber, clipNumber, int(Helpers.clip(trackNumber, clipNumber).looping)))
            else:
                self.oscEndpoint.send('/live/clip/loopstate', int(Helpers.clip(trackNumber, clipNumber).looping))
        elif len(msg) == 5:
            loopState = msg[4]
            Helpers.clip(trackNumber, clipNumber).looping = loopState

    def loopStartCB(self, msg, source):
        type = msg[0] == '/live/clip/loopstart_id' and 1 or 0
        trackNumber = msg[2]
        clipNumber = msg[3]
        if len(msg) == 4:
            if type == 1:
                self.oscEndpoint.send('/live/clip/loopstart', (
                 trackNumber, clipNumber, float(Helpers.clip(trackNumber, clipNumber).loop_start)))
            else:
                self.oscEndpoint.send('/live/clip/loopstart', float(Helpers.clip(trackNumber, clipNumber).loop_start))
        elif len(msg) == 5:
            loopStart = msg[4]
            Helpers.clip(trackNumber, clipNumber).loop_start = loopStart

    def loopEndCB(self, msg, source):
        type = msg[0] == '/live/clip/loopend_id' and 1 or 0
        trackNumber = msg[2]
        clipNumber = msg[3]
        if len(msg) == 4:
            if type == 1:
                self.oscEndpoint.send('/live/clip/loopend', (
                 trackNumber, clipNumber, float(Helpers.clip(trackNumber, clipNumber).loop_end)))
            else:
                self.oscEndpoint.send('/live/clip/loopend', float(Helpers.clip(trackNumber, clipNumber).loop_end))
        elif len(msg) == 5:
            loopEnd = msg[4]
            Helpers.clip(trackNumber, clipNumber).loop_end = loopEnd

    def quantizationCB(self, msg, source):
        if len(msg) == 4:
            recordQuantization = msg[2]
            clipTriggerQuantization = msg[3]
            Helpers.song().midi_recording_quantization = recordQuantization
            Helpers.song().clip_trigger_quantization = clipTriggerQuantization
        else:
            recordQuantization = int(Helpers.song().midi_recording_quantization)
            clipTriggerQuantization = int(Helpers.song().clip_trigger_quantization)
            self.oscEndpoint.send('/live/quantization', (recordQuantization, clipTriggerQuantization))
# okay decompiling src/_NativeInstruments/NIControllerCallbacks.pyc
