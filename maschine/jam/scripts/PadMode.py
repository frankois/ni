# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/PadMode.py
# Compiled at: 2021-04-29 13:54:08
# Size of source mod 2**32: 11389 bytes
from .MidiMap import ND_KEYBOARD1, SCALES, toHSB, PAD_MODE, BASE_NOTE, NAV_SRC_ENCODER
from .PadScale import *
from .MaschineMode import MaschineMode
from _Framework.InputControlElement import MIDI_NOTE_ON_STATUS, MIDI_NOTE_OFF_STATUS
from _Framework.SubjectSlot import subject_slot
LAYOUT_SPREAD = 0
LAYOUT_ISO_4_INKEY = 1
LAYOUT_ISO_3_INKEY = 2
LAYOUT_ISO_4_CHROM = 3
LAYOUT_ISO_3_CHROM = 4
LAYOUT_NAME = ('Normal', 'Isomorphic 4ths In Key', 'Isomorphic 3rds In Key', 'Isomorphic 4ths Chromatic',
               'Isomorphic 3rds Chromatic')

def find_drum_device(track):
    devices = track.devices
    for device in devices:
        if device.can_have_drum_pads:
            return device


class PadMode(MaschineMode):
    _PadMode__modifier_component = None
    _editmode = None
    _focus_track = None
    _PadMode__layout = LAYOUT_ISO_4_INKEY

    def __init__(self, button_index, monochrome=False, *a, **k):
        (super(PadMode, self).__init__)(button_index, *a, **k)
        self._note_display_mode = ND_KEYBOARD1
        self._base_note = 0
        self._octave = 2
        self.current_scale_index = 0
        self._is_monochrome = monochrome
        self._scale = SCALES[self.current_scale_index]
        self.assign_transpose(SCALES[self.current_scale_index])
        self._focus_track = None

    def set_edit_mode(self, editmode):
        self._editmode = editmode

    @property
    def get_scale(self):
        """
        :rtype : PadScale
        """
        return SCALES[self.current_scale_index]

    def get_base_note(self):
        return self._base_note

    def _get_ref_color(self):
        if self._focus_track:
            return toHSB(self._focus_track.color)
        return (72, 75)

    def device_dependent(self):
        return True

    def get_color(self, value, column, row):
        color = self._get_ref_color()
        button = self.canonical_parent.get_button_matrix().get_button(column, row)
        if button is not None:
            if button.state == 0:
                return 0
            scale = SCALES[self.current_scale_index]
            if self._PadMode__layout == LAYOUT_ISO_3_CHROM or self._PadMode__layout == LAYOUT_ISO_4_CHROM:
                full_color = color[1]
                note_val = button.get_identifier() % 12
                if note_val == self._base_note:
                    return BASE_NOTE_FIX_COLOR
                if scale.in_scale((note_val + (12 - self._base_note)) % 12):
                    return full_color
                return 0
            return scale.convert_color(button.get_identifier(), self._base_note, color)
        return

    def navigate(self, nav_dir, modifier, alt_modifier=False, nav_src=NAV_SRC_ENCODER):
        if modifier:
            if alt_modifier:
                self.inc_octave(-nav_dir)
            else:
                self.inc_base_note(-nav_dir)
        elif alt_modifier:
            self.inc_layout(nav_dir)
        else:
            self.inc_scale(nav_dir)

    def get_mode_id(self):
        return PAD_MODE

    def ext_name(self):
        return 'pad_mode'

    def notify(self, blink_state):
        pass

    def inc_layout(self, inc):
        new_value = self._PadMode__layout + inc
        if new_value < 0:
            self._PadMode__layout = LAYOUT_ISO_3_CHROM
        else:
            if new_value > LAYOUT_ISO_3_CHROM:
                self._PadMode__layout = LAYOUT_SPREAD
            else:
                self._PadMode__layout = new_value
        self.canonical_parent.show_message(' Pad Layout: ' + LAYOUT_NAME[self._PadMode__layout] + ' / ' + self._current_scale_name(SCALES[self.current_scale_index]))
        self.update_transpose()

    def _current_scale_name(self, scale):
        return scale.name + ' ' + BASE_NOTE[self._base_note] + str(self._octave - 2)

    def inc_base_note(self, inc):
        new_value = self._base_note + inc
        if new_value < 0:
            new_value = 11
            self._octave = max(0, self._octave - 1)
        else:
            if new_value > 11:
                new_value = 0
                self._octave = self._octave + 1
        self._base_note = new_value
        scale = SCALES[self.current_scale_index]
        self.canonical_parent.show_message(' PAD Mode Scale: ' + self._current_scale_name(scale))
        self.update_transpose()

    def inc_octave(self, inc):
        new_value = self._octave + inc
        if new_value >= 0:
            if new_value < 8:
                self._octave = new_value
                scale = SCALES[self.current_scale_index]
                self.update_transpose()
                self.canonical_parent.show_message(' PAD Mode Scale: ' + self._current_scale_name(scale))

    def inc_scale(self, inc, update=True):
        nr_of_scales = len(SCALES) - 1
        prev_value = self.current_scale_index
        self.current_scale_index = min(nr_of_scales, max(0, self.current_scale_index + inc))
        if prev_value != self.current_scale_index:
            new_scale = SCALES[self.current_scale_index]
            self.canonical_parent.show_message(' PAD Mode Scale: ' + self._current_scale_name(new_scale))
            if update:
                self.update_transpose()

    def get_octave(self):
        return SCALES[self.current_scale_index].to_octave(self._octave)

    def update_transpose(self):
        if self._active:
            self.clear_transpose()
            self.assign_transpose(SCALES[self.current_scale_index])
            self.canonical_parent._set_suppress_rebuild_requests(True)
            self.canonical_parent.request_rebuild_midi_map()
            self.canonical_parent._set_suppress_rebuild_requests(False)

    def fitting_mode(self, track):
        if not track:
            return self
        drum_device = find_drum_device(track)
        if drum_device != None:
            if self._alternate_mode != None:
                return self._alternate_mode
        return self

    def refresh(self):
        if self._active:
            matrix = self.canonical_parent.get_button_matrix()
            matrix.prepare_update()
            for button, (_, _) in matrix.iterbuttons():
                if button:
                    button.send_value(0, True)

            matrix.commit_update()

    def get_in_notes(self):
        cs = self.song().view.highlighted_clip_slot
        if cs.has_clip:
            if cs.clip.is_midi_clip:
                in_notes = set()
                notes = cs.clip.get_notes_extended(0, 127, 0.0, cs.clip.length)
                for note in notes:
                    in_notes.add(note.pitch)

                return in_notes

    def clear_transpose(self):
        for button, (_, _) in self.canonical_parent.get_button_matrix().iterbuttons():
            if button:
                button.set_to_notemode(False)
                button.remove_value_listener(self.handle_button)

    def assign_transpose(self, scale):
        assert isinstance(scale, PadScale)
        self._scale = scale
        if self._active:
            matrix = self.canonical_parent.get_button_matrix()
            self.layout_normal(matrix)

    def layout_normal(self, matrix):
        matrix.prepare_update()
        scale_len = len(self._scale.notevalues)
        octave = self._octave
        for button, (column, row) in matrix.iterbuttons():
            if button:
                if button.state == 0:
                    button.remove_value_listener(self._dummy_lister)
                elif self._PadMode__layout == LAYOUT_SPREAD:
                    note_index = (7 - row) * 8 + column
                else:
                    if self._PadMode__layout == LAYOUT_ISO_3_INKEY:
                        note_index = (7 - row) * (self.current_scale_index == 0 and 4 or 2) + column
                    else:
                        if self._PadMode__layout == LAYOUT_ISO_4_INKEY:
                            note_index = (7 - row) * (self.current_scale_index == 0 and 5 or 3) + column
                        else:
                            if self._PadMode__layout == LAYOUT_ISO_3_CHROM:
                                note_index = (7 - row) * 4 + column
                            else:
                                if self._PadMode__layout == LAYOUT_ISO_4_CHROM:
                                    note_index = (7 - row) * 5 + column
                                else:
                                    scale_index = note_index % scale_len
                                    octave_offset = note_index / scale_len
                                    if self._PadMode__layout == LAYOUT_ISO_3_CHROM or self._PadMode__layout == LAYOUT_ISO_4_CHROM:
                                        scale_index = note_index % 12
                                        octave_offset = note_index / 12
                                        note_value = SCALES[0].notevalues[scale_index] + self._base_note + octave * 12 + octave_offset * 12
                                scale_index = note_index % scale_len
                                octave_offset = note_index / scale_len
                                note_value = self._scale.notevalues[scale_index] + self._base_note + octave * 12 + octave_offset * 12
                if note_value < 128:
                    button.set_to_notemode(True)
                    button.set_send_note(note_value)
                    button.state = 1
                    button.send_value(0, True)
                else:
                    button.set_send_note(button.get_identifier())
                    button.set_to_notemode(False)
                    button.state = 0
                    button.add_value_listener(self._dummy_lister)
                    button.send_color_direct(0)

        matrix.commit_update()

    def auto_select(self):
        return True

    def _dummy_lister(self, value):
        pass

    def set_modifier_component(self, component):
        self._PadMode__modifier_component = component

    def handle_shift(self, shift_value):
        if shift_value:
            for button, (_, _) in self.canonical_parent.get_button_matrix().iterbuttons():
                if button:
                    button.set_to_notemode(False)
                    button.add_value_listener(self.handle_button, True)

        else:
            for button, (_, _) in self.canonical_parent.get_button_matrix().iterbuttons():
                if button:
                    button.remove_value_listener(self.handle_button)

            self.update_transpose()

    def __determine_focus_track(self):
        return self.song().view.selected_track

    def handle_button(self, value, button):
        if value != 0:
            col, row = button.get_position()
            if row == 0:
                self._PadMode__modifier_component.handle_edit_action(col)

    @subject_slot('selected_track')
    def on_track_changed(self):
        self._focus_track = self._PadMode__determine_focus_track()
        self.refresh()

    def enter(self):
        self._active = True
        self._focus_track = self._PadMode__determine_focus_track()
        self.on_track_changed.subject = self.song().view
        matrix = self.canonical_parent.get_button_matrix()
        for button, (_, _) in matrix.iterbuttons():
            if button:
                button.set_to_notemode(True)
                self.canonical_parent._forwarding_registry[(MIDI_NOTE_ON_STATUS, button.get_identifier())] = button
                self.canonical_parent._forwarding_registry[(MIDI_NOTE_OFF_STATUS, button.get_identifier())] = button

        self.update_transpose()

    def exit(self):
        self._active = False
        self.on_track_changed.subject = None
        for button, (_, _) in self.canonical_parent.get_button_matrix().iterbuttons():
            if button:
                button.set_to_notemode(False)
                button.remove_value_listener(self.handle_button)
# okay decompiling scripts/PadMode.pyc
