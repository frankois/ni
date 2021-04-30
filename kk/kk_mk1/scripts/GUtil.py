# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Trial.app/Contents/App-Resources/MIDI Remote Scripts/Komplete_Kontrol_Mk1/GUtil.py
# Compiled at: 2021-04-28 16:44:03
# Size of source mod 2**32: 253 bytes
import Live
RecordingQuantization = Live.Song.RecordingQuantization
msg_sender = None

def register_sender(sender):
    global msg_sender
    msg_sender = sender


def debug_out(message):
    msg_sender.log_message(message)
# okay decompiling src/GUtil.pyc
