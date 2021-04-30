# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/UserMode.py
# Compiled at: 2021-04-29 13:54:08
# Size of source mod 2**32: 1380 bytes
from .MaschineMode import MaschineMode
from .MidiMap import USER_MODE

class UserMode(MaschineMode):
    __module__ = __name__

    def __init__(self, button_index, *a, **k):
        (super(UserMode, self).__init__)(button_index, *a, **k)

    def get_color(self, value, column_index, row_index):
        return 0

    def notify(self, blink_state):
        pass

    def get_mode_id(self):
        return USER_MODE

    def ext_name(self):
        return 'user_mode'

    def spec_unbind(self, index=0):
        pass

    def enter(self):
        self._active = True
        matrix = self.canonical_parent.get_button_matrix()
        matrix.prepare_update()
        for button, (_, _) in matrix.iterbuttons():
            if button:
                button.set_to_notemode(False)
                button.send_value(0, True)

        matrix.commit_update()

    def refresh(self):
        if self._active:
            matrix = self.canonical_parent.get_button_matrix()
            matrix.prepare_update()
            for button, (_, _) in matrix.iterbuttons():
                if button:
                    button.reset()
                    button.refresh()

            matrix.commit_update()

    def exit(self):
        self._active = False
        self.canonical_parent.deassign_matrix()
        self.canonical_parent.get_session().set_clip_launch_buttons(None)
# okay decompiling scripts/UserMode.pyc
