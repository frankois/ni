# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/DrumMode.py
# Compiled at: 2021-05-04 12:11:01
# Size of source mod 2**32: 11343 bytes
from .MaschineMode import MaschineMode
from .MidiMap import AUTO_NAME, DEFAULT_DRUM_COLOR, PAD_TRANSLATIONS, PAD_MODE, COLOR_BLACK, find_drum_device
from _Framework.InputControlElement import MIDI_NOTE_ON_STATUS, MIDI_NOTE_OFF_STATUS
from _Framework.SubjectSlot import subject_slot

def color_by_name(name):
    for match in AUTO_NAME:
        if match[0].search(name):
            return match[1]

    return DEFAULT_DRUM_COLOR


class DrumPad(object):

    def __init__(self, index, *a, **k):
        self.index = index
        self._color = (72, 72)
        self.selected = False
        self._pad = None
        self._button = None
        self._notemode = True
        self._action_callback = None
        self._DrumPad__has_val_listener = False
        self._note_index = None

    def set_notemode(self, mode):
        self._notemode = mode
        if self._button:
            self._button.set_to_notemode(mode)
        if self._DrumPad__has_val_listener:
            self._button.remove_value_listener(self._handle_selection)
            self._DrumPad__has_val_listener = False
        if not mode:
            self._button.add_value_listener(self._handle_selection)
            self._DrumPad__has_val_listener = True

    @property
    def button(self):
        return self._button

    def set_note_index(self, note_index):
        self._note_index = note_index

    def assign_midi(self):
        if self._button:
            self._button.set_send_note(PAD_TRANSLATIONS[self._note_index][2])

    def set_action_callback(self, callback):
        self._action_callback = callback

    def release(self):
        if self._DrumPad__has_val_listener:
            self._button.remove_value_listener(self._handle_selection)

    def _handle_selection(self, value):
        if self._action_callback:
            self._action_callback(self.index, value)

    def set_color(self, color):
        self._color = color

    def set_pad(self, pad):
        self._pad = pad

    def set_button(self, button):
        self._button = button
        button._pad = None

    def send_color(self):
        if self._button and self.selected:
            self._button.send_color_direct(self._color[1])
        else:
            if self._button:
                self._button.send_color_direct(self._color[0])

    def get_color(self):
        if self.selected:
            return self._color[1]
        return self._color[0]


