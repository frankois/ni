# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/JamModes.py
# Compiled at: 2021-04-29 13:54:08
# Size of source mod 2**32: 24974 bytes
Instruction context:
   
 L.  33         6  UNPACK_SEQUENCE_2     2 
                   8  STORE_FAST               'idx'
                  10  STORE_FAST               'val'
                  12  LOAD_FAST                'idx'
                  14  LOAD_CONST               2
                  16  BINARY_MODULO    
                  18  LOAD_CONST               0
                  20  COMPARE_OP               ==
                  22  POP_JUMP_IF_FALSE    46  'to 46'
                  24  LOAD_FAST                'idx'
                  26  LOAD_DEREF               'nr_index'
                  28  COMPARE_OP               ==
                  30  POP_JUMP_IF_FALSE    42  'to 42'
                  32  LOAD_STR                 '[[{}]]'
                  34  LOAD_METHOD              format
                  36  LOAD_FAST                'val'
                  38  CALL_METHOD_1         1  '1 positional argument'
                  40  JUMP_IF_TRUE_OR_POP    48  'to 48'
                42_0  COME_FROM            30  '30'
                  42  LOAD_FAST                'val'
                  44  JUMP_IF_TRUE_OR_POP    48  'to 48'
->              46_0  COME_FROM            22  '22'
                  46  LOAD_STR                 ''
                48_0  COME_FROM            44  '44'
                48_1  COME_FROM            40  '40'
                  48  LIST_APPEND           2  ''
                  50  JUMP_BACK             4  'to 4'
                  52  RETURN_VALUE     

