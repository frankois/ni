# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_Mikro_Mk2/__init__.py
# Compiled at: 2021-04-30 12:09:45
# Size of source mod 2**32: 618 bytes
from .MaschineMikroMk2 import MaschineMikroMk2
from _Framework.Capabilities import *

def create_instance(c_instance):
    return MaschineMikroMk2(c_instance)


def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=9000, product_ids=[
                         2],
                          model_name='Maschine Mikro Mk2'), 
     
     PORTS_KEY: [
                 inport(props=[HIDDEN, NOTES_CC, SCRIPT]),
                 inport(props=[]),
                 outport(props=[HIDDEN,
                  NOTES_CC,
                  SYNC,
                  SCRIPT]),
                 outport(props=[])]}
# okay decompiling src/__init__.pyc
