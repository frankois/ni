# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/MaschineMode.py
# Compiled at: 2021-05-04 12:11:01
# Size of source mod 2**32: 1333 bytes
import _Framework.CompoundComponent as CompoundComponent

class MaschineMode(CompoundComponent):
    __module__ = __name__

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)
        self._active = False
        self._alternate_mode = None

    def get_color(self, value, column_index, row_index):
        pass

    def notify(self, blink_state):
        pass

    def notify_mono(self, blink_state):
        pass

    def navigate(self, direction, modifier, alt_modifier=False):
        pass

    def unbind(self):
        pass

    def is_lock_mode(self):
        return True

    def enter(self):
        raise NotImplementedError(self.__class__)

    def exit(self):
        raise NotImplementedError(self.__class__)

    def ext_name(self):
        return 'undefined'

    def enter_edit_mode(self, action_type):
        pass

    def exit_edit_mode(self, action_type):
        pass

    def get_mode_id(self):
        return 0

    def spec_unbind(self, index=0):
        pass

    def disconnect(self):
        super().disconnect()

    def fitting_mode(self, track):
        return self

    def device_dependent(self):
        return False

    def set_alternate_mode(self, mode):
        self._alternate_mode = mode

    def refresh(self):
        pass

    def update(self):
        pass
# okay decompiling src/MaschineMode.pyc
