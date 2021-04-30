# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/JamSessionComponent.py
# Compiled at: 2021-04-29 13:54:08
# Size of source mod 2**32: 7972 bytes
from .MidiMap import STEP1, COLOR_BLACK, COLOR_WHITE, COLOR_WHITE_DIM, toHSB
import _Framework.SessionComponent as SessionComponent
from .JamSceneComponent import JamSceneComponent
COLOR_MODE_WHITE = 1
COLOR_MODE_STD = 0

class JamSessionComponent(SessionComponent):
    __doc__ = 'Session Component for Maschine Jam'
    __module__ = __name__
    _JamSessionComponent__matrix = None
    _JamSessionComponent__matrix_lookup = []
    scene_component_type = JamSceneComponent
    _track_offset_listener = None
    _advance = STEP1
    _JamSessionComponent__color_mode = COLOR_MODE_STD

    def __init__(self, *a, **k):
        (super(JamSessionComponent, self).__init__)(8, 8, *a, **k)
        self._JamSessionComponent__to_std_cmode()

    def _allow_updates(self):
        return True

    def set_color_mode(self, mode=None):
        if mode == None:
            if self._JamSessionComponent__color_mode == COLOR_MODE_STD:
                self._JamSessionComponent__to_white_cmode()
            else:
                self._JamSessionComponent__to_std_cmode()
        elif mode == COLOR_MODE_STD:
            self._JamSessionComponent__to_std_cmode()
        else:
            self._JamSessionComponent__to_white_cmode()

    def __to_std_cmode(self):
        self.get_color = self._JamSessionComponent__color_cmode
        self.notify = self._JamSessionComponent__notify_cmode_std
        self._JamSessionComponent__color_mode = COLOR_MODE_STD

    def __to_white_cmode(self):
        self.get_color = self._JamSessionComponent__color_wht_mode
        self.notify = self._JamSessionComponent__notify_cmode_wht
        self._JamSessionComponent__color_mode = COLOR_MODE_WHITE

    def get_color_mode(self):
        return self._JamSessionComponent__color_mode

    def set_matrix(self, matrix, matrix_lookup):
        self._JamSessionComponent__matrix = matrix
        self._JamSessionComponent__matrix_lookup = matrix_lookup

    def bank_down(self, amount=1):
        if self.is_enabled():
            newoff = max(0, self._scene_offset - amount)
            self.set_offsets(self._track_offset, newoff)

    def bank_up(self, amount=1):
        if self.is_enabled():
            self.set_offsets(self._track_offset, self._scene_offset + amount)

    def set_offsets(self, track_offset, scene_offset):
        if self._JamSessionComponent__matrix:
            self._JamSessionComponent__matrix.prepare_update()
        prevoffset = self._track_offset
        super(JamSessionComponent, self).set_offsets(track_offset, scene_offset)
        if prevoffset != self._track_offset:
            if self._track_offset_listener:
                self._track_offset_listener(self._track_offset)
        if self._JamSessionComponent__matrix:
            self._JamSessionComponent__matrix.commit_update()

    def bank_left(self, amount=1):
        if self.is_enabled():
            self.set_offsets(max(0, self._track_offset - amount), self._scene_offset)

    def bank_right(self, amount=1):
        if self.is_enabled():
            self.set_offsets(self._track_offset + amount, self._scene_offset)

    def set_track_offset_listener(self, listener):
        self._track_offset_listener = listener

    def __color_cmode(self, clip_slot):
        if clip_slot == None:
            return COLOR_BLACK
        oncolor, offcolor = self.get_color_cmode_base(clip_slot)
        if clip_slot.has_clip and not clip_slot.clip.is_recording:
            if clip_slot.clip.will_record_on_start:
                return oncolor
            if clip_slot.clip.is_triggered:
                return oncolor
            if clip_slot.clip.is_playing:
                return oncolor
            return offcolor
            if clip_slot.will_record_on_start:
                return oncolor
            if clip_slot.is_playing:
                return COLOR_WHITE
            if clip_slot.controls_other_clips:
                return COLOR_WHITE_DIM
            if clip_slot.is_triggered:
                return COLOR_WHITE_DIM
        return COLOR_BLACK

    def __color_wht_mode(self, clip_slot):
        if clip_slot == None:
            return COLOR_BLACK
        oncolor, _ = self.get_color_cmode_base(clip_slot)
        if clip_slot.has_clip and not clip_slot.clip.is_recording:
            if clip_slot.clip.will_record_on_start:
                return COLOR_WHITE
            if clip_slot.clip.is_triggered:
                return COLOR_WHITE
            if clip_slot.clip.is_playing:
                return COLOR_WHITE
            return oncolor
            if clip_slot.will_record_on_start:
                return oncolor
            if clip_slot.is_playing:
                return COLOR_WHITE
            if clip_slot.controls_other_clips:
                return COLOR_WHITE_DIM
            if clip_slot.is_triggered:
                return COLOR_WHITE_DIM
        return COLOR_BLACK

    def __notify_cmode_wht(self, blink):
        sblink = blink / 2
        for scene_index in range(8):
            scene = self.scene(scene_index)
            for track_index in range(8):
                clip_slot = scene.clip_slot(track_index)._clip_slot
                if clip_slot:
                    button = self._JamSessionComponent__matrix_lookup[scene_index][track_index]
                    if clip_slot.has_clip:
                        if clip_slot.clip.is_recording or clip_slot.clip.will_record_on_start:
                            oncolor, _ = self.get_color_cmode_base(clip_slot)
                            button.send_color_direct(sblink == 0 and oncolor or 7)
                        else:
                            if clip_slot.clip.is_triggered:
                                oncolor, _ = self.get_color_cmode_base(clip_slot)
                                button.send_color_direct(sblink == 0 and oncolor or COLOR_WHITE - 1)
                            else:
                                if clip_slot.clip.is_playing:
                                    pass
                        continue
                    if clip_slot.will_record_on_start:
                        button.send_color_direct(sblink == 0 and 4 or 0)
                    elif clip_slot.is_playing:
                        button.send_color_direct(COLOR_WHITE)
                    elif clip_slot.is_triggered:
                        button.send_color_direct(sblink == 0 and COLOR_WHITE or COLOR_WHITE_DIM)
                    elif clip_slot.controls_other_clips:
                        button.send_color_direct(COLOR_WHITE_DIM)

    def __notify_cmode_std(self, blink):
        sblink = blink / 2
        for scene_index in range(8):
            scene = self.scene(scene_index)
            for track_index in range(8):
                clip_slot = scene.clip_slot(track_index)._clip_slot
                if clip_slot:
                    button = self._JamSessionComponent__matrix_lookup[scene_index][track_index]
                    if clip_slot.has_clip:
                        if clip_slot.clip.is_recording or clip_slot.clip.will_record_on_start:
                            oncolor, _ = self.get_color_cmode_base(clip_slot)
                            button.send_color_direct(sblink == 0 and oncolor or 7)
                        else:
                            if clip_slot.clip.is_triggered:
                                oncolor, offcolor = self.get_color_cmode_base(clip_slot)
                                button.send_color_direct(sblink == 0 and oncolor or offcolor)
                            else:
                                if clip_slot.clip.is_playing:
                                    pass
                        continue
                    if clip_slot.will_record_on_start:
                        button.send_color_direct(sblink == 0 and 4 or 0)
                    elif clip_slot.is_playing:
                        button.send_color_direct(COLOR_WHITE)
                    elif clip_slot.is_triggered:
                        button.send_color_direct(sblink == 0 and COLOR_WHITE or COLOR_WHITE_DIM)
                    elif clip_slot.controls_other_clips:
                        button.send_color_direct(COLOR_WHITE_DIM)

    def get_color_cmode_base(self, clip_slot):
        if clip_slot != None:
            if clip_slot.has_clip:
                color = toHSB(clip_slot.clip.color)
                return color
            if clip_slot.controls_other_clips:
                pass
        return (0, 0)

    def disconnect(self):
        super(JamSessionComponent, self).disconnect()
# okay decompiling scripts/JamSessionComponent.pyc
