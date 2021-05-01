# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_Mikro_Mk2/EditSection.py
# Compiled at: 2021-04-30 12:09:45
# Size of source mod 2**32: 25948 bytes
Instruction context:
   
 L. 299       444  LOAD_GLOBAL              arm_exclusive
               446_0  COME_FROM            42  '42'
->               446  LOAD_FAST                'self'
                 448  LOAD_METHOD              song
                 450  CALL_METHOD_0         0  '0 positional arguments'
                 452  CALL_FUNCTION_1       1  '1 positional argument'
                 454  POP_TOP          
               456_0  COME_FROM           440  '440'
               456_1  COME_FROM           418  '418'
               456_2  COME_FROM           408  '408'
               456_3  COME_FROM           382  '382'
               456_4  COME_FROM           340  '340'
               456_5  COME_FROM           296  '296'
               456_6  COME_FROM           168  '168'
               456_7  COME_FROM           126  '126'
               456_8  COME_FROM            78  '78'
               456_9  COME_FROM            66  '66'
import Live
from _Framework.SubjectSlot import subject_slot
import _Framework.CompoundComponent as CompoundComponent
import _Framework.ButtonElement as ButtonElement
from _Framework.InputControlElement import *
import time
from .StateButton import StateButton
from .MIDI_Map import *
import _Framework.SliderElement as SliderElement
ES_NONE = 0
ES_DUPLICATE = 1
ES_NEW = 2
ES_DOUBLE = 3
ES_CLEAR = 4
ES_QUANT = 5
ES_NUDGE = 6
ES_NAVIGATE = 7
ES_KNOB = 8

def select_clip_slot(song, slot):
    if slot:
        song.view.highlighted_clip_slot = slot


def is_clicked(downtime):
    clicktime = int(round(time.time() * 1000)) - downtime
    if clicktime < 500:
        return True
    return False


