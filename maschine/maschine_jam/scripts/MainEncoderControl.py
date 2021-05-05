# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/MainEncoderControl.py
# Compiled at: 2021-05-04 10:35:59
# Size of source mod 2**32: 4891 bytes
from .MidiMap import SEL_MODE_ARM, SEL_MODE_SOLO, CLIQ_DESCR, calc_new_parm
ME_MASTER = 0
ME_GROUP = 1
ME_CUE = 2
ME_GRID = 3
ME_TEMPO = 4
ME_NOTE_REPEAT = 5
ME_STEP_LEN = 6
ME_PAT_LEN = 7

class MainEncoderControl:
    _MainEncoderControl__master_button = None
    _MainEncoderControl__group_button = None
    _MainEncoderControl__cue_button = None
    _MainEncoderControl__grid_button = None
    _MainEncoderControl__tempo_button = None
    _MainEncoderControl__solo_button = None
    _MainEncoderControl__mode = ME_MASTER
    _MainEncoderControl__last_mode = ME_MASTER
    _MainEncoderControl__action_map = {}
    _MainEncoderControl__selected_track = None
    _MainEncoderControl__song = None
    _MainEncoderControl__back_action = None
    _MainEncoderControl__back_mode = None

    def __init__(self, jam_mode, master, group, cue, grid, tempo, note_repeat, solo):
        self._MainEncoderControl__song = jam_mode.song()
        self._MainEncoderControl__parent = jam_mode
        self._MainEncoderControl__master_button = master
        self._MainEncoderControl__cue_button = cue
        self._MainEncoderControl__grid_button = grid
        self._MainEncoderControl__group_button = group
        self._MainEncoderControl__tempo_button = tempo
        self._MainEncoderControl__note_repeat_button = note_repeat
        self._MainEncoderControl__solo_button = solo
        self._encoder_action = self._MainEncoderControl__do_master
        self._MainEncoderControl__action_map = {ME_MASTER: self._MainEncoderControl__do_master, ME_TEMPO: self._MainEncoderControl__do_tempo, ME_GRID: self._MainEncoderControl__do_grid, 
         ME_CUE: self._MainEncoderControl__do_cue, ME_GROUP: self._MainEncoderControl__do_group, ME_NOTE_REPEAT: self._MainEncoderControl__do_note_repeat, 
         ME_STEP_LEN: self._MainEncoderControl__do_step_len, ME_PAT_LEN: self._MainEncoderControl__do_pat_len}

    def update_mode(self):
        self._MainEncoderControl__master_button.set_display_value(self._MainEncoderControl__mode == ME_MASTER and 127 or 0, True)
        self._MainEncoderControl__cue_button.set_display_value(self._MainEncoderControl__mode == ME_CUE and 127 or 0, True)
        self._MainEncoderControl__group_button.set_display_value(self._MainEncoderControl__mode == ME_GROUP and 127 or 0, True)
        self._MainEncoderControl__tempo_button.set_display_value(self._MainEncoderControl__mode == ME_TEMPO and 127 or 0, True)
        if self._MainEncoderControl__parent.is_shift_down():
            self._MainEncoderControl__grid_button.set_display_value(self._MainEncoderControl__parent.in_track_mode(SEL_MODE_ARM) and 127 or 0, True)
            self._MainEncoderControl__solo_button.set_display_value(self._MainEncoderControl__mode == ME_PAT_LEN and 127 or 0, True)
        else:
            self._MainEncoderControl__grid_button.set_display_value(self._MainEncoderControl__mode == ME_GRID and 127 or 0, True)
            self._MainEncoderControl__solo_button.set_display_value(self._MainEncoderControl__parent.in_track_mode(SEL_MODE_SOLO) and 127 or 0, True)
        self._encoder_action = self._MainEncoderControl__action_map[self._MainEncoderControl__mode]

    def trigger_mode(self, mode):
        if mode in (ME_PAT_LEN, ME_GRID, ME_TEMPO, ME_NOTE_REPEAT):
            if self._MainEncoderControl__mode == mode:
                self.reset_mode()
            else:
                self._MainEncoderControl__mode = mode
                self.update_mode()
        else:
            self._MainEncoderControl__last_mode = mode
            self._MainEncoderControl__mode = mode
            self.update_mode()

    def update_note_repeat(self, value):
        self._MainEncoderControl__note_repeat_button.set_display_value(value, True)

    def reset_mode(self):
        self._MainEncoderControl__mode = self._MainEncoderControl__last_mode
        self._MainEncoderControl__tempo_button.selected = False
        self._MainEncoderControl__grid_button.selected = False
        self.update_mode()

    def __do_grid(self, value, push_down):
        quant = self._MainEncoderControl__song.clip_trigger_quantization
        self._MainEncoderControl__song.clip_trigger_quantization = max(0, min(13, quant + value))
        self._MainEncoderControl__parent.canonical_parent.show_message('Clip Quantize ' + CLIQ_DESCR[self._MainEncoderControl__song.clip_trigger_quantization])

    def __do_note_repeat(self, value, push_down):
        self._MainEncoderControl__parent.set_nr_value(value, push_down)

    def __do_step_len(self, value, push_down):
        self._MainEncoderControl__parent._step_mode.adjust_step_len(value, push_down)

    def __do_pat_len(self, value, push_down):
        self._MainEncoderControl__parent.change_pattern_length(value, push_down)

    def set_selected_track(self, track):
        self._MainEncoderControl__selected_track = track

    def __do_group(self, value, push_down):
        if self._MainEncoderControl__selected_track:
            delta = push_down and value or value * 8
            self._MainEncoderControl__selected_track.mixer_device.volume.value = calc_new_parm(self._MainEncoderControl__selected_track.mixer_device.volume, delta)

    def __do_cue(self, value, push_down):
        delta = push_down and value or value * 8
        self._MainEncoderControl__song.master_track.mixer_device.cue_volume.value = calc_new_parm(self._MainEncoderControl__song.master_track.mixer_device.cue_volume, delta)

    def __do_master(self, value, push_down):
        delta = push_down and value or value * 8
        self._MainEncoderControl__song.master_track.mixer_device.volume.value = calc_new_parm(self._MainEncoderControl__song.master_track.mixer_device.volume, delta)

    def __do_tempo(self, value, push_down):
        if push_down:
            self._MainEncoderControl__song.tempo = max(20, min(999, self._MainEncoderControl__song.tempo + value * 0.1))
        else:
            self._MainEncoderControl__song.tempo = max(20, min(999, self._MainEncoderControl__song.tempo + value))

    def handle_encoder(self, value, push_down):
        self._encoder_action(value, push_down)

    @property
    def mode(self):
        return self._MainEncoderControl__mode
# okay decompiling src/MainEncoderControl.pyc
