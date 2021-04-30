# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/EncoderComponent.py
# Compiled at: 2021-04-29 13:54:08
# Size of source mod 2**32: 26004 bytes
Instruction context:
   
 L. 416       332  LOAD_FAST                'parmlist'
                 334  LOAD_METHOD              append
                 336  LOAD_GLOBAL              EMPTY_PARAM
                 338  CALL_METHOD_1         1  '1 positional argument'
                 340  POP_TOP          
->             342_0  COME_FROM           292  '292'
                 342  JUMP_BACK           122  'to 122'
                 344  POP_BLOCK        
               346_0  COME_FROM_LOOP      110  '110'
import Live
from .EncoderHandler import EncoderHandler
from .MaschineMode import MaschineMode
from .TouchStripSlider import TouchStripSlider
from .StateButton import TouchButton
from _Framework.SubjectSlot import subject_slot
from .ParameterUtil import EMPTY_PARAM, DEVICE_MAP, DEF_NAME
from .MidiMap import SENDS, vindexof, NAV_SRC_ENCODER, toHSB, TSM_PAN, TSM_BAR, TSM_BAR_DOT, TSM_DOT
from .ModifierComponent import StateButton, MIDI_CC_TYPE, MASK_CLEAR
ENC_MODE_VOL = 0
ENC_MODE_PAN = 1
ENC_MODE_SENDS = 2
ENC_MODE_DEVICE = 3
EMPTY_CONFIG = [0, 0, 0, 0, 0, 0, 0, 0]

class TrackDeviceSelection:
    __module__ = __name__
    _TrackDeviceSelection__device_bank_map = {}
    _TrackDeviceSelection__track = None

    def __init__(self, track, *a, **k):
        self._TrackDeviceSelection__track = track

    def register_selected_bank(self, device, bank_index):
        self._TrackDeviceSelection__device_bank_map[device] = bank_index

    def get_bank_index(self, device):
        if device in self._TrackDeviceSelection__device_bank_map:
            return self._TrackDeviceSelection__device_bank_map[device]
        self._TrackDeviceSelection__device_bank_map[device] = 0
        return 0