class EditSection(CompoundComponent):

    def __init__(self, *a, **k):
        (super(EditSection, self).__init__)(*a, **k)
        is_momentary = True
        self.mikro_shift_button = ButtonElement(is_momentary, MIDI_CC_TYPE, 2, 80)
        self._do_shift_mikro.subject = self.mikro_shift_button
        self.shift_button = ButtonElement(is_momentary, MIDI_CC_TYPE, 1, 80)
        self._do_shift.subject = self.shift_button
        self.alt_button = ButtonElement(is_momentary, MIDI_CC_TYPE, 1, 82)
        self._do_alt.subject = self.alt_button
        self.mikro_shift = False
        self.shiftdown = False
        self.altdown = False
        self.edit_state = ES_NONE
        self._down_button = None
        self._action_set_quant.subject = SliderElement(MIDI_CC_TYPE, 2, 110)
        self._action_init_loop.subject = SliderElement(MIDI_CC_TYPE, 2, 111)
        self._nav_button = StateButton(is_momentary, MIDI_CC_TYPE, 0, 115)
        self._action_navigate.subject = self._nav_button
        self._copy_button = StateButton(is_momentary, MIDI_CC_TYPE, 0, 95)
        self._action_duplicate.subject = self._copy_button
        self._quantize_button = StateButton(is_momentary, MIDI_CC_TYPE, 0, 97)
        self._action_quantize.subject = self._quantize_button
        self._paste_button = StateButton(is_momentary, MIDI_CC_TYPE, 0, 96)
        self._action_new.subject = self._paste_button
        self._note_button = StateButton(is_momentary, MIDI_CC_TYPE, 0, 101)
        self._action_note.subject = self._note_button
        self._clear_button = StateButton(is_momentary, MIDI_CC_TYPE, 0, 103)
        self._action_clear.subject = self._clear_button
        self._nudge_button = StateButton(is_momentary, MIDI_CC_TYPE, 0, 100)
        self._action_nudge_button.subject = self._nudge_button
        self.action_time = False
        self.pad_action = False
        self.pad_wheel_action = False
        self.quantize = 5
        self.quantize_amount = 1.0
        self.initial_clip_len = 4.0
        self._focused_clip = None
        self._focused_c_index = None
        self._color_edit = False
        self.nav_index = 0

    def disconnect(self):
        super(EditSection, self).disconnect()

    def init(self):
        self._color_edit_button.send_value(0, True)

    def set_color_edit(self, val):
        self._color_edit = val

    def is_color_edit(self):
        return self._color_edit

    def connect_session(self, session):
        for sindex in range(session.height()):
            scene = session.scene(sindex)
            for cindex in range(session.width()):
                clip = scene.clip_slot(cindex)
                clip.set_modifier(self)

    def set_mode_selector(self, mode_selector):
        self._mode_selector = mode_selector
        self._mode_selector.assign_edit_section(self)

    @subject_slot('value')
    def _do_shift_mikro(self, value):
        self.mikro_shift = value != 0
        self.shiftdown = value != 0
        if self._mode_selector:
            self._mode_selector.set_shift_state(self.mikro_shift)

    @subject_slot('value')
    def _do_shift(self, value):
        self.shiftdown = value != 0

    @subject_slot('value')
    def _do_alt(self, value):
        self.altdown = value != 0

    def modifiers(self):
        return (self.shiftdown and 1) | (self.altdown and 1) << 1

    def isShiftdown(self):
        return self.shiftdown

    def isAltdown(self):
        return self.altdown

    def isClipAltDown(self):
        return self.altdown or self._mode_selector.isClipDown()

    def hasModification(self, mode):
        if mode == SCENE_MODE:
            return self.edit_state != ES_NONE
        if mode == CLIP_MODE:
            if self.edit_state != ES_NONE:
                return True
            if self._color_edit:
                return True
        return False

    def update(self):
        pass

    def _get_current_slot(self, song):
        scene = song.view.selected_scene
        track = song.view.selected_track
        clip_slot = song.view.highlighted_clip_slot
        scenes = song.scenes
        tracks = song.tracks
        sindex = vindexof(scenes, scene)
        tindex = vindexof(tracks, track)
        return (clip_slot, track, scenes, tindex, sindex)

    def do_message(self, msg, statusbarmsg=None):
        if statusbarmsg == None:
            self.canonical_parent.show_message(msg)
        else:
            self.canonical_parent.show_message(statusbarmsg)
        self.canonical_parent.timed_message(2, msg)

    def edit_note(self, note_value):
        self.pad_action = True
        if self.edit_state == ES_CLEAR:
            cs = self.song().view.highlighted_clip_slot
            if cs:
                if cs.has_clip:
                    if cs.clip.is_midi_clip:
                        if self.shiftdown:
                            cs.clip.remove_notes_extended(0, 127, 0.0, cs.clip.length)
                        else:
                            cs.clip.remove_notes_extended(note_value, 1, 0.0, cs.clip.length)

    def edit_scene_slot(self, scene, index):
        self.pad_action = True
        if scene != None:
            song = self.song()
            if self.edit_state == ES_DUPLICATE:
                self.do_message('Duplicate Scene ' + str(scene.name))
                song.duplicate_scene(index)
            else:
                if self.edit_state == ES_NEW:
                    idx = 1
                    if self.shiftdown:
                        idx = 0
                    song.create_scene(index + idx)
                    self.do_message('Create Scene ' + str(self.song().view.selected_scene.name))
                else:
                    if self.edit_state == ES_CLEAR:
                        self.do_message('Delete Scene ' + str(scene.name))
                        song.delete_scene(index)
                    else:
                        if self.edit_state == ES_DOUBLE:
                            song.capture_and_insert_scene()
                            scene = self.song().view.selected_scene
                            self.do_message('Capture to ' + scene.name)
                        else:
                            if self.edit_state == ES_NUDGE:
                                self.clear_auto_scene(scene, index)
                                self.do_message('Clr Env in Scene ' + scene.name)
                            else:
                                if self.edit_state == ES_QUANT:
                                    pass
                                elif self.edit_state == ES_NAVIGATE:
                                    self.song().view.selected_scene = scene

    def duplciate_clip_slot(self, clip_slot):
        if clip_slot.has_clip:
            try:
                track = clip_slot.canonical_parent
                index = list(track.clip_slots).index(clip_slot)
                track.duplicate_clip_slot(index)
                self.do_message('Duplicate Clip ' + clip_slot.clip.name)
                select_clip_slot(self.song(), track.clip_slots[(index + 1)])
            except Live.Base.LimitationError:
                pass
            except RuntimeError:
                pass

    @subject_slot('value')
    def _action_set_quant(self, value):
        self.mod_quant_size(value == REL_KNOB_DOWN and -1 or 1)

    @subject_slot('value')
    def _action_init_loop(self, value):
        self.mod_new_initlen(value == REL_KNOB_DOWN and -1 or 1)

    def mod_new_initlen(self, diff):
        if abs(diff) == 4:
            newval = self.initial_clip_len + diff
            newval = int(newval / 4) * 4
            self.initial_clip_len = max(4.0, min(64.0, newval))
        else:
            self.initial_clip_len = max(1.0, min(64.0, self.initial_clip_len + diff))
        self.canonical_parent.timed_message(2, 'Init Clip Len: ' + str(int(self.initial_clip_len)) + ' Beats', True)
        self.canonical_parent.show_message('Initial Clip Length : ' + str(int(self.initial_clip_len)) + ' beats')

    def mod_quant_size(self, diff):
        self.quantize = max(1, min(len(QUANT_CONST) - 1, self.quantize + diff))
        self.canonical_parent.timed_message(2, 'Quantize: ' + QUANT_STRING[self.quantize], True)
        self.canonical_parent.show_message('Quantize set to : ' + QUANT_STRING[self.quantize])

    def knob_pad_action(self, activate):
        if activate:
            self.pad_wheel_action = True
            self.edit_state = ES_KNOB
            self._focused_clip = None
        else:
            self.pad_wheel_action = False
            self.edit_state = ES_NONE
            self._focused_clip = None

    def edit_colors(self, diff, jump_selection=False):
        pass

    def edit_clip_slot--- This code section failed: ---

 L. 250         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _color_edit
                4  POP_JUMP_IF_FALSE    54  'to 54'

 L. 251         6  LOAD_FAST                'value'
                8  LOAD_CONST               0
               10  COMPARE_OP               !=
               12  POP_JUMP_IF_FALSE    44  'to 44'

 L. 252        14  LOAD_FAST                'clipslot_component'
               16  LOAD_ATTR                _clip_slot
               18  LOAD_CONST               None
               20  COMPARE_OP               !=
               22  POP_JUMP_IF_FALSE    50  'to 50'

 L. 253        24  LOAD_FAST                'clipslot_component'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _focused_clip

 L. 254        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _mode_selector
               34  LOAD_METHOD              pick_color
               36  LOAD_FAST                'clipslot_component'
               38  CALL_METHOD_1         1  '1 positional argument'
               40  POP_TOP          
               42  JUMP_FORWARD        456  'to 456'
             44_0  COME_FROM            12  '12'

 L. 256        44  LOAD_CONST               None
               46  LOAD_FAST                'self'
               48  STORE_ATTR               _focused_clip
             50_0  COME_FROM            22  '22'
            50_52  JUMP_FORWARD        456  'to 456'
             54_0  COME_FROM             4  '4'

 L. 258        54  LOAD_CONST               True
               56  LOAD_FAST                'self'
               58  STORE_ATTR               pad_action

 L. 259        60  LOAD_FAST                'value'
               62  LOAD_CONST               0
               64  COMPARE_OP               !=
            66_68  POP_JUMP_IF_FALSE   456  'to 456'
               70  LOAD_FAST                'clipslot_component'
               72  LOAD_ATTR                _clip_slot
               74  LOAD_CONST               None
               76  COMPARE_OP               !=
            78_80  POP_JUMP_IF_FALSE   456  'to 456'

 L. 260        82  LOAD_FAST                'clipslot_component'
               84  LOAD_ATTR                _clip_slot
               86  STORE_FAST               'clip_slot'

 L. 261        88  LOAD_FAST                'self'
               90  LOAD_ATTR                edit_state
               92  LOAD_GLOBAL              ES_DUPLICATE
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   130  'to 130'

 L. 262        98  LOAD_FAST                'self'
              100  LOAD_ATTR                shiftdown
              102  POP_JUMP_IF_FALSE   116  'to 116'

 L. 263       104  LOAD_FAST                'self'
              106  LOAD_METHOD              duplicate_track_cs
              108  LOAD_FAST                'clip_slot'
              110  CALL_METHOD_1         1  '1 positional argument'
              112  POP_TOP          
              114  JUMP_FORWARD        456  'to 456'
            116_0  COME_FROM           102  '102'

 L. 265       116  LOAD_FAST                'self'
              118  LOAD_METHOD              duplciate_clip_slot
              120  LOAD_FAST                'clip_slot'
              122  CALL_METHOD_1         1  '1 positional argument'
              124  POP_TOP          
          126_128  JUMP_FORWARD        456  'to 456'
            130_0  COME_FROM            96  '96'

 L. 266       130  LOAD_FAST                'self'
              132  LOAD_ATTR                edit_state
              134  LOAD_GLOBAL              ES_NEW
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE   172  'to 172'

 L. 267       140  LOAD_FAST                'self'
              142  LOAD_ATTR                shiftdown
              144  POP_JUMP_IF_FALSE   158  'to 158'

 L. 268       146  LOAD_FAST                'self'
              148  LOAD_METHOD              create_new_midi_track
              150  LOAD_FAST                'clip_slot'
              152  CALL_METHOD_1         1  '1 positional argument'
              154  POP_TOP          
              156  JUMP_FORWARD        456  'to 456'
            158_0  COME_FROM           144  '144'

 L. 270       158  LOAD_FAST                'self'
              160  LOAD_METHOD              create_new_clip
              162  LOAD_FAST                'clip_slot'
              164  CALL_METHOD_1         1  '1 positional argument'
              166  POP_TOP          
          168_170  JUMP_FORWARD        456  'to 456'
            172_0  COME_FROM           138  '138'

 L. 271       172  LOAD_FAST                'self'
              174  LOAD_ATTR                edit_state
              176  LOAD_GLOBAL              ES_CLEAR
              178  COMPARE_OP               ==
          180_182  POP_JUMP_IF_FALSE   298  'to 298'

 L. 272       184  LOAD_FAST                'self'
              186  LOAD_ATTR                altdown
              188  POP_JUMP_IF_FALSE   242  'to 242'

 L. 273       190  LOAD_FAST                'clip_slot'
              192  LOAD_ATTR                clip
              194  LOAD_CONST               None
              196  COMPARE_OP               !=
              198  POP_JUMP_IF_FALSE   240  'to 240'

 L. 274       200  LOAD_FAST                'clip_slot'
              202  LOAD_ATTR                clip
              204  STORE_FAST               'clip'

 L. 275       206  LOAD_FAST                'clip'
              208  LOAD_ATTR                is_midi_clip
              210  POP_JUMP_IF_FALSE   240  'to 240'

 L. 276       212  LOAD_FAST                'self'
              214  LOAD_METHOD              do_message
              216  LOAD_STR                 'Clear all Notes in Clip'
              218  CALL_METHOD_1         1  '1 positional argument'
              220  POP_TOP          

 L. 277       222  LOAD_FAST                'clip'
              224  LOAD_METHOD              remove_notes_extended
              226  LOAD_CONST               0
              228  LOAD_CONST               127
              230  LOAD_CONST               0.0
              232  LOAD_FAST                'clip'
              234  LOAD_ATTR                length
              236  CALL_METHOD_4         4  '4 positional arguments'
              238  POP_TOP          
            240_0  COME_FROM           210  '210'
            240_1  COME_FROM           198  '198'
              240  JUMP_FORWARD        296  'to 296'
            242_0  COME_FROM           188  '188'

 L. 278       242  LOAD_FAST                'self'
              244  LOAD_ATTR                shiftdown
          246_248  POP_JUMP_IF_FALSE   262  'to 262'

 L. 279       250  LOAD_FAST                'self'
              252  LOAD_METHOD              delete_track_cs
              254  LOAD_FAST                'clip_slot'
              256  CALL_METHOD_1         1  '1 positional argument'
              258  POP_TOP          
              260  JUMP_FORWARD        296  'to 296'
            262_0  COME_FROM           246  '246'

 L. 281       262  LOAD_FAST                'clip_slot'
              264  LOAD_ATTR                clip
          266_268  POP_JUMP_IF_FALSE   288  'to 288'

 L. 282       270  LOAD_FAST                'self'
              272  LOAD_METHOD              do_message
              274  LOAD_STR                 'Delete Clip '
              276  LOAD_FAST                'clip_slot'
              278  LOAD_ATTR                clip
              280  LOAD_ATTR                name
              282  BINARY_ADD       
              284  CALL_METHOD_1         1  '1 positional argument'
              286  POP_TOP          
            288_0  COME_FROM           266  '266'

 L. 283       288  LOAD_FAST                'clipslot_component'
              290  LOAD_METHOD              _do_delete_clip
              292  CALL_METHOD_0         0  '0 positional arguments'
              294  POP_TOP          
            296_0  COME_FROM           260  '260'
            296_1  COME_FROM           240  '240'
              296  JUMP_FORWARD        456  'to 456'
            298_0  COME_FROM           180  '180'

 L. 284       298  LOAD_FAST                'self'
              300  LOAD_ATTR                edit_state
              302  LOAD_GLOBAL              ES_DOUBLE
              304  COMPARE_OP               ==
          306_308  POP_JUMP_IF_FALSE   342  'to 342'

 L. 285       310  LOAD_FAST                'self'
              312  LOAD_ATTR                shiftdown
          314_316  POP_JUMP_IF_FALSE   330  'to 330'

 L. 286       318  LOAD_FAST                'self'
              320  LOAD_METHOD              create_new_audio_track
              322  LOAD_FAST                'clip_slot'
              324  CALL_METHOD_1         1  '1 positional argument'
              326  POP_TOP          
              328  JUMP_FORWARD        340  'to 340'
            330_0  COME_FROM           314  '314'

 L. 288       330  LOAD_FAST                'self'
              332  LOAD_METHOD              double_clipslot
              334  LOAD_FAST                'clip_slot'
              336  CALL_METHOD_1         1  '1 positional argument'
              338  POP_TOP          
            340_0  COME_FROM           328  '328'
              340  JUMP_FORWARD        456  'to 456'
            342_0  COME_FROM           306  '306'

 L. 289       342  LOAD_FAST                'self'
              344  LOAD_ATTR                edit_state
              346  LOAD_GLOBAL              ES_NUDGE
              348  COMPARE_OP               ==
          350_352  POP_JUMP_IF_FALSE   384  'to 384'

 L. 290       354  LOAD_FAST                'self'
              356  LOAD_ATTR                shiftdown
          358_360  POP_JUMP_IF_FALSE   372  'to 372'

 L. 291       362  LOAD_FAST                'self'
              364  LOAD_METHOD              _new_return_track
              366  CALL_METHOD_0         0  '0 positional arguments'
              368  POP_TOP          
              370  JUMP_FORWARD        382  'to 382'
            372_0  COME_FROM           358  '358'

 L. 293       372  LOAD_FAST                'self'
              374  LOAD_METHOD              clear_automation
              376  LOAD_FAST                'clip_slot'
              378  CALL_METHOD_1         1  '1 positional argument'
              380  POP_TOP          
            382_0  COME_FROM           370  '370'
              382  JUMP_FORWARD        456  'to 456'
            384_0  COME_FROM           350  '350'

 L. 294       384  LOAD_FAST                'self'
              386  LOAD_ATTR                edit_state
              388  LOAD_GLOBAL              ES_QUANT
              390  COMPARE_OP               ==
          392_394  POP_JUMP_IF_FALSE   410  'to 410'

 L. 295       396  LOAD_FAST                'self'
              398  LOAD_METHOD              quantize_clisplot
              400  LOAD_FAST                'clipslot_component'
              402  LOAD_ATTR                _clip_slot
              404  CALL_METHOD_1         1  '1 positional argument'
              406  POP_TOP          
              408  JUMP_FORWARD        456  'to 456'
            410_0  COME_FROM           392  '392'

 L. 296       410  LOAD_FAST                'self'
              412  LOAD_ATTR                edit_state
              414  LOAD_GLOBAL              ES_NAVIGATE
              416  COMPARE_OP               ==
          418_420  POP_JUMP_IF_FALSE   456  'to 456'

 L. 297       422  LOAD_FAST                'clipslot_component'
              424  LOAD_METHOD              _do_select_clip
              426  LOAD_FAST                'clipslot_component'
              428  LOAD_ATTR                _clip_slot
              430  CALL_METHOD_1         1  '1 positional argument'
              432  POP_TOP          

 L. 298       434  LOAD_FAST                'self'
              436  LOAD_ATTR                canonical_parent
              438  LOAD_ATTR                arm_selected_track
          440_442  POP_JUMP_IF_FALSE   456  'to 456'

 L. 299       444  LOAD_GLOBAL              arm_exclusive
            446_0  COME_FROM            42  '42'
              446  LOAD_FAST                'self'
              448  LOAD_METHOD              song
              450  CALL_METHOD_0         0  '0 positional arguments'
              452  CALL_FUNCTION_1       1  '1 positional argument'
              454  POP_TOP          
            456_0  COME_FROM           440  '440'
            456_1  COME_FROM           418  '418'
            456_2  COME_FROM           408  '408'
            456_3  COME_FROM           382  '382'
            456_4  COME_FROM           340  '340'
            456_5  COME_FROM           296  '296'
            456_6  COME_FROM           168  '168'
            456_7  COME_FROM           126  '126'
            456_8  COME_FROM            78  '78'
            456_9  COME_FROM            66  '66'
           456_10  COME_FROM            50  '50'

