# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Trial.app/Contents/App-Resources/MIDI Remote Scripts/Komplete_Kontrol_Mk1/SimpleDeviceComponent.py
# Compiled at: 2021-04-28 16:44:03
# Size of source mod 2**32: 950 bytes
import _Framework.DeviceComponent as DeviceComponent
import _Framework.ChannelTranslationSelector as ChannelTranslationSelector

class SimpleDeviceComponent(DeviceComponent):
    __doc__ = ' Class representing a device in Live '

    def __init__(self):
        DeviceComponent.__init__(self)
        self._control_translation_selector = ChannelTranslationSelector(8)

    def set_device(self, device):
        DeviceComponent.set_device(self, device)
        if device:
            vparm = device.parameters

    def disconnect(self):
        self._control_translation_selector.disconnect()
        DeviceComponent.disconnect(self)
# okay decompiling src/SimpleDeviceComponent.pyc
