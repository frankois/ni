# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/DrumStepMode.py
# Compiled at: 2021-05-04 12:11:01
# Size of source mod 2**32: 24007 bytes
import Live
from _Framework.SubjectSlot import subject_slot
from _Framework.InputControlElement import MIDI_NOTE_ON_STATUS, MIDI_NOTE_OFF_STATUS
from .MidiMap import colorOnOff, quantize_settings, quantize_clip_live, qauntize_is_triplet, quantize_base, quantize_string, find_drum_device, PAD_MODE, CI_WHITE
from .MaschineMode import MaschineMode
from .ModifierComponent import ModifierComponent, VARIATION_BUTTON, CLEAR_ACTION, DUPLICATE_ACTION, MASK_CLEAR
from .DrumMode import DrumPad, color_by_name
GridQuantization = Live.Clip.GridQuantization
VEL_MAP = [
 1, 10, 20, 30, 40, 50, 60, 70, 75, 80, 85, 90, 100, 110, 120, 127]

def wrap_triplet_index(index32):
    return int(index32 / 6) * 8 + index32 % 6


def arm_to_clip_slot(song, clip_slot=None):
    track = None
    if not clip_slot:
        clip_slot = song.view.highlighted_clip_slot
        track = clip_slot.track.canonical_parent
    else:
        track = clip_slot.canonical_parent
    if track:
        if track.can_be_armed:
            if not track.arm:
                tracks = song.tracks
                for songtrack in tracks:
                    if songtrack != track and songtrack and songtrack.can_be_armed and songtrack.arm:
                        songtrack.arm = False

                track.arm = True
                song.view.selected_track = track


def arm_to_clips_track(song, clip):
    track = clip.canonical_parent.canonical_parent
    if track:
        if track.can_be_armed:
            if not track.arm:
                tracks = song.tracks
                for songtrack in tracks:
                    if songtrack != track and songtrack and songtrack.can_be_armed and songtrack.arm:
                        songtrack.arm = False

                track.arm = True
                song.view.selected_track = track


class VelocityPad:

    def __init__(self, velocity_index, callback):
        self.index = velocity_index
        self._VelocityPad__button = None
        self._VelocityPad__callback = callback

    def assign_button(self, button):
        if button:
            self._VelocityPad__button = button
            self._VelocityPad__button.add_value_listener(self.handle_selection)
        else:
            self._VelocityPad__button.remove_value_listener(self.handle_selection)
            self._VelocityPad__button = None

    def handle_selection(self, value):
        if value:
            self._VelocityPad__callback(self.index)

    def update_button(self, selected):
        if selected:
            self._VelocityPad__button.send_color_direct(38)
        else:
            self._VelocityPad__button.send_color_direct(36)


class DrumStepPad:

    def __init__(self, index, callback):
        self.index = index
        self._DrumStepPad__button = None
        self._DrumStepPad__callback = callback
        self._DrumStepPad__color = colorOnOff(CI_WHITE)
        self._DrumStepPad__note = None

    def assign_button(self, button):
        if button:
            self._DrumStepPad__button = button
            self._DrumStepPad__button.add_value_listener(self.handle_selection)
        else:
            self._DrumStepPad__button.remove_value_listener(self.handle_selection)
            self._DrumStepPad__button = None

    def handle_selection(self, value):
        if value:
            self._DrumStepPad__callback(self.index)

    def set_note(self, note):
        self._DrumStepPad__note = note

    def set_color(self, color):
        self._DrumStepPad__color = color
        self._DrumStepPad__button.send_color_direct(color)

    def brighten(self):
        self._DrumStepPad__button.send_color_direct(123)

    def restore(self):
        self._DrumStepPad__button.send_color_direct(self._DrumStepPad__color)

    @property
    def note(self):
        return self._DrumStepPad__note


