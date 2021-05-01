# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/TrackButtonHandler.py
# Compiled at: 2021-04-29 13:54:08
# Size of source mod 2**32: 10800 bytes
from _Framework.SubjectSlot import subject_slot
import _Framework.CompoundComponent as CompoundComponent
from .MidiMap import toHSB
from .PadColorButton import IndexedButton

def track_status(track):
    clipslots = track.clip_slots
    stop_fired = track.fired_slot_index == -2
    play_fired = track.fired_slot_index >= 0
    clip_playing = False
    has_clip = False
    if clipslots is not None:
        for cs_index in range(len(clipslots)):
            clip_slot = clipslots[cs_index]
            if clip_slot.has_clip:
                has_clip = True
                if clip_slot.clip.is_playing:
                    clip_playing = True
            elif clip_slot.controls_other_clips:
                has_clip = True
                if clip_slot.is_playing:
                    clip_playing = True
                if clip_slot.is_triggered:
                    play_fired = True
            elif clip_slot.is_triggered:
                stop_fired = True

    return (
     has_clip, clip_playing, stop_fired, play_fired)


def arm_exclusive(song, track=None):
    if not track:
        track = song.view.selected_track
    if track:
        if track.can_be_armed:
            tracks = song.tracks
            for songtrack in tracks:
                if songtrack != track and songtrack and songtrack.can_be_armed and songtrack.arm:
                    songtrack.arm = False

            track.arm = not track.arm


def solo_exclusive(song, track):
    if track:
        if not track.solo:
            tracks = song.tracks
            for songtrack in tracks:
                if songtrack != track and songtrack and songtrack.solo:
                    songtrack.solo = False

        track.solo = not track.solo


