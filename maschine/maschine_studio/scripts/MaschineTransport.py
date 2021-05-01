# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_Studio/MaschineTransport.py
# Compiled at: 2021-04-30 12:12:38
# Size of source mod 2**32: 1240 bytes
import Live
import _Framework.CompoundComponent as CompoundComponent
import _Framework.ToggleComponent as ToggleComponent

class MaschineTransport(CompoundComponent):
    __doc__ = "\n    Class encapsulating all functions in Live's transport section.\n    "

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)
        song = self.song()
        self._automation_toggle, self._re_enable_automation_toggle, self._delete_automation, self._arrangement_overdub_toggle, self._back_to_arrange_toggle = self.register_components(ToggleComponent('session_automation_record', song), ToggleComponent('re_enable_automation_enabled', song, read_only=True), ToggleComponent('has_envelopes', None, read_only=True), ToggleComponent('arrangement_overdub', song), ToggleComponent('back_to_arranger', song))

    def set_back_arrange_button(self, button):
        self._back_to_arrange_toggle.set_toggle_button(button)

    def set_session_auto_button(self, button):
        self._automation_toggle.set_toggle_button(button)

    def set_arrangement_overdub_button(self, button):
        self._arrangement_overdub_toggle.set_toggle_button(button)

    def update(self):
        pass
# okay decompiling src/MaschineTransport.pyc
