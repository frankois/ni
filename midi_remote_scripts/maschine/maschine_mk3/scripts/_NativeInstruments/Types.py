# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/_NativeInstruments/Types.py
# Compiled at: 2021-05-19 16:03:51
# Size of source mod 2**32: 653 bytes


class TrackType:
    MIDI = 0
    AUDIO = 1
    GROUP = 2
    RETURN = 3
    MASTER = 4
    GENERIC = 5
    EMPTY = 6


class PlayingStatus:
    READY = 0
    TRIGGERED = 1
    PLAYING = 2
    ARMED = 3
    RECORDING = 4
    EMPTY = 5


def typeToString(my_class_num, the_class):
    try:
        return next((k for k, v in the_class.__dict__.items() if v == my_class_num))
    except OSError:
        return 'UNKNOWN'
# okay decompiling src/_NativeInstruments/Types.pyc
