# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/JamClipSlotComponent.py
# Compiled at: 2021-04-29 13:54:08
# Size of source mod 2**32: 1113 bytes
import _Framework.ClipSlotComponent as ClipSlotComponent
from _Framework.SubjectSlot import subject_slot

class JamClipSlotComponent(ClipSlotComponent):
    __doc__ = '\n    Clip Slot Component for Maschine Jam\n    '
    _modifier = None

    def __init__(self, *a, **k):
        (super(JamClipSlotComponent, self).__init__)(*a, **k)
        self._JamClipSlotComponent__index = (0, 0)

    def set_modifier(self, modifier):
        self._modifier = modifier

    def set_index(self, index):
        self._JamClipSlotComponent__index = index

    def get_index(self):
        return self._JamClipSlotComponent__index

    def get_track(self):
        if self._clip_slot is not None:
            return self._clip_slot.canonical_parent
        return

    @subject_slot('value')
    def _launch_button_value(self, value):
        if self.is_enabled():
            if self._modifier and self._modifier.in_spec_mode():
                self._modifier.handle_edit(self, value)
            else:
                if self._clip_slot is not None:
                    self._do_launch_clip(value)

    def get_launch_button(self):
        return self._launch_button_value_slot.subject
# okay decompiling scripts/JamClipSlotComponent.pyc
