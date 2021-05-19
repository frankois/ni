# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/MidiMap.py
# Compiled at: 2021-05-04 10:35:59
# Size of source mod 2**32: 14040 bytes
import Live, re
from .PadScale import PadScale, BASE_NOTE_FIX_COLOR
GridQuantization = Live.Clip.GridQuantization
RecordingQuantization = Live.Song.RecordingQuantization
_color_table = {}
msg_sender = None

class SetterProperty(object):

    def __init__(self, func, doc=None):
        self.func = func
        self.__doc__ = doc if doc is not None else func.__doc__

    def __set__(self, obj, value):
        return self.func(obj, value)


def register_sender(sender):
    global msg_sender
    msg_sender = sender


def debug_out(message):
    if msg_sender:
        msg_sender.log_message(message)


COLOR_BLACK = 0
COLOR_WHITE = 127
COLOR_WHITE_DIM = 124
PARM_RANGE = 127
NOTES_STR = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
quantize_settings = [
 4.0, 2.0, 1.3333333333333333, 1.0, 0.6666666666666666, 0.5, 0.3333333333333333, 0.25, 0.16666666666666666, 0.125]
quantize_base = [4.0, 2.0, 1.0, 1.0, 0.5, 0.5, 0.25, 0.25, 0.125, 0.125]
quantize_string = ['1bar', '1/2', '1/2T', '1/4', '1/4T', '1/8', '1/8T', '1/16', '1/16T', '1/32']
quantize_clip_live = [GridQuantization.g_bar, GridQuantization.g_half, GridQuantization.g_half,
 GridQuantization.g_quarter,
 GridQuantization.g_quarter,
 GridQuantization.g_eighth, GridQuantization.g_eighth, GridQuantization.g_sixteenth,
 GridQuantization.g_sixteenth,
 GridQuantization.g_thirtysecond]
qauntize_is_triplet = [False, False, True, False, True, False, True, False, True, False]
CLIQ_DESCR = ('None', '8 Bars', '4 Bars', '2 Bars', '1 Bar', '1/2', '1/2T', '1/4',
              '1/4T', '1/8', '1/8T', '1/16', '1/16T', '1/32')

def from_midi_note(note):
    note_index = note % 12
    octave = note / 12 - 2
    return NOTES_STR[note_index] + ' ' + str(octave)


def select_clip_slot(song, slot):
    if slot:
        song.view.highlighted_clip_slot = slot


def calc_new_parm(parm, delta):
    parm_range = parm.max - parm.min
    int_val = int((parm.value - parm.min) / parm_range * PARM_RANGE + 0.1)
    inc_val = min(PARM_RANGE, max(0, int_val + delta))
    return float(inc_val) / float(PARM_RANGE) * parm_range + parm.min


def calc_parm_range(parm, rangevalue):
    parm_range = parm.max - parm.min
    int_val = int((parm.value - parm.min) / parm_range * rangevalue + 0.1)
    return int_val


def repeat(parm, delta):
    count = 0
    while count < SHIFT_INC:
        parm.value = calc_new_parm(parm, delta)
        count += 1


def vindexof(element_list, element):
    index = 0
    for ele in element_list:
        if ele == element:
            return index
        index = index + 1


def arm_exclusive(song, track=None):
    if not track:
        track = song.view.selected_track
    if track:
        if track.can_be_armed:
            if not track.arm:
                tracks = song.tracks
                for songtrack in tracks:
                    if songtrack != track and songtrack and songtrack.can_be_armed and songtrack.arm:
                        songtrack.arm = False

                track.arm = True


def track_index(song, track):
    if track == song.master_track:
        return (
         0, TYPE_TRACK_MASTER)
    element_list = song.tracks
    index = 0
    for tr in element_list:
        if tr == track:
            return (
             index, TYPE_TRACK_SESSION)
        index += 1

    element_list = song.return_tracks
    index = 0
    for tr in element_list:
        if tr == track:
            return (
             index, TYPE_TRACK_RETURN)
        index += 1

    return