class EncoderComponent(MaschineMode):
    __module__ = __name__
    _EncoderComponent__mode = ENC_MODE_VOL
    _EncoderComponent__prev_mode = None
    _EncoderComponent__session = None
    _EncoderComponent__encoders = None
    _EncoderComponent__send_offset = 0
    _EncoderComponent__last_non_step_mode = ENC_MODE_VOL
    _EncoderComponent__led_msg = None
    _EncoderComponent__led_msg_dirty = False
    _EncoderComponent__bar_msg = None
    _EncoderComponent__bar_msg_dirty = False
    _EncoderComponent__cfg_msg = None
    _EncoderComponent__cfg_msg_dirty = False
    _EncoderComponent__state_listener = None
    _EncoderComponent__selection_map = {}

    def __init__(self, session, *a, **k):
        (super(EncoderComponent, self).__init__)(*a, **k)
        self._EncoderComponent__session = session
        self._EncoderComponent__level_pan_mode_button = StateButton(True, MIDI_CC_TYPE, 0, 91, name='Level_Button')
        self._EncoderComponent__handle_level_button.subject = self._EncoderComponent__level_pan_mode_button
        self._EncoderComponent__send_mode_button = StateButton(True, MIDI_CC_TYPE, 0, 92, name='Aux_Button')
        self._EncoderComponent__handle_sends_button.subject = self._EncoderComponent__send_mode_button
        self._EncoderComponent__device_mode_button = StateButton(True, MIDI_CC_TYPE, 0, 97, name='Control_Button')
        self._EncoderComponent__handle_device_button.subject = self._EncoderComponent__device_mode_button
        self._EncoderComponent__init_led_feedback()
        self._EncoderComponent__init_bar_feedback()
        self._EncoderComponent__init_config()
        self._EncoderComponent__encoders = [self.create_encoders(index) for index in range(8)]
        self._return_tracks_change.subject = self.song()
        self._tracks_change.subject = self.song()
        self._handle_track_changed.subject = self.song().view
        self._handle_visble_tracks_changed.subject = self.song()
        self._track = None
        self._device = None
        self.setup_select_track()
        self._device_index = 0
        self._bank_index = 0
        self._nr_of_banks = 0
        self._EncoderComponent__device_mode_down = False

    def setup_select_track(self):
        if self._track:
            self._handle_device_changed.subject = None
            self._handle_devices_changed.subject = None
        else:
            self._track = self.song().view.selected_track
            if self._track:
                self._device = self._track.view.selected_device
                self._handle_device_changed.subject = self._track.view
                self._handle_devices_changed.subject = self._track
                self._handle_color_changed.subject = self._track
                self._handle_device_changed(True)
                if self._device:
                    self._handle_parameters_changed.subject = self._device
                else:
                    self._handle_parameters_changed.subject = None

    def set_state_listener(self, listener):
        self._EncoderComponent__state_listener = listener

    def _cleanup_mapping(self):
        tracks = self.song().visible_tracks
        cmaps = {}
        keys = list(self._EncoderComponent__selection_map.keys())
        for track in tracks:
            cmaps[track] = True

        for track in keys:
            if track not in cmaps and track in self._EncoderComponent__selection_map:
                del self._EncoderComponent__selection_map[track]

    @subject_slot('color')
    def _handle_color_changed(self):
        if self._track:
            if self._EncoderComponent__mode == ENC_MODE_DEVICE:
                paramlist = self.get_device_parameter()
                self.update_touchstrip_color(paramlist)

    @subject_slot('devices')
    def _handle_devices_changed(self):
        if self._device != self._track.view.selected_device:
            self._handle_device_changed()

    @subject_slot('parameters')
    def _handle_parameters_changed(self):
        if self._EncoderComponent__mode == ENC_MODE_DEVICE:
            self._EncoderComponent__assign_encoders(False)

    @subject_slot('selected_track')
    def _handle_track_changed(self):
        self.setup_select_track()

    @subject_slot('visible_tracks')
    def _handle_visble_tracks_changed(self):
        self._EncoderComponent__assign_encoders(False)
        self._cleanup_mapping()
        if self._EncoderComponent__mode == ENC_MODE_VOL:
            self.refresh_state()

    def refresh_state(self):
        for encoder in self._EncoderComponent__encoders:
            encoder.refresh()

        self._EncoderComponent__led_msg_dirty = True
        self._EncoderComponent__bar_msg_dirty = True
        self.update_led()
        self.update_touchstrip_color()

    def _choose_device(self):
        device_list = self._track.devices
        if not device_list or len(device_list) == 0:
            return
        if len(device_list) > 0:
            return device_list[0]
        return

    @subject_slot('selected_device')
    def _handle_device_changed(self, force_change=False):
        self._device = self._track.view.selected_device
        if self._device:
            self._handle_parameters_changed.subject = self._device
        else:
            self._handle_parameters_changed.subject = None
        if self._EncoderComponent__mode == ENC_MODE_DEVICE:
            if not self._device:
                self._device = self._choose_device()
                if self._device:
                    self.song().view.select_device(self._device)
            self._bank_index = self._get_stored_bank_index()
            self._EncoderComponent__assign_encoders(True)

    def reset_led(self):
        self._EncoderComponent__led_msg_dirty = True

    def set_led_value(self, index, val):
        if self._EncoderComponent__led_msg[(11 + index)] != val:
            self._EncoderComponent__led_msg[11 + index] = val
            self._EncoderComponent__led_msg_dirty = True

    def update_led(self):
        if self._EncoderComponent__led_msg_dirty:
            self.canonical_parent._send_midi(tuple(self._EncoderComponent__led_msg))
            self._EncoderComponent__led_msg_dirty = False

    def __init_config(self):
        self._EncoderComponent__cfg_msg = [
         240, 0, 33, 9, 21, 0, 77, 80, 0, 1, 5]
        for _ in range(8):
            self._EncoderComponent__cfg_msg.append(0)
            self._EncoderComponent__cfg_msg.append(0)

        self._EncoderComponent__cfg_msg.append(247)

    def update_bar_config(self):
        for index, encoder in enumerate(self._EncoderComponent__encoders):
            mode, color = encoder.get_strip_cfg()
            self._EncoderComponent__cfg_msg[11 + index * 2] = mode
            self._EncoderComponent__cfg_msg[11 + index * 2 + 1] = color

        if self.canonical_parent:
            self.canonical_parent._send_midi(tuple(self._EncoderComponent__cfg_msg))

    def set_bar_config(self, modelist, colorlist):
        assert len(colorlist) == 8
        assert len(modelist) == 8
        for i in range(8):
            self._EncoderComponent__cfg_msg[11 + i * 2] = modelist[i]
            self._EncoderComponent__cfg_msg[11 + i * 2 + 1] = colorlist[i]

        if self.canonical_parent:
            self.canonical_parent._send_midi(tuple(self._EncoderComponent__cfg_msg))

    def set_bar_config_cfglist(self, configlist):
        assert len(configlist) == 8
        for i in range(8):
            mode, color = configlist[i]
            self._EncoderComponent__cfg_msg[11 + i * 2] = mode
            self._EncoderComponent__cfg_msg[11 + i * 2 + 1] = color

        if self.canonical_parent:
            self.canonical_parent._send_midi(tuple(self._EncoderComponent__cfg_msg))

    def turn_off_bars(self):
        self.set_bar_config([0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])

    def __init_led_feedback(self):
        self._EncoderComponent__led_msg = [
         240, 0, 33, 9, 21, 0, 77, 80, 0, 1, 4]
        for _ in range(8):
            self._EncoderComponent__led_msg.append(0)

        self._EncoderComponent__led_msg.append(247)

    def __init_bar_feedback(self):
        self._EncoderComponent__bar_msg = [
         240, 0, 33, 9, 21, 0, 77, 80, 0, 1, 3]
        for _ in range(8):
            self._EncoderComponent__bar_msg.append(0)

        self._EncoderComponent__bar_msg.append(247)

    def create_encoders(self, index):
        touch = TouchButton(MIDI_CC_TYPE, 0, (20 + index), name=('Touch_Tap' + str(index + 1) + '_Control'))
        touch.cindex = index
        slider = TouchStripSlider(MIDI_CC_TYPE, 0, (8 + index), index, self, name=('Touch_Slider' + str(index + 1) + '_Control'))
        slider.cindex = index
        return EncoderHandler(index, slider, touch, self)

    def invoke_nav_left(self):
        if self._EncoderComponent__mode == ENC_MODE_DEVICE:
            if self.canonical_parent._modifier.is_select_down():
                self.navigate_device(-1)
            elif self._EncoderComponent__device_mode_down:
                self.navigate_chain(-1)
            else:
                self.nav_device_param_banks(-1)
        elif self._EncoderComponent__mode == ENC_MODE_SENDS:
            self.nav_send_offset(-1)

    def invoke_nav_right(self):
        if self._EncoderComponent__mode == ENC_MODE_DEVICE:
            if self.canonical_parent._modifier.is_select_down():
                self.navigate_device(1)
            elif self._EncoderComponent__device_mode_down:
                self.navigate_chain(1)
            else:
                self.nav_device_param_banks(1)
        elif self._EncoderComponent__mode == ENC_MODE_SENDS:
            self.nav_send_offset(1)

    def nav_send_offset(self, nav_dir):
        new_pos = self._EncoderComponent__send_offset + nav_dir
        if new_pos >= len(self.song().return_tracks) or new_pos < 0:
            return
        self._EncoderComponent__send_offset = new_pos
        self._EncoderComponent__assign_encoders(False)
        self.canonical_parent.show_message('Control Send ' + str(SENDS[self._EncoderComponent__send_offset]))

    def nav_device_param_banks(self, nav_dir):
        prev = self._bank_index
        newpos = min(max(0, prev + nav_dir), self._nr_of_banks - 1)
        if newpos != prev:
            self._bank_index = newpos
            selmap = self._get_selmap()
            if selmap:
                selmap.register_selected_bank(self._device, self._bank_index)
            self._EncoderComponent__assign_encoders(True)

    def navigate_device(self, nav_dir):
        device_list = self._track.devices
        if self._device:
            if isinstance(self._device.canonical_parent, Live.Chain.Chain):
                device_list = self._device.canonical_parent.devices
        self._EncoderComponent__do_device_nav(vindexof(device_list, self._device), device_list, nav_dir)

    def __do_device_nav(self, index, device_list, nav_dir):
        if index != None:
            if len(device_list) > 1:
                newvalue = min(max(0, index + nav_dir), len(device_list) - 1)
                if newvalue != index:
                    self.song().view.select_device(device_list[newvalue])

    def navigate_chain(self, nav_dir):
        return self._device and isinstance(self._device.canonical_parent, Live.Chain.Chain) or None
        my_chain = self._device.canonical_parent
        chain_device = my_chain.canonical_parent
        chain_list = chain_device.chains
        index = vindexof(chain_list, my_chain)
        if index != None:
            if len(chain_list) > 0:
                newvalue = min(max(0, index + nav_dir), len(chain_list) - 1)
                if newvalue != index:
                    newchain = chain_list[newvalue]
                    device_list = newchain.devices
                    if len(device_list) > 0:
                        self.song().view.select_device(device_list[0])

    def navigate(self, nav_dir, modifier, alt_modifier=False, nav_src=NAV_SRC_ENCODER):
        if self._EncoderComponent__device_mode_down:
            if self._EncoderComponent__mode == ENC_MODE_DEVICE:
                if modifier:
                    self.nav_device_param_banks(-nav_dir)
            else:
                device_list = self._track.devices
                index = vindexof(device_list, self._device)
                if index != None:
                    newvalue = min(max(0, index + nav_dir), len(device_list) - 1)
                    if newvalue != index:
                        self.song().view.select_device(device_list[newvalue])
        else:
            self._EncoderComponent__assign_encoders(False)

    def notify(self, blink_state):
        pass

    def connect(self):
        self._EncoderComponent__assign_encoders()
        self._EncoderComponent__send_mode_button.set_display_value(0, True)
        self._EncoderComponent__device_mode_button.set_display_value(0, True)
        self._EncoderComponent__level_pan_mode_button.set_display_value(127, True)

    def apply_send_offset(self, offset):
        self._EncoderComponent__send_offset = offset
        if self._EncoderComponent__mode == ENC_MODE_SENDS:
            self._EncoderComponent__assign_encoders()

    def gettrack(self, index, off):
        tracks = self.song().visible_tracks
        if index + off < len(tracks):
            return tracks[(index + off)]
        return

    def set_step_note_levels(self, which, value, grid_control):
        assert which in range(8)

    def get_device_colors(self, parameters):
        colors = [
         0, 0, 0, 0, 0, 0, 0, 0]
        modes = [0, 0, 0, 0, 0, 0, 0, 0]
        if self._device:
            trackcolor = toHSB(self._track.color)[0]
            for i in range(8):
                if i < len(parameters):
                    param_ele = parameters[i]
                if param_ele != EMPTY_PARAM:
                    param = param_ele[0]
                    if param.min < 0:
                        if abs(param.min) == param.max:
                            modes[i] = TSM_PAN
                            colors[i] = trackcolor
                    modes[i] = TSM_BAR
                    colors[i] = trackcolor

        return (
         modes, colors)

    def get_param_list_str(self, paramlist):
        if self._device:
            result = ' Device: ' + self._device.name + ' Params: '
            for i in range(0, 8):
                if i < len(paramlist) and paramlist[i] != EMPTY_PARAM:
                    result += '{}:[{}]  '.format(i + 1, paramlist[i][0].name)
                else:
                    result += '{}:[----]  '.format(i + 1)

            return result
        return ''

    def get_device_parameter--- This code section failed: ---

 L. 391         0  LOAD_CONST               None
                2  STORE_FAST               'mapping'

 L. 392         4  LOAD_FAST                'self'
                6  LOAD_ATTR                _device
             8_10  POP_JUMP_IF_FALSE   464  'to 464'

 L. 393        12  BUILD_LIST_0          0 
               14  STORE_FAST               'parmlist'

 L. 394        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _device
               20  LOAD_ATTR                parameters
               22  STORE_FAST               'params'

 L. 395        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _device
               28  LOAD_ATTR                class_name
               30  LOAD_GLOBAL              DEVICE_MAP
               32  COMPARE_OP               in
               34  POP_JUMP_IF_FALSE    80  'to 80'

 L. 396        36  LOAD_GLOBAL              DEVICE_MAP
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                _device
               42  LOAD_ATTR                class_name
               44  BINARY_SUBSCR    
               46  STORE_FAST               'mappingObj'

 L. 397        48  LOAD_GLOBAL              isinstance
               50  LOAD_FAST                'mappingObj'
               52  LOAD_GLOBAL              tuple
               54  CALL_FUNCTION_2       2  '2 positional arguments'
               56  POP_JUMP_IF_FALSE    64  'to 64'

 L. 398        58  LOAD_FAST                'mappingObj'
               60  STORE_FAST               'mapping'
               62  JUMP_FORWARD         80  'to 80'
             64_0  COME_FROM            56  '56'

 L. 399        64  LOAD_STR                 'params'
               66  LOAD_FAST                'mappingObj'
               68  COMPARE_OP               in
               70  POP_JUMP_IF_FALSE    80  'to 80'

 L. 400        72  LOAD_FAST                'mappingObj'
               74  LOAD_STR                 'params'
               76  BINARY_SUBSCR    
               78  STORE_FAST               'mapping'
             80_0  COME_FROM            70  '70'
             80_1  COME_FROM            62  '62'
             80_2  COME_FROM            34  '34'

 L. 401        80  LOAD_FAST                'mapping'
               82  LOAD_CONST               None
               84  COMPARE_OP               !=
            86_88  POP_JUMP_IF_FALSE   350  'to 350'

 L. 402        90  LOAD_GLOBAL              len
               92  LOAD_FAST                'mapping'
               94  CALL_FUNCTION_1       1  '1 positional argument'
               96  LOAD_FAST                'self'
               98  STORE_ATTR               _nr_of_banks

 L. 403       100  LOAD_FAST                'mapping'
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                _bank_index
              106  BINARY_SUBSCR    
              108  STORE_FAST               'bank_mapping'

 L. 404       110  SETUP_LOOP          346  'to 346'
              112  LOAD_GLOBAL              range
              114  LOAD_CONST               0
              116  LOAD_CONST               8
              118  CALL_FUNCTION_2       2  '2 positional arguments'
              120  GET_ITER         
            122_0  COME_FROM           156  '156'
            122_1  COME_FROM           144  '144'
            122_2  COME_FROM           132  '132'
              122  FOR_ITER            344  'to 344'
              124  STORE_FAST               'idx'

 L. 405       126  LOAD_FAST                'bank_mapping'
              128  LOAD_CONST               None
              130  COMPARE_OP               !=
              132  POP_JUMP_IF_FALSE   122  'to 122'
              134  LOAD_FAST                'idx'
              136  LOAD_GLOBAL              len
              138  LOAD_FAST                'bank_mapping'
              140  CALL_FUNCTION_1       1  '1 positional argument'
              142  COMPARE_OP               <
              144  POP_JUMP_IF_FALSE   122  'to 122'
              146  LOAD_FAST                'bank_mapping'
              148  LOAD_FAST                'idx'
              150  BINARY_SUBSCR    
              152  LOAD_CONST               None
              154  COMPARE_OP               !=
              156  POP_JUMP_IF_FALSE   122  'to 122'

 L. 406       158  LOAD_FAST                'bank_mapping'
              160  LOAD_FAST                'idx'
              162  BINARY_SUBSCR    
              164  STORE_FAST               'mp'

 L. 407       166  LOAD_GLOBAL              isinstance
              168  LOAD_FAST                'mp'
              170  LOAD_GLOBAL              tuple
              172  CALL_FUNCTION_2       2  '2 positional arguments'
          174_176  POP_JUMP_IF_FALSE   332  'to 332'

 L. 408       178  LOAD_GLOBAL              len
              180  LOAD_FAST                'mp'
              182  CALL_FUNCTION_1       1  '1 positional argument'
              184  STORE_FAST               'mp_len'

 L. 409       186  LOAD_FAST                'mp_len'
              188  LOAD_CONST               4
              190  COMPARE_OP               ==
              192  POP_JUMP_IF_FALSE   238  'to 238'

 L. 410       194  LOAD_FAST                'parmlist'
              196  LOAD_METHOD              append
              198  LOAD_FAST                'self'
              200  LOAD_ATTR                _device
              202  LOAD_ATTR                parameters
              204  LOAD_FAST                'mp'
              206  LOAD_CONST               0
              208  BINARY_SUBSCR    
              210  BINARY_SUBSCR    
              212  LOAD_FAST                'mp'
              214  LOAD_CONST               1
              216  BINARY_SUBSCR    
              218  LOAD_FAST                'mp'
              220  LOAD_CONST               2
              222  BINARY_SUBSCR    
              224  LOAD_FAST                'mp'
              226  LOAD_CONST               3
              228  BINARY_SUBSCR    
              230  BUILD_TUPLE_4         4 
              232  CALL_METHOD_1         1  '1 positional argument'
              234  POP_TOP          
              236  JUMP_FORWARD        330  'to 330'
            238_0  COME_FROM           192  '192'

 L. 411       238  LOAD_FAST                'mp_len'
              240  LOAD_CONST               3
              242  COMPARE_OP               ==
          244_246  POP_JUMP_IF_FALSE   286  'to 286'

 L. 412       248  LOAD_FAST                'parmlist'
              250  LOAD_METHOD              append
              252  LOAD_FAST                'self'
              254  LOAD_ATTR                _device
              256  LOAD_ATTR                parameters
              258  LOAD_FAST                'mp'
              260  LOAD_CONST               0
              262  BINARY_SUBSCR    
              264  BINARY_SUBSCR    
              266  LOAD_FAST                'mp'
              268  LOAD_CONST               1
              270  BINARY_SUBSCR    
              272  LOAD_FAST                'mp'
              274  LOAD_CONST               2
              276  BINARY_SUBSCR    
              278  BUILD_TUPLE_3         3 
              280  CALL_METHOD_1         1  '1 positional argument'
              282  POP_TOP          
              284  JUMP_FORWARD        330  'to 330'
            286_0  COME_FROM           244  '244'

 L. 413       286  LOAD_FAST                'mp_len'
              288  LOAD_CONST               2
              290  COMPARE_OP               ==
          292_294  POP_JUMP_IF_FALSE   342  'to 342'

 L. 414       296  LOAD_FAST                'parmlist'
              298  LOAD_METHOD              append
              300  LOAD_FAST                'self'
              302  LOAD_ATTR                _device
              304  LOAD_ATTR                parameters
              306  LOAD_FAST                'mp'
              308  LOAD_CONST               0
              310  BINARY_SUBSCR    
              312  BINARY_SUBSCR    
              314  LOAD_FAST                'mp'
              316  LOAD_CONST               1
              318  BINARY_SUBSCR    
              320  LOAD_CONST               None
              322  LOAD_CONST               None
              324  BUILD_TUPLE_4         4 
              326  CALL_METHOD_1         1  '1 positional argument'
              328  POP_TOP          
            330_0  COME_FROM           284  '284'
            330_1  COME_FROM           236  '236'
              330  JUMP_BACK           122  'to 122'
            332_0  COME_FROM           174  '174'

 L. 416       332  LOAD_FAST                'parmlist'
              334  LOAD_METHOD              append
              336  LOAD_GLOBAL              EMPTY_PARAM
              338  CALL_METHOD_1         1  '1 positional argument'
              340  POP_TOP          
            342_0  COME_FROM           292  '292'
              342  JUMP_BACK           122  'to 122'
              344  POP_BLOCK        
            346_0  COME_FROM_LOOP      110  '110'

 L. 418       346  LOAD_FAST                'parmlist'
              348  RETURN_VALUE     
            350_0  COME_FROM            86  '86'

 L. 419       350  LOAD_GLOBAL              max
              352  LOAD_CONST               0
              354  LOAD_GLOBAL              len
              356  LOAD_FAST                'params'
              358  CALL_FUNCTION_1       1  '1 positional argument'
              360  LOAD_CONST               2
              362  BINARY_SUBTRACT  
              364  CALL_FUNCTION_2       2  '2 positional arguments'
              366  LOAD_CONST               8
              368  BINARY_TRUE_DIVIDE
              370  LOAD_CONST               1
              372  BINARY_ADD       
              374  LOAD_FAST                'self'
              376  STORE_ATTR               _nr_of_banks

 L. 420       378  SETUP_LOOP          460  'to 460'
              380  LOAD_GLOBAL              range
              382  LOAD_CONST               0
              384  LOAD_CONST               8
              386  CALL_FUNCTION_2       2  '2 positional arguments'
              388  GET_ITER         
            390_0  COME_FROM           426  '426'
              390  FOR_ITER            458  'to 458'
              392  STORE_FAST               'i'

 L. 421       394  LOAD_FAST                'self'
              396  LOAD_ATTR                _bank_index
              398  LOAD_CONST               8
              400  BINARY_MULTIPLY  
              402  LOAD_FAST                'i'
              404  BINARY_ADD       
              406  LOAD_CONST               1
              408  BINARY_ADD       
              410  STORE_FAST               'idx'

 L. 422       412  LOAD_FAST                'idx'
              414  LOAD_GLOBAL              len
              416  LOAD_FAST                'self'
              418  LOAD_ATTR                _device
              420  LOAD_ATTR                parameters
              422  CALL_FUNCTION_1       1  '1 positional argument'
              424  COMPARE_OP               <
          426_428  POP_JUMP_IF_FALSE   390  'to 390'

 L. 423       430  LOAD_FAST                'parmlist'
              432  LOAD_METHOD              append
              434  LOAD_FAST                'self'
              436  LOAD_ATTR                _device
              438  LOAD_ATTR                parameters
              440  LOAD_FAST                'idx'
              442  BINARY_SUBSCR    
              444  LOAD_GLOBAL              DEF_NAME
              446  LOAD_CONST               None
              448  BUILD_TUPLE_3         3 
              450  CALL_METHOD_1         1  '1 positional argument'
              452  POP_TOP          
          454_456  JUMP_BACK           390  'to 390'
              458  POP_BLOCK        
            460_0  COME_FROM_LOOP      378  '378'

 L. 425       460  LOAD_FAST                'parmlist'
              462  RETURN_VALUE     
            464_0  COME_FROM             8  '8'

 L. 427       464  LOAD_CONST               None
              466  RETURN_VALUE     

