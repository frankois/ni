# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_Studio/JogWheelSection.py
# Compiled at: 2021-04-30 12:12:38
# Size of source mod 2**32: 13939 bytes
import Live
from _Framework.SubjectSlot import subject_slot
RecordingQuantization = Live.Song.RecordingQuantization
from _Framework.ButtonElement import *
from _Framework.SliderElement import *
from _Framework.CompoundComponent import *
from .MIDI_Map import *
from .Maschine import arm_exclusive
from .StateButton import StateButton
PARM_RANGE = 127
SHIFT_INC = 4
QUANT_DESCR = (' No Rec Quantize', ' 1/4 Rec Quantize', ' 1/8 Rec Quantize', ' 1/8 Rec Triplet Quantize',
               '1/8 & 1/8 Triplet Quantize', ' 1/16 Rec Quantize', ' 1/16 Triplet Rec Quantize',
               ' 1/16 & 1/16 Triplet Rec Quantize', '1/32 Rec Quantize')
QUANTIZATION_NAMES = ('1/4', '1/8', '1/8t', '1/8+t', '1/16', '1/16t', '1/16+t', '1/32')
CLIQ_DESCR = ('None', '8 Bars', '4 Bars', '2 Bars', '1 Bar', '1/2', '1/2T', '1/4',
              '1/4T', '1/8', '1/8T', '1/16', '1/16T', '1/32')
TRANSPORT_STEPS = (0.25, 0.5, 4.0, 1.0)

def record_quantization_to_float(quantize):
    return float(list(QUANT_CONST).index(quantize) - 1) / float(len(QUANT_CONST) - 2)


def float_to_record_quantization(quantize):
    return QUANT_CONST[(int(quantize * (len(QUANT_CONST) - 1)) + 1)]


def calc_new_parm(parm, delta):
    parm_range = parm.max - parm.min
    int_val = int((parm.value - parm.min) / parm_range * PARM_RANGE + 0.1)
    inc_val = min(PARM_RANGE, max(0, int_val + delta))
    return float(inc_val) / float(PARM_RANGE) * parm_range + parm.min


def repeat(parm, delta):
    count = 0
    while count < SHIFT_INC:
        parm.value = calc_new_parm(parm, delta)
        count += 1


