# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/TrackControlComponent.py
# Compiled at: 2021-05-04 12:11:01
# Size of source mod 2**32: 6484 bytes
from _Framework.SubjectSlot import subject_slot
import _Framework.CompoundComponent as CompoundComponent
from _Framework.InputControlElement import MIDI_NOTE_TYPE
from .MidiMap import colorOnOff, CI_WARM_YELLOW, CI_BLUE, CI_RED, CI_CYAN, CI_PURPLE, CI_LIGHT_ORANGE, CI_OFF, SEL_MODE_SELECT, SEL_MODE_SOLO, SEL_MODE_STOP, SEL_MODE_MUTE, SEL_MODE_ARM, SEL_MODE_XFADE
from .TrackButtonHandler import TrackButtonHandler
from .PadColorButton import IndexedButton
from .ModifierComponent import MASK_SELECT, MASK_SHIFT, MASK_BROWSE
from .JamButtonMatrix import IndexButtonMatrix
COLORLIST = [
 colorOnOff(CI_WARM_YELLOW),
 colorOnOff(CI_BLUE),
 colorOnOff(CI_RED),
 colorOnOff(CI_CYAN),
 colorOnOff(CI_PURPLE),
 colorOnOff(CI_LIGHT_ORANGE),
 colorOnOff(CI_OFF),
 colorOnOff(CI_OFF)]

class TrackControlComponent(CompoundComponent):

    def __init__(self, session, track_editor, *a, **k):
        (super().__init__)(*a, **k)
        self._bmatrix = IndexButtonMatrix(72, name='Track_Select_Button_Matrix')
        self._buttons = [self.create_buttons(index, track_editor) for index in range(8)]
        self._bmatrix.add_row(tuple([trackButtonHandler._button for trackButtonHandler in self._buttons]))
        self._TrackControlComponent__session = session
        self._handle_selection.subject = self.song().view
        self.assign_buttons = self._assign_track_buttons
        self._run_index = -1
        self._mode = SEL_MODE_SELECT
        self._tracks_change.subject = self.song()
        self._visible_changed.subject = self.song()
        self._prev_mode_button = None
        self._prev_mode = None

    @subject_slot('tracks')
    def _tracks_change(self):
        self._assign_track_buttons()

    @subject_slot('visible_tracks')
    def _visible_changed(self):
        self._assign_track_buttons()

    def refresh_state(self):
        for button in self._buttons:
            button.reset()

    def create_buttons(self, index, track_editor):
        button = IndexedButton(False, MIDI_NOTE_TYPE, index + 8, 1, COLORLIST[0])
        button.index = index
        return TrackButtonHandler(index, button, track_editor)

    def mode_changed(self, newmode):
        self.assign_buttons()

    def gettrack(self, index, off):
        tracks = self.song().visible_tracks
        if index + off < len(tracks):
            return tracks[(index + off)]
        return

    @subject_slot('selected_track')
    def _handle_selection(self):
        if self._mode == SEL_MODE_SELECT:
            for i in range(8):
                self._buttons[i].update_value()

    def notify(self, blinking_state):
        if self._bmatrix.grabbed:
            return
        if self._mode == SEL_MODE_STOP:
            for button in self._buttons:
                button.update_value(blinking_state)

    @property
    def mode(self):
        return self._mode

    def trigger_solo(self, button):
        if self._mode == SEL_MODE_SOLO:
            button.set_display_value(0, True)
            self._mode = SEL_MODE_SELECT
            self._assign_track_buttons()
            self._prev_mode_button = None
        else:
            self._mode = SEL_MODE_SOLO
            if self._prev_mode_button:
                self._prev_mode_button.set_display_value(0, True)
            button.set_display_value(127, True)
            self._assign_track_buttons()
            self._prev_mode_button = button
            self._prev_mode = SEL_MODE_SOLO

    def trigger_mute(self, button):
        if self._mode == SEL_MODE_MUTE:
            button.set_display_value(0, True)
            self._mode = SEL_MODE_SELECT
            self._assign_track_buttons()
            self._prev_mode_button = None
        else:
            self._mode = SEL_MODE_MUTE
            if self._prev_mode_button:
                self._prev_mode_button.set_display_value(0, True)
            button.set_display_value(127, True)
            self._assign_track_buttons()
            self._prev_mode_button = button
            self._prev_mode = SEL_MODE_MUTE

    def trigger_stop(self):
        self._mode = SEL_MODE_STOP
        self._assign_track_buttons()

    def trigger_to_prev(self):
        if self._prev_mode_button and self._prev_mode:
            self._mode = self._prev_mode
            self._prev_mode_button.set_display_value(127, True)
            self._assign_track_buttons()
        else:
            self._mode = SEL_MODE_SELECT
            self._assign_track_buttons()
            self._prev_mode_button = None

    def trigger_arm(self, button):
        if self._mode == SEL_MODE_ARM:
            button.set_display_value(0, True)
            self._mode = SEL_MODE_SELECT
            self._assign_track_buttons()
            self._prev_mode_button = None
        else:
            self._mode = SEL_MODE_ARM
            if self._prev_mode_button:
                self._prev_mode_button.set_display_value(0, True)
            button.set_display_value(127, True)
            self._assign_track_buttons()
            self._prev_mode_button = button

    def _assign_track_buttons(self):
        trackoff = self._TrackControlComponent__session.track_offset()
        for i in range(8):
            track = self.gettrack(i, trackoff)
            button = self._buttons[i]
            if track is None:
                button.disable(self.empty_action)
            else:
                if self._mode == SEL_MODE_MUTE:
                    button.assign_mute(track)
                if self._mode == SEL_MODE_SOLO:
                    button.assign_solo(track)
                if self._mode == SEL_MODE_ARM:
                    button.assign_arm(track)
                if self._mode == SEL_MODE_SELECT:
                    button.assign_select(track)
                if self._mode == SEL_MODE_STOP:
                    button.assign_stop(track)
                if self._mode == SEL_MODE_XFADE:
                    button.assign_xfade(track)
                button.update_value(0)

    def empty_action(self):
        modifer = self.canonical_parent.modifier_mask()
        if modifer == MASK_SHIFT:
            self.song().create_audio_track(-1)
        else:
            if modifer == MASK_SELECT | MASK_BROWSE:
                self.song().create_return_track()
            else:
                self.song().create_midi_track(-1)

    def disconnect(self):
        super().disconnect()
        for button in self._buttons:
            button.disable()
# okay decompiling src/TrackControlComponent.pyc
