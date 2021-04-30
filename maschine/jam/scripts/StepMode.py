# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/StepMode.py
# Compiled at: 2021-04-29 13:54:08
# Size of source mod 2**32: 20584 bytes
import Live
from _Framework.SubjectSlot import subject_slot
from _Framework.InputControlElement import MIDI_NOTE_ON_STATUS, MIDI_NOTE_OFF_STATUS
GridQuantization = Live.Clip.GridQuantization
from .MidiMap import COLOR_BLACK, quantize_settings, qauntize_is_triplet, quantize_base, quantize_clip_live, quantize_string, STEP_MODE, toHSB, BASE_NOTE_FIX_COLOR, from_midi_note, debug_out
from .MaschineMode import MaschineMode
from .PadMode import PadMode
from .ModifierComponent import ModifierComponent, LOCK_BUTTON, VARIATION_BUTTON, CLEAR_ACTION, DUPLICATE_ACTION
from .EncoderComponent import EncoderComponent
grid_offset_percentage = 0.0

def modify_color(color, brightness):
    return (
     color[0], color[1], brightness)


class GridElement:

    def __init__(self, note_handler):
        self._button = None
        self._col = 0
        self._row = 0
        self._note_handler = note_handler
        self._notes = None
        self._GridElement__tmp = None
        self.is_base_note = False
        self._GridElement__restore_color = 0

    def assign_notes(self, notes):
        self._notes = notes

    def has_notes(self):
        return self._notes is not None and len(self._notes) >= 0

    def pre_add_note(self, note):
        if not self._GridElement__tmp:
            self._GridElement__tmp = []
        self._GridElement__tmp.append(note)

    @property
    def col(self):
        return self._col

    @property
    def row(self):
        return self._row

    @property
    def coords(self):
        return (self._col, self._row)

    def notes(self):
        return self._notes

    def brighten(self):
        self._button.send_color_direct(self._note_handler.on_color + 1)

    def restore(self):
        self._button.send_color_direct(self._GridElement__restore_color)

    def note_finalize(self, force=False):
        if (self._GridElement__tmp or self)._notes:
            self._notes = None
            self._button.send_value(COLOR_BLACK)
        else:
            if self._GridElement__tmp:
                self._notes = self._notes or self._GridElement__tmp
                self._button.send_value(COLOR_BLACK)
            else:
                if self._GridElement__tmp and self._notes:
                    self._notes = self._GridElement__tmp
                    force and self._button.send_value(COLOR_BLACK)
                else:
                    force and self._button.send_value(COLOR_BLACK)
        self._GridElement__tmp = None

    def release(self):
        if self._button is not None:
            self._button.remove_value_listener(self._launch_value)
            self._button = None

    def set_button(self, button, col, row):
        self._col = col
        self._row = row
        if button != self._button:
            if self._button is not None:
                self._button.remove_value_listener(self._launch_value)
            self._button = button
            if self._button is not None:
                self._button.add_value_listener(self._launch_value)

    def _launch_value(self, value):
        if value:
            self._note_handler.select_note(self)

    def color(self):
        if self._notes is None:
            if self.is_base_note:
                self._GridElement__restore_color = self._note_handler.bs_color
                return self._note_handler.bs_color
            self._GridElement__restore_color = COLOR_BLACK
            return
        if self.is_base_note:
            self._GridElement__restore_color = self._note_handler.on_color
            return self._note_handler.on_color
        self._GridElement__restore_color = self._note_handler.on_color
        return self._note_handler.on_color

    def __str__(self):
        return 'GRID(' + str(self._row) + ',' + str(self._col) + ') Notes = ' + str(self._GridElement__tmp)


