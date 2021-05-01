# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_Mikro_Mk2/MaschineMixerComponent.py
# Compiled at: 2021-04-30 12:09:45
# Size of source mod 2**32: 1122 bytes
import Live
import _Framework.MixerComponent as MixerComponent
from .MaschineChannelStripComponent import MaschineChannelStripComponent

class MaschineMixerComponent(MixerComponent):
    __doc__ = ' Class encompassing several channel strips to form a mixer '

    def __init__(self, num_tracks, num_returns=0, with_eqs=False, with_filters=False):
        MixerComponent.__init__(self, num_tracks, num_returns, with_eqs, with_filters)
        self.num_tracks = num_tracks

    def set_touch_mode(self, touchchannel):
        for index in range(self.num_tracks):
            strip = self.channel_strip(index)
            strip.set_touch_mode(touchchannel)

    def _create_strip(self):
        return MaschineChannelStripComponent()

    def enter_clear_mode(self):
        for index in range(self.num_tracks):
            strip = self.channel_strip(index)
            strip.enter_clear()

    def exit_clear_mode(self):
        for index in range(self.num_tracks):
            strip = self.channel_strip(index)
            strip.exit_clear()

    def disconnect(self):
        super(MaschineMixerComponent, self).disconnect()
# okay decompiling src/MaschineMixerComponent.pyc
