# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_Mk3/__init__.py
# Compiled at: 2021-05-19 16:01:56
# Size of source mod 2**32: 308 bytes
from .Maschine import Maschine

def create_instance(c_instance):
    return Maschine(c_instance)
# okay decompiling src/Maschine_Mk3/__init__.pyc