class StepMode(MaschineMode):

    def __init__(self, button_index, padmode, monochrome=False, *a, **k):
        (super(StepMode, self).__init__)(button_index, *a, **k)
        assert isinstance(padmode, PadMode)
        self._padmode = padmode
        self._mono_mode = False
        self._grid = [[GridElement(self) for _ in range(8)] for _ in range(8)]
        self._base_pitch = 60
        self._pos_scroll = 0.0
        self._note_length = 0.95
        self._in_velocity = 100
        self._clip = None
        self.on_color = None
        self.bs_color = None
        self._encoder_handler = None
        self._modifier_componenet = None
        self._step_values = [None, None, None, None, None, None, None, None]
        self._steps_notes = None
        self._length_listener = None
        self._quantize_index = 7
        self._quantize = quantize_settings[self._quantize_index]
        self._istriplet = qauntize_is_triplet[self._quantize_index]
        self._quantize_base = quantize_base[self._quantize_index]
        self._quantize_grid_max = 8
        self._page_handler = None
        self._StepMode__current_run_index = -1

    def set_mode_elements(self, modifier_component, encoder_handler):
        assert isinstance(modifier_component, ModifierComponent)
        assert isinstance(encoder_handler, EncoderComponent)
        self._modifier_componenet = modifier_component
        self._encoder_handler = encoder_handler

    def ext_name(self):
        return 'step_mode'

    def set_page_handler(self, handler):
        self._page_handler = handler

    def get_color(self, value, column_index, row_index):
        return self._grid[column_index][row_index].color()

    def notify(self, blink_state):
        pass

    def device_dependent(self):
        return True

    def adjust_step_len(self, value, push_down):
        factor = 0.1 * value
        if push_down:
            factor *= 0.1
        self._note_length = max(0.1, min(1.0, self._note_length + factor))
        self.canonical_parent.notify_state('step', value)
        self.canonical_parent.show_message('Step Length {}%'.format(int(self._note_length * 100)))

    def select_note(self, grid):
        if not self._clip:
            return
        col, row = grid.coords
        if self._modifier_componenet.is_shift_down():
            if row == 0:
                self._modifier_componenet.handle_edit_action(col, (
                 self._padmode.get_base_note(), self._padmode.get_scale))
        else:
            ls = []
            noteval = self._padmode.get_scale.grid_row_to_note(row)
            if grid.has_notes():
                self._clip.remove_notes_extended(noteval, 1, self._pos_scroll + self._quantize * col, self._quantize)
            else:
                if self._mono_mode:
                    self._clip.remove_notes_extended(0, 128, self._pos_scroll + self._quantize * col, self._quantize)
                note_specification = Live.Clip.MidiNoteSpecification(noteval, self._pos_scroll + self._quantize * col, self._quantize * self._note_length, self._in_velocity)
                ls.append(note_specification)
                self._clip.add_new_notes(ls)

    def page_index(self):
        seg_len = self._quantize_base * 8
        if not self._clip:
            return (0, 1)
        pages_precise = self._clip.length / seg_len
        pages = int(self._clip.length / seg_len)
        if pages != pages_precise:
            pages += 1
        return (int(self._pos_scroll / seg_len), max(1, pages))

    def select_pos(self, scroll_index):
        self._pos_scroll = scroll_index * (self._quantize_base * 8)
        self._assign_notes(True)
        self._page_handler.update_buttons()

    def get_clip(self):
        return self._clip

    def _change_quantize(self, nav_dir):
        if self._quantize_index + nav_dir in range(len(quantize_settings)):
            self._quantize_index += nav_dir
            self._quantize = quantize_settings[self._quantize_index]
            self._istriplet = qauntize_is_triplet[self._quantize_index]
            self._quantize_base = quantize_base[self._quantize_index]
            self._quantize_grid_max = self._istriplet and 6 or 8
            self._assign_notes(True)
            self._handle_loop_end_changed()
            self._clip.view.grid_quantization = quantize_clip_live[self._quantize_index]
            self._clip.view.grid_is_triplet = qauntize_is_triplet[self._quantize_index]
            self.canonical_parent.show_message('Step Edit Grid ' + quantize_string[self._quantize_index])

    def navigate(self, nav_dir, modifier, shift_modifier=False, source=0):
        if modifier == 0:
            if shift_modifier:
                self._change_quantize(nav_dir)
            else:
                self._padmode.inc_scale(nav_dir, False)
                self._base_pitch = self._padmode.get_scale.set_grid_map(self._padmode._base_note, self._base_pitch, 0)
                self._assign_notes(True)
        else:
            self._base_pitch += -nav_dir * (shift_modifier and self._padmode.get_scale.inc_steps() or 1)
            if self._base_pitch in range(8, 120):
                self._base_pitch = self._padmode.get_scale.set_grid_map(self._padmode._base_note, self._base_pitch, -nav_dir)
                self.canonical_parent.show_message('Step Edit ' + from_midi_note(self._base_pitch))
                self._assign_notes(True)

    def get_mode_id(self):
        return STEP_MODE

    def assign_highlighted_clip_slot(self):
        self._clip = self.song().view.detail_clip
        if self._clip:
            if self._clip.is_midi_clip:
                _, oncolor = toHSB(self._clip.color)
                self.on_color = oncolor + 2
                self.bs_color = BASE_NOTE_FIX_COLOR - 1
                self._handle_play_head.subject = self._clip
                self._handle_notes_changed.subject = self._clip
                self._handle_end_time_changed.subject = self._clip
                self._handle_loop_end_changed.subject = self._clip
                self._handle_playing.subject = self._clip
                self._handle_color_changed.subject = self._clip

    def note_to_grid(self, note, scale, scale_base_note):
        rowindex = scale.note_to_gridrow(note[0])
        ci = (note[1] - self._pos_scroll + self._quantize * grid_offset_percentage) / self._quantize
        if ci < 0:
            colindex = -1
        else:
            colindex = int(ci + 0.01)
        if rowindex in range(8):
            if colindex in range(self._quantize_grid_max):
                return (
                 colindex, rowindex)
        if colindex in range(self._quantize_grid_max):
            return (
             colindex, -1)
        return (-1, -1)

    def set_length_listener(self, listener):
        self._length_listener = listener

    def _assign_notes(self, force=False):
        if not self._clip:
            return
        matrix = self.canonical_parent.get_button_matrix()
        matrix.prepare_update()
        max_index = int(self._clip.length / self._quantize_base)
        offset = int(self._pos_scroll / self._quantize)
        if offset >= max_index:
            pass
        notes = self._clip.get_notes_extended(0, 127, 0.0, self._clip.length)
        scale_base_note = self._padmode.get_base_note()
        scale = self._padmode.get_scale
        self._step_values = [None, None, None, None, None, None, None, None]
        self._steps_notes = [None, None, None, None, None, None, None, None]
        for note in notes:
            note = (
             note.pitch, note.start_time, note.duration, note.velocity, note.mute)
            col, row = self.note_to_grid(note, scale, scale_base_note)
            if row >= 0:
                self._grid[col][row].pre_add_note(note)
            if col >= 0:
                if self._step_values[col] is None:
                    self._step_values[col] = note[3]
                    self._steps_notes[col] = []
                    self._steps_notes[col].append(note)
                else:
                    self._steps_notes[col].append(note)
                    self._step_values[col] = max(note[3], self._step_values[col])

        for row in range(8):
            rownote = scale.grid_row_to_note(row)
            isbase = rownote % 12 == scale_base_note
            for column in range(8):
                grid = self._grid[column][row]
                if column + offset < max_index and column < self._quantize_grid_max:
                    grid.is_base_note = isbase
                    grid.note_finalize(force)
                else:
                    grid.is_base_note = False
                    grid.note_finalize(force)

        matrix.commit_update()
        self.assign_encoders()
        return

    def assign_encoders(self):
        for col in range(8):
            self._encoder_handler.set_step_note_levels(col, self._step_values[col], self)

    def level_change(self, col, value):
        if self._step_values[col] is not None:
            if len(self._steps_notes[col]) > 0:
                update_notes = []
                self._in_velocity = max(1, value)
                for note in self._steps_notes[col]:
                    pitch, pos, dur, vel, mute = note
                    update_notes.append((pitch, pos, dur, value, mute))
                    note_specification = Live.Clip.MidiNoteSpecification(pitch, pos, dur, vel)
                    update_notes.append(note_specification)

                self._clip.add_new_notes(update_notes)

    def _change_clip_slot(self):
        self.assign_highlighted_clip_slot()

    @subject_slot('playing_position')
    def _handle_play_head(self):
        relpos = (self._clip.playing_position - self._pos_scroll) / self._quantize
        if relpos < 0:
            colindex = -1
        else:
            colindex = int(relpos)
        if colindex in range(self._quantize_grid_max):
            self.set_run_light(colindex)
        else:
            self.set_run_light(-1)
        self._page_handler.notify_position(self._clip.playing_position, self._quantize_base)

    def set_run_light(self, run_index):
        if run_index != self._StepMode__current_run_index:
            if self._StepMode__current_run_index != -1:
                for rowindex in range(8):
                    self._grid[self._StepMode__current_run_index][rowindex].restore()

            self._StepMode__current_run_index = run_index
            if self._StepMode__current_run_index != -1:
                for rowindex in range(8):
                    self._grid[run_index][rowindex].brighten()

    @subject_slot('notes')
    def _handle_notes_changed(self):
        self._assign_notes()

    def refresh(self):
        if self._active:
            for button, (_, _) in self.canonical_parent.get_button_matrix().iterbuttons():
                if button:
                    button.send_value(0, True)

    def _assign_buttons(self):
        for button, (column, row) in self.canonical_parent._bmatrix.iterbuttons():
            if button:
                self._grid[column][row].set_button(button, column, row)
                self.canonical_parent._forwarding_registry[(MIDI_NOTE_ON_STATUS, button.get_identifier())] = button
                self.canonical_parent._forwarding_registry[(MIDI_NOTE_OFF_STATUS, button.get_identifier())] = button
                button.set_to_notemode(False)

    def notify_edit_toggle(self, which, shift):
        if which == LOCK_BUTTON:
            self._mono_mode = not self._mono_mode
            self.canonical_parent.show_message('Step Edit in ' + (self._mono_mode and 'Mono' or 'Poly') + ' mode')
            return self._mono_mode and 127 or 0
        if which == VARIATION_BUTTON:
            return 0
        return 0

    def notify_edit_action(self, val, action_type, modifier):
        if action_type == CLEAR_ACTION and self._clip:
            self._clip.remove_notes_extended(0, 128, 0.0, self._clip.length)
        else:
            if action_type == DUPLICATE_ACTION:
                if self._clip:
                    if modifier:
                        if self._clip.length <= 2048.0:
                            self._clip.duplicate_loop()
                            self.canonical_parent.show_message('Double Loop : ' + str(int(self._clip.length / 4)) + ' Bars')
                            self.song().view.detail_clip = self._clip
                            self.application().view.focus_view('Detail/Clip')
                        else:
                            self.canonical_parent.show_message('Clip is to long to Duplicate')

    def clear_clip(self, option=False):
        if not self._clip:
            return
        elif option:
            self._clip.remove_notes_extended(0, 128, self._pos_scroll, self._quantize * 8)
        else:
            self._clip.remove_notes_extended(0, 128, 0.0, self._clip.length)

    def repeat_section(self, option=False):
        if not self._clip:
            return
        notes = self._clip.get_notes_extended(0, 127, self._pos_scroll, self._quantize * 8)
        sections = int(self._clip.length / (self._quantize * 8))
        if sections > 1:
            ls = []
            for sec_index in range(sections):
                copypos = sec_index * self._quantize * 8
                for note in notes:
                    note = (
                     note.pitch, note.start_time, note.duration, note.velocity, note.mute)
                    noteval = note[0]
                    basepos = note[1] - self._pos_scroll
                    note_specification = Live.Clip.MidiNoteSpecification(noteval, copypos + basepos, note[2], note[3], note[4])
                    ls.append(note_specification)

            self._clip.add_new_notes(ls)

    def double_clip(self, option=False):
        if not self._clip:
            return
        if self._clip.length <= 2048.0:
            self._clip.duplicate_loop()
            self.canonical_parent.show_message('Double Loop : ' + str(int(self._clip.length / 4)) + ' Bars')

    @subject_slot('playing_status')
    def _handle_playing(self):
        if not self._clip.is_playing:
            pass

    @subject_slot('color')
    def _handle_color_changed(self):
        if self._clip:
            _, oncolor = toHSB(self._clip.color)
            self.on_color = oncolor + 2
            self.bs_color = oncolor
            self._page_handler.update_buttons()
            self._assign_notes(True)

    @subject_slot('loop_end')
    def _handle_loop_end_changed(self):
        self._page_handler.update_buttons()
        self._assign_notes(True)

    @subject_slot('end_marker')
    def _handle_end_time_changed(self):
        pass

    def register_page_handler(self):
        self._page_handler.set_page_control(self)

    def spec_unbind(self, index=0):
        self._page_handler.set_page_control(None)

    def get_grid_info(self):
        return (
         self._quantize, self._clip.length, 8)

    def enter(self):
        self._active = True
        self.assign_highlighted_clip_slot()
        self._modifier_componenet.set_action_listener(self)
        self._modifier_componenet.set_edit_state(lock=(self._mono_mode))
        self._pos_scroll = 0.0
        self._base_pitch = self._padmode.get_scale.set_grid_map(self._padmode._base_note, self._base_pitch)
        self.canonical_parent.show_message('Step Edit ' + from_midi_note(self._base_pitch))
        self.application().view.focus_view('Detail/Clip')
        self._assign_buttons()
        self._assign_notes(True)

    def exit(self):
        self._active = False
        self.canonical_parent.deassign_matrix()
        self.canonical_parent.get_session().set_clip_launch_buttons(None)
        self._modifier_componenet.set_edit_state()
        self._handle_play_head.subject = None
        self._handle_notes_changed.subject = None
        self._handle_loop_end_changed.subject = None
        self._handle_end_time_changed.subject = None
        self._handle_playing.subject = None
        self._handle_color_changed.subject = None
        self._modifier_componenet.set_action_listener(None)
        for row in self._grid:
            for cell in row:
                cell.release()
# okay decompiling scripts/StepMode.pyc
