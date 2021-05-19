# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_Studio/MaschineMode.py
# Compiled at: 2021-04-30 12:12:38
# Size of source mod 2**32: 3842 bytes
import Live
import _Framework.CompoundComponent as CompoundComponent
from _Framework.InputControlElement import *
from .MIDI_Map import *

def find_drum_device(track):
    devices = track.devices
    for device in devices:
        if device.can_have_drum_pads:
            return device


class MaschineMode(CompoundComponent):
    __module__ = __name__

    def __init__(self, button_index=None, *a, **k):
        (super().__init__)(*a, **k)
        self._active = False
        self._alternate_mode = None
        self.button_index = button_index

    def get_color(self, value, column_index, row_index):
        pass

    def notify(self, blink_state):
        pass

    def notify_mono(self, blink_state):
        pass

    def navigate(self, dir, modifier, alt_modifier=False):
        pass

    def unbind(self):
        pass

    def is_lock_mode(self):
        return True

    def enter(self):
        raise NotImplementedError(self.__class__)

    def exit(self):
        raise NotImplementedError(self.__class__)

    def enter_edit_mode(self, type):
        pass

    def exit_edit_mode(self, type):
        pass

    def get_mode_id(self):
        return OTHER_MODE

    def enter_clear_state(self):
        pass

    def exit_clear_state(self):
        pass

    def disconnect(self):
        super().disconnect()

    def fitting_mode(self, track):
        return self

    def set_alternate_mode(self, mode):
        self._alternate_mode = mode

    def isShiftDown(self):
        return self.canonical_parent.isShiftDown()

    def handle_push(self, value):
        pass

    def refresh(self):
        pass

    def _device_changed(self):
        pass

    def update(self):
        pass


class StudioClipMode(MaschineMode):
    __module__ = __name__

    def __init__(self, button_index, *a, **k):
        (super().__init__)(button_index, *a, **k)

    def get_color(self, value, column_index, row_index):
        session = self.canonical_parent._session
        scene = session.scene(row_index)
        clip_slot = scene.clip_slot(column_index)._clip_slot
        color = session.get_color(clip_slot)
        cindex = value == 0 and 1 or 0
        return color[int(cindex)]

    def notify(self, blink_state):
        self.canonical_parent._session.notify(blink_state)

    def notify_mono(self, blink_state):
        self.canonical_parent._session.notify_mono(blink_state)

    def enter_edit_mode(self, type):
        self.canonical_parent._session.set_enabled(False)

    def exit_edit_mode(self, type):
        self.canonical_parent._session.set_enabled(True)

    def get_mode_id(self):
        return CLIP_MODE

    def navigate(self, dir, modifier, alt_modifier=False):
        if modifier:
            if dir == 1:
                self.canonical_parent._session.bank_up()
            else:
                self.canonical_parent._session.bank_down()
        elif dir == 1:
            self.canonical_parent._session.bank_right()
        else:
            self.canonical_parent._session.bank_left()

    def enter(self):
        self._active = True
        for button, (column, row) in self.canonical_parent._bmatrix.iterbuttons():
            if button:
                button.set_to_notemode(False)
                scene = self.canonical_parent._session.scene(row)
                clip_slot = scene.clip_slot(column)
                clip_slot.set_launch_button(button)

    def refresh(self):
        if self._active:
            for button, (column, row) in self.canonical_parent._bmatrix.iterbuttons():
                if button:
                    button.reset()
                    button.refresh()

    def exit(self):
        self._active = False
        self.canonical_parent._deassign_matrix()
        self.canonical_parent._session.set_clip_launch_buttons(None)
# okay decompiling src/MaschineMode.pyc
