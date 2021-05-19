# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_Studio/ModSceneComponent.py
# Compiled at: 2021-04-30 12:12:38
# Size of source mod 2**32: 458 bytes
import Live
import _Framework.SceneComponent as SceneComponent
from _Framework.Util import in_range, nop
from .ModClipSlotComponent import ModClipSlotComponent

class ModSceneComponent(SceneComponent):
    __doc__ = '\n    Special Scene Component for Maschine\n    '
    clip_slot_component_type = ModClipSlotComponent

    def __init__(self, num_slots=0, tracks_to_use_callback=nop, *a, **k):
        (super().__init__)(num_slots, tracks_to_use_callback, *a, **k)
# okay decompiling src/ModSceneComponent.pyc
