# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/JamButtonMatrix.py
# Compiled at: 2021-05-04 12:11:01
# Size of source mod 2**32: 7331 bytes
import _Framework.ButtonMatrixElement as ButtonMatrixElement
from _Framework.Util import in_range

class JamButtonMatrix(ButtonMatrixElement):

    def __init__(self, index_offset, rows=[], *a, **k):
        (super().__init__)(*a, **k)
        self._grabbed = False
        self._JamButtonMatrix__index_offset = index_offset
        self._listern_stack = None
        self._value_listener_action = None
        self._external_unbind_lister = None
        self._JamButtonMatrix__batch_updater = None
        self.resource.on_received = self._JamButtonMatrix__on_received
        self.resource.on_lost = self._JamButtonMatrix__on_lost

    def __on_received(self, client, **k):
        self.switch_to_user_action()
        self.canonical_parent._main_mode_container.enter_user_mode()

    def __on_lost(self, client):
        self.exit_user_action()
        self.canonical_parent._main_mode_container.exit_user_mode()

    def on_nested_control_element_lost(self, control):
        pass

    def switch_to_user_action(self):
        if self._value_listener_action:
            super().add_value_listener(self._value_listener_action)
            self._grabbed = True
        else:
            self._grabbed = True

    def exit_user_action(self):
        self._grabbed = False

    def set_user_unbind_listener(self, listener):
        self._external_unbind_lister = listener

    def register_batch_updater(self, updater):
        self._JamButtonMatrix__batch_updater = updater

    def prepare_update(self):
        for button, (_, _) in self.iterbuttons():
            if button:
                button.disable_cc_midi()

    def commit_update(self):
        if self._JamButtonMatrix__batch_updater:
            self._JamButtonMatrix__batch_updater.update_all()
        for button, (_, _) in self.iterbuttons():
            if button:
                button.enable_cc_midi()

    def remove_value_listener(self, *a, **k):
        (super().remove_value_listener)(*a, **k)
        if self._external_unbind_lister:
            self._external_unbind_lister.handle_user_mode_removed()

    def update_all(self, data):
        if not self._grabbed:
            return
        self.prepare_update()
        for button, (col, row) in self.iterbuttons():
            idx = row * 8 + col
            if idx < len(data) and button and data[idx] in range(128):
                button.send_color_direct(data[idx])

        self.commit_update()

    @property
    def grabbed(self):
        return self._grabbed

    @property
    def index_offset(self):
        return self._JamButtonMatrix__index_offset

    def send_value(self, column, row, value, force=False):
        if self.grabbed:
            if not in_range(value, 0, 128):
                raise AssertionError
            elif not in_range(column, 0, self.width()):
                raise AssertionError
            else:
                assert in_range(row, 0, self.height())
                if len(self._buttons[row]) > column:
                    button = self._buttons[row][column]
                    if button:
                        if value == 0:
                            button.send_color_direct(0)
                        else:
                            button.send_color_direct(value)


class IndexButtonMatrix(ButtonMatrixElement):

    def __init__(self, index_offset, rows=[], *a, **k):
        (super().__init__)(*a, **k)
        self._IndexButtonMatrix__grabbed = False
        self._IndexButtonMatrix__batch_updater = None
        self._IndexButtonMatrix__index_offset = index_offset
        self.resource.on_received = self._IndexButtonMatrix__on_received
        self.resource.on_lost = self._IndexButtonMatrix__on_lost

    def __on_received(self, client):
        self.notify_ownership_change(client, True)
        self.grab_control()

    def __on_lost(self, client):
        self.release_control()
        self.notify_ownership_change(client, False)

    def on_nested_control_element_lost(self, control):
        pass

    def register_batch_updater(self, updater):
        self._IndexButtonMatrix__batch_updater = updater

    def grab_control(self):
        self._IndexButtonMatrix__grabbed = True
        for button, (_, _) in self.iterbuttons():
            if button:
                button.unlight(True)
                button.update_grab(True)

    def release_control(self):
        self._IndexButtonMatrix__grabbed = False
        for button, (_, _) in self.iterbuttons():
            if button:
                button.set_to_black()
                button.update_grab(False)

    def update_all(self, data):
        if not self._IndexButtonMatrix__grabbed:
            return
        for button, (col, row) in self.iterbuttons():
            idx = row * 8 + col
            if idx < len(data) and button and data[idx] in range(128):
                button.send_color(data[idx], True)

    def remove_value_listener(self, *a, **k):
        (super().remove_value_listener)(*a, **k)
        if self._IndexButtonMatrix__grabbed:
            self.resource.release_all()

    @property
    def index_offset(self):
        return self._IndexButtonMatrix__index_offset

    @property
    def grabbed(self):
        return self._IndexButtonMatrix__grabbed

    def send_value(self, column, row, value, force=False):
        if self._IndexButtonMatrix__grabbed:
            if not in_range(value, 0, 128):
                raise AssertionError
            else:
                assert in_range(column, 0, self.width())
                assert in_range(row, 0, self.height())
                if len(self._buttons[row]) > column:
                    button = self._buttons[row][column]
                    if button:
                        button.send_color(value)


class MatrixState:

    def __init__(self, parent):
        self._MatrixState__cfg_msg = [
         240, 0, 33, 9, 21, 0, 77, 80, 0, 1, 2]
        for _ in range(80):
            self._MatrixState__cfg_msg.append(0)

        self._MatrixState__cfg_msg.append(247)
        self._MatrixState__parent = parent
        self._MatrixState__controls = []

    def register_matrix(self, bmatrix):
        self._MatrixState__controls.append(bmatrix)
        self._MatrixState__controls.sort(key=(lambda c: c.index_offset))
        bmatrix.register_batch_updater(self)

    def update_all(self):
        self.refresh_state()
        self._MatrixState__parent._send_midi(tuple(self._MatrixState__cfg_msg))

    def refresh_state(self):
        for bmatrix in self._MatrixState__controls:
            for button, (col, row) in bmatrix.iterbuttons():
                if button:
                    index = bmatrix.index_offset + row * 8 + col
                    self._MatrixState__cfg_msg[index + 11] = button.color_value()

    def update_all_values(self, data):
        self.refresh_state()
        for c in self._MatrixState__controls:
            for button, (col, row) in c.iterbuttons():
                if button:
                    index = row * 8 + col + c.index_offset
                    if index < len(data):
                        color = data[index]
                        self._MatrixState__cfg_msg[index + 11] = color
                        button.set_color_value(color)
                    else:
                        self._MatrixState__cfg_msg[index + 11] = 0
                        button.set_color_value(0)

        self.send_update()

    def update_values(self, control, data):
        self.refresh_state()
        for button, (col, row) in control.iterbuttons():
            if button:
                index = row * 8 + col
                if index < len(data):
                    color = data[index]
                    self._MatrixState__cfg_msg[index + control.index_offset + 11] = color
                    button.set_color_value(color)
                else:
                    self._MatrixState__cfg_msg[index + control.index_offset + 11] = 0
                    button.set_color_value(0)

        self.send_update()

    def send_update(self):
        self._MatrixState__parent._send_midi(tuple(self._MatrixState__cfg_msg))
# okay decompiling src/JamButtonMatrix.pyc