class DrumStepMode(MaschineMode):
    __subject_events__ = ('pressed_pads', )
    _DrumStepMode__selected_velocity_index = 15
    _DrumStepMode__pad_selection_only = False
    _DrumStepMode__pad_select_direct = False
    _modifier_componenet = None
    _length_listener = None
    _page_handler = None

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
            self.pad_to_color = self._DrumStepMode__pad_to_onoff
        else:
            self.pad_to_color = self._DrumStepMode__pad_to_color
        self._DrumStepMode__vel_pads = tuple((VelocityPad(index, self.vel_changed) for index in range(16)))
        self._DrumStepMode__step_pads = tuple((DrumStepPad(index, self.step_selected_changed) for index in range(32)))
        self._selected_note = 60
        self._pos_scroll = 0.0
        self._clip = None
        self._run_light_handler = None
        self._quantize_index = 7
        self._quantize = quantize_settings[self._quantize_index]
        self._istriplet = qauntize_is_triplet[self._quantize_index]
        self._quantize_base = quantize_base[self._quantize_index]
        self.on_color = 0
        self.st_color = 0
        self._current_runindex = -1

    def set_page_handler(self, handler):
        self._page_handler = handler

    def get_color(self, value, column, row):
        note_index = row * 4 + column
        return self._pads[note_index].get_color()

    def get_mode_id(self):
        return PAD_MODE

    def device_dependent(self):
        return True

    def ext_name(self):
        return 'step_mode'

    def page_index(self):
        seg_len = self._quantize_base * 32
        return (int(self._pos_scroll / seg_len), max(1, int(self._clip.length / seg_len)))

    def select_pos(self, scroll_index):
        self._pos_scroll = scroll_index * (self._quantize_base * 32)
        self._assign_notes()
        self._page_handler.update_buttons()

    def set_mode_elements(self, modifier_component):
        assert isinstance(modifier_component, ModifierComponent)
        self._modifier_componenet = modifier_component

    def get_clip(self):
        return self._clip

    def step_length_change(self):
        pass

    def set_run_light(self, run_index):
        if run_index != self._current_runindex:
            if self._current_runindex != -1:
                self._DrumStepMode__step_pads[self._current_runindex].restore()
            self._current_runindex = run_index
            if self._current_runindex != -1:
                self._DrumStepMode__step_pads[run_index].brighten()

    def vel_changed(self, index):
        if index != self._DrumStepMode__selected_velocity_index:
            self._DrumStepMode__vel_pads[self._DrumStepMode__selected_velocity_index].update_button(False)
            self._DrumStepMode__selected_velocity_index = index
            self._DrumStepMode__vel_pads[self._DrumStepMode__selected_velocity_index].update_button(True)

    def __pad_to_onoff(self, pad):
        if pad:
            if len(pad.chains) == 0:
                return (0, 0)
            return (0, 0)
        else:
            return (0, 0)

    def __pad_to_color(self, pad):
        if pad:
            chains = pad.chains
            name = pad.name
            if len(chains) == 0:
                return (72, 72)
            col = color_by_name(name) << 2
            return (col, col + 2)
        return (8, 10)

    def step_selected_changed(self, step_index):
        if self._modifier_componenet.is_shift_down():
            if step_index < 8:
                self._modifier_componenet.handle_edit_action(step_index)
        else:
            index = step_index
            if self._istriplet:
                rowx = int(step_index / 8)
                colx = step_index % 8
                if colx >= 6:
                    return
                index = rowx * 6 + colx
            step = self._DrumStepMode__step_pads[step_index]
            note = self.device.view.selected_drum_pad.note
            position = self._pos_scroll + self._quantize * index
            if step.note:
                self._clip.remove_notes_extended(note, 1, position, self._quantize)
            else:
                note_specification = Live.Clip.MidiNoteSpecification(note, position, self._quantize, VEL_MAP[self._DrumStepMode__selected_velocity_index])
                self._clip.add_new_notes([note_specification])

    def note_color(self, note):
        vel = note.velocity
        if vel < 51:
            return self.on_color - 2
        if vel < 96:
            return self.on_color - 1
        return self.on_color

    def _assign_notes(self):
        if not self._clip:
            return
        if self.device:
            note = self.device.view.selected_drum_pad.note
            notes = self._clip.get_notes_extended(note, 1, 0.0, self._clip.length)
            for step in self._DrumStepMode__step_pads:
                step.set_note(None)

            for note in notes:
                ci = (note.start_time - self._pos_scroll) / self._quantize
                if ci < 0:
                    colindex = -1
                else:
                    colindex = int(ci + 0.05)
                if self._istriplet:
                    if colindex in range(24):
                        self._DrumStepMode__step_pads[wrap_triplet_index(colindex)].set_note(note)
                    elif colindex in range(32):
                        self._DrumStepMode__step_pads[colindex].set_note(note)

            for step in self._DrumStepMode__step_pads:
                if step.note:
                    step.set_color(self.note_color(step.note))
                else:
                    step.set_color(None)

            return

    @subject_slot('playing_position')
    def _handle_play_head(self):
        if self._run_light_handler:
            ci = (self._clip.playing_position - self._pos_scroll) / self._quantize
            if ci < 0:
                colindex = -1
            else:
                colindex = int(ci + 0.01)
            if self._istriplet:
                if colindex in range(24):
                    self._run_light_handler.set_run_light(wrap_triplet_index(colindex))
                else:
                    self._run_light_handler.set_run_light(-1)
            elif colindex in range(32):
                self._run_light_handler.set_run_light(colindex)
            else:
                self._run_light_handler.set_run_light(-1)
            self._page_handler.notify_position(self._clip.playing_position, self._quantize, 32)

    @subject_slot('notes')
    def _handle_notes_changed(self):
        self._assign_notes()

    def notify_edit_toggle(self, which, shift):
        if which == VARIATION_BUTTON:
            return 0
        return 0

    def handle_shift(self, shift_value):
        self._DrumStepMode__pad_selection_only = shift_value
        self.reassign_drum_pads()

    def notify_edit_action(self, val, action_type, modifier):
        note = self.device.view.selected_drum_pad.note
        if action_type == CLEAR_ACTION:
            if self._clip:
                if modifier:
                    self._clip.remove_notes_extended(0, 128, 0.0, self._clip.length)
            else:
                self._clip.remove_notes_extended(note, 1, 0.0, self._clip.length)
        elif action_type == DUPLICATE_ACTION:
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
        pass

    def double_clip(self, option=False):
        if not self._clip:
            return
        if self._clip.length <= 2048.0:
            self._clip.duplicate_loop()
            self.canonical_parent.show_message('Double Loop : ' + str(int(self._clip.length / 4)) + ' Bars')

    def _change_quantize(self, nav_dir):
        if self._quantize_index + nav_dir in range(len(quantize_settings)):
            self._quantize_index += nav_dir
            self._quantize = quantize_settings[self._quantize_index]
            self._istriplet = qauntize_is_triplet[self._quantize_index]
            self._quantize_base = quantize_base[self._quantize_index]
            self._assign_notes()
            self._handle_loop_end_changed()
            self._clip.view.grid_quantization = quantize_clip_live[self._quantize_index]
            self._clip.view.grid_is_triplet = qauntize_is_triplet[self._quantize_index]
            self.canonical_parent.show_message('Step Edit Grid ' + quantize_string[self._quantize_index])

    def navigate(self, nav_dir, modifier, alt_modifier=False, nav_source=0):
        if modifier == 0:
            if alt_modifier:
                self._change_quantize(nav_dir)
            else:
                newpos = self._pos_scroll + nav_dir * (self._quantize * 32)
                if newpos < 0.0:
                    self._pos_scroll = self._clip.length - self._quantize * 32
                else:
                    if newpos >= self._clip.length:
                        self._pos_scroll = 0.0
                    else:
                        self._pos_scroll = newpos
                self._assign_notes()
                self._page_handler.update_buttons()
        elif self.device:
            if self.device.view:
                self.device.view.drum_pads_scroll_position = max(0, min(28, self.device.view.drum_pads_scroll_position + nav_dir))

    def hande_drum_pad_selection(self, index, value):
        if value:
            if self.device:
                pad_idx = self.device.view.drum_pads_scroll_position * 4 + index
                self.device.view.selected_drum_pad = self.device.drum_pads[pad_idx]
                modmode = self._modifier_componenet.modifier_mask()
                if modmode == MASK_CLEAR:
                    self._clip.remove_notes_extended(self.device.view.selected_drum_pad.note, 1, 0.0, self._clip.length)

    def reassign_drum_pads(self):
        for pad in self._pads:
            pad.set_notemode(not self._DrumStepMode__pad_selection_only)
            if not self._DrumStepMode__pad_selection_only:
                button = pad.button
                self.canonical_parent._forwarding_registry[(MIDI_NOTE_ON_STATUS, button.get_identifier())] = button
                self.canonical_parent._forwarding_registry[(MIDI_NOTE_OFF_STATUS, button.get_identifier())] = button
                pad.assign_midi()

    def notify(self, blink_state):
        pass

    def arm_to_clip(self):
        if self._clip:
            arm_to_clips_track(self.song(), self._clip)

    def register_page_handler(self):
        self._page_handler.set_page_control(self)

    def spec_unbind(self, index=0):
        self._page_handler.set_page_control(None)

    def get_grid_info(self):
        return (
         self._quantize, self._clip.length, 32)

    def enter(self):
        self._active = True
        self.assign_track_device()
        self.assign_highlighted_clip_slot()
        _DrumStepMode__pad_selection_only = False
        self._modifier_componenet.set_action_listener(self)
        self._modifier_componenet.set_edit_state(lock=False)
        matrix = self.canonical_parent._bmatrix
        matrix.prepare_update()
        for button, (column, row) in matrix.iterbuttons():
            if button:
                if row > 3:
                    if column > 3:
                        pad_index = (7 - row) * 4 + column - 4
                        note_index = (3 - (7 - row)) * 4 + column - 4
                        pad = self._pads[pad_index]
                        pad.set_notemode(not self._DrumStepMode__pad_selection_only)
                        pad.set_action_callback(self.hande_drum_pad_selection)
                        pad.set_note_index(note_index)
                        self.canonical_parent._forwarding_registry[(MIDI_NOTE_ON_STATUS, button.get_identifier())] = self._DrumStepMode__pad_selection_only or button
                        self.canonical_parent._forwarding_registry[(MIDI_NOTE_OFF_STATUS, button.get_identifier())] = button
                        pad.assign_midi()
                        button.send_color_direct(pad.get_color())
                    else:
                        vel_index = (7 - row) * 4 + column
                        self._DrumStepMode__vel_pads[vel_index].assign_button(button)
                        self._DrumStepMode__vel_pads[vel_index].update_button(vel_index == self._DrumStepMode__selected_velocity_index)
                else:
                    step_index = row * 8 + column
                    self._DrumStepMode__step_pads[step_index].assign_button(button)
                    self._DrumStepMode__step_pads[step_index].set_color(None)

        self.set_step_colors()
        self._assign_notes()
        matrix.commit_update()
        self.track = self.song().view.selected_track
        if self.device:
            self._on_name_changed.subject = self.device.view.selected_drum_pad
        self._run_light_handler = self

    def exit(self):
        if self._active:
            if self.canonical_parent:
                if self.canonical_parent._bmatrix:
                    matrix = self.canonical_parent._bmatrix
                    matrix.prepare_update()
                    for button, (column, row) in matrix.iterbuttons():
                        if button:
                            if row > 3:
                                if column > 3:
                                    pad_index = (7 - row) * 4 + column - 4
                                    pad = self._pads[pad_index]
                                    pad.release()
                            if row < 4:
                                step_index = row * 8 + column
                                self._DrumStepMode__step_pads[step_index].assign_button(None)
                            elif column < 4:
                                vel_index = (7 - row) * 4 + column
                                self._DrumStepMode__vel_pads[vel_index].assign_button(None)

                    matrix.commit_update()
        self._modifier_componenet.set_action_listener(self)
        self._active = False
        self._on_scroll_index_changed.subject = None
        self._on_selected_drum_pad_changed.subject = None
        self._on_name_changed.subject = None
        self._handle_play_head.subject = None
        self._handle_notes_changed.subject = None
        self._handle_end_time_changed.subject = None
        self._handle_loop_end_changed.subject = None
        self._handle_color_changed.subject = None
        self._handle_playing.subject = None
        self._run_light_handler = None
        self.device = None
        self.track = None

    def _change_clip_slot(self):
        self.assign_highlighted_clip_slot()

    def assign_highlighted_clip_slot(self):
        self._clip = self.song().view.detail_clip
        if self._clip.is_midi_clip:
            self._handle_play_head.subject = self._clip
            self._handle_notes_changed.subject = self._clip
            self._handle_end_time_changed.subject = self._clip
            self._handle_loop_end_changed.subject = self._clip
            self._handle_playing.subject = self._clip
            self._handle_color_changed.subject = self._clip

    @subject_slot('playing_status')
    def _handle_playing(self):
        if self._run_light_handler:
            if not self._clip.is_playing:
                self._run_light_handler.set_run_light(-1)

    @subject_slot('loop_end')
    def _handle_loop_end_changed(self):
        self._page_handler.update_buttons()
        if self._run_light_handler:
            if self._length_listener:
                self._length_listener.step_length_change()

    @subject_slot('end_marker')
    def _handle_end_time_changed(self):
        pass

    @subject_slot('color')
    def _handle_color_changed(self):
        if self._clip:
            self._page_handler.update_buttons()

    def update_pads(self):
        if self._active:
            for dpad in self._pads:
                dpad.send_color()

    def refresh(self):
        if self._active:
            for dpad in self._pads:
                dpad._button.reset()
                dpad.send_color()

    def assign_track_device(self):
        if self.device:
            if self.device.view:
                self._on_scroll_index_changed.subject = None
                self._on_selected_drum_pad_changed.subject = None
                self._on_name_changed.subject = None
        self.track = self.song().view.selected_track
        self.device = find_drum_device(self.track)
        if self.device:
            self._on_scroll_index_changed.subject = self.device.view
            self._on_selected_drum_pad_changed.subject = self.device.view
            self._on_name_changed.subject = self.device
        self.assign_pads()

    def assign_pads(self):
        global matrix
        matrix = self.canonical_parent._bmatrix
        matrix.prepare_update()
        self._visible_drum_pads = None
        self._selected_pad = None
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
                dpad.set_color((0, 0))
                dpad.set_pad(None)

            matrix = self.canonical_parent._bmatrix
            matrix.prepare_update()
            for button, (column, row) in matrix.iterbuttons():
                if column > 3 and row > 3:
                    pad_index = (7 - row) * 4 + column - 4
                    self._pads[pad_index].set_button(button)
                    self._pads[pad_index].send_color()

        matrix.commit_update()

    def index_of(self, pad):
        for index in range(16):
            if self._pads[index]._pad == pad:
                return index

        return -1

    def set_step_colors(self):
        _, oncolor = self.pad_to_color(self.device.view.selected_drum_pad)
        self.on_color = oncolor
        self.st_color = oncolor

    @subject_slot('name')
    def _on_name_changed(self):
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
                self.set_step_colors()
                self._assign_notes()

    @subject_slot('drum_pads_scroll_position')
    def _on_scroll_index_changed(self):
        if self._active:
            if self.device:
                self.assign_pads()
                self.update_pads()

    def disconnect(self):
        self.exit()
        self.track = None
        self.device = None
        self._visible_drum_pad_slots = None
        self._visible_drum_pads = None
        self._pads = None
        self._selected_pad = None
        super().disconnect()
# okay decompiling src/DrumStepMode.pyc
