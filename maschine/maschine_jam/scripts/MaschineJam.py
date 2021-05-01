# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/MaschineJam.py
# Compiled at: 2021-04-29 13:54:08
# Size of source mod 2**32: 16005 bytes
import Live, time
from _Framework.SubjectSlot import subject_slot
import _Framework.ControlSurface as ControlSurface
from _Framework.InputControlElement import nop, MIDI_CC_TYPE
import _Framework.SliderElement as SliderElement
from .JamModes import JamModes
from .JamSessionComponent import JamSessionComponent
from .PadColorButton import PadColorButton
from .EncoderComponent import EncoderComponent
from .StateButton import StateButton, SysExButton
from .ModifierComponent import ModifierComponent
from .JamButtonMatrix import JamButtonMatrix, MatrixState
from .MidiMap import register_sender, PAD_TRANSLATIONS, FEEDBACK_CHANNELS, arm_exclusive, NAV_SRC_BUTTON, COLOR_BLACK, debug_out

class MaschineJam(ControlSurface):
    __doc__ = 'Control Script for Maschine JAM Controller'
    __module__ = __name__
    _midi_count = 0
    _arm_exclusive = True
    _solo_exclusive = True
    _blink_state = 0
    _MaschineJam__midi_count = 0
    _MaschineJam__play_button = None
    _MaschineJam__block_nav = False
    _MaschineJam__matrix_state = None

    def __init__(self, c_instance):
        super(MaschineJam, self).__init__(c_instance)
        with self.component_guard():
            self._suppress_send_midi = True
            register_sender(self)
            self._challenge = Live.Application.get_random_int(0, 400000000) & 2139062143
            self._set_suppress_rebuild_requests(True)
            self._c_ref = c_instance
            self.request_rebuild_midi_map()
            self._MaschineJam__matrix_state = MatrixState(self)
            self._main_mode_container = JamModes(c_instance.note_repeat)
            self._set_suppress_rebuild_requests(False)
            self._active = True
            self._display_device_param = False
            self._setup_transport()
            self._setup_session()
            self._encoder_modes = EncoderComponent(self._session)
            self._encoder_modes.connect()
            self._encoder_modes.set_state_listener(self)
            self._modifier = ModifierComponent(self._session)
            self._connect_session()
            self._main_mode_container.bind_session(self._MaschineJam__matrix_state)
            self._main_mode_container.bind_modify_component(self._modifier)
            self._setup_mainjogwheel()
            self._init_m4l()
            self._init_settings()
            self.set_pad_translations(PAD_TRANSLATIONS)
            self.set_feedback_channels(FEEDBACK_CHANNELS)
            self._suppress_send_midi = False
            self._main_mode_container._step_mode.set_mode_elements(self._modifier, self._encoder_modes)
            self._main_mode_container._drum_step_mode.set_mode_elements(self._modifier)
            self._final_init()
            self.apply_preferences()

    def _init_m4l(self):
        self._bmatrix.set_user_unbind_listener(self._main_mode_container)

    def _init_settings(self):
        from pickle import loads, dumps
        from encodings import ascii
        nop(ascii)
        preferences = self._c_instance.preferences(self.preferences_name())
        self._pref_dict = {}
        try:
            self._pref_dict = loads(str(preferences))
        except Exception:
            pass

        pref_dict = self._pref_dict
        preferences.set_serializer(lambda : dumps(pref_dict))

    def store_preferences(self):
        self._pref_dict['matrix_color_mode'] = self._session.get_color_mode()

    def apply_preferences(self):
        pref_dict = self._pref_dict
        if 'matrix_color_mode' in pref_dict:
            self._session.set_color_mode(pref_dict['matrix_color_mode'])

    def preferences_name(self):
        return 'MaschineJam'

    def _final_init(self):
        debug_out('########## LIVE 11 Maschine JAM V 1.4 #############')
        self._auto_button.set_display_value(self.song().session_automation_record and 127 or 0)
        self._main_mode_container.init_elements()

    def _init_map(self):
        msgsysex = [
         240, 0, 33, 9, 21, 0, 77, 80, 0, 1, 2]
        for _ in range(80):
            msgsysex.append(COLOR_BLACK)

        msgsysex.append(247)
        self._send_midi(tuple(msgsysex))

    def _set_touch_strip_led(self):
        msgsysex = [
         240, 0, 33, 9, 21, 0, 77, 80, 0, 1, 4]
        for _ in range(8):
            msgsysex.append(0)

        msgsysex.append(247)
        self._send_midi(tuple(msgsysex))

    def handle_sysex(self, midi_bytes):
        if len(midi_bytes) > 11:
            if midi_bytes[0:10] == (240, 0, 33, 9, 21, 0, 77, 80, 0, 1):
                msg, value = midi_bytes[10:12]
                if msg == 70:
                    self.refresh_state()
                    self._modifier.set_shiftstatus(1)
                else:
                    if msg == 77:
                        self.shiftButton.notify_value(value == 1 and 127 or 0)
                        if not self.shiftButton.is_grabbed:
                            self._modifier.set_shiftstatus(value)

    def _setup_transport(self):
        is_momentary = True
        self.shiftButton = SysExButton(120, name='Shift_Button')
        self._MaschineJam__play_button = StateButton(is_momentary, MIDI_CC_TYPE, 0, 108, name='Play_Button')
        self._hand_play_pressed.subject = self._MaschineJam__play_button
        self._listen_playing.subject = self.song()
        self._channel_led_left = SliderElement(MIDI_CC_TYPE, 0, 38)
        self._channel_led_right = SliderElement(MIDI_CC_TYPE, 0, 39)
        self._channel_led_left.last_raw = 0.0
        self._channel_led_left.last_send = 0
        self._channel_led_right.last_raw = 0.0
        self._channel_led_right.last_send = 0
        self._listen_master_left.subject = self.song().master_track
        self._listen_master_right.subject = self.song().master_track
        self._auto_button = StateButton(is_momentary, MIDI_CC_TYPE, 0, 98, name='Auto_Button')
        self._listen_automation_record.subject = self.song()
        self._handle_automation_record.subject = self._auto_button
        self._do_direction_up.subject = StateButton(is_momentary, MIDI_CC_TYPE, 0, 40, name='Up_Arrow')
        self._do_direction_down.subject = StateButton(is_momentary, MIDI_CC_TYPE, 0, 41, name='Down_Arrow')
        self._do_direction_left.subject = StateButton(is_momentary, MIDI_CC_TYPE, 0, 42, name='Left_Arrow')
        self._do_direction_right.subject = StateButton(is_momentary, MIDI_CC_TYPE, 0, 43, name='Right_Arrow')

    @subject_slot('output_meter_left')
    def _listen_master_left(self):
        cvl = self.song().master_track.output_meter_left
        if cvl != self._channel_led_left.last_raw:
            val = cvl > 0.92 and 127 or int(127 * (cvl * cvl))
            if val != self._channel_led_left.last_send:
                self._channel_led_left.last_raw = cvl
                self._channel_led_left.last_send = val
                self._channel_led_left.send_value(val, True)

    @subject_slot('output_meter_right')
    def _listen_master_right(self):
        cvl = self.song().master_track.output_meter_right
        if cvl != self._channel_led_right.last_raw:
            val = cvl > 0.92 and 127 or int(127 * (cvl * cvl))
            if val != self._channel_led_right.last_send:
                self._channel_led_right.last_raw = cvl
                self._channel_led_right.last_send = val
                self._channel_led_right.send_value(val, True)

    def is_monochrome(self):
        return False

    def _send_midi(self, midi_bytes, **keys):
        self._c_ref.send_midi(midi_bytes)
        if self._midi_count > 2:
            time.sleep(0.001)
            self._midi_count = 0
        self._midi_count += 1
        return True

    def _setup_mainjogwheel(self):
        self._prev_mode = None

    def is_shift_down(self):
        return self._modifier.is_shift_down()

    def modifier_mask(self):
        return self._modifier.modifier_mask()

    def _setup_session(self):
        self._session = JamSessionComponent()
        self._matrix = []
        self._bmatrix = JamButtonMatrix(8, name='Button_Matrix')
        for sceneIndex in range(8):
            button_row = []
            for trackindex in range(8):
                button = PadColorButton(True, 0, sceneIndex, trackindex, self._main_mode_container)
                button_row.append(button)

            self._matrix.append(tuple(button_row))
            self._bmatrix.add_row(tuple(button_row))

        self._session.set_matrix(self._bmatrix, self._matrix)
        self._MaschineJam__matrix_state.register_matrix(self._bmatrix)
        self._bmatrix.prepare_update()
        for button, (trackIndex, sceneIndex) in self._bmatrix.iterbuttons():
            if button:
                scene = self._session.scene(sceneIndex)
                clip_slot = scene.clip_slot(trackIndex)
                clip_slot.set_launch_button(button)
                clip_slot.set_triggered_to_play_value(1)
                clip_slot.set_triggered_to_record_value(1)
                clip_slot.set_started_value(1)
                clip_slot.set_recording_value(1)
                clip_slot.set_stopped_value(1)

        self._session._link()
        self._bmatrix.commit_update()
        self.set_highlighting_session_component(self._session)

    def _connect_session(self):
        for sindex in range(self._session.height()):
            scene = self._session.scene(sindex)
            for cindex in range(self._session.width()):
                clip = scene.clip_slot(cindex)
                clip.set_modifier(self._modifier)
                clip.set_index((cindex, sindex))

    def update_display(self):
        with self.component_guard():
            self._main_mode_container.notify(self._blink_state)
            self._encoder_modes.notify(self._blink_state)
            self._blink_state = (self._blink_state + 1) % 4

    def refresh_state(self):
        self._bmatrix.prepare_update()
        ControlSurface.refresh_state(self)
        self.update_hardware()
        self._bmatrix.commit_update()

    def update_hardware(self):
        self._session.update()
        self._MaschineJam__play_button.set_display_value(self.song().is_playing and 127 or 0, True)
        self._main_mode_container.refresh_state()
        self._encoder_modes.refresh_state()

    def invoke_nav_left(self):
        self._encoder_modes.invoke_nav_left()

    def invoke_nav_right(self):
        self._encoder_modes.invoke_nav_right()

    def invoke_rec(self):
        slot = self.song().view.highlighted_clip_slot
        if slot == None:
            return
        if slot.controls_other_clips:
            slot.fire()
        else:
            if slot.has_clip:
                track = slot.canonical_parent
                if track.can_be_armed:
                    arm_exclusive(self.song(), track)
                self.song().overdub = True
                slot.fire()
            else:
                track = slot.canonical_parent
                if track.can_be_armed:
                    arm_exclusive(self.song(), track)
                    slot.fire()
        return

    @subject_slot('session_automation_record')
    def _listen_automation_record(self):
        self._auto_button.set_display_value(self.song().session_automation_record and 127 or 0, True)

    @subject_slot('value', identify_sender=True)
    def _handle_automation_record(self, value, sender):
        if value == 0 or sender.grabbed:
            return
        self.song().session_automation_record = not self.song().session_automation_record

    @subject_slot('is_playing')
    def _listen_playing(self):
        if self.song().is_playing:
            self._MaschineJam__play_button.set_display_value(127, True)
        else:
            self._MaschineJam__play_button.set_display_value(0, True)

    @subject_slot('value', identify_sender=True)
    def _hand_play_pressed(self, value, sender):
        if value == 0 or sender.grabbed:
            return
        elif self.song().is_playing:
            if self._modifier.is_shift_down():
                self.song().start_playing()
            else:
                self.song().stop_playing()
        else:
            self.song().start_playing()

    @subject_slot('value', identify_sender=True)
    def do_undo(self, value, sender):
        if not value == 0:
            if sender.grabbed:
                return
            if self._modifier.is_shift_down():
                if self.song().can_redo == 1:
                    self.song().redo()
                    self.show_message(str('REDO'))
        elif self.song().can_undo == 1:
            self.song().undo()
            self.show_message(str('UNDO'))

    def notify_state(self, state, value):
        if state == 'controldown':
            self._MaschineJam__block_nav = value
        else:
            if state == 'step':
                self._main_mode_container.notify_state(state, value)

    @subject_slot('value', identify_sender=True)
    def _do_direction_up(self, value, sender):
        if value == 0 or sender.grabbed:
            return
        elif not self._MaschineJam__block_nav:
            self._main_mode_container.navigate(-1, 1, self._modifier.is_shift_down(), NAV_SRC_BUTTON)
        else:
            self._encoder_modes.navigate(-1, 1, self._modifier.is_shift_down(), NAV_SRC_BUTTON)

    @subject_slot('value', identify_sender=True)
    def _do_direction_down(self, value, sender):
        if value == 0 or sender.grabbed:
            return
        elif not self._MaschineJam__block_nav:
            self._main_mode_container.navigate(1, 1, self._modifier.is_shift_down(), NAV_SRC_BUTTON)
        else:
            self._encoder_modes.navigate(1, -1, self._modifier.is_shift_down(), NAV_SRC_BUTTON)

    @subject_slot('value', identify_sender=True)
    def _do_direction_left(self, value, sender):
        if not value == 0:
            if sender.grabbed:
                return
            if not self._MaschineJam__block_nav:
                encoder_changed = self._main_mode_container.navigate(-1, 0, self._modifier.is_shift_down(), NAV_SRC_BUTTON)
                if encoder_changed:
                    self._encoder_modes.navigate(-1, 0, self._modifier.is_shift_down(), NAV_SRC_BUTTON)
        else:
            self._encoder_modes.navigate(-1, 0, self._modifier.is_shift_down(), NAV_SRC_BUTTON)

    @subject_slot('value', identify_sender=True)
    def _do_direction_right(self, value, sender):
        if not value == 0:
            if sender.grabbed:
                return
            if not self._MaschineJam__block_nav:
                encoder_changed = self._main_mode_container.navigate(1, 0, self._modifier.is_shift_down(), NAV_SRC_BUTTON)
                if encoder_changed:
                    self._encoder_modes.navigate(1, 0, self._modifier.is_shift_down(), NAV_SRC_BUTTON)
        else:
            self._encoder_modes.navigate(1, 0, self._modifier.is_shift_down(), NAV_SRC_BUTTON)

    @property
    def selected_mode(self):
        return self._main_mode_container.selected_mode

    @selected_mode.setter
    def selected_mode(self, value):
        self._main_mode_container.selected_mode = value

    def get_session(self):
        return self._session

    def toggle_mode(self):
        self._session.set_color_mode()
        self.refresh_state()

    def get_button_matrix(self):
        return self._bmatrix

    def deassign_matrix(self):
        for scene_index in range(8):
            scene = self._session.scene(scene_index)
            for track_index in range(8):
                clip_slot = scene.clip_slot(track_index)
                clip_slot.set_launch_button(None)

    def _pre_serialize(self):
        from pickle import dumps
        from encodings import ascii
        nop(ascii)
        preferences = self._c_instance.preferences('MaschineJam')
        self.store_preferences()
        dump = dumps(self._pref_dict)
        preferences.set_serializer(lambda : dump)

    def disconnect(self):
        self._pre_serialize()
        self._set_touch_strip_led()
        self._encoder_modes.turn_off_bars()
        self._init_map()
        self._channel_led_left.send_value(0, True)
        self._channel_led_right.send_value(0, True)
        self._active = False
        self._suppress_send_midi = True
        super(MaschineJam, self).disconnect()
# okay decompiling scripts/MaschineJam.pyc