Parse error at or near `COME_FROM' instruction at offset 342_0

    def set_encoder_cfg(self, mode_list, color_list):
        for index, encoder in enumerate(self._EncoderComponent__encoders):
            encoder.set_encoder_cfg(mode_list[index], color_list[index])

    def get_strip_track_config(self, basemode, trackoffset):
        colors = [0, 0, 0, 0, 0, 0, 0, 0]
        modes = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(8):
            track = self.gettrack(i, trackoffset)
            if track:
                colors[i] = toHSB(track.color)[0]
                modes[i] = basemode
            else:
                colors[i] = 0
                modes[i] = 0

        return (modes, colors)

    def update_touchstrip_color(self, paramlist=None):
        trackoff = self._EncoderComponent__session.track_offset()
        if self._EncoderComponent__mode == ENC_MODE_VOL:
            modes, colors = self.get_strip_track_config(TSM_BAR_DOT, trackoff)
            self.set_encoder_cfg(modes, colors)
            self.update_bar_config()
        else:
            if self._EncoderComponent__mode == ENC_MODE_PAN:
                modes, colors = self.get_strip_track_config(TSM_PAN, trackoff)
                self.set_encoder_cfg(modes, colors)
                self.update_bar_config()
            else:
                if self._EncoderComponent__mode == ENC_MODE_SENDS:
                    modes, colors = self.get_strip_track_config(TSM_DOT, trackoff)
                    self.set_encoder_cfg(modes, colors)
                    self.update_bar_config()
                else:
                    if self._EncoderComponent__mode == ENC_MODE_DEVICE:
                        if paramlist:
                            modes, colors = self.get_device_colors(paramlist)
                            self.set_encoder_cfg(modes, colors)
                            self.update_bar_config()
                        else:
                            self.set_encoder_cfg(EMPTY_CONFIG, EMPTY_CONFIG)
                            self.update_bar_config()

    def update_encoders(self):
        self._EncoderComponent__led_msg_dirty = True
        self._EncoderComponent__assign_encoders(False)

    def __assign_encoders(self, show_message=True):
        trackoff = self._EncoderComponent__session.track_offset()
        paramlist = None
        if self._EncoderComponent__mode == ENC_MODE_DEVICE:
            paramlist = self.get_device_parameter()
        self.update_touchstrip_color(paramlist)
        for i in range(8):
            slider = self._EncoderComponent__encoders[i]
            track = self.gettrack(i, trackoff)
            if self._EncoderComponent__mode in (ENC_MODE_VOL, ENC_MODE_PAN, ENC_MODE_SENDS):
                if track is None:
                    if self._EncoderComponent__mode == ENC_MODE_VOL:
                        slider.reset_level_led()
                    slider.assign_parameter(None)
                else:
                    if self._EncoderComponent__mode == ENC_MODE_VOL:
                        slider.assign_parameter(track.mixer_device.volume, track, True, True)
                    else:
                        if self._EncoderComponent__mode == ENC_MODE_PAN:
                            slider.assign_parameter(track.mixer_device.panning, track)
                        else:
                            if self._EncoderComponent__mode == ENC_MODE_SENDS:
                                slider.assign_parameter(track.mixer_device.sends[self._EncoderComponent__send_offset], track)
            elif self._EncoderComponent__mode == ENC_MODE_DEVICE:
                if paramlist and i < len(paramlist):
                    if paramlist[i] == EMPTY_PARAM:
                        slider.assign_parameter(None)
                    else:
                        slider.assign_parameter(paramlist[i][0], False)
            else:
                slider.assign_parameter(None)

        if self._EncoderComponent__mode == ENC_MODE_VOL:
            self.update_led()
        if show_message:
            if self._EncoderComponent__mode == ENC_MODE_DEVICE:
                if self._device:
                    self.canonical_parent.show_message(self.get_param_list_str(paramlist))

    @subject_slot('return_tracks')
    def _return_tracks_change(self):
        if self._EncoderComponent__send_offset >= len(self.song().return_tracks):
            self.apply_send_offset(len(self.song().return_tracks) - 1)

    @subject_slot('tracks')
    def _tracks_change(self):
        self._EncoderComponent__assign_encoders(False)
        self._cleanup_mapping()

    def is_modifier_down(self):
        return self.canonical_parent._modifier.is_delete_down()

    def is_shift_down(self):
        return self.canonical_parent._modifier.is_shift_down()

    def notify_touch(self, parameter):
        if parameter:
            mode = self.canonical_parent._modifier.modifier_mask()
            if mode == MASK_CLEAR:
                clip_slot = self.song().view.highlighted_clip_slot
                clip = clip_slot.clip
                if clip:
                    clip.clear_envelope(parameter)
                    self.canonical_parent.show_message('Clear Automation for Clip ' + clip.name + ' for Parmeter: ' + parameter.name)

    def __to_mode(self, mode):
        if mode == ENC_MODE_VOL:
            self._EncoderComponent__mode = ENC_MODE_VOL
            self._EncoderComponent__last_non_step_mode = ENC_MODE_VOL
            self._EncoderComponent__assign_encoders(False)
            self.canonical_parent.show_message('Level Mode')
        else:
            if mode == ENC_MODE_PAN:
                self._EncoderComponent__mode = ENC_MODE_PAN
                self._EncoderComponent__last_non_step_mode = ENC_MODE_PAN
                self._EncoderComponent__assign_encoders(False)
                self.canonical_parent.show_message('Pan Mode')
            else:
                if mode == ENC_MODE_SENDS:
                    if self._EncoderComponent__mode == ENC_MODE_SENDS:
                        self._EncoderComponent__send_offset += 1
                        if self._EncoderComponent__send_offset >= len(self.song().return_tracks):
                            self._EncoderComponent__send_offset = 0
                    else:
                        self._EncoderComponent__send_offset = 0
                    self._EncoderComponent__mode = ENC_MODE_SENDS
                    self._EncoderComponent__last_non_step_mode = ENC_MODE_SENDS
                    self._EncoderComponent__assign_encoders(False)
                    self.canonical_parent.show_message('Control Send ' + str(SENDS[self._EncoderComponent__send_offset]))
                else:
                    if mode == ENC_MODE_DEVICE:
                        self._EncoderComponent__mode = ENC_MODE_DEVICE
                        self._EncoderComponent__last_non_step_mode = ENC_MODE_SENDS
                        self._EncoderComponent__assign_encoders(True)

    def __set_radio_buttons(self):
        if not self._EncoderComponent__mode == ENC_MODE_VOL:
            if self._EncoderComponent__mode == ENC_MODE_PAN:
                if self._EncoderComponent__prev_mode != ENC_MODE_VOL or self._EncoderComponent__prev_mode != ENC_MODE_PAN:
                    self._EncoderComponent__send_mode_button.set_display_value(0, True)
                    self._EncoderComponent__device_mode_button.set_display_value(0, True)
                    self._EncoderComponent__level_pan_mode_button.set_display_value(127, True)
            if self._EncoderComponent__mode == ENC_MODE_SENDS and self._EncoderComponent__prev_mode != ENC_MODE_SENDS:
                self._EncoderComponent__send_mode_button.set_display_value(127, True)
                self._EncoderComponent__device_mode_button.set_display_value(0, True)
                self._EncoderComponent__level_pan_mode_button.set_display_value(0, True)
        elif self._EncoderComponent__mode == ENC_MODE_DEVICE:
            if self._EncoderComponent__prev_mode != ENC_MODE_DEVICE:
                self._EncoderComponent__send_mode_button.set_display_value(0, True)
                self._EncoderComponent__device_mode_button.set_display_value(127, True)
                self._EncoderComponent__level_pan_mode_button.set_display_value(0, True)

    @subject_slot('value', identify_sender=True)
    def __handle_level_button(self, value, sender):
        if not value == 0:
            if sender.grabbed:
                return
            self._EncoderComponent__prev_mode = self._EncoderComponent__mode
            if self.is_shift_down():
                if self._EncoderComponent__mode != ENC_MODE_PAN:
                    self._EncoderComponent__to_mode(ENC_MODE_PAN)
                    self._EncoderComponent__set_radio_buttons()
        elif self._EncoderComponent__mode != ENC_MODE_VOL:
            self._EncoderComponent__to_mode(ENC_MODE_VOL)
            self._EncoderComponent__set_radio_buttons()

    @subject_slot('value', identify_sender=True)
    def __handle_sends_button(self, value, sender):
        if value == 0 or sender.grabbed:
            return
        self._EncoderComponent__prev_mode = self._EncoderComponent__mode
        self._EncoderComponent__to_mode(ENC_MODE_SENDS)
        self._EncoderComponent__set_radio_buttons()

    def _get_selmap(self):
        if self._track not in self._EncoderComponent__selection_map:
            self._EncoderComponent__selection_map[self._track] = TrackDeviceSelection(self._track)
        return self._EncoderComponent__selection_map[self._track]

    def _get_stored_bank_index(self):
        if not self._device:
            return 0
        selmap = self._get_selmap()
        if selmap:
            return selmap.get_bank_index(self._device)
        return 0

    @subject_slot('value', identify_sender=True)
    def __handle_device_button(self, value, sender):
        if sender.grabbed:
            return
        else:
            self._EncoderComponent__device_mode_down = value != 0
            if self._EncoderComponent__state_listener:
                self._EncoderComponent__state_listener.notify_state('controldown', self._EncoderComponent__device_mode_down)
            if value == 0:
                return
            if not self._device:
                track = self._track
                if track:
                    if self._track.devices and len(self._track.devices) > 0:
                        device_list = device_list = self._track.devices
                        sel_device = device_list[0]
                        self.song().view.select_device(sel_device)
                    else:
                        return
                else:
                    return
        self._EncoderComponent__prev_mode = self._EncoderComponent__mode
        if self._EncoderComponent__mode != ENC_MODE_DEVICE:
            self._EncoderComponent__mode = ENC_MODE_DEVICE
            self._EncoderComponent__send_mode_button.set_display_value(0, True)
            self._EncoderComponent__device_mode_button.set_display_value(127, True)
            self._EncoderComponent__level_pan_mode_button.set_display_value(0, True)
            self._EncoderComponent__assign_encoders(True)
        else:
            paramlist = self.get_device_parameter()
            self.canonical_parent.show_message(self.get_param_list_str(paramlist))
            if self._device:
                if self.is_shift_down() and isinstance(self._device.canonical_parent, Live.Chain.Chain):
                    chain = self._device.canonical_parent
                    topdevice = chain.canonical_parent
                    self.song().view.select_device(topdevice)
                else:
                    if (self.is_shift_down() or self._device).can_have_chains:
                        if len(self._device.chains) > 0:
                            device_list = self._device.chains[0].devices
                            self.song().view.select_device(device_list[0])
            self.application().view.show_view('Detail/DeviceChain')
            self._EncoderComponent__set_radio_buttons()

    def exit(self):
        pass

    def enter(self):
        pass

    def disconnect(self):
        for encoder in self._EncoderComponent__encoders:
            encoder.send_value(0, True)