class DrumMode(MaschineMode):
    __subject_events__ = ('pressed_pads', )
    _DrumMode__modifier_component = None

    def __init__(self, button_index, monochrome=False, *a, **k):
        (super().__init__)(button_index, *a, **k)
        self.track = None
        self.device = None
        self._is_monochrome = monochrome
        self._visible_drum_pad_slots = None
        self._visible_drum_pads = None
        self._pads = tuple((DrumPad(index) for index in range(16)))
        self._selected_pad = None
        if self.canonical_parent.is_monochrome():
            self.pad_to_color = self._DrumMode__pad_to_onoff
        else:
            self.pad_to_color = self._DrumMode__pad_to_color

    def get_color(self, value, column, row):
        note_index = row * 4 + column
        return self._pads[note_index].get_color()

    def get_mode_id(self):
        return PAD_MODE

    def device_dependent(self):
        return True

    def ext_name(self):
        return 'pad_mode'

    def set_modifier_component(self, component):
        self._DrumMode__modifier_component = component

    def __pad_to_onoff(self, pad):
        if pad:
            if len(pad.chains) == 0:
                return (
                 COLOR_BLACK, COLOR_BLACK)
            return (
             COLOR_BLACK, COLOR_BLACK)
        else:
            return (COLOR_BLACK, COLOR_BLACK)

    def __pad_to_color(self, pad):
        if pad:
            chains = pad.chains
            name = pad.name
            if len(chains) == 0:
                return (72, 72)
            col = color_by_name(name) << 2
            return (col, col + 2)
        return (4, 6)

    def navigate(self, nav_dir, modifier, alt_modifier=False, nav_source=0):
        if self.device:
            if self.device.view:
                self.device.view.drum_pads_scroll_position = max(0, min(28, self.device.view.drum_pads_scroll_position + nav_dir))

    def enter(self):
        self._active = True
        self.assign_track_device()
        matrix = self.canonical_parent._bmatrix
        matrix.prepare_update()
        for button, (column, row) in matrix.iterbuttons():
            if button:
                if column > 3:
                    if row > 3:
                        pad_index = (7 - row) * 4 + column - 4
                        note_index = (3 - (7 - row)) * 4 + column - 4
                        pad = self._pads[pad_index]
                        button.set_to_notemode(True)
                        self.canonical_parent._forwarding_registry[(MIDI_NOTE_ON_STATUS, button.get_identifier())] = button
                        self.canonical_parent._forwarding_registry[(MIDI_NOTE_OFF_STATUS, button.get_identifier())] = button
                        button.set_send_note(PAD_TRANSLATIONS[note_index][2])
                        button.send_color_direct(pad.get_color())
                note_index = (7 - row) * 7 + column + 12
                button.send_color_direct(COLOR_BLACK)
                button.set_to_notemode(False)
                button.add_value_listener(self.button_listener, True)

        matrix.commit_update()
        self.track = self.song().view.selected_track
        self._on_name_changed.subject = self.device.view.selected_drum_pad

    def button_listener(self, value, button):
        if value == 0:
            return
        col, row = button.get_position()
        if row == 0:
            self._DrumMode__modifier_component.handle_edit_action(col)

    def _get_note_set(self):
        in_notes = set()
        cs = self.song().view.highlighted_clip_slot
        if cs.has_clip:
            if cs.clip.is_midi_clip:
                notes = cs.clip.get_notes_extended(0, 127, 0.0, cs.clip.length)
                for note in notes:
                    in_notes.add(note.pitch)

        return in_notes

    def update_pads(self):
        if self._active:
            for dpad in self._pads:
                dpad.send_color()

    def refresh(self):
        if self._active:
            for dpad in self._pads:
                dpad._button.reset()
                dpad.send_color()

    def assign_pads(self):
        self._visible_drum_pads = None
        self._selected_pad = None
        matrix = self.canonical_parent._bmatrix
        matrix.prepare_update()
        if self.device:
            self._visible_drum_pads = self.device.visible_drum_pads
            selected_drum_pad = self.device.view.selected_drum_pad
            self._on_name_changed.subject = selected_drum_pad
            index = 0
            for pad in self._visible_drum_pads:
                if pad == selected_drum_pad:
                    self._pads[index].selected = True
                    self._selected_pad = self._pads[index]
                else:
                    self._pads[index].selected = False
                self._pads[index].set_color(self.pad_to_color(pad))
                self._pads[index].set_pad(pad)
                index += 1

        else:
            for dpad in self._pads:
                dpad.set_color((8, 10))
                dpad.set_pad(None)

            for button, (column, row) in self.canonical_parent._bmatrix.iterbuttons():
                if column > 3 and row > 3:
                    pad_index = (7 - row) * 4 + column - 4
                    self._pads[pad_index].set_button(button)
                    self._pads[pad_index].send_color()

        matrix.commit_update()

    def assign_track_device(self):
        if self.device:
            if self.device.view:
                self._on_scroll_index_changed.subject = None
                self._on_selected_drum_pad_changed.subject = None
                self._on_chains_changed.subject = None
                self._on_name_changed.subject = None
        self.track = self.song().view.selected_track
        self.device = find_drum_device(self.track)
        if self.device:
            self._on_scroll_index_changed.subject = self.device.view
            self._on_selected_drum_pad_changed.subject = self.device.view
            self._on_chains_changed.subject = self.device
            self._on_name_changed.subject = self.device
        self.assign_pads()

    def notify(self, blink_state):
        pass

    def index_of(self, pad):
        for index in range(16):
            if self._pads[index]._pad == pad:
                return index

        return -1

    @subject_slot('name')
    def _on_name_changed(self):
        if self._active:
            if self.device:
                self.assign_pads()
                self.update_pads()

    def _device_changed(self):
        if self._active:
            self.assign_track_device()
            self.update_pads()

    @subject_slot('chains')
    def _on_chains_changed(self):
        if self._active:
            if self.device:
                self.assign_pads()
                self.update_pads()

    @subject_slot('selected_drum_pad')
    def _on_selected_drum_pad_changed(self):
        if self._active:
            if self.device:
                if self._selected_pad:
                    self._selected_pad.selected = False
                    self._selected_pad.send_color()
                selected_drum_pad = self.device.view.selected_drum_pad
                self._on_name_changed.subject = selected_drum_pad
                new_index = self.index_of(selected_drum_pad)
                if new_index in range(16):
                    self._selected_pad = self._pads[new_index]
                    self._selected_pad.selected = True
                    self._selected_pad.send_color()

    @subject_slot('drum_pads_scroll_position')
    def _on_scroll_index_changed(self):
        if self._active:
            if self.device:
                self.assign_pads()
                self.update_pads()

    def fitting_mode(self, track):
        if not track:
            return self
        drum_device = find_drum_device(track)
        if drum_device is None:
            if self._alternate_mode is not None:
                return self._alternate_mode
        return self

    def exit(self):
        if self._active:
            if self.canonical_parent:
                if self.canonical_parent._bmatrix:
                    buttons = self.canonical_parent._bmatrix.iterbuttons()
                    if buttons:
                        for button, (column, row) in buttons:
                            if not button or column < 4 or row < 4:
                                button.remove_value_listener(self.button_listener)

        self._active = False
        self._on_scroll_index_changed.subject = None
        self._on_selected_drum_pad_changed.subject = None
        self._on_chains_changed.subject = None
        self._on_name_changed.subject = None
        self.device = None
        self.track = None

    def disconnect(self):
        self.exit()
        self.track = None
        self.device = None
        self._visible_drum_pad_slots = None
        self._visible_drum_pads = None
        self._pads = None
        self._selected_pad = None
        super().disconnect()
# okay decompiling src/DrumMode.pyc