class JogWheelSection(CompoundComponent):

    def __init__(self, modeselector, editsection, *a, **k):
        (super().__init__)(*a, **k)
        self._modesel = modeselector
        self._editsection = editsection
        is_momentary = True
        self._do_push_button.subject = ButtonElement(is_momentary, MIDI_CC_TYPE, 0, 82)
        self._do_edit_slider.subject = SliderElement(MIDI_CC_TYPE, 1, 81)
        self._do_channel_slider.subject = SliderElement(MIDI_CC_TYPE, 1, 83)
        self._do_channel_button.subject = ButtonElement(is_momentary, MIDI_CC_TYPE, 1, 63)
        self._do_req_quantize.subject = SliderElement(MIDI_CC_TYPE, 1, 100)
        self._do_browse.subject = SliderElement(MIDI_CC_TYPE, 1, 84)
        self._do_tempo.subject = SliderElement(MIDI_CC_TYPE, 1, 101)
        self._do_volume.subject = SliderElement(MIDI_CC_TYPE, 1, 103)
        self._do_dedicated_rec_quantize.subject = SliderElement(MIDI_CC_TYPE, 2, 112)
        self._do_dedicated_clip_quantize.subject = SliderElement(MIDI_CC_TYPE, 2, 113)
        self.set_up_function_buttons()
        self._wheel_overide = None
        self.scrub_mode = True
        self.select_arm_mode = True
        self._push_down = False

    def set_up_function_buttons(self):
        is_momentary = True
        self._do_octave_button.subject = StateButton(is_momentary, MIDI_CC_TYPE, 1, 70)
        self._do_scale_button.subject = StateButton(is_momentary, MIDI_CC_TYPE, 1, 71)
        self._do_note_button.subject = StateButton(is_momentary, MIDI_CC_TYPE, 1, 72)
        self._do_loop_mod.subject = StateButton(is_momentary, MIDI_CC_TYPE, 1, 69)
        self._color_edit_button = ButtonElement(is_momentary, MIDI_CC_TYPE, 3, 114)
        self._do_color_button.subject = self._color_edit_button
        self.scrub_mode_button = StateButton(is_momentary, MIDI_CC_TYPE, 2, 53)
        self._action_scrub_mode.subject = self.scrub_mode_button
        self._action_loop_button.subject = StateButton(is_momentary, MIDI_CC_TYPE, 2, 54)
        self._action_quant_button.subject = StateButton(is_momentary, MIDI_CC_TYPE, 2, 55)

    def set_overide(self, overide_callback):
        self._wheel_overide = overide_callback

    def reset_overide(self):
        self._wheel_overide = None
        if self._editsection.is_color_edit():
            self._color_edit_button.send_value(0, True)
            self._editsection.knob_pad_action(False)
            self._editsection.set_color_edit(False)

    def message(self, message):
        self.canonical_parent.show_message(message)

    def use_scrub_mode(self):
        return self.scrub_mode

    def set_scrub_mode(self, value):
        self.scrub_mode = value
        self.scrub_mode_button.send_value(value and 127 or 0)

    def modifier1(self):
        return self._push_down

    def modifier2(self):
        return self._editsection.isShiftdown()

    def modifier3(self):
        return self._editsection.isAltdown()

    @subject_slot('value')
    def _do_push_button(self, value):
        if value != 0:
            self._push_down = True
        else:
            self._push_down = False
        self._modesel.handle_push(value != 0)

    @subject_slot('value')
    def _action_scrub_mode(self, value):
        if value > 0:
            self.set_scrub_mode(not self.scrub_mode)

    def _action_set_quant(self, diff):
        val = self._editsection.quantize
        self._editsection.quantize = max(1, min(len(QUANT_CONST) - 1, val + diff))
        self.canonical_parent.timed_message(2, 'Quantize: ' + QUANT_STRING[self._editsection.quantize], True)

    def _action_init_loop(self, diff):
        val = self._editsection.initial_clip_len
        self._editsection.initial_clip_len = max(1.0, min(64.0, val + diff))
        self.canonical_parent.timed_message(2, 'Init Clip Len: ' + str(self._editsection.initial_clip_len), True)

    @subject_slot('value')
    def _action_loop_button(self, value):
        if value > 0:
            self.canonical_parent.timed_message(2, 'Init Clip Len: ' + str(self._editsection.initial_clip_len), True)
            self.set_overide(self._action_init_loop)
        else:
            self.canonical_parent.timed_message_release()
            self.reset_overide()

    @subject_slot('value')
    def _action_quant_button(self, value):
        if value > 0:
            self.canonical_parent.timed_message(2, 'Quantize: ' + QUANT_STRING[self._editsection.quantize], True)
            self.set_overide(self._action_set_quant)
        else:
            self.canonical_parent.timed_message_release()
            self.reset_overide()

    def chg_tempo(self, diff):
        self.song().tempo = max(20, min(999, self.song().tempo + diff))
        self.canonical_parent.timed_message(2, 'Tempo: ' + str(round(self.song().tempo, 2)))

    @subject_slot('value')
    def _do_edit_slider(self, value):
        diff = value == 127 and -1 or 1
        if self._wheel_overide:
            self._wheel_overide(diff)
        else:
            self._modesel.navigate(diff, self.modifier1(), self.modifier2())

    @subject_slot('value')
    def _do_channel_slider(self, value):
        if self._wheel_overide:
            self._wheel_overide(value == 127 and -1 or 1)
        else:
            song = self.song()
        if self.modifier1():
            dir = value == 127 and -1 or 1
            scenes = song.scenes
            scene = song.view.selected_scene
            sindex = vindexof(scenes, scene)
            sel_scene = sindex + dir
            if sel_scene >= 0:
                if sel_scene < len(scenes):
                    song.view.selected_scene = scenes[sel_scene]
        else:
            if self.modifier2():
                dir = value == 127 and Live.Application.Application.View.NavDirection.left or Live.Application.Application.View.NavDirection.right
                self.application().view.scroll_view(dir, 'Detail/DeviceChain', True)
            else:
                dir = value == 127 and -1 or 1
                tracks = song.tracks
                direction = value == 127 and Live.Application.Application.View.NavDirection.left or Live.Application.Application.View.NavDirection.right
                self.application().view.scroll_view(direction, 'Session', True)
                if self.select_arm_mode:
                    arm_exclusive(song)

    @subject_slot('value')
    def _do_channel_button(self, value):
        arm_exclusive(self.song())

    @subject_slot('value')
    def _do_browse(self, value):
        diff = value == 127 and -1 or 1
        if self._wheel_overide:
            self._wheel_overide(diff)
        else:
            step = 1.0
            if self.modifier1():
                step = 0.25
            else:
                if self.modifier2():
                    step = 4.0
                elif self.scrub_mode:
                    self.song().scrub_by(step * diff)
                else:
                    self.song().jump_by(step * diff)

    @subject_slot('value')
    def _do_tempo(self, value):
        diff = value == 127 and -1 or 1
        if self._wheel_overide:
            self._wheel_overide(diff)
        else:
            if self.modifier1():
                self.chg_tempo(diff * 0.01)
            else:
                if self.modifier2():
                    self.chg_tempo(diff * 0.1)
                else:
                    self.chg_tempo(diff)

    @subject_slot('value')
    def _do_req_quantize(self, value):
        diff = value == 127 and -1 or 1
        if self._wheel_overide:
            self._wheel_overide(diff)
        else:
            song = self.song()
        if self.modifier2():
            swing = song.swing_amount
            song.swing_amount = max(0.0, min(1, swing + diff * 0.01))
            msg = 'Swing Amount: ' + str(int(song.swing_amount * 100)) + '%'
            self.message(msg)
            self.canonical_parent.timed_message(2, msg)
        else:
            if self.modifier1():
                quant = song.clip_trigger_quantization
                song.clip_trigger_quantization = max(0, min(13, quant + diff))
                self.message('Clip Quantize ' + CLIQ_DESCR[song.clip_trigger_quantization])
                self.canonical_parent.timed_message(2, 'Clip Quantize: ' + CLIQ_DESCR[song.clip_trigger_quantization])
            else:
                rec_quant = song.midi_recording_quantization
                index = QUANT_CONST.index(rec_quant) + diff
                if index >= 0:
                    if index < len(QUANT_CONST):
                        song.midi_recording_quantization = QUANT_CONST[index]
                        self.message(QUANT_DESCR[index])
                        self.canonical_parent.timed_message(2, 'Rec Quantize: ' + QUANT_STRING[index])

    @subject_slot('value')
    def _do_dedicated_clip_quantize(self, value):
        diff = value == REL_KNOB_DOWN and -1 or 1
        song = self.song()
        quant = song.clip_trigger_quantization
        song.clip_trigger_quantization = max(0, min(13, quant + diff))
        self.message('Clip Quantize ' + CLIQ_DESCR[song.clip_trigger_quantization])
        self.canonical_parent.timed_message(2, 'Clip Quantize: ' + CLIQ_DESCR[song.clip_trigger_quantization])

    @subject_slot('value')
    def _do_dedicated_rec_quantize(self, value):
        diff = value == REL_KNOB_DOWN and -1 or 1
        song = self.song()
        rec_quant = song.midi_recording_quantization
        index = QUANT_CONST.index(rec_quant) + diff
        if index >= 0:
            if index < len(QUANT_CONST):
                song.midi_recording_quantization = QUANT_CONST[index]
                self.message(QUANT_DESCR[index])
                self.canonical_parent.timed_message(2, 'Rec Quantize: ' + QUANT_STRING[index])

    @subject_slot('value')
    def _do_volume(self, value):
        diff = value == 127 and -1 or 1
        if self._wheel_overide:
            self._wheel_overide(diff)
        else:
            if self.modifier2():
                self.chg_cue(diff)
            else:
                self.chg_volume(diff)

    @subject_slot('value')
    def _do_color_button(self, value):
        if value > 0:
            if self._editsection.is_color_edit():
                self.reset_overide()
            else:
                self._color_edit_button.send_value(1, True)
                self._editsection.knob_pad_action(True)
                self._editsection.set_color_edit(True)

    def set_color_edit(self, active):
        if active:
            self.set_overide(self._color_change)
        else:
            self.reset_overide()

    def _color_change(self, value):
        diff = value == 127 and -1 or 1
        self._editsection.edit_colors(diff)

    @subject_slot('value')
    def _do_note_button(self, value):
        if not value in range(128):
            raise AssertionError
        elif value > 0:
            self.set_overide(self.canonical_parent._handle_base_note)
        else:
            self.reset_overide()

    @subject_slot('value')
    def _do_octave_button(self, value):
        if not value in range(128):
            raise AssertionError
        elif value > 0:
            self.set_overide(self.canonical_parent._handle_octave)
        else:
            self.reset_overide()

    @subject_slot('value')
    def _do_scale_button(self, value):
        if not value in range(128):
            raise AssertionError
        elif value > 0:
            self.set_overide(self.canonical_parent._handle_scale)
        else:
            self.reset_overide()

    def _handle_loop_mod(self, diff):
        factor = (self.modifier1() and 1.0 or 4.0) * diff
        if self.modifier2():
            self.canonical_parent.adjust_loop_length(factor)
        else:
            self.canonical_parent.adjust_loop_start(factor)

    @subject_slot('value')
    def _do_loop_mod(self, value):
        if not value in range(128):
            raise AssertionError
        elif value > 0:
            self.set_overide(self._handle_loop_mod)
        else:
            self.reset_overide()

    def chg_volume(self, diff):
        mdevice = self.song().master_track.mixer_device
        if self.modifier2():
            mdevice.volume.value = calc_new_parm(mdevice.volume, diff)
        else:
            repeat(mdevice.volume, diff)

    def chg_cue(self, diff):
        mdevice = self.song().master_track.mixer_device
        if self.modifier2():
            mdevice.cue_volume.value = calc_new_parm(mdevice.cue_volume, diff)
        else:
            repeat(mdevice.cue_volume, diff)

    def update(self):
        pass

    def refresh(self):
        pass

    def disconnect(self):
        super().disconnect()
# okay decompiling src/JogWheelSection.pyc