def toHSB(rgb_val):
    if rgb_val in _color_index_table:
        return _color_index_table[rgb_val]
    else:
        hue, sat, bright = rgbToHsb(rgb_val)
        if bright < 1 or sat < 3:
            color = __ci(CI_WHITE)
            _color_index_table[rgb_val] = color
            return color
        off = 0
        if bright + sat < 22:
            off = 1
        if hue in range(2, 6) and bright < 13:
            off = 2
    color_index = min(hue + off + 1, 16)
    color = __ci(color_index)
    _color_index_table[rgb_val] = color
    return color


def rgbToHsb(rgb_val):
    rv = rgb_val // 65536
    rp = rv * 65536
    gv = (rgb_val - rp) // 256
    gp = gv * 256
    bv = rgb_val - rp - gp
    rgb_max = max(max(rv, gv), bv)
    rgb_min = min(min(rv, gv), bv)
    bright = rgb_max
    if bright == 0:
        return (0, 0, 0)
    else:
        sat = 255 * (rgb_max - rgb_min) // bright
        if sat == 0:
            return (0, 0, 0)
            hue = 0
            if rgb_max == rv:
                hue = 0 + 43 * (gv - bv) // (rgb_max - rgb_min)
        elif rgb_max == gv:
            hue = 85 + 43 * (bv - rv) // (rgb_max - rgb_min)
        else:
            hue = 171 + 43 * (rv - gv) // (rgb_max - rgb_min)
    if hue < 0:
        hue = 256 + hue
    return (int(hue // 16.0 + 0.3), sat >> 4, bright >> 4)


TYPE_TRACK_SESSION = 0
TYPE_TRACK_RETURN = 1
TYPE_TRACK_MASTER = 2
NAV_SRC_BUTTON = 1
NAV_SRC_ENCODER = 0
USE_DISPLAY = True
PM_OFF = 0
PM_ON = 1
CLIP_MODE = 0
PAD_MODE = 1
STEP_MODE = 2
USER_MODE = 3
STEP1 = 1
STEP4 = 4
MODE_PRESS_NONE = 0
MODE_PRESS_SELECT = 1
MODE_PRESS_SOLO = 2
BASIC_CHANNEL = 3
SHIFT_BUTTON = 1
MOD_CLIP_MODE_BUTTON = 2
MOD_SCENE_MODE_BUTTON = 3
MOD_PAD_MODE_BUTTON = 4
MOD_SYNC_MODE_BUTTON = 5
MODE_MOD_STOP = 2
DEVICE_CC_OFF = 40
DEVICE_BUTTON_CC_OFF = 100
SEL_MODE_MUTE = 1
SEL_MODE_SOLO = 2
SEL_MODE_ARM = 3
SEL_MODE_SELECT = 4
SEL_MODE_STOP = 5
SEL_MODE_XFADE = 6

def colorIndex(colorIndex, brightness):
    return colorIndex * 4 + brightness


def colorOnOff(colorIndex, adjust=0):
    return (
     colorIndex << 2, (colorIndex << 2) + 2 - adjust)


def __ci(colorIndex, adjust=0):
    return (
     (colorIndex << 2) + 2 - adjust, colorIndex << 2)


CI_OFF = 0
CI_RED = 1
CI_ORANGE = 2
CI_LIGHT_ORANGE = 3
CI_WARM_YELLOW = 4
CI_YELLOW = 5
CI_LIME = 6
CI_GREEN = 7
CI_MINT = 8
CI_CYAN = 9
CI_TURQUOISE = 10
CI_BLUE = 11
CI_PLUM = 12
CI_VIOLET = 13
CI_PURPLE = 14
CI_MAGENTA = 15
CI_FUCHSIA = 16
CI_WHITEA = 17
CI_WHITE = 30
CB_DIM = 0
CB_DIMFL = 1
CB_BRIGHT = 2
CB_BRIGHTFL = 3
_color_index_table = {}
TSM_BAR = 0
TSM_DOT = 1
TSM_PAN = 2
TSM_BAR_DOT = 3
CONTROL_LEVEL = 0
CONTROL_PAN = 1
CONTROL_SEND = 2
CONTROL_DEVICE = 3
SHIFT_INC = 4
INIT_SLOT = 10
REL_KNOB_DOWN = 127
CLICK_TIME = 500
ND_BASE_OTHER = 0
ND_KEYBOARD1 = 1
ND_INTERVAL = 2
SENDS = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
         'P')
BASE_NOTE = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
VIEWS_ALL = ('Session', 'Detail/Clip', 'Detail/DeviceChain', 'Browser', 'Arranger')
VIEWS = ('Browser', 'Detail/Clip', 'Detail/DeviceChain', 'Session')
QUANT_CONST = [
 RecordingQuantization.rec_q_no_q,
 RecordingQuantization.rec_q_quarter,
 RecordingQuantization.rec_q_eight,
 RecordingQuantization.rec_q_eight_triplet,
 RecordingQuantization.rec_q_eight_eight_triplet,
 RecordingQuantization.rec_q_sixtenth,
 RecordingQuantization.rec_q_sixtenth_triplet,
 RecordingQuantization.rec_q_sixtenth_sixtenth_triplet,
 RecordingQuantization.rec_q_thirtysecond]
QUANT_STRING = [
 'None', '1/4', '1/8', '1/8T', '1/8+1/8T', '1/16', '1/16T', '1/16+1/16T', '1/32']
AUTO_NAME = (
 (
  re.compile('kick|bd|bassdrum', re.IGNORECASE), CI_RED),
 (
  re.compile('snare|sn|sd', re.IGNORECASE), CI_BLUE),
 (
  re.compile('tom|tm|strike', re.IGNORECASE), CI_ORANGE),
 (
  re.compile('crash|crsh', re.IGNORECASE), CI_VIOLET),
 (
  re.compile('ride|rd', re.IGNORECASE), CI_MAGENTA),
 (
  re.compile('hit|strike|metal', re.IGNORECASE), CI_FUCHSIA),
 (
  re.compile('shaker|tamb', re.IGNORECASE), CI_LIGHT_ORANGE),
 (
  re.compile('clp|clap|hand|slap', re.IGNORECASE), CI_LIME),
 (
  re.compile('rim|rm|stick', re.IGNORECASE), CI_LIME),
 (
  re.compile('(bell|tri|gong|clav)', re.IGNORECASE), CI_MINT),
 (
  re.compile('(perc|cong|bong|ag)', re.IGNORECASE), CI_TURQUOISE),
 (
  re.compile('(glitch|fx|noise)', re.IGNORECASE), CI_WHITE),
 (
  re.compile('((hat|hh)(.*)(cl))|((cl)(.*)(hihat|hh)|ch)', re.IGNORECASE), CI_GREEN),
 (
  re.compile('((hat|hh)(.*)(op))|((op)(.*)(hihat|hh)|oh)', re.IGNORECASE), CI_LIME),
 (
  re.compile('(hh|hat|click)', re.IGNORECASE), CI_PURPLE))
DEFAULT_DRUM_COLOR = CI_YELLOW
PAD_TRANSLATIONS = ((0, 0, 28, 0), (1, 0, 29, 0), (2, 0, 30, 0), (3, 0, 31, 0), (0, 1, 24, 0),
                    (1, 1, 25, 0), (2, 1, 26, 0), (3, 1, 27, 0), (0, 2, 20, 0), (1, 2, 21, 0),
                    (2, 2, 22, 0), (3, 2, 23, 0), (0, 3, 16, 0), (1, 3, 17, 0), (2, 3, 18, 0),
                    (3, 3, 19, 0))
FEEDBACK_CHANNELS = list(range(0, 4))
PAD_FEEDBACK_CHANNEL = 10
NON_FEEDBACK_CHANNEL = 15
MATRIX_NOTE_NR = 22
COLOR_HUE_NAV = 84
COLOR_BRIGHTNESS_OFF = 30

def color_by_chromatic(midi_note, base_note, color):
    noteindex = midi_note % 12
    if noteindex == 0:
        return BASE_NOTE_FIX_COLOR
    return color[1]


def __find_drum_rack(chainlist):
    for chain in chainlist:
        for device in chain.devices:
            if device.can_have_drum_pads:
                return device


def find_drum_device(track):
    devices = track.devices
    for device in devices:
        if device.can_have_drum_pads:
            return device
            if device.can_have_chains:
                nested_drum = __find_drum_rack(device.chains)
                if nested_drum:
                    return nested_drum


SCALES = (
 PadScale('Chromatic', (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), color_by_chromatic),
 PadScale('Ionian/Major', (0, 2, 4, 5, 7, 9, 11)),
 PadScale('Aeolian/Minor', (0, 2, 3, 5, 7, 8, 10)),
 PadScale('Pentatonic', (0, 2, 4, 7, 9)),
 PadScale('Pentatonic Minor', (0, 3, 5, 7, 10)),
 PadScale('Dorian (B/g)', (0, 2, 3, 5, 7, 9, 10)),
 PadScale('Phrygian (A-flat/f)', (0, 1, 3, 5, 7, 8, 10)),
 PadScale('Lydian (D/e)', (0, 2, 4, 6, 7, 9, 11)),
 PadScale('Mixolydian (F/d)', (0, 2, 4, 5, 7, 9, 10)),
 PadScale('Locrian (D-flat/b-flat)', (0, 1, 3, 5, 6, 8, 10)),
 PadScale('Diminish', (0, 2, 3, 5, 6, 8, 9, 10)),
 PadScale('Major Blues', (0, 3, 4, 7, 9, 10)),
 PadScale('Minor Blues', (0, 3, 4, 6, 7, 10)),
 PadScale('Whole', (0, 2, 4, 6, 8, 10)),
 PadScale('Arabian', (0, 2, 4, 5, 6, 8, 10)),
 PadScale('Egyptian', (0, 2, 5, 7, 10)),
 PadScale('Gypsi', (0, 2, 3, 6, 7, 8, 11)),
 PadScale('Spanish Scale', (0, 1, 3, 4, 5, 7, 8, 10)),
 PadScale('Raga Bhairav', (0, 1, 4, 5, 7, 8, 11)),
 PadScale('Raga Gamanasrama', (0, 1, 4, 6, 7, 9, 11)),
 PadScale('Rag Todi', (0, 1, 3, 6, 7, 8, 11)))

def enum(**enums):
    return type('Enum', (), enums)


OFF_COLOR = (0, 0, 0, 0, 0)
PColor = enum(CLIP_PLAY=((36, 127, 127, 1, 1), (36, 100, 30, 1, 0)), CLIP_STOPPED=((14, 127, 127, 1, 0),
                                                                                   (14, 100, 30, 1, 0)),
  CLIP_RECORD=((0, 127, 127, 1, 1), (0, 127, 30, 1, 0)),
  CLIP_RECORD_TRIGGER=((0, 127, 127, 1, 2), (0, 127, 30, 1, 0)),
  CLIP_GROUP_PLAY=((43, 127, 110, 1, 0), (43, 127, 10, 1, 0)),
  CLIP_GROUP_CONTROL=((6, 127, 110, 1, 0), (6, 127, 10, 1, 0)),
  CLIP_GROUP_TRIGGER=((36, 127, 110, 1, 2), (36, 127, 10, 1, 0)),
  CLIP_PLAY_TRIGGER=((36, 127, 127, 1, 2), (36, 100, 30, 1, 0)),
  XFADE_A=((10, 127, 127, 1, 0), (10, 127, 127, 1, 0)),
  XFADE_BOTH=((65, 127, 5, 0, 0), (65, 127, 5, 0, 0)),
  XFADE_B=((4, 127, 127, 1, 1), (4, 127, 127, 1, 1)),
  STOP_G_PLAY=((96, 127, 127, 1, 1), (96, 127, 20, 0, 0)),
  STOP_G_NO_PLAY=((9, 127, 127, 1, 0), (9, 127, 20, 0, 0)),
  STOP_PLAY=((80, 127, 127, 1, 1), (80, 127, 20, 0, 0)),
  STOP_NO_PLAY=((14, 127, 127, 1, 0), (14, 127, 20, 0, 0)),
  STOP_NO_CLIPS=((16, 100, 40, 0, 0), (16, 100, 20, 0, 0)),
  ARM_MIDI=((0, 127, 127, 1, 0), (0, 127, 20, 0, 0)),
  ARM_AUDIO=((125, 127, 127, 1, 0), (125, 127, 20, 0, 0)),
  ARM_OTHER=((2, 127, 127, 1, 0), (0, 127, 20, 0, 0)),
  ARM_NO_ARM=((2, 40, 30, 1, 0), (2, 40, 30, 0, 0)),
  MUTE_TRACK=((22, 127, 127, 1, 0), (22, 127, 20, 0, 0)),
  SOLO_TRACK=((85, 127, 127, 1, 0), (85, 127, 25, 0, 0)),
  SELECT=((64, 127, 127, 1, 0), (64, 127, 10, 0, 0)),
  DEVICE_ON_OFF=((97, 80, 120, 1, 0), (97, 80, 50, 0, 0)),
  DEVICE_LEFT=((3, 127, 127, 1, 0), (3, 127, 30, 0, 0)),
  DEVICE_RIGHT=((5, 127, 127, 1, 0), (5, 127, 30, 0, 0)),
  BANK_LEFT=((90, 127, 127, 1, 0), (90, 127, 20, 0, 0)),
  BANK_RIGHT=((90, 127, 127, 1, 0), (90, 127, 20, 0, 0)),
  MIX_SELECT_SEND=((21, 127, 127, 1, 0), (21, 127, 20, 0, 0)),
  SCENE_PLAYING=((36, 127, 127, 1, 1), (36, 100, 25, 0, 0)),
  SCENE_HASCLIPS=((27, 127, 127, 1, 0), (27, 127, 25, 0, 0)),
  SCENE_NO_CLIPS=((65, 127, 127, 0, 0), (65, 127, 8, 0, 0)),
  MIX_SEL_VOLUME=((45, 127, 127, 1, 0), (45, 127, 20, 0, 0)),
  MIX_SEL_PANNING=((3, 127, 127, 1, 0), (3, 127, 20, 0, 0)),
  MIX_SEL_SEND=((70, 127, 127, 1, 0), (70, 127, 20, 0, 0)),
  MIX_SEL_DEVICE=((110, 127, 127, 1, 0), (110, 100, 20, 0, 0)),
  MIX_MODE_VOLUME=((32, 127, 127, 1, 0), (32, 127, 8, 0, 0)),
  MIX_MODE_PANNING=((0, 127, 127, 1, 0), (0, 127, 8, 0, 0)),
  MIX_MODE_SEND=((60, 127, 127, 1, 0), (60, 127, 8, 0, 0)),
  MIX_MODE_DEVICE=((95, 127, 127, 1, 0), (95, 100, 8, 0, 0)),
  MIX_MODE_DEVICE_OFF=((95, 10, 127, 1, 0), (95, 10, 30, 0, 0)),
  OFF=((0, 0, 0, 0, 0), (0, 0, 0, 0, 0)))

def device_get_color(mode, ind):
    if mode == CONTROL_LEVEL:
        return PColor.MIX_SEL_VOLUME[ind]
    if mode == CONTROL_PAN:
        return PColor.MIX_SEL_PANNING[ind]
    if mode == CONTROL_SEND:
        return PColor.MIX_SEL_SEND[ind]
    if mode == CONTROL_DEVICE:
        return PColor.MIX_SEL_DEVICE[ind]
    return


def device_get_mode_color(mode, ind):
    if mode == CONTROL_LEVEL:
        return PColor.MIX_MODE_VOLUME[ind]
    if mode == CONTROL_PAN:
        return PColor.MIX_MODE_PANNING[ind]
    if mode == CONTROL_SEND:
        return PColor.MIX_MODE_SEND[ind]
    if mode == CONTROL_DEVICE:
        return PColor.MIX_MODE_DEVICE[ind]
    return
# okay decompiling src/MidiMap.pyc
