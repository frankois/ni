# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_Mk3/Maschine.py
# Compiled at: 2021-05-19 16:08:09
# Size of source mod 2**32: 764 bytes
import _NativeInstruments.NIController as NIController
from _NativeInstruments import RemixNet

class Maschine(NIController):

    def __init__(self, c_instance):
        oscEndpoint = RemixNet.OSCEndpoint(remoteHost='localhost', remotePort=7579, localHost='', localPort=7580)
        NIController.__init__(self, c_instance, oscEndpoint)

    def getControllerName(self):
        return 'Maschine MK3'
# okay decompiling src/Maschine_Mk3/Maschine.pyc
