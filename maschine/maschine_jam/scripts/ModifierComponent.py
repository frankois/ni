# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/ModifierComponent.py
# Compiled at: 2021-04-29 13:54:08
# Size of source mod 2**32: 13931 bytes
import Live
from _Framework.SubjectSlot import subject_slot
from _Framework.InputControlElement import MIDI_CC_TYPE
from .StateButton import StateButton
import _Framework.CompoundComponent as CompoundComponent
from .MidiMap import QUANT_CONST, QUANT_STRING, find_drum_device, select_clip_slot
CLEAR_ACTION = 0
DUPLICATE_ACTION = 1
LOCK_BUTTON = 10
VARIATION_BUTTON = 11
TRANSPOSE = [0, 0, 0, 0, -1, 1, -12, 12]
MASK_SHIFT = 1
MASK_BROWSE = 2
MASK_CLEAR = 4
MASK_DUPLICATE = 8
MASK_SPEC = 16
MASK_SELECT = 32

class ModifierComponent(CompoundComponent):
    _ModifierComponent__shift_down = False
    _ModifierComponent__select_down = False
    _ModifierComponent__delete_down = False
    _ModifierComponent__duplicate_down = False
    _ModifierComponent__browse_down = False
    _ModifierComponent__macro_down = False
    _ModifierComponent__quantize_setting = 5

    def __init__(self, session, *a, **k):
        (super(ModifierComponent, self).__init__)(*a, **k)
        self._ModifierComponent__session = session
        self._ModifierComponent__delete_button = StateButton(True, MIDI_CC_TYPE, 0, 95, name='Clear_Button')
        self._ModifierComponent__do_delete.subject = self._ModifierComponent__delete_button
        self._ModifierComponent__duplicate_button = StateButton(True, MIDI_CC_TYPE, 0, 96, name='Duplicate_Button')
        self._ModifierComponent__do_duplicate.subject = self._ModifierComponent__duplicate_button
        self._select_button = StateButton(True, MIDI_CC_TYPE, 0, 80, name='Select_Button')
        self._ModifierComponent__do_select_button.subject = self._select_button
        self._ModifierComponent__lock_button = StateButton(True, MIDI_CC_TYPE, 0, 47, name='Lock_Button')
        self._ModifierComponent__do_lock.subject = self._ModifierComponent__lock_button
        self._ModifierComponent__macro_button = StateButton(True, MIDI_CC_TYPE, 0, 90, name='Macro_Button')
        self._ModifierComponent__do_macro.subject = self._ModifierComponent__macro_button
        self._left_button = StateButton(True, MIDI_CC_TYPE, 0, 107, name='Metro_Button')
        self._right_button = StateButton(True, MIDI_CC_TYPE, 0, 104, name='Loop_Button')
        self._rec_button = StateButton(True, MIDI_CC_TYPE, 0, 109, name='Record_Button')
        self._do_left_button.subject = self._left_button
        self._do_right_button.subject = self._right_button
        self._do_rec_button.subject = self._rec_button
        self._listen_overdub.subject = self.song()
        self._listen_loop.subject = self.song()
        self._listen_metronome.subject = self.song()
        self._ModifierComponent__action_listener = None
        self._ModifierComponent__shift_listener = None

    @subject_slot('overdub')
    def _listen_overdub(self):
        if self._ModifierComponent__shift_down:
            self._rec_button.set_display_value(self.song().overdub and 127 or 0, True)

    @subject_slot('loop')
    def _listen_loop(self):
        if self._ModifierComponent__shift_down:
            self._right_button.set_display_value(self.song().loop and 127 or 0, True)

    @subject_slot('metronome')
    def _listen_metronome(self):
        if self._ModifierComponent__shift_down:
            self._left_button.set_display_value(self.song().metronome and 127 or 0, True)

    def _update_shift_status(self):
        if self._ModifierComponent__shift_down:
            self._rec_button.set_display_value(self.song().overdub and 127 or 0, True)
            self._right_button.set_display_value(self.song().loop and 127 or 0, True)
            self._left_button.set_display_value(self.song().metronome and 127 or 0, True)
        else:
            self._rec_button.set_display_value(0, True)
            self._left_button.set_display_value(0, True)
            self._right_button.set_display_value(0, True)

    def set_browse_down(self, value):
        self._ModifierComponent__browse_down = value

    @subject_slot('value', identify_sender=True)
    def __do_lock(self, value, sender):
        if sender.grabbed:
            return
        if self._ModifierComponent__action_listener:
            if value > 0:
                newstate = self._ModifierComponent__action_listener.notify_edit_toggle(LOCK_BUTTON, self._ModifierComponent__shift_down)
                self._ModifierComponent__lock_button.set_value(newstate)

    @subject_slot('value', identify_sender=True)
    def __do_macro(self, value, sender):
        if sender.grabbed:
            return
        self._ModifierComponent__macro_down = value > 0
        self._ModifierComponent__macro_button.set_display_value(value, True)

    def set_edit_state(self, **args):
        if 'lock' in args:
            self._ModifierComponent__lock_button.set_value(args['lock'] and 127 or 0)
        else:
            self._ModifierComponent__lock_button.set_value(0)

    def set_shiftstatus(self, value):
        self._ModifierComponent__shift_down = value > 0
        self._update_shift_status()
        if self._ModifierComponent__shift_listener:
            self._ModifierComponent__shift_listener.notify_shift(self._ModifierComponent__shift_down)

    @subject_slot('value', identify_sender=True)
    def __do_select_button(self, value, sender):
        if sender.grabbed:
            return
        self._select_button.send_value(value)
        self._ModifierComponent__select_down = value > 0

    def register_shift_listener(self, listener):
        self._ModifierComponent__shift_listener = listener

    @subject_slot('value', identify_sender=True)
    def __do_delete(self, value, sender):
        if sender.grabbed:
            return
        self._ModifierComponent__delete_button.send_value(value)
        if not self._ModifierComponent__shift_down:
            self._ModifierComponent__delete_down = value > 0
        else:
            if value != 0:
                clip = self.song().view.detail_clip
                if clip != None:
                    clip.clear_all_envelopes()
                    self.canonical_parent.show_message('Clear Envelopes ' + clip.name)
        return

    @subject_slot('value', identify_sender=True)
    def __do_duplicate(self, value, sender):
        if sender.grabbed:
            return
        self._ModifierComponent__duplicate_button.send_value(value)
        if not self._ModifierComponent__shift_down:
            self._ModifierComponent__duplicate_down = value > 0
        else:
            if value != 0:
                clip = self.song().view.detail_clip
                if clip != None:
                    if clip.is_midi_clip:
                        if clip.length <= 128.0:
                            clip.duplicate_loop()
                            self.canonical_parent.show_message('Double Loop : ' + str(int(clip.length / 4)) + ' Bars')
                            self.application().view.focus_view('Detail/Clip')
                        else:
                            self.canonical_parent.show_message('Clip is to long to Duplicate')
        return

    def set_action_listener(self, listener):
        self._ModifierComponent__action_listener = listener

    def handle_edit(self, clipslotcomp, value):
        if value == 0:
            return
        if clipslotcomp._clip_slot is not None:
            if self._ModifierComponent__delete_down:
                self._ModifierComponent__handle_delete(clipslotcomp)
            elif self._ModifierComponent__duplicate_down:
                self._ModifierComponent__handle_duplicate(clipslotcomp)
            elif self._ModifierComponent__browse_down:
                self._ModifierComponent__handle_mode_scene_clip(clipslotcomp)
            elif self._ModifierComponent__macro_down:
                self._ModifierComponent__handle_new_action(clipslotcomp)
            elif self._ModifierComponent__select_down:
                self._ModifierComponent__handle_select_action(clipslotcomp)
            elif self._ModifierComponent__shift_down:
                self._ModifierComponent__handle_shift_action(clipslotcomp)
        elif self._ModifierComponent__browse_down:
            self._ModifierComponent__handle_mode_scene_clip(clipslotcomp)
        else:
            if self._ModifierComponent__shift_down:
                self._ModifierComponent__handle_shift_action(clipslotcomp)
        return

    def __handle_shift_action(self, clipslotcomp):
        columm, row = clipslotcomp.get_index()
        if row == 0:
            self.handle_edit_action(columm)

    def __handle_select_action(self, clipslotcomp):
        self.song().view.highlighted_clip_slot = clipslotcomp._clip_slot

    @subject_slot('value', identify_sender=True)
    def _do_left_button(self, value, sender):
        if sender.grabbed:
            return
        if self._ModifierComponent__shift_down:
            if value == 0:
                return
            self.song().metronome = not self.song().metronome
        else:
            self._left_button.set_display_value(value > 0 and 127 or 0, True)
            if value == 0:
                return
            self.canonical_parent.invoke_nav_left()

    @subject_slot('value', identify_sender=True)
    def _do_right_button(self, value, sender):
        if sender.grabbed:
            return
        if self._ModifierComponent__shift_down:
            if value == 0:
                return
            self.song().loop = not self.song().loop
        else:
            self._right_button.set_display_value(value > 0 and 127 or 0, True)
            if value == 0:
                return
            self.canonical_parent.invoke_nav_right()

    @subject_slot('value', identify_sender=True)
    def _do_rec_button(self, value, sender):
        if sender.grabbed:
            return
        if self._ModifierComponent__shift_down:
            if value == 0:
                return
            self.song().overdub = not self.song().overdub
        else:
            self._rec_button.set_display_value(value > 0 and 127 or 0, True)
            if value > 0:
                self.canonical_parent.invoke_rec()

    def handle_edit_action(self, index, scale=None):
        if not self._ModifierComponent__shift_down:
            return
            if index == 0:
                if self.song().can_undo == 1:
                    self.song().undo()
                    self.canonical_parent.show_message(str('UNDO'))
            elif index == 1:
                if self.song().can_redo == 1:
                    self.song().redo()
                    self.canonical_parent.show_message(str('REDO'))
        elif index == 2 or index == 3:
            clip = self.song().view.detail_clip
            if clip:
                clip.quantize(QUANT_CONST[self._ModifierComponent__quantize_setting], index == 2 and 1.0 or 0.5)
                self.canonical_parent.show_message('Quantize Clip ' + clip.name + ' by ' + QUANT_STRING[self._ModifierComponent__quantize_setting])
        else:
            clip = self.song().view.detail_clip
        if clip:
            if clip.is_midi_clip:
                track = clip.canonical_parent.canonical_parent
                drum_device = find_drum_device(track)
                if not drum_device:
                    self._ModifierComponent__transpose_clip(clip, TRANSPOSE[index], scale)

    def __transpose_clip(self, clip, amount, bn_scale):
        notes = clip.get_selected_notes_extended()
        if len(notes) == 0:
            clip.select_all_notes()
            notes = clip.get_selected_notes_extended()
        for note in notes:
            if bn_scale:
                basenote, scale = bn_scale
                pv = scale.transpose_by_scale(basenote, note.pitch, amount)
            else:
                pv = note.pitch + amount
            if not pv < 0:
                if pv > 127:
                    pv = note.pitch
                note.pitch = pv
                notes.append(note)

        clip.apply_note_modifications(notes)

    def __handle_mode_scene_clip(self, clipslotcomp):
        if clipslotcomp._clip_slot is None:
            return
        clip_slot = clipslotcomp._clip_slot
        self.song().view.highlighted_clip_slot = clip_slot
        return

    def __handle_delete(self, clipslotcomp):
        if self._ModifierComponent__shift_down:
            pass
        else:
            clipslotcomp._do_delete_clip()

    def __handle_duplicate(self, clipslotcomp):
        if self._ModifierComponent__shift_down:
            pass
        else:
            self.duplicate_clip_slot(clipslotcomp._clip_slot)

    def __handle_new_action(self, clipslotcomp):
        song = self.song()
        clip_slot = clipslotcomp._clip_slot
        track = clip_slot.canonical_parent
        if clip_slot.clip == None:
            if track.has_midi_input:
                try:
                    clip_slot.create_clip(4.0)
                    song.view.detail_clip = clip_slot.clip
                    select_clip_slot(song, clip_slot)
                    self.application().view.focus_view('Detail/Clip')
                    self.canonical_parent.show_message('New Midi Clip ' + song.view.highlighted_clip_slot.clip.name)
                except Live.Base.LimitationError:
                    pass
                except RuntimeError:
                    pass

    def double_clipslot(self, clip_slot):
        song = self.song()
        track = clip_slot.canonical_parent
        if clip_slot.clip is not None:
            if track.has_midi_input:
                clip = clip_slot.clip
                if clip.length <= 2048.0:
                    clip.duplicate_loop()
                    self.canonical_parent.show_message('Double Loop : ' + str(int(clip.length / 4)) + ' Bars')
                    song.view.detail_clip = clip
                    self.application().view.focus_view('Detail/Clip')
                else:
                    self.canonical_parent.show_message('Clip is to long to Duplicate')

    def duplicate_clip_slot(self, clip_slot):
        if clip_slot.has_clip:
            try:
                track = clip_slot.canonical_parent
                index = list(track.clip_slots).index(clip_slot)
                track.duplicate_clip_slot(index)
                self.canonical_parent.show_message('Duplicate Clip ' + clip_slot.clip.name)
                select_clip_slot(self.song(), track.clip_slots[(index + 1)])
            except Live.Base.LimitationError:
                pass
            except RuntimeError:
                pass

    def in_spec_mode(self):
        return self._ModifierComponent__shift_down or self._ModifierComponent__delete_down or self._ModifierComponent__duplicate_down or self._ModifierComponent__browse_down or self._ModifierComponent__macro_down or self._ModifierComponent__select_down

    def modifier_mask(self):
        return (self._ModifierComponent__shift_down and MASK_SHIFT or 0) | (self._ModifierComponent__browse_down and MASK_BROWSE or 0) | (self._ModifierComponent__delete_down and MASK_CLEAR or 0) | (self._ModifierComponent__duplicate_down and MASK_DUPLICATE or 0) | (self._ModifierComponent__macro_down and MASK_SPEC or 0) | (self._ModifierComponent__select_down and MASK_SELECT or 0)

    def is_select_down(self):
        return self._ModifierComponent__select_down

    def is_browse_down(self):
        return self._ModifierComponent__browse_down

    def is_shift_down(self):
        return self._ModifierComponent__shift_down

    def is_delete_down(self):
        return self._ModifierComponent__delete_down

    def is_duplicate_down(self):
        return self._ModifierComponent__duplicate_down
# okay decompiling scripts/ModifierComponent.pyc