Parse error at or near `LOAD_FAST' instruction at offset 446

    def _new_return_track(self):
        song = self.song()
        song.create_return_track()
        self.do_message('New Return Track')

    def _new_scene(self):
        song = self.song()
        scene = song.view.selected_scene
        sindex = vindexof(song.scenes, scene)
        sindex = sindex >= 0 and sindex or 0
        song.create_scene(sindex + 1)
        new_scene = song.view.selected_scene
        self.do_message('New Scene ' + new_scene.name)

    def _new_audio_track(self):
        song = self.song()
        track = song.view.selected_track
        tindex = 0
        if not track.can_be_armed:
            tindex = len(song.tracks) - 1
        else:
            tindex = vindexof(song.tracks, track)
        tindex = tindex >= 0 and tindex or 0
        song.create_audio_track(tindex + 1)
        track = song.view.selected_track
        self.do_message('New Audio Track ' + track.name)

    def _new_midi_track(self):
        song = self.song()
        track = song.view.selected_track
        tindex = 0
        if not track.can_be_armed:
            tindex = len(song.tracks) - 1
        else:
            tindex = vindexof(song.tracks, track)
        tindex = tindex >= 0 and tindex or 0
        song.create_midi_track(tindex + 1)
        track = song.view.selected_track
        self.do_message('New MIDI Track ' + track.name)

    def _new_midi_clip(self):
        song = self.song()
        if song.view.selected_track.has_midi_input:
            clip_slot = song.view.highlighted_clip_slot
            if clip_slot != None:
                if not clip_slot.has_clip:
                    clip_slot.create_clip(self.initial_clip_len)
                    song.view.detail_clip = clip_slot.clip
                    self.do_message('New MIDI Clip ' + clip_slot.clip.name)
                    self.application().view.show_view('Detail')

    def quantize_scene(self, scene, index, fiftyPerc):
        tracks = self.song().tracks
        for track in tracks:
            clipslots = track.clip_slots
            if len(clipslots) >= index and clipslots[index].clip is not None:
                clipslots[index].clip.quantize(QUANT_CONST[self.quantize], self.shiftdown and 0.5 or 1.0)

    def clear_auto_scene(self, scene, index):
        tracks = self.song().tracks
        for track in tracks:
            clipslots = track.clip_slots
            if len(clipslots) >= index and clipslots[index].clip != None:
                clipslots[index].clip.clear_all_envelopes()

    def _capture_new_scene(self):
        self.song().capture_and_insert_scene()
        scene = self.song().view.selected_scene
        self.do_message('Capture to ' + scene.name)

    def _duplicate_selected_scene(self):
        song = self.song()
        scene = song.view.selected_scene
        sindex = vindexof(song.scenes, scene)
        if scene:
            if sindex >= 0:
                self.do_message('Duplicate Scene ' + scene.name)
                song.duplicate_scene(sindex)

    def _duplicate_selected_track(self):
        song = self.song()
        track = song.view.selected_track
        t_index = track_index(song, track)
        if track:
            if t_index:
                if t_index[1] == TYPE_TRACK_SESSION:
                    tindex = t_index[0]
                    self.do_message('Dupl. Track ' + track.name, 'Duplicate Track ' + track.name)
                    song.duplicate_track(tindex)

    def _duplicate_selected_clip(self):
        song = self.song()
        clip_slot, track, scenes, tindex, sindex = self._get_current_slot(song)
        if clip_slot != None:
            if clip_slot.clip != None:
                self.do_message('Duplicate ' + clip_slot.clip.name, 'Duplicate Clip ' + clip_slot.clip.name)
                track.duplicate_clip_slot(sindex)
                index = sindex + 1
                if index >= 0:
                    if index < len(scenes):
                        song.view.selected_scene = scenes[index]

    def duplicate_track_cs(self, clip_slot):
        if clip_slot != None:
            song = self.song()
            track = clip_slot.canonical_parent
            t_index = track_index(song, track)
            if track:
                if t_index:
                    if t_index[1] == TYPE_TRACK_SESSION:
                        tindex = t_index[0]
                        self.do_message('Duplicate Track ' + track.name)
                        song.duplicate_track(tindex)

    def clear_automation(self, clip_slot):
        song = self.song()
        if clip_slot != None:
            if clip_slot.clip != None:
                self.do_message('Clr.Env. ' + clip_slot.clip.name, 'Clear Envelopes ' + clip_slot.clip.name)
                clip_slot.clip.clear_all_envelopes()

    def quantize_clisplot(self, clip_slot):
        if clip_slot.clip is not None:
            self.do_message('Quantize Clip: ' + clip_slot.clip.name + (self.shiftdown and ' 50%' or ''))
            clip_slot.clip.quantize(QUANT_CONST[self.quantize], self.shiftdown and 0.5 or 1.0)
            self.song().view.detail_clip = clip_slot.clip
            self.canonical_parent.focus_clip_detail()

    def double_clipslot(self, clip_slot):
        song = self.song()
        track = clip_slot.canonical_parent
        if clip_slot.clip is not None:
            if track.has_midi_input:
                clip = clip_slot.clip
                if clip.length <= 2048.0:
                    clip.duplicate_loop()
                    self.do_message('Dupl. Lp: ' + str(int(clip.length / 4)) + ' Bars')
                    song.view.detail_clip = clip
                    self.canonical_parent.focus_clip_detail()
                else:
                    self.do_message('Clip is to long to Duplicate')

    def create_new_clip(self, clip_slot):
        song = self.song()
        track = clip_slot.canonical_parent
        if clip_slot.clip == None:
            if track.has_midi_input:
                clip_slot.create_clip(self.initial_clip_len)
                song.view.detail_clip = clip_slot.clip
                select_clip_slot(song, clip_slot)
                self.canonical_parent.focus_clip_detail()
                self.do_message('New Midi Clip ' + song.view.highlighted_clip_slot.clip.name)

    def create_new_midi_track(self, clip_slot):
        if clip_slot != None:
            song = self.song()
            track = clip_slot.canonical_parent
            tindex = vindexof(song.tracks, track)
            tindex = tindex >= 0 and tindex or 0
            song.create_midi_track(tindex + 1)
            track = song.view.selected_track
            self.do_message('New Midi Track ' + track.name)

    def create_new_audio_track(self, clip_slot):
        if clip_slot != None:
            song = self.song()
            track = clip_slot.canonical_parent
            tindex = vindexof(song.tracks, track)
            tindex = tindex >= 0 and tindex or 0
            song.create_audio_track(tindex + 1)
            track = song.view.selected_track
            self.do_message('New Audio Track ' + track.name)

    def delete_track_cs(self, clip_slot):
        if clip_slot != None:
            song = self.song()
            track = clip_slot.canonical_parent
            t_index = track_index(song, track)
            if track:
                if len(song.tracks) > 1:
                    if t_index:
                        if t_index[1] == TYPE_TRACK_SESSION:
                            self.do_message('Delete Track ' + track.name)
                            song.delete_track(t_index[0])

    def _double_selected_clip(self):
        song = self.song()
        clip_slot = song.view.highlighted_clip_slot
        if clip_slot is not None:
            if clip_slot.clip is not None:
                if song.view.selected_track.has_midi_input:
                    clip = clip_slot.clip
                    if clip.length <= 2048.0:
                        clip_slot.clip.duplicate_loop()
                        self.do_message('Dupl. Lp ' + str(int(clip_slot.clip.length / 4)) + ' Bars')
                        song.view.detail_clip = clip_slot.clip
                        self.canonical_parent.focus_clip_detail()
                    else:
                        self.do_message('Clip is to long to Duplicate')

    def _clear_events(self):
        song = self.song()
        clip_slot = song.view.highlighted_clip_slot
        if clip_slot != None:
            if clip_slot.clip != None:
                self.do_message('Clr.Env. ' + clip_slot.clip.name, 'Clear Envelopes ' + clip_slot.clip.name)
                clip_slot.clip.clear_all_envelopes()

    def _delete_current_clip(self):
        song = self.song()
        clip_slot = song.view.highlighted_clip_slot
        if clip_slot != None:
            if clip_slot.clip != None:
                self.do_message('Delete Clip ' + clip_slot.clip.name)
                clip_slot.delete_clip()

    def _delete_selected_track(self):
        song = self.song()
        track = song.view.selected_track
        t_index = track_index(song, track)
        if track:
            if len(song.tracks) > 1:
                if t_index:
                    if t_index[1] == TYPE_TRACK_SESSION:
                        self.do_message('Delete Track ' + track.name)
                        song.delete_track(t_index[0])

    def _delete_selected_scene(self):
        song = self.song()
        scene = song.view.selected_scene
        sindex = vindexof(song.scenes, scene)
        if scene:
            if len(song.scenes) > 1:
                if sindex >= 0:
                    self.do_message('Delete Scene ' + scene.name)
                    song.delete_scene(sindex)

    def _click_duplicate(self):
        modifiers = self.modifiers()
        if modifiers == 0:
            self._duplicate_selected_clip()
        else:
            if modifiers == 1:
                self._duplicate_selected_track()
            else:
                if modifiers == 2:
                    self._duplicate_selected_scene()

    def _click_new(self):
        modifiers = self.modifiers()
        if modifiers == 0:
            self._new_midi_clip()
        else:
            if modifiers == 1:
                self._new_midi_track()
            else:
                if modifiers == 2:
                    self._new_scene()

    def _click_double(self):
        modifiers = self.modifiers()
        if modifiers == 0:
            self._double_selected_clip()
        else:
            if modifiers == 1:
                self._new_audio_track()
            else:
                if modifiers == 2:
                    self._capture_new_scene()

    def _click_clear(self):
        modifiers = self.modifiers()
        if modifiers == 0:
            self._delete_current_clip()
        else:
            if modifiers == 1:
                self._delete_selected_track()
            else:
                if modifiers == 2:
                    self._delete_selected_scene()

    def _click_quantize(self):
        song = self.song()
        clip_slot = song.view.highlighted_clip_slot
        if clip_slot != None:
            self.quantize_clisplot(clip_slot)

    def _click_nudge(self):
        modifiers = self.modifiers()
        if modifiers == 0:
            self._clear_events()
        else:
            if modifiers == 1:
                self._new_return_track()
            else:
                if modifiers == 2:
                    pass

    def _select(self, button):
        if self._down_button:
            self._down_button.turn_off()
        button.turn_on()
        self._down_button = button
        self.action_time = int(round(time.time() * 1000))

    def _deselect(self, button):
        if button == self._clear_button:
            self._mode_selector.exit_clear_state()
        if self._down_button == button:
            self._down_button.turn_off()
            self._down_button = None
            prev_state = self.edit_state
            self.edit_state = ES_NONE
            modeid = self._mode_selector.mode().get_mode_id()
            if self.pad_action:
                self.pad_action = False
                return False
            else:
                if modeid == CLIP_MODE or modeid == SCENE_MODE:
                    return False
                if modeid == PAD_MODE or modeid == CONTROL_MODE:
                    if prev_state == ES_CLEAR:
                        return False
            return True
        self.pad_action = False
        return False

    @subject_slot('value')
    def _action_navigate(self, value):
        if self.isShiftdown() and value != 0:
            self.nav_index = (self.nav_index + 1) % len(VIEWS_ALL)
            self.application().view.focus_view(VIEWS_ALL[self.nav_index])
            self.canonical_parent.show_message('Focus on : ' + str(VIEWS_ALL[self.nav_index]))
        else:
            if value != 0:
                self._select(self._nav_button)
                self.edit_state = ES_NAVIGATE
            else:
                self._deselect(self._nav_button)

    @subject_slot('value')
    def _action_duplicate(self, value):
        if value != 0:
            self._select(self._copy_button)
            self.edit_state = ES_DUPLICATE
        else:
            if self._deselect(self._copy_button):
                self._click_duplicate()

    @subject_slot('value')
    def _action_new(self, value):
        if value != 0:
            self._select(self._paste_button)
            self.edit_state = ES_NEW
        else:
            if self._deselect(self._paste_button):
                self._click_new()

    @subject_slot('value')
    def _action_note(self, value):
        if value != 0:
            self._select(self._note_button)
            self.edit_state = ES_DOUBLE
        else:
            if self._deselect(self._note_button):
                self._click_double()

    @subject_slot('value')
    def _action_clear(self, value):
        self.canonical_parent._hold_clear_action(value)
        if value != 0:
            self._mode_selector.enter_clear_state()
            self._select(self._clear_button)
            self.edit_state = ES_CLEAR
        else:
            if self._deselect(self._clear_button):
                self._click_clear()

    @subject_slot('value')
    def _action_nudge_button(self, value):
        if value != 0:
            self._select(self._nudge_button)
            self.edit_state = ES_NUDGE
        else:
            if self._deselect(self._nudge_button):
                self._click_nudge()

    @subject_slot('value')
    def _action_quantize(self, value):
        if value != 0:
            self._select(self._quantize_button)
            self.edit_state = ES_QUANT
        else:
            if self._deselect(self._quantize_button):
                self._click_quantize()

    @subject_slot('value')
    def _toggle_color_mode(self, value):
        if value != 0:
            session = self.canonical_parent._session
            if session.is_color_mode():
                self._color_mode_button.switch_off()
                session._change_color_mode(1)
            else:
                self._color_mode_button.send_color(1)
                session._change_color_mode(1)
