# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_Studio/ModClipSlotComponent.py
# Compiled at: 2021-04-30 12:12:38
# Size of source mod 2**32: 1551 bytes
import Live
import _Framework.ClipSlotComponent as ClipSlotComponent
from .MIDI_Map import debug_out, vindexof, CLIP_MODE
from _Framework.SubjectSlot import subject_slot

class ModClipSlotComponent(ClipSlotComponent):
    __doc__ = '\n    Clip Slot Component for Maschine\n    '

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)

    def set_modifier(self, modifier):
        self._modifier = modifier

    @subject_slot('value')
    def _launch_button_value(self, value):
        if self.is_enabled():
            if self._modifier and self._modifier.hasModification(CLIP_MODE):
                self._modifier.edit_clip_slot(self, value)
            else:
                if self._clip_slot is not None and self._modifier and self._modifier.isShiftdown() and value != 0:
                    track = self._clip_slot.canonical_parent
                    scenes = self.song().scenes
                    index = vindexof(track.clip_slots, self._clip_slot)
                    scenes[index].fire()
                else:
                    if self._clip_slot is not None:
                        if self._modifier and self._modifier.isClipAltDown() and value != 0:
                            track = self._clip_slot.canonical_parent
                            if track.is_foldable and value != 0:
                                if track.fold_state == 0:
                                    track.fold_state = 1
                        else:
                            track.fold_state = 0
                    elif self._clip_slot is not None:
                        self._do_launch_clip(value)

    def get_launch_button(self):
        return self._launch_button_value_slot.subject
# okay decompiling src/ModClipSlotComponent.pyc