class TrackButtonHandler(CompoundComponent):

    def __init__(self, index, button, track_editor, *a, **k):
        (super(TrackButtonHandler, self).__init__)(*a, **k)
        assert isinstance(button, IndexedButton)
        self._index = index
        self._handle_button_value.subject = button
        self._button = button
        self._parameter = None
        self._track = None
        self._unbinder = None
        self._valueupdater = None
        self._action = None
        self._track_editor = track_editor
        self._use_track_color = True
        self._button.set_resource_handler(self.set_grabbed_state)

    def unbind(self):
        if self._unbinder:
            self._unbinder()

    def unbind_track(self):
        if self._track:
            self.unbind()
            self._track = None
            self._action = None
            self._button.unlight()
            self._unbinder = None

    def reset(self):
        self._button.refresh()

    @property
    def index(self):
        return self._index

    def set_color(self, color_list):
        self._button.set_color(color_list)

    def send_value(self, index):
        self._button.send_index(index)

    def unlight(self):
        self._button.unlight()

    def restore_color(self, color):
        pass

    def set_grabbed_state(self, grabbed):
        if not grabbed:
            if self._valueupdater:
                self._valueupdater(0)
            else:
                self._button.send_color(0)

    def update_value(self, blink_state=0):
        if not self._button.grabbed:
            if self._valueupdater:
                self._valueupdater(blink_state)

    def assign_xfade(self, track):
        self.unbind()
        if track is None:
            self._track = None
            return
        self._track = track
        self._handle_xfader.subject = track.mixer_device

        def unbind():
            self._handle_xfader.subject = None

        def update(blink_state=0):
            if self._track.mixer_device.crossfade_assign == 1:
                self._button.send_index(1)
            else:
                if self._track.mixer_device.crossfade_assign == 0:
                    self._button.send_index(0)
                else:
                    self._button.send_index(2)

        def action():
            self._track.mixer_device.crossfade_assign = (self._track.mixer_device.crossfade_assign + 1) % 3

        self._button.set_color((17, 37, 9))
        self._unbinder = unbind
        self._valueupdater = update
        self._action = action
        self._use_track_color = False
        return

    def assign_mute(self, track):
        self.unbind()
        if track is None:
            self._track = None
            return
        self._track = track
        self._handle_mute.subject = track

        def unbind():
            self._handle_mute.subject = None

        def update(blink_state=0):
            self._button.send_index(not self._track.mute and 1 or 0)

        def action():
            self._track.mute = not self._track.mute

        self._button.set_color((16, 18))
        self._unbinder = unbind
        self._valueupdater = update
        self._action = action
        self._use_track_color = False
        return

    def assign_solo(self, track):
        self.unbind()
        if track is None:
            self.disable()
            return
        self._track = track
        self._handle_solo.subject = track

        def unbind():
            self._handle_solo.subject = None

        def update(blink_state=0):
            self._button.send_index(self._track.solo and 1 or 0)

        def action():
            if self.canonical_parent.is_shift_down():
                self._track.solo = not self._track.solo
            else:
                solo_exclusive(self.song(), self._track)

        self._button.set_color((44, 46))
        self._unbinder = unbind
        self._valueupdater = update
        self._action = action
        self._use_track_color = False
        return

    def assign_arm(self, track):
        self.unbind()
        if track is None:
            self.disable()
            return
        else:
            self._track = track
            self._handle_arm.subject = track

            def unbind():
                self._handle_arm.subject = None

            def update(blink_state=0):
                if self._track.can_be_armed:
                    self._button.send_index(self._track.arm and 1 or 0)

            def action():
                if self._track.can_be_armed:
                    if self.canonical_parent.is_shift_down():
                        self._track.arm = not self._track.arm
                    else:
                        arm_exclusive(self.song(), self._track)

            if self._track.can_be_armed:
                self._button.set_color((4, 6))
            else:
                self._button.set_color((7, 7))
        self._unbinder = unbind
        self._valueupdater = update
        self._action = action
        self._use_track_color = False
        return

    @subject_slot('color')
    def _handle_color_changed(self):
        if self._track:
            if self._use_track_color:
                self._button.set_color(toHSB(self._track.color))

    def assign_select(self, track):
        self.unbind()
        if track is None:
            self.disable()
            return
        self._track = track

        def unbind():
            self._handle_color_changed.subject = None

        def update(blink_state=0):
            self._button.send_index(self._track != self.song().view.selected_track and 1 or 0)

        def action():
            self._track_editor.handle_track_select(self._track)

        self._handle_color_changed.subject = track
        self._button.set_color(toHSB(self._track.color))
        self._unbinder = unbind
        self._valueupdater = update
        self._action = action
        self._use_track_color = True
        return

    def handle_empty_selection(self):
        pass

    def assign_stop(self, track):
        self.unbind()
        if track is None:
            self.disable()
            return
        self._track = track
        self._handle_arm.subject = track

        def unbind():
            pass

        def update(blink_state=0):
            has_clip, clip_playing, stop_fired, _ = track_status(self._track)
            if has_clip:
                if stop_fired:
                    if blink_state % 2 == 1:
                        self._button.send_index(0)
                    else:
                        self._button.send_index(1)
                elif clip_playing:
                    self._button.send_index(1)
                else:
                    self._button.send_index(0)
            else:
                self._button.send_index(0)

        def action():
            self._track.stop_all_clips()

        oncolor, offcolor = toHSB(self._track.color)
        self._button.set_color((offcolor, oncolor))
        self._unbinder = unbind
        self._valueupdater = update
        self._action = action
        self._use_track_color = True
        return

    def disable(self, optional_action=None):
        self._button.unlight()
        if self._unbinder:
            self._unbinder()
            self._unbinder = None
        self._track = None
        self._action = optional_action
        self._valueupdater = None

    @subject_slot('mute')
    def _handle_mute(self):
        if self._track:
            self.update_value()

    @subject_slot('crossfade_assign')
    def _handle_xfader(self):
        if self._track:
            self.update_value()

    @subject_slot('arm')
    def _handle_arm(self):
        if self._track:
            self.update_value()

    @subject_slot('solo')
    def _handle_solo(self):
        if self._track:
            self.update_value()

    @subject_slot('value', identify_sender=True)
    def _handle_button_value(self, value, sender):
        if sender.grabbed:
            return
            if not self._button.grabbed:
                if value > 0 and self._action:
                    if self.canonical_parent.is_shift_down() and self._index == 1:
                        self.canonical_parent.toggle_mode()
        else:
            self._action()

    def assign_parameter(self, parameter):
        if self._parameter is not None:
            self._handle_value_changed.subject = None
        self._handle_value_changed.subject = parameter
        self._parameter = parameter
        self._button.send_value(self._parameter_to_value())
# okay decompiling scripts/TrackButtonHandler.pyc
