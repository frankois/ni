# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Maschine_JAM/ParameterUtil.py
# Compiled at: 2021-04-29 13:54:08
# Size of source mod 2**32: 73239 bytes


def shorten_devname(name):
    if name == None or len(name) < 9:
        return name
    splt = name.split()
    rstr = ''
    if len(splt) > 1:
        splt = [filter_vowels(s, 7) for s in splt]
        rstr = rstr.join(splt)
        if len(rstr) > 8:
            return filter_vowels(rstr, 8)[:8]
        return rstr[:8]
    return filter_vowels(name, 8)[:8]


def filter_vowels(string, lenx):
    fltrstr = ''
    clen = len(string)
    if clen <= lenx:
        return string
    for c in string[::-1]:
        if clen <= lenx or c not in FILTER_CHAR:
            fltrstr = c + fltrstr

    return fltrstr[:8]


INT_PARAM = 2
SELECT_TUPLE = 10
PARM_DELAY = 11
UNICODE_VAL = 12
INT_VALUE = 13
DEF_NAME = 0
EMPTY_PARAM = -1
TYPE_RANGE = 1
TYPE_INT_MAP = 2
TYPE_FLOAT_MULT = 3
INT_127_RANGE = {'spec':TYPE_RANGE,  'max':127,  'type':INT_PARAM}
FILTER_CHAR = {'a':True,  'e':True,  'i':True,  'o':True,  'u':True}
DEVICE_SHORT_NAMES = {'AutoFilter':'AutoFLTR',  'BeatRepeat':'Beat RPT', 
 'FilterDelay':'FILT DLY'}
DEVICE_MAP = {'Amp':(
  (
   (
    1, DEF_NAME, 'AMP', SELECT_TUPLE),
   (
    2, DEF_NAME),
   (
    3, DEF_NAME),
   (
    4, DEF_NAME),
   (
    5, DEF_NAME),
   (
    6, DEF_NAME),
   (
    7, DEF_NAME),
   (8, 'DualMono')),
  (
   (
    9, DEF_NAME),
   None)), 
 'AutoFilter':(
  (
   (
    1, 'Type', 'FILTER', SELECT_TUPLE),
   (2, 'FREQ'),
   (3, 'Resonanc'),
   EMPTY_PARAM,
   (4, 'Mod AMT', 'Envelope'),
   (5, 'Attack'),
   (6, 'Release')),
  (
   (7, 'Amont', 'LFO'),
   (
    8, 'Wave', None, SELECT_TUPLE),
   (9, 'FREQUENC', 'LFO RATE'),
   (10, 'Sync'),
   (
    11, 'SyncRate', None, SELECT_TUPLE),
   (
    12, 'Ster.Mode', None, SELECT_TUPLE),
   (13, 'Spin'),
   (
    14, 'Phase', None, UNICODE_VAL)),
  (
   (
    15, 'LFO OffS', 'LFO PHS', UNICODE_VAL),
   (16, 'LFO QUAN'),
   (17, 'LFO Q RT'),
   (
    18, 'On', 'EXT IN', SELECT_TUPLE),
   (19, 'GAIN'),
   (20, 'Dry/WET'))), 
 'BeatRepeat':(
  (
   (
    1, DEF_NAME, 'BEAT RPT'),
   (
    2, DEF_NAME, None, SELECT_TUPLE),
   (
    3, DEF_NAME, None, SELECT_TUPLE),
   (
    4, DEF_NAME, None, SELECT_TUPLE),
   (
    5, 'BLK.TRIPL', None, SELECT_TUPLE),
   (6, 'Var'),
   (
    7, 'Var Type', None, SELECT_TUPLE),
   (
    8, DEF_NAME, None, SELECT_TUPLE)),
  (
   (17, 'Repeat', 'BEAT RPT'),
   (
    9, DEF_NAME),
   (10, 'Decay', 'PITCH'),
   (11, 'Pitch'),
   EMPTY_PARAM,
   (
    12, DEF_NAME, 'OUTPUT', SELECT_TUPLE),
   (
    13, DEF_NAME)),
  ((14, 'ACTIVATE', 'FILTER'), (15, 'FREQUENC'), (16, 'WIDTH'))), 
 'AutoPan':(
  (
   (
    9, 'Waveform', 'AUTO PAN', SELECT_TUPLE),
   (
    1, DEF_NAME, None, SELECT_TUPLE),
   (
    2, DEF_NAME),
   (3, 'Frequenc'),
   (
    4, DEF_NAME, None, SELECT_TUPLE),
   (
    5, DEF_NAME, None, UNICODE_VAL)),
  (
   (6, 'Spin', 'AUTO PAN'),
   (
    7, 'St.Mode', None, SELECT_TUPLE),
   (
    8, DEF_NAME, None, UNICODE_VAL),
   (
    10, DEF_NAME),
   (11, 'WDH RND'),
   (
    12, DEF_NAME, None, SELECT_TUPLE))), 
 'Cabinet':(
  (
   (
    1, 'Cab Type', 'CABINET', SELECT_TUPLE),
   (
    2, 'Mic Type', None, SELECT_TUPLE),
   (
    3, 'Mic Pos', None, SELECT_TUPLE),
   (
    4, 'DualMono', None, SELECT_TUPLE),
   (
    5, DEF_NAME)),
  None), 
 'Corpus':(
  (
   (
    1, 'Res.Type', 'CORPUS', SELECT_TUPLE),
   (
    2, 'Reso.Qual', None, SELECT_TUPLE),
   (
    3, DEF_NAME),
   (4, 'Transpos'),
   (
    5, DEF_NAME),
   (
    6, DEF_NAME),
   (
    7, DEF_NAME),
   (
    8, DEF_NAME)),
  (
   (
    9, DEF_NAME, 'CORPUS'),
   (10, 'Brightne'),
   (11, 'Inharmon'),
   (
    12, DEF_NAME),
   (
    13, DEF_NAME),
   (
    14, DEF_NAME),
   (15, 'Listen L'),
   (16, 'Listen R')),
  (
   (
    27, 'On/Off', 'FILTER', SELECT_TUPLE),
   (
    28, DEF_NAME),
   (
    29, DEF_NAME),
   (
    35, DEF_NAME),
   (
    36, DEF_NAME),
   (
    37, DEF_NAME),
   EMPTY_PARAM,
   (
    38, DEF_NAME, 'MIX')),
  (
   (17, 'ACTIVATE', 'LFO'),
   (
    18, 'LFO SHP', None, SELECT_TUPLE),
   (
    19, DEF_NAME, None, SELECT_TUPLE),
   (
    20, DEF_NAME),
   (
    21, 'LFOSyn.R', None, SELECT_TUPLE),
   (
    22, 'LFOSt.Mo', None, SELECT_TUPLE),
   (
    23, DEF_NAME),
   (
    24, DEF_NAME, None, UNICODE_VAL)),
  (
   (
    25, DEF_NAME, 'LFO', UNICODE_VAL),
   (26, 'LFO Amt'),
   EMPTY_PARAM,
   (30, 'MIDIFreq', 'MIDI'),
   (
    31, 'MIDIMode', None, SELECT_TUPLE),
   (
    32, DEF_NAME),
   (
    33, DEF_NAME, None, SELECT_TUPLE),
   (34, 'Off Dcy'))), 
 'Chorus':(
  (
   (1, 'Del1 Tim'),
   (2, 'Del1 HP'),
   (3, 'Del2 Tim'),
   (
    4, 'Del2 Mod', None, SELECT_TUPLE),
   (
    9, DEF_NAME),
   (
    6, DEF_NAME, 'LFO'),
   (
    7, DEF_NAME),
   (
    11, DEF_NAME, 'MIX')),
  (
   (
    5, DEF_NAME, None, SELECT_TUPLE),
   (
    8, 'LFOExten', None, SELECT_TUPLE),
   (
    10, DEF_NAME, None, SELECT_TUPLE))), 
 'FilterDelay':{'bankGroups':(0, 2, 4), 
  'params':(
   (
    (1, 'Input On', 'DELAY 1'),
    (
     5, 'Mode', None, SELECT_TUPLE),
    (
     6, 'Beat Dly', None, SELECT_TUPLE),
    (7, 'Beat Swi'),
    (8, 'Time Dly'),
    (9, 'Feedbck'),
    (10, 'Pan'),
    (11, 'Volume')),
   ((2, 'FLT On', 'FILTER 1'), (3, 'FREQUENC'), (4, 'WIDTH')),
   (
    (12, 'Input On', 'DELAY 2'),
    (
     16, 'Mode', None, SELECT_TUPLE),
    (
     17, 'Beat Dly', None, SELECT_TUPLE),
    (18, 'Beat Swi'),
    (19, 'Time Dly'),
    (20, 'Feedbck'),
    (21, 'Pan'),
    (22, 'Volume')),
   ((13, 'FLT On', 'FILTER 2'), (14, 'FREQUENC'), (15, 'WIDTH')),
   (
    (23, 'Input On', 'DELAY 3'),
    (
     27, 'Mode', None, SELECT_TUPLE),
    (
     28, 'Beat Dly', None, SELECT_TUPLE),
    (29, 'Beat Swi'),
    (30, 'Time Dly'),
    (31, 'Feedbck'),
    (32, 'Pan'),
    (33, 'Volume')),
   ((24, 'FLT On', 'FILTER 3'), (25, 'FREQUENC'), (26, 'WIDTH'), (34, 'Dry/Wet', 'MIX')))}, 
 'Compressor2':(
  (
   (
    1, DEF_NAME, 'COMPRESS'),
   (
    2, DEF_NAME),
   (3, 'ExpRatio'),
   (
    4, DEF_NAME),
   (
    5, DEF_NAME),
   (
    6, DEF_NAME, None, SELECT_TUPLE),
   (
    7, DEF_NAME),
   (
    8, DEF_NAME, None, SELECT_TUPLE)),
  (
   (
    9, DEF_NAME, 'MIX'),
   (
    10, DEF_NAME, 'MODE', SELECT_TUPLE),
   (
    11, DEF_NAME, None, SELECT_TUPLE),
   (
    12, DEF_NAME),
   (
    13, 'LookAhea', None, SELECT_TUPLE),
   EMPTY_PARAM,
   EMPTY_PARAM,
   (
    14, 'LISTEN', 'SIDECHN', SELECT_TUPLE)),
  (
   (
    15, 'ON', 'SC EXTIN', SELECT_TUPLE),
   (16, 'GAIN'),
   (17, 'MIX'),
   (
    19, 'On', 'SDCH EQ', SELECT_TUPLE),
   (
    18, 'Mode', None, SELECT_TUPLE),
   (20, 'Freq'),
   (22, 'Q'),
   (21, 'Gain'))), 
 'Tube':(
  (
   (9, 'TubeType', 'TUBE'),
   (
    2, DEF_NAME),
   (
    3, DEF_NAME),
   (
    4, DEF_NAME),
   (
    5, DEF_NAME),
   (
    6, DEF_NAME),
   (
    7, DEF_NAME),
   (
    8, DEF_NAME)),
  (
   (
    1, DEF_NAME),
   None)), 
 'Eq8':{'bankGroups':(0, 1, 9), 
  'params':(
   (
    (1, 'Out Gain', 'EQ OUT'),
    (
     2, DEF_NAME),
    (3, 'Adapt Q')),
   (
    (
     4, '1A On', 'BAND 1A', SELECT_TUPLE),
    (
     5, '1A Type', None, SELECT_TUPLE),
    (6, '1A Freq'),
    (7, '1A Gain'),
    (8, '1A Res')),
   (
    (
     14, '2A On', 'BAND 2A', SELECT_TUPLE),
    (
     15, '2A Type', None, SELECT_TUPLE),
    (16, '2A Freq'),
    (17, '2A Gain'),
    (18, '2A Res')),
   (
    (
     24, '3A On', 'BAND 3A', SELECT_TUPLE),
    (
     25, '3A Type', None, SELECT_TUPLE),
    (26, '3A Freq'),
    (27, '3A Gain'),
    (28, '3A Res')),
   (
    (
     34, '4A On', 'BAND 4A', SELECT_TUPLE),
    (
     35, '4A Type', None, SELECT_TUPLE),
    (36, '4A Freq'),
    (37, '4A Gain'),
    (38, '4A Res')),
   (
    (
     44, '5A On', 'BAND 5A', SELECT_TUPLE),
    (
     45, '5A Type', None, SELECT_TUPLE),
    (46, '5A Freq'),
    (47, '5A Gain'),
    (48, '5A Res')),
   (
    (
     54, '6A On', 'BAND 6A', SELECT_TUPLE),
    (
     55, '6A Type', None, SELECT_TUPLE),
    (56, '6A Freq'),
    (57, '6A Gain'),
    (58, '6A Res')),
   (
    (
     64, '7A On', 'BAND 7A', SELECT_TUPLE),
    (
     65, '7A Type', None, SELECT_TUPLE),
    (66, '7A Freq'),
    (67, '7A Gain'),
    (68, '7A Res')),
   (
    (
     74, '8A On', 'BAND 8A', SELECT_TUPLE),
    (
     75, '8A Type', None, SELECT_TUPLE),
    (76, '8A Freq'),
    (77, '8A Gain'),
    (78, '8A Res')),
   (
    (
     9, '1B On', 'BAND 1B', SELECT_TUPLE),
    (
     10, '1B Type', None, SELECT_TUPLE),
    (11, '1B Freq'),
    (12, '1B Gain'),
    (13, '1B Res')),
   (
    (
     19, '2B On', 'BAND 2B', SELECT_TUPLE),
    (
     20, '2B Type', None, SELECT_TUPLE),
    (21, '2B Freq'),
    (22, '2B Gain'),
    (23, '2B Res')),
   (
    (
     29, '3B On', 'BAND 3B', SELECT_TUPLE),
    (
     30, '3B Type', None, SELECT_TUPLE),
    (31, '3B Freq'),
    (32, '3B Gain'),
    (33, '3B Res')),
   (
    (
     39, '4B On', 'BAND 4B', SELECT_TUPLE),
    (
     40, '4B Type', None, SELECT_TUPLE),
    (41, '4B Freq'),
    (42, '4B Gain'),
    (43, '4B Res')),
   (
    (
     49, '5B On', 'BAND 5B', SELECT_TUPLE),
    (
     50, '5B Type', None, SELECT_TUPLE),
    (51, '5B Freq'),
    (52, '5B Gain'),
    (53, '5B Res')),
   (
    (
     59, '6B On', 'BAND 6B', SELECT_TUPLE),
    (
     60, '6B Type', None, SELECT_TUPLE),
    (61, '6B Freq'),
    (62, '6B Gain'),
    (63, '6B Res')),
   (
    (
     69, '7B On', 'BAND 7B', SELECT_TUPLE),
    (
     70, '7B Type', None, SELECT_TUPLE),
    (71, '7B Freq'),
    (72, '7B Gain'),
    (73, '7B Res')),
   (
    (
     79, '8B On', 'BAND 8B', SELECT_TUPLE),
    (
     80, '8B Type', None, SELECT_TUPLE),
    (81, '8B Freq'),
    (82, '8B Gain'),
    (83, '8B Res')))}, 
 'Flanger':(
  (
   (2, 'DLY Time', 'FLNG DLY'),
   (
    3, DEF_NAME),
   (
    4, DEF_NAME, None, SELECT_TUPLE),
   (5, 'LFO Amt'),
   (
    6, DEF_NAME),
   (7, 'Env.Modu', 'ENVELOPE'),
   (8, 'Env.Attac'),
   (9, 'Env.Relea')),
  (
   (
    10, 'Waveform', 'LFO', SELECT_TUPLE),
   (11, 'Rate'),
   (
    12, DEF_NAME),
   (
    13, 'Sync.Rate', None, SELECT_TUPLE),
   (
    14, 'LFO St.Mo', None, SELECT_TUPLE),
   (
    15, DEF_NAME, 'LF PHASE'),
   (
    16, 'LFOPhase', None, UNICODE_VAL),
   (
    17, 'LFO Ofs', None, UNICODE_VAL)),
  (
   (18, 'LFO WID.R'),
   (
    1, DEF_NAME, 'MIX'))), 
 'FilterEQ3':(
  (
   (
    6, 'LowOn', 'LOW', SELECT_TUPLE),
   (1, 'GainLo'),
   (4, 'FreqLo'),
   (
    7, 'MidOn', 'MID', SELECT_TUPLE),
   (2, 'GainMid'),
   (
    8, 'HighOn', 'HIGH', SELECT_TUPLE),
   (3, 'GainHi'),
   (5, 'FreqHi')),
  (
   (
    9, 'Slope', 'SLOPE', SELECT_TUPLE),
   None)), 
 'Erosion':(
  (
   (
    1, 'Mode', 'EROSION', SELECT_TUPLE),
   (2, 'Frequenc'),
   (
    3, DEF_NAME),
   (
    4, DEF_NAME)),
  None), 
 'ProxyAudioEffectDevice':(
  (
   (2, 'Out Gain'),
   (3, 'Int Gain'),
   EMPTY_PARAM,
   EMPTY_PARAM,
   EMPTY_PARAM,
   (
    1, DEF_NAME)),
  None), 
 'FrequencyShifter':(
  (
   (
    1, 'Mode', 'FREQUENC', SELECT_TUPLE),
   (
    2, DEF_NAME),
   (
    3, DEF_NAME),
   (4, 'RM FQ'),
   (
    6, DEF_NAME, None, SELECT_TUPLE),
   (7, 'On/Off', 'DRIVE'),
   (
    8, DEF_NAME),
   (
    5, DEF_NAME, 'MIX')),
  (
   (9, 'Amount', 'LFO'),
   (
    10, 'Waveform', None, SELECT_TUPLE),
   (11, 'Frequenc'),
   (
    12, 'Sync', None, SELECT_TUPLE),
   (
    13, 'Sync Rat', None, SELECT_TUPLE),
   (
    14, 'STER.MODE', None, SELECT_TUPLE),
   (15, 'Spin'),
   (
    16, 'Phaes', None, UNICODE_VAL)),
  (
   (
    17, 'Offset', None, UNICODE_VAL),
   (18, 'Width'))), 
 'Gate':(
  (
   (1, 'Thresh', 'Gate'),
   (
    2, DEF_NAME),
   (
    3, DEF_NAME),
   (
    4, DEF_NAME),
   (
    5, DEF_NAME),
   (
    6, DEF_NAME),
   (
    8, DEF_NAME, None, SELECT_TUPLE),
   (
    9, 'LookAhea', None, SELECT_TUPLE)),
  (
   (
    10, DEF_NAME, 'SC EXTIN'),
   (
    11, DEF_NAME),
   (
    12, DEF_NAME),
   (
    7, DEF_NAME),
   (
    14, DEF_NAME, 'SC EQ'),
   (
    13, DEF_NAME, None, SELECT_TUPLE),
   (
    15, DEF_NAME),
   (
    16, DEF_NAME)),
  (
   (
    17, DEF_NAME),
   None)), 
 'GlueCompressor':(
  (
   (1, 'Threshol', 'GLUE'),
   (
    2, DEF_NAME),
   (
    3, DEF_NAME),
   (
    4, DEF_NAME, None, SELECT_TUPLE),
   (
    5, DEF_NAME, None, SELECT_TUPLE),
   (
    6, DEF_NAME, None, SELECT_TUPLE),
   EMPTY_PARAM,
   (
    7, DEF_NAME, 'MIX')),
  (
   (8, 'Pk Clip.I', 'SIDECH'),
   (9, 'Side CHN'),
   (10, 'SCN Gain'),
   (11, 'SCN Mix'),
   (
    13, DEF_NAME, 'SC EQ'),
   (
    12, DEF_NAME, None, SELECT_TUPLE),
   (
    14, DEF_NAME),
   (
    15, DEF_NAME)),
  (
   (
    16, DEF_NAME),
   None)), 
 'GrainDelay':(
  (
   (
    7, 'Dly Mode', 'DELAY', SELECT_TUPLE),
   (
    8, 'Beat Dly', None, SELECT_TUPLE),
   (9, 'BeatSwin'),
   (10, 'Time Dly'),
   EMPTY_PARAM,
   EMPTY_PARAM,
   (
    5, DEF_NAME)),
  (
   (
    1, DEF_NAME, 'PITCH'),
   (2, 'Frequenc'),
   (
    3, DEF_NAME),
   (
    4, DEF_NAME),
   EMPTY_PARAM,
   EMPTY_PARAM,
   (6, 'Dry/Wet'))), 
 'Limiter':(
  (
   (
    1, DEF_NAME, 'LIMIT'),
   (
    2, DEF_NAME),
   (3, 'Releaset'),
   (
    4, DEF_NAME, None, ('OFF', 'AUTO')),
   (5, 'LinkChan', None, ('L/R', 'STEREO')),
   (
    6, 'Lookahea', None, SELECT_TUPLE)),
  None), 
 'Looper':(
  (
   (
    1, DEF_NAME, None, SELECT_TUPLE),
   (
    2, DEF_NAME),
   (
    3, DEF_NAME, None, SELECT_TUPLE),
   (
    4, DEF_NAME, None, SELECT_TUPLE),
   (
    5, DEF_NAME),
   (
    6, 'Quantiza', None, SELECT_TUPLE),
   (
    7, 'SongCont', None, SELECT_TUPLE),
   (
    8, 'TempoCon', None, SELECT_TUPLE)),
  None), 
 'MultibandDynamics':{'bankGroups':(0, 1, 6, 12), 
  'params':(
   (
    (1, 'Lo-Mi X-', 'MB COMP'),
    (2, 'MI-HI X-'),
    (
     3, 'Soft Kne', None, SELECT_TUPLE),
    (
     4, 'Pk/RMS M', None, SELECT_TUPLE),
    (5, 'Master.Ou'),
    (6, 'Amount'),
    EMPTY_PARAM,
    (7, 'Time Sca')),
   (
    (8, 'LOW OUT', 'OUT GAIN'),
    (9, 'MID OUT'),
    (10, 'HIGH OUT'),
    EMPTY_PARAM,
    EMPTY_PARAM,
    (11, 'LOW IN', 'IN GAIN'),
    (12, 'MID IN'),
    (13, 'HIGH IN')),
   (
    (
     14, 'LOW BAND', 'BAND', SELECT_TUPLE),
    EMPTY_PARAM,
    (
     15, 'MID BAND', None, SELECT_TUPLE),
    EMPTY_PARAM,
    (
     16, 'HI BAND', None, SELECT_TUPLE)),
   (
    (17, 'LOW Ab T', 'THRESHLD'),
    (18, 'MID Ab T'),
    (19, 'HI Ab Th'),
    EMPTY_PARAM,
    EMPTY_PARAM,
    (20, 'LOW BW T', 'BW THRESH'),
    (20, 'MID BW T'),
    (20, 'HI BW Th')),
   (
    (23, 'LOW AB R', 'ABV RATIO'),
    (24, 'MID AB R'),
    (25, 'HI AB Ra'),
    EMPTY_PARAM,
    EMPTY_PARAM,
    (26, 'LOW BW R', 'BW RATIO'),
    (27, 'MID BW R'),
    (28, 'HI BW Ra')),
   (
    (29, 'LOW ATTA', 'ATTACK'),
    (30, 'MID ATTA'),
    (31, 'HI ATTAC'),
    EMPTY_PARAM,
    EMPTY_PARAM,
    (33, 'LOW RELE', 'RELEASE'),
    (34, 'MID RELE'),
    (35, 'HI RELEA')),
   (
    (8, 'OUT GAIN', 'LOW BAND'),
    (11, 'IN GAIN'),
    (
     14, 'BAND', None, SELECT_TUPLE),
    (17, 'Ab Thres'),
    (20, 'BW Thres'),
    (23, 'AB Ratio'),
    (26, 'BW Ratio')),
   ((29, 'ATTACK', 'LOW A/R'), (32, 'RELEASE')),
   (
    (9, 'OUT GAIN', 'MID BAND'),
    (12, 'IN GAIN'),
    (
     15, 'BAND', None, SELECT_TUPLE),
    (18, 'Ab Thres'),
    (21, 'Bw Thres'),
    (24, 'AB Ratio'),
    (27, 'BW Ratio')),
   ((30, 'ATTACK', 'MID A/R'), (33, 'RELEASE')),
   (
    (10, 'OUT Gain', 'HI BAND'),
    (13, 'IN GAIN'),
    (
     16, 'BAND', None, SELECT_TUPLE),
    (19, 'Ab Thres'),
    (22, 'Bw Thres'),
    (25, 'AB Ratio'),
    (28, 'BW Ratio')),
   ((31, 'ATTACK', 'HI A/R'), (34, 'RELEASE')),
   (
    (
     35, 'Ex.In On', 'SIDECHN', SELECT_TUPLE),
    (36, 'Ex.In Gai'),
    (37, 'Ex.In Mix')))}, 
 'Overdrive':(
  (
   (1, 'FLT Freq', 'FILTER'),
   (2, 'FLT Widt'),
   (
    3, DEF_NAME, 'DRIVE'),
   (
    5, DEF_NAME),
   (6, 'Prsrv.Dyn'),
   EMPTY_PARAM,
   EMPTY_PARAM,
   (
    4, DEF_NAME, 'MIX')),
  None), 
 'Phaser':(
  (
   (
    2, DEF_NAME, 'PHASER', SELECT_TUPLE),
   (
    3, DEF_NAME, None, SELECT_TUPLE),
   (
    4, DEF_NAME),
   (5, 'Frequenc'),
   (
    6, DEF_NAME),
   (7, 'LFO Amt'),
   EMPTY_PARAM,
   (
    1, DEF_NAME, 'MIX')),
  (
   (8, 'Modulati', 'ENVELOPE'),
   (9, 'Attack'),
   (10, 'Release'),
   (
    11, 'LFO Wave', 'LFO', SELECT_TUPLE),
   (12, 'LFO FRQ'),
   (
    13, 'LFO Sync', None, SELECT_TUPLE),
   (
    14, 'LFO Syn.R', None, SELECT_TUPLE),
   (
    15, 'LFO St.Mo', None, SELECT_TUPLE)),
  (
   (16, 'LFO Spin', 'LFO'),
   (
    17, 'LFO Phas', None, UNICODE_VAL),
   (
    18, 'LFO Offs', None, UNICODE_VAL),
   (19, 'LFO WD.RN'))), 
 'PingPongDelay':(
  (
   (1, 'FLT Freq', 'PP DELAY'),
   (2, 'FLTWidth'),
   (
    3, 'Dly Mode', None, SELECT_TUPLE),
   (
    4, 'Beat Dly', None, SELECT_TUPLE),
   (5, 'BeatSwin'),
   (6, 'Time Dly'),
   (
    7, DEF_NAME)),
  (
   (
    8, DEF_NAME, 'MIX'),
   (
    9, DEF_NAME))), 
 'Redux':(
  (
   (
    1, DEF_NAME, 'REDUX'),
   (2, 'BitDepth'),
   (
    3, 'SMP Mode', None, SELECT_TUPLE),
   (4, 'SMP Hard'),
   (5, 'SMP Soft')),
  None), 
 'Resonator':(
  (
   (1, 'FLTR On', 'RESONATOR'),
   (2, 'Freq'),
   (3, 'FLT Type'),
   (
    4, DEF_NAME, None, SELECT_TUPLE),
   (
    5, DEF_NAME),
   (
    6, DEF_NAME, None, SELECT_TUPLE),
   (
    7, DEF_NAME),
   (
    8, DEF_NAME)),
  (
   (
    11, DEF_NAME, 'NOTE 1'),
   (
    12, DEF_NAME, None, INT_VALUE),
   (
    13, DEF_NAME),
   (
    14, DEF_NAME),
   (
    15, DEF_NAME, 'NOTE 2'),
   (
    16, DEF_NAME),
   (
    17, DEF_NAME),
   (
    18, DEF_NAME)),
  (
   (
    19, DEF_NAME, 'NOTE 3'),
   (20, 'III P'),
   (
    21, DEF_NAME),
   (
    22, DEF_NAME),
   (
    23, DEF_NAME, 'NOTE 4'),
   (
    24, DEF_NAME),
   (
    25, DEF_NAME),
   (
    26, DEF_NAME)),
  (
   (
    27, DEF_NAME, 'NOTE 5'),
   (
    28, DEF_NAME),
   (
    29, DEF_NAME),
   (
    30, DEF_NAME),
   EMPTY_PARAM,
   EMPTY_PARAM,
   (
    9, DEF_NAME, 'MIX'),
   (
    10, DEF_NAME))), 
 'Reverb':(
  (
   (19, 'Dcy Time', 'MAIN RV'),
   (25, 'RoomSize'),
   (
    20, DEF_NAME),
   (
    21, DEF_NAME),
   (26, 'StereoIm'),
   (
    28, DEF_NAME),
   EMPTY_PARAM,
   (
    30, DEF_NAME, 'MIX')),
  (
   (22, 'FreezeOn', 'LEVEL'),
   (
    23, DEF_NAME),
   (
    24, DEF_NAME),
   (
    27, DEF_NAME, None, SELECT_TUPLE),
   (29, 'Diff Lev')),
  ((1, 'PreDelay', 'PRE DELAY'), (2, 'In.LC On'), (3, 'In.HC On'), (4, 'In.FL FRQ'),
 (5, 'In.FL WID'), (6, 'ER.Spin', 'EARL RFL'), (7, 'ER.Spin R'), (8, 'ER.Spin A')),
  ((9, 'ER.Shape'), (10, 'HiSh On', 'HI SHELF'), (11, 'HiSh FRQ'), (12, 'HiSh Gai'),
 (13, 'LoSh On', 'LO SHELF'), (14, 'LoSh Fre'), (15, 'LoShf Ga')),
  ((16, 'Chor On', 'CHORUS'), (17, 'Chor Rat'), (18, 'Chor AMT'))), 
 'CrossDelay':(
  (
   (
    2, 'L DLY Mo', 'LEFT', SELECT_TUPLE),
   (
    3, 'L Beat D', None, SELECT_TUPLE),
   (4, 'L Beat S'),
   (5, 'L TM Del'),
   (
    6, 'R Delay ', 'RIGHT', SELECT_TUPLE),
   (
    7, 'R Beat D', None, SELECT_TUPLE),
   (8, 'R Beat S'),
   (9, 'R TM Del')),
  (
   (
    1, DEF_NAME, 'MIX', SELECT_TUPLE),
   (
    10, DEF_NAME),
   (
    11, DEF_NAME))), 
 'Saturator':(
  (
   (
    2, DEF_NAME, 'DRIVE'),
   (
    3, DEF_NAME),
   (
    4, DEF_NAME, None, SELECT_TUPLE),
   (
    5, DEF_NAME),
   (
    6, DEF_NAME),
   (7, 'Frequenc'),
   (
    8, DEF_NAME),
   (
    1, DEF_NAME, 'MIX')),
  (
   (
    9, DEF_NAME),
   (10, 'SoftClip'),
   (
    11, DEF_NAME, 'WAVESHAPE'),
   (
    12, DEF_NAME),
   (
    13, DEF_NAME),
   (
    14, DEF_NAME),
   (15, 'WSPeriod'),
   (
    16, DEF_NAME))), 
 'StereoGain':(
  (
   (
    1, DEF_NAME, 'UTIL'),
   (
    2, DEF_NAME),
   (
    3, 'Sig Sour', None, SELECT_TUPLE),
   (4, 'St.Sep'),
   (5, 'PhsInv L'),
   (6, 'PhsInv R'),
   (
    7, DEF_NAME),
   (
    8, DEF_NAME)),
  None), 
 'Vinyl':(
  (
   (1, 'Tracing ', 'TRACING'),
   (2, 'Trac Dri'),
   (3, 'Trac Fre'),
   (4, 'Trac Wid'),
   EMPTY_PARAM,
   EMPTY_PARAM,
   (9, 'GLb Driv', 'DRIVE')),
  ((5, 'Pinch On', 'PINCH'), (6, 'Pnc Driv'), (7, 'Pnc Freq.'), (8, 'Pnc Widt'), (10, 'Pnc Soft'),
 (11, 'Pnc Mono'), (12, 'Crackle ', 'CRACKLE'), (13, 'Crackle '))), 
 'Vocoder':(
  (
   (1, 'Lo.FLT BN', 'FILTER'),
   (2, 'Up.FLT BN'),
   (
    3, 'Frmt Sh', None, INT_VALUE),
   (4, 'FLT BW'),
   (5, 'Prc/Retr'),
   (6, 'Gt Thres'),
   EMPTY_PARAM,
   (7, 'Out Leve', 'LEVEL')),
  (
   (8, 'Att Time', 'ENVELOPE'),
   (9, 'Rel Time'),
   (10, 'Sens', 'Unvoiced'),
   (
    11, 'Speed', None, SELECT_TUPLE),
   (12, 'Level'),
   (
    13, 'Enhance', 'OUT/MIX', SELECT_TUPLE),
   (
    14, 'Mono/St', None, SELECT_TUPLE),
   (15, 'Dry/Wet')),
  (
   (16, 'Env Dept'),
   (17, 'RATE', 'NOISE'),
   (18, 'CRACKLE'),
   (19, 'Lower', 'PITCH DET'),
   (20, 'Upeer'),
   (
    21, 'Osc Pitc', 'OSC', INT_VALUE),
   (
    22, 'Osc Wave', None, SELECT_TUPLE),
   (23, 'Gain', 'EXT IN'))), 
 'Operator':{'bankGroups':(0, 1, 5, 9, 13, 17, 21, 24), 
  'params':(
   (
    (1, 'Algorith', 'MAIN', ('D>C>B>A', 'D-C>B>A', 'C>B+D)>A', 'D>C-B)>A', 'D>C>B-A', 'A+D>C>B', 'D-C-B>A', 'D>C+B>A', 'D>C-B-A', 'A+B+D>C', 'A+B+C+D')),
    (2, 'Transpos'),
    (
     3, DEF_NAME),
    (
     8, DEF_NAME),
    (
     9, DEF_NAME),
    (
     5, DEF_NAME),
    (
     4, DEF_NAME)),
   (
    (12, 'A On', 'OSC A'),
    (20, 'A Level'),
    (
     13, DEF_NAME, None, PARM_DELAY),
    (
     14, DEF_NAME, None, PARM_DELAY),
    (
     25, 'A Wave', None, SELECT_TUPLE),
    (
     17, DEF_NAME, 'A FIX', SELECT_TUPLE),
    (
     18, DEF_NAME),
    (
     19, 'AFixFQMu', None, SELECT_TUPLE)),
   (
    (29, 'Ae.Attack', 'A ENV'),
    (30, 'Ae.Init'),
    (31, 'Ae.Decay'),
    (33, 'Ae.Sustai'),
    (32, 'Ae.Peak'),
    (34, 'Ae.Releas'),
    EMPTY_PARAM,
    (
     16, 'AQuantiz', None, SELECT_TUPLE)),
   (
    (
     35, 'Ae.Mode', 'A ENV-M', SELECT_TUPLE),
    (36, 'Ae.Loop'),
    (
     37, 'Ae.Retrig', None, SELECT_TUPLE),
    (38, 'Ae.R<V'),
    EMPTY_PARAM,
    (15, 'AFreq<Ve', 'A MOD'),
    (21, 'A Retrig'),
    (22, 'A Phase')),
   ((23, 'A Lev<V', 'A MOD'), (24, 'A L<Key'), (26, 'A Feedb'), (27, 'A < Pe'), (28, 'A < LFO')),
   (
    (39, 'B On', 'OSC B'),
    (47, 'B Level'),
    (
     40, DEF_NAME, None, PARM_DELAY),
    (
     41, DEF_NAME, None, PARM_DELAY),
    (
     52, 'B Wave', None, SELECT_TUPLE),
    (
     44, DEF_NAME, 'B FIX', SELECT_TUPLE),
    (45, 'BFixFreq'),
    (
     46, 'BFixFreq', None, SELECT_TUPLE)),
   (
    (56, 'Be.Attack', 'B ENV'),
    (57, 'Be.Init'),
    (58, 'Be.Decay'),
    (60, 'Be.Sustai'),
    (59, 'Be.Peak'),
    (61, 'Be.Releas'),
    EMPTY_PARAM,
    (
     43, 'BQuantiz', None, SELECT_TUPLE)),
   (
    (
     62, 'Be.Mode', 'B ENV-M', SELECT_TUPLE),
    (63, 'Be.Loop'),
    (
     64, 'Be.Retrig', None, SELECT_TUPLE),
    (
     65, DEF_NAME),
    EMPTY_PARAM,
    (42, 'BFreq<Ve', 'B MOD'),
    (48, 'B Retrig'),
    (49, 'B Phase')),
   ((50, 'B Lev<V', 'B MOD'), (51, 'B Lev<K'), (53, 'B Feedb'), (54, 'B<Pe'), (55, 'B<LFO')),
   (
    (66, 'C On', 'OSC C'),
    (74, 'C Level'),
    (
     67, DEF_NAME, None, PARM_DELAY),
    (
     68, DEF_NAME, None, PARM_DELAY),
    (
     79, 'C Wave', None, SELECT_TUPLE),
    (
     71, DEF_NAME, 'C FIX', SELECT_TUPLE),
    (
     72, DEF_NAME),
    (
     73, 'CFixFQMu', None, SELECT_TUPLE)),
   (
    (
     83, 'Ce.Attack', 'C ENV', SELECT_TUPLE),
    (84, 'Ce.Init'),
    (85, 'Ce.Decay'),
    (87, 'Ce.Sustai'),
    (86, 'Ce.Peak'),
    (88, 'Ce.Releas'),
    EMPTY_PARAM,
    (
     70, 'CQuantiz', None, SELECT_TUPLE)),
   (
    (
     89, 'Ce.Mode', 'C ENV-M', SELECT_TUPLE),
    (90, 'Ce.Loop'),
    (
     91, 'Ce.Retrig', None, SELECT_TUPLE),
    (92, 'Ce.R<V'),
    (69, 'CFreq<Ve'),
    (75, 'C Retrig'),
    (76, 'C Phase')),
   ((77, 'C Lev<V', 'C MOD'), (78, 'C Lev<K'), (80, 'C Feedb'), (81, 'C<Pe'), (82, 'C<LFO')),
   (
    (93, 'D On', 'OSC D'),
    (101, 'D Level'),
    (
     94, DEF_NAME, None, PARM_DELAY),
    (
     95, DEF_NAME, None, PARM_DELAY),
    (
     106, 'D Wave', None, SELECT_TUPLE),
    (
     98, DEF_NAME, 'D FIX', SELECT_TUPLE),
    (
     99, DEF_NAME),
    (
     100, 'DFixFQMu', None, SELECT_TUPLE)),
   (
    (
     110, 'De.Attack', 'D ENV', SELECT_TUPLE),
    (
     111, 'De.Init', None, SELECT_TUPLE),
    (112, 'De.Decay'),
    (114, 'De.Sustai'),
    (113, 'De.Peak'),
    (115, 'De.Releas'),
    EMPTY_PARAM,
    (
     97, 'DQuantiz', None, SELECT_TUPLE)),
   (
    (
     116, 'De.Mode', 'D ENV-M', SELECT_TUPLE),
    (117, 'De.Loop'),
    (
     118, 'De.Retrig', None, SELECT_TUPLE),
    (119, 'De.R<V'),
    (96, 'DFreq<Ve'),
    (102, 'D Retrig'),
    (103, 'D Phase')),
   ((104, 'D Lev<V', 'D MOD'), (105, 'D Lev<K'), (107, 'D Feedb'), (108, 'D<Pe'), (109, 'D<LFO')),
   (
    (165, 'Filt On', 'FILTER'),
    (
     166, 'Filt Typ', None, SELECT_TUPLE),
    (167, 'Filt Fre'),
    (168, 'Filt Res'),
    (171, 'Fe Amoun', 'FLTR MOD'),
    (169, 'Filt<V'),
    (170, 'Filt<K'),
    (172, 'Filt<LFO')),
   (
    (173, 'FeAttack', 'F-ENV 1'),
    (
     174, DEF_NAME),
    (175, 'FeASlope'),
    (
     176, DEF_NAME),
    (
     177, DEF_NAME),
    (178, 'FeDSlope'),
    (179, 'FeSustai'),
    (180, 'FeReleas')),
   (
    (
     181, DEF_NAME, 'F-ENV 2'),
    (182, 'FeRSlope'),
    (
     183, DEF_NAME, None, SELECT_TUPLE),
    (
     184, DEF_NAME),
    (
     185, 'Fe Rtg', None, SELECT_TUPLE),
    (
     186, DEF_NAME)),
   (
    (
     187, 'ShaperTy', 'SHAPER', SELECT_TUPLE),
    (188, 'ShaperAm'),
    (189, 'ShaperAm')),
   ((122, 'PE.On', 'PITCH EV'), (123, 'PE.Attack'), (124, 'PE.Init'), (126, 'PE.Decay'),
 (127, 'PE.Peak'), (129, 'PE.Sustai'), (130, 'PE.Releas'), (131, 'PE.End')),
   (
    (137, 'PE.Amount', 'PTCH EV-2'),
    (125, 'PE.A Slop'),
    (128, 'PE.D Slop'),
    (132, 'PE.R Slop'),
    (
     133, 'PE.Mode', None, SELECT_TUPLE),
    (134, 'PE.Loop'),
    (
     135, 'PE.Retrig', None, SELECT_TUPLE),
    (136, 'PE.R<V')),
   (
    (138, 'PE.Amt A', 'PTCH MOD'),
    (139, 'PE.Dst B'),
    (140, 'PE.Amt B'),
    (
     120, DEF_NAME),
    (121, 'Time<Key')),
   (
    (
     141, DEF_NAME, 'LFO'),
    (
     142, DEF_NAME, None, SELECT_TUPLE),
    (
     143, 'LFORange', None, SELECT_TUPLE),
    (
     144, DEF_NAME),
    (
     145, DEF_NAME, None, SELECT_TUPLE),
    (147, 'LFORetri'),
    (
     148, DEF_NAME),
    (146, 'LFO RT<K')),
   ((149, 'LFOAmtA', 'LFO MOD'), (150, 'LFODstB'), (151, 'LFOAmtB'), (152, 'LFO<V'), (153, 'LFO<Pe')),
   ((154, 'LE.Attack', 'LFO ENV'), (155, 'LE.Init'), (156, 'LE.Decay'), (157, 'LE.Peak'),
 (158, 'LE.Sustai'), (159, 'LE.Releas'), (160, 'LE.End')),
   (
    (
     161, 'LE.Mode', 'LFO ENV-M', SELECT_TUPLE),
    (162, 'LE.Loop'),
    (
     163, 'LE.Retrig', None, SELECT_TUPLE),
    (164, 'LE.R<V')))}, 
 'InstrumentGroupDevice':(
  (
   (
    1, DEF_NAME),
   (
    2, DEF_NAME),
   (
    3, DEF_NAME),
   (
    4, DEF_NAME),
   (
    5, DEF_NAME),
   (
    6, DEF_NAME),
   (
    7, DEF_NAME),
   (
    8, DEF_NAME)),
  ((9, 'ChainSel'), None)), 
 'OriginalSimpler':(
  (
   (
    1, DEF_NAME, 'SAMPE'),
   (2, 'Sampl.Sel'),
   (3, 'S Start'),
   (4, 'S Length'),
   (5, 'S Loop O'),
   (6, 'S Loop L'),
   (7, 'S Loop F'),
   (8, 'Spread')),
  (
   (25, 'FLT On', 'FILTER'),
   (
    26, 'FLT Type', None, SELECT_TUPLE),
   (27, 'FLT Freq'),
   (28, 'FLT Res'),
   EMPTY_PARAM,
   (30, 'FLT<Env')),
  ((29, 'On', 'FLTR ENV'), (31, 'Attack'), (32, 'Decay'), (33, 'Sustain'), (34, 'Release'),
 (35, 'Filt<Key'), (36, 'Filt<V'), (37, 'Filt<LFO')),
  ((21, 'Attack', 'AMP ENV'), (22, 'Decay'), (23, 'Sustain'), (24, 'Release'), (38, 'L On')),
  ((14, 'Pe On', 'PITCH'), (9, 'Glide Mo'), (10, 'Glide Ti'), (11, 'Transpos'), (12, 'Detune'),
 (13, 'Ptch<LFO'), (15, 'Volume', 'VOLUME'), (16, 'Vol<V')),
  ((17, 'Vol<LFO'), (18, 'Pan', 'PAN'), (19, 'Pan<Rnd'), (20, 'Pan<LFO'))), 
 'UltraAnalog':{'bankGroups':(0, 2, 4, 5, 7, 9, 11, 13, 16, 19, 21, 23), 
  'params':(
   (
    (29, 'On/Off', 'OSC 1'),
    (
     30, 'Shape', None, SELECT_TUPLE),
    (31, 'Octave'),
    (32, 'Semi'),
    (33, 'Mode'),
    (34, 'PEG1 Tim'),
    (35, 'OSC1 Det'),
    (43, 'OSC1 Lev')),
   ((37, 'OSC1 PW', 'OSC 1'), (38, 'Sub/Sync'), (39, 'Balance'), (40, 'PEG1 Amo', 'OSC 1 MOD'),
 (41, 'OSC1<LFO'), (42, 'PW<LFO'), (36, 'Keytrack')),
   (
    (96, 'O2 OnOff', 'OSC 2'),
    (
     97, 'O2 Shape', None, SELECT_TUPLE),
    (98, 'O2 Oct'),
    (99, 'O2 Semi'),
    (100, 'O2 Mode'),
    (101, 'PEG2Time'),
    (102, 'O2Detune'),
    (110, 'O2 Level')),
   ((104, 'PW', 'OSC 2'), (105, 'Sub/Sync'), (106, 'Balance'), (107, 'PEG2 Amo', 'OSC 1 MOD'),
 (108, 'OSC2<LFO'), (109, 'PW<LFO'), (103, 'Keytrack')),
   ((25, 'NoiseOnO', 'Noise'), (26, 'NoiseCol'), (27, 'NoiseBal'), (28, 'NoiseLev')),
   (
    (
     48, DEF_NAME, 'FILTER 1'),
    (50, 'F1 Res'),
    (44, 'F1 OnOff'),
    (
     45, DEF_NAME, None, SELECT_TUPLE),
    (
     46, DEF_NAME, None, SELECT_TUPLE),
    (
     51, DEF_NAME),
    EMPTY_PARAM,
    (53, 'F1FQ<Env', 'FL 1 MOD')),
   (
    (55, 'F1RES<En', 'FL 1 MOD'),
    EMPTY_PARAM,
    (47, 'F1FQ<Key'),
    (49, 'F1RES<Ke'),
    (52, 'F1FQ<LFO'),
    (54, 'F1RES<LF')),
   (
    (61, 'FEG1Atta', 'FL 1 ENV'),
    (62, 'FEG1 Dcy'),
    (64, 'FEG1Sust'),
    (65, 'FEG1STim'),
    (
     66, DEF_NAME),
    (
     56, DEF_NAME)),
   (
    (
     57, 'FEG1Loop', 'FL 1 ENV', SELECT_TUPLE),
    (58, 'FEG1Free'),
    (59, 'FEG1Lega'),
    (60, 'FEG1<V'),
    (63, 'FEG1<V')),
   (
    (
     115, DEF_NAME, 'FILTER 2'),
    (117, 'F2 Res'),
    (111, 'F2 OnOff'),
    (
     112, DEF_NAME, None, SELECT_TUPLE),
    (
     113, DEF_NAME, None, SELECT_TUPLE),
    (
     118, DEF_NAME),
    EMPTY_PARAM,
    (120, 'F2FQ<Env', 'FL 2 MOD')),
   (
    (122, 'F2RES<En', 'FL 2 MOD'),
    EMPTY_PARAM,
    (114, 'F2FQ<Key'),
    (116, 'F2RES<Ke'),
    (119, 'F2FQ<LFO'),
    (121, 'F2RES<LF')),
   (
    (128, 'FEG2Atta', 'FL 1 ENV'),
    (129, 'FEG2 Dcy'),
    (131, 'FEG2Sust'),
    (132, 'FEG2STim'),
    (
     133, DEF_NAME),
    (
     123, DEF_NAME)),
   (
    (
     124, 'FEG2Loop', 'FL 1 ENV', SELECT_TUPLE),
    (125, 'FEG2Free'),
    (126, 'FEG2Lega'),
    (127, 'FEG2 A<V'),
    (130, 'FEG2<V')),
   ((67, 'On/Off', 'AMP 1'), (71, 'Pan'), (69, 'Level'), (80, 'Attack', 'AMP1 ENV'), (81, 'Decay'),
 (83, 'Sustain'), (84, 'Sus Time'), (85, 'Release')),
   (
    (
     75, DEF_NAME, 'AMP1 ENV'),
    (
     76, 'AEG1Loop', None, SELECT_TUPLE),
    (77, 'AEG1Free'),
    (78, 'AEG1Lega'),
    (
     79, DEF_NAME),
    (
     82, DEF_NAME)),
   (
    (
     68, DEF_NAME, 'AMP1 MOD'),
    (
     70, DEF_NAME),
    (
     72, DEF_NAME),
    (
     73, DEF_NAME),
    (
     74, DEF_NAME)),
   ((134, 'On/Off', 'AMP 2'), (138, 'Pan'), (136, 'Level'), (147, 'Attack', 'AMP2 ENV'),
 (148, 'Decay'), (150, 'Sustain'), (151, 'Sus Time'), (152, 'Release')),
   (
    (142, 'AEG2 Exp', 'AMP2 ENV'),
    (
     143, 'AEG2 Loo', None, SELECT_TUPLE),
    (144, 'AEG2 Fre'),
    (145, 'AEG2 Leg'),
    (146, 'AEG2 A<V', 'AMP2 MOD'),
    (149, 'AEG2<V')),
   ((135, 'AMP2<Key', 'AMP2 MOD'), (137, 'Pan<Key'), (139, 'AMP2<LFO'), (140, 'Pan<LFO'),
 (141, 'Pan<Env')),
   (
    (
     86, 'LF1OnOff', 'LFO 1', SELECT_TUPLE),
    (
     87, 'LF1 SHP', None, SELECT_TUPLE),
    (
     88, 'LF1SncRa', None, SELECT_TUPLE),
    (89, 'LF1 Sync'),
    (90, 'LF1 Rtg'),
    (
     91, DEF_NAME)),
   ((92, 'LF1Speed', 'LFO 1'), (93, 'LF1Phase'), (94, 'LF1 Dly'), (95, 'LF1FdIn')),
   (
    (
     153, 'LF2OnOff', 'LFO 2', SELECT_TUPLE),
    (
     154, 'LF2 SHP', None, SELECT_TUPLE),
    (
     155, 'LF2SncRa', None, SELECT_TUPLE),
    (156, 'LF2 Sync'),
    (157, 'LF2 Rtg')),
   (
    (
     158, DEF_NAME, 'LFO 2'),
    (159, 'LF2Speed'),
    (160, 'LF2Phase'),
    (161, 'LF2 Dly'),
    (162, 'LF2FdIn')),
   (
    (
     1, DEF_NAME, 'VOI/TUNE'),
    (
     2, DEF_NAME),
    (
     3, DEF_NAME),
    (
     4, DEF_NAME, None, INT_VALUE),
    (
     5, DEF_NAME),
    (
     6, DEF_NAME)),
   ((7, 'On/Off', 'UNISON'), (8, 'Voices'), (9, 'Detune'), (10, 'Delay'), (11, 'Priority', 'KEY'),
 (12, 'Stretch'), (13, 'Error')),
   ((14, 'On/Off', 'VIBRATO'), (15, 'Speed'), (16, 'Fade-In'), (17, 'Amount'), (18, 'Error'),
 (19, 'Delay'), (20, 'Vib<MW')),
   ((21, 'GlideOnO'), (22, 'GlideTim'), (23, 'GlideMod'), (24, 'GlideLeg')))}, 
 'Collision':{'bankGroups':(0, 1, 3, 5, 10, 15, 17), 
  'params':(
   (
    (
     1, 'Structur', 'COLLISION', SELECT_TUPLE),
    (
     2, DEF_NAME, None, INT_VALUE),
    (
     3, DEF_NAME, None, SELECT_TUPLE),
    (
     4, 'Retrigge', None, SELECT_TUPLE),
    EMPTY_PARAM,
    (
     5, DEF_NAME)),
   (
    (
     6, 'On/Off', 'MALLET', SELECT_TUPLE),
    (7, 'Vol'),
    (8, 'Vel<VL'),
    (9, 'Vel<KY'),
    (10, 'Stiffnes'),
    (11, 'Stiff<VL'),
    (12, 'Stiff<KY'),
    (13, 'Noise AM')),
   (
    (14, 'NS A<VL', 'MALLET'),
    (15, 'NS A<KY'),
    (16, 'Ns Color'),
    (
     17, 'ON/OfF', 'NOISE', SELECT_TUPLE),
    (18, 'Vol'),
    (19, 'Vl<VL'),
    (20, 'Vl<KY')),
   (
    (
     21, 'FLT Type', 'NOIS FLT', SELECT_TUPLE),
    (22, 'FLT Freq'),
    (26, 'FLT Q'),
    (23, 'Fq<VL', 'NS FLT.MD'),
    (24, 'Fq<Key'),
    (25, 'Fq<Env')),
   ((27, 'Attack', 'NOIS ENV'), (28, 'Decay'), (29, 'Sustain'), (30, 'Release')),
   (
    (31, 'On/Off', 'RESNAT 1'),
    (
     32, 'Type', None, SELECT_TUPLE),
    (
     33, 'Quality', None, SELECT_TUPLE),
    (
     34, 'Tune', None, INT_VALUE),
    (
     35, 'Fine', None, INT_VALUE),
    (36, 'Tn<KY')),
   ((37, 'P.Env', 'RES1 PE'), (38, 'P.ENV<VL'), (39, 'P.ENV TIM'), (40, 'Decay', 'RES2 DEC'),
 (41, 'Decay<VL'), (42, 'Decay<KY'), (43, 'Off Deca')),
   ((44, 'Material', 'RESNAT 1'), (45, 'Mater<VL'), (46, 'Mater<KY'), (47, 'Radius'),
 (48, 'Radius<V'), (49, 'Radius<K'), (50, 'Ratio'), (51, 'Bright')),
   ((52, 'Bleed', 'RESNAT 1'), (53, 'Inharm'), (54, 'Inharm<V'), (55, 'Open'), (56, 'Open<VL'),
 (57, 'Hit'), (58, 'Hit<RAND')),
   ((59, 'LISTEN L', 'RESNAT 1'), (60, 'LISTEN R'), (61, 'Panorama'), (62, 'Pan<Key'),
 (63, 'Volume')),
   (
    (
     64, 'On/Off', 'RESNAT 2', SELECT_TUPLE),
    (
     65, 'Type', None, SELECT_TUPLE),
    (
     66, 'Quality', None, SELECT_TUPLE),
    (
     67, 'Tune', None, INT_VALUE),
    (
     68, 'Fine TUN', None, INT_VALUE),
    (69, 'Tune<KEY')),
   ((70, 'P.Env', 'RES2 PE'), (71, 'P.ENV<VL'), (72, 'P.ENV TIM'), (73, 'Decay', 'RES2 DEC'),
 (74, 'Decay<VL'), (75, 'Decay<KE'), (76, 'Off Deca')),
   ((77, 'Mater', 'RESNAT 2'), (78, 'Mater<VL'), (79, 'Mater<KE'), (80, 'Radius'), (81, 'Radius<V'),
 (82, 'Radius<K'), (83, 'Ratio'), (84, 'Brightne')),
   ((85, 'Bleed', 'RESNAT 2'), (86, 'Inharm'), (87, 'Inharm<V'), (88, 'Open'), (89, 'Open<VL'),
 (90, 'Hit'), (91, 'Hit<RAND')),
   ((92, 'LISTEN L', 'RESNAT 2'), (93, 'LISTEN R'), (94, 'Panorama'), (95, 'Pan<KEY'),
 (96, 'Vol')),
   (
    (
     97, 'LF1 On/O', 'LFO 1', SELECT_TUPLE),
    (
     98, 'LF1 Shap', None, SELECT_TUPLE),
    (
     99, 'LF1 Retr', None, SELECT_TUPLE),
    (
     100, 'LF1 Sync', None, SELECT_TUPLE),
    (101, 'LF1 Rate'),
    (
     102, 'LF1 Syn.R', None, SELECT_TUPLE),
    (103, 'LF1 RT<K'),
    (
     104, 'LF1 Off', None, UNICODE_VAL)),
   (
    (105, 'Depth', 'LFO 1'),
    (106, 'Depth<V'),
    (
     107, 'DST-A', None, SELECT_TUPLE),
    (108, 'DST-A AM'),
    (
     109, 'DST-B', None, SELECT_TUPLE),
    (110, 'DST-B AM')),
   (
    (
     111, 'On/Off', 'LFO 2', SELECT_TUPLE),
    (
     112, 'Shape', None, SELECT_TUPLE),
    (
     113, 'Retrig', None, SELECT_TUPLE),
    (
     114, 'Sync', None, SELECT_TUPLE),
    (115, 'Rate'),
    (
     116, 'Syn.Rt', None, SELECT_TUPLE),
    (117, 'RT<KEY'),
    (
     118, 'Off', None, UNICODE_VAL)),
   (
    (119, 'Dep', 'LFO 2'),
    (120, 'Dp<VL'),
    (
     121, 'Dst A', None, SELECT_TUPLE),
    (122, 'DST A AM'),
    (
     123, 'DST B', None, SELECT_TUPLE),
    (124, 'DST B AM')),
   (
    (
     125, 'DST A', 'PI BEND', SELECT_TUPLE),
    (126, 'DST AMT'),
    (
     127, 'DST A', 'MOD WHL', SELECT_TUPLE),
    (128, 'DST A AM'),
    (
     129, 'DST B', None, SELECT_TUPLE),
    (130, 'DST B AM')),
   (
    (
     131, 'DST A', 'AFTERTOUCH', SELECT_TUPLE),
    (132, 'DST AMT'),
    (
     133, 'DST B', None, SELECT_TUPLE),
    (134, 'DST B AM')))}, 
 'LoungeLizard':(
  (
   (
    1, DEF_NAME, 'ELECTRIC', INT_VALUE),
   (
    2, DEF_NAME),
   (
    3, DEF_NAME),
   (
    4, DEF_NAME, None, INT_VALUE),
   (
    5, DEF_NAME),
   (6, 'KBStretc')),
  ((7, 'Stiff', 'MALLET ST'), (8, 'Stif<KEY'), (9, 'Stif<V'), (10, 'Force', 'MAL FORCE'),
 (11, 'Frc<KEY'), (12, 'Frc<V')),
  ((13, 'Noise.Pi', 'NOISE'), (14, 'Noise.Dcy'), (15, 'Noise.Amt'), (16, 'Noise<Ke')),
  ((17, 'Release', 'FORK'), (18, 'TINE Dcy'), (19, 'TINE Vol'), (20, 'TINE<Key'), (21, 'TINE Col'),
 (22, 'Tone Dcy'), (23, 'Tone Vol')),
  (
   (24, 'Symm', 'PICKUP'),
   (25, 'Dist'),
   (
    26, 'Pic Mode', None, INT_VALUE),
   (27, 'Amp In'),
   (28, 'Amp Out'),
   (29, 'Amp<Key')),
  ((30, 'Damp Ton', 'DAMP'), (31, 'Damp Am'), (32, 'Damp Bal'))), 
 'InstrumentImpulse':{'bankGroups':(0, 1, 4, 7, 10, 13, 16, 19, 22), 
  'params':(
   (
    (1, 'GLVolume'),
    (
     2, DEF_NAME),
    (
     3, 'GLTransp', None, INT_VALUE)),
   (
    (4, 'Start', 'INST1'),
    (
     5, 'Transp', None, INT_VALUE),
    (6, 'TRNS<VEL'),
    (7, 'TRNS<RND'),
    (8, 'STR Mode'),
    (9, 'STR Fact'),
    (10, 'STR<VEL'),
    (11, 'Sat Drv')),
   (
    (
     12, 'FLT Type', 'INST1', SELECT_TUPLE),
    (13, 'FLT FRQ'),
    (14, 'FLT Res'),
    (15, 'FLT<VEL'),
    (16, 'FLT<RND'),
    (17, 'Env Type'),
    (18, 'Env Deca')),
   ((19, 'Pan', 'INST1'), (20, 'Pan<VEL'), (21, 'Pan<RND'), (22, 'Volume'), (23, 'VOL<VEL')),
   (
    (24, 'Start', 'INST2'),
    (
     25, 'Transp', None, INT_VALUE),
    (26, 'TRNS<VEL'),
    (27, 'TRNS<RND'),
    (
     28, 'STR Mode', None, SELECT_TUPLE),
    (29, 'STR Fact'),
    (30, 'STR<VEL'),
    (31, 'Sat Drv')),
   (
    (
     32, 'FLT Type', 'INST2', SELECT_TUPLE),
    (33, 'FLT FRQ'),
    (34, 'FLT Res'),
    (35, 'FLT<VEL'),
    (36, 'FLT<RND'),
    (
     37, 'Env Type', None, SELECT_TUPLE),
    (38, 'Env Deca')),
   ((39, 'Pan', 'INST2'), (40, 'Pan<VEL'), (41, 'Pan<RND'), (42, 'Volume'), (43, 'VOL<VEL')),
   (
    (44, 'Start', 'INST3'),
    (
     45, 'Transp', None, INT_VALUE),
    (46, 'TRNS<VEL'),
    (47, 'TRNS<RND'),
    (
     48, 'STR Mode', None, SELECT_TUPLE),
    (49, 'STR Fact'),
    (50, 'STR<VEL'),
    (51, 'Sat Drv')),
   (
    (
     52, 'FLT Type', 'INST3', SELECT_TUPLE),
    (53, 'FLT FRQ'),
    (54, 'FLT Res'),
    (55, 'FLT<VEL'),
    (56, 'FLT<RND'),
    (
     57, 'Env Type', None, SELECT_TUPLE),
    (58, 'Env Deca')),
   ((59, 'Pan', 'INST3'), (60, 'Pan<VEL'), (61, 'Pan<RND'), (62, 'Volume'), (63, 'VOL<VEL')),
   (
    (64, 'Start', 'INST4'),
    (
     65, 'Transp', None, INT_VALUE),
    (66, 'TRNS<VEL'),
    (67, 'TRNS<RND'),
    (
     68, 'STR Mode', None, SELECT_TUPLE),
    (69, 'STR Fact'),
    (70, 'STR<VEL'),
    (71, 'Sat Drv')),
   (
    (
     72, 'FLT Type', 'INST4', SELECT_TUPLE),
    (73, 'FLT FRQ'),
    (74, 'FLT Res'),
    (75, 'FLT<VEL'),
    (76, 'FLT<RND'),
    (
     77, 'Env Type', None, SELECT_TUPLE),
    (78, 'Env Deca')),
   ((79, 'Pan', 'INST4'), (80, 'Pan<VEL'), (81, 'Pan<RND'), (82, 'Volume'), (83, 'VOL<VEL')),
   (
    (84, 'Start', 'INST4'),
    (
     85, 'Transp', None, INT_VALUE),
    (86, 'TRNS<VEL'),
    (87, 'TRNS<RND'),
    (
     88, 'STR Mode', None, SELECT_TUPLE),
    (89, 'STR Fact'),
    (90, 'STR<VEL'),
    (91, 'Sat Drv')),
   (
    (
     92, 'FLT Type', 'INST5', SELECT_TUPLE),
    (93, 'FLT FRQ'),
    (94, 'FLT Res'),
    (95, 'FLT<VEL'),
    (96, 'FLT<RND'),
    (
     97, 'Env Type', None, SELECT_TUPLE),
    (98, 'Env Deca')),
   ((99, 'Pan', 'INST5'), (100, 'Pan<VEL'), (101, 'Pan<RND'), (102, 'Volume'), (103, 'VOL<VEL')),
   (
    (104, 'Start', 'INST5'),
    (
     105, 'Transp', None, INT_VALUE),
    (106, 'TRNS<VEL'),
    (107, 'TRNS<RND'),
    (
     108, 'STR Mode', None, SELECT_TUPLE),
    (109, 'STR Fact'),
    (110, 'STR<VEL'),
    (111, 'Sat Drv')),
   (
    (
     112, 'FLT Type', 'INST6', SELECT_TUPLE),
    (113, 'FLT FRQ'),
    (114, 'FLT Res'),
    (115, 'FLT<VEL'),
    (116, 'FLT<RND'),
    (
     117, 'Env Type', None, SELECT_TUPLE),
    (118, 'Env Deca')),
   ((119, 'Pan', 'INST6'), (120, 'Pan<VEL'), (121, 'Pan<RND'), (122, 'Volume'), (123, 'VOL<VEL')),
   (
    (124, 'Start', 'INST7'),
    (
     125, 'Transp', None, INT_VALUE),
    (126, 'TRNS<VEL'),
    (127, 'TRNS<RND'),
    (
     128, 'STR Mode', None, SELECT_TUPLE),
    (129, 'STR Fact'),
    (130, 'STR<VEL'),
    (131, 'Sat Drv')),
   (
    (
     132, 'FLT Type', 'INST7', SELECT_TUPLE),
    (133, 'FLT FRQ'),
    (134, 'FLT Res'),
    (135, 'FLT<VEL'),
    (136, 'FLT<RND'),
    (
     137, 'Env Type', None, SELECT_TUPLE),
    (138, 'Env Deca')),
   ((139, 'Pan'), (140, 'Pan<VEL', 'INST7'), (141, 'Pan<RND'), (142, 'Volume'), (143, 'VOL<VEL')),
   (
    (144, 'Start', 'INST8'),
    (
     145, 'Transp', None, INT_VALUE),
    (146, 'TRNS<VEL'),
    (147, 'TRNS<RND'),
    (
     148, 'STR Mode', None, SELECT_TUPLE),
    (149, 'STR Fact'),
    (150, 'STR<VEL'),
    (151, 'Sat Drv')),
   (
    (
     152, 'FLT Type', 'INST8', SELECT_TUPLE),
    (153, 'FLT FRQ'),
    (154, 'FLT Res'),
    (155, 'FLT<VEL'),
    (156, 'FLT<RND'),
    (
     157, 'Env Type', None, SELECT_TUPLE),
    (158, 'Env Deca')),
   ((159, 'Pan', 'INST8'), (160, 'Pan<VEL'), (161, 'Pan<RND'), (162, 'Volume'), (163, 'VOL<VEL')))}, 
 'MultiSampler':{'bankGroups':(0, 5), 
  'params':(
   (
    (
     1, DEF_NAME, 'SAMPLE', SELECT_TUPLE),
    (
     2, DEF_NAME, None, SELECT_TUPLE),
    (3, 'S.Selecto'),
    (
     4, DEF_NAME, None, SELECT_TUPLE),
    (
     5, DEF_NAME),
    (
     6, 'KeyZ Shf', None, INT_VALUE),
    (
     7, 'Gld Mode', 'GLIDE', SELECT_TUPLE),
    (8, 'Gld Time')),
   (
    (
     9, 'Time', 'TIME', INT_VALUE),
    (
     10, 'Time<Key', None, INT_VALUE),
    (
     11, 'Transpos', 'PITCH', INT_VALUE),
    (
     12, 'Detune', None, INT_VALUE),
    (13, 'Pi<LFO'),
    (
     14, 'Pe On', None, SELECT_TUPLE)),
   (
    (15, 'Volume', 'VOLUME'),
    (16, 'Vol<Vel'),
    (17, 'Vol<LFO'),
    EMPTY_PARAM,
    EMPTY_PARAM,
    (18, 'Pan', 'PAN'),
    (19, 'Pan<Rnd'),
    (20, 'Pan<LFO')),
   ((21, 'Attack', 'AMP ENV'), (22, 'Init'), (23, 'A Slope'), (24, 'Decay'), (25, 'Peak'),
 (26, 'D Slope'), (27, 'Sustain'), (28, 'Release')),
   (
    (29, 'Ve.R Slop', 'AMP ENV'),
    (
     30, 'Mode', None, SELECT_TUPLE),
    (
     31, 'Loop', None, SELECT_TUPLE),
    (
     32, 'Retrig', None, SELECT_TUPLE),
    (33, 'R<Vel')),
   (
    (34, 'On', 'FILTER'),
    (
     35, 'Type', None, SELECT_TUPLE),
    (36, 'Freq'),
    (37, 'Res'),
    (38, 'Morph'),
    (
     39, 'Fe On', None, SELECT_TUPLE),
    (
     40, 'Fe<Env', None, INT_VALUE)),
   (
    (41, 'Fe Att', 'FLTR ENV'),
    (
     42, 'Fe Init', None, INT_VALUE),
    (
     43, 'Fe A.Sl', None, INT_VALUE),
    (44, 'Fe Decay'),
    (
     45, 'Fe Peak', None, INT_VALUE),
    (
     46, 'Fe D.Sl', None, INT_VALUE),
    (47, 'Fe Sust'),
    (48, 'Fe Rel')),
   (
    (49, 'Fe End', 'FLTR ENV'),
    (50, 'Fe R Slo'),
    (
     51, 'Fe Mode', None, SELECT_TUPLE),
    (52, 'Fe Loop'),
    (
     53, 'Fe Retri', None, SELECT_TUPLE)),
   ((54, 'Fe R<Vel', 'FENV MOD'), (55, 'Filt<Key'), (56, 'Filt<Vel'), (57, 'Filt<LFO')),
   (
    (
     58, DEF_NAME, 'SHAPE', SELECT_TUPLE),
    (
     59, DEF_NAME, None, SELECT_TUPLE),
    (
     60, DEF_NAME, None, SELECT_TUPLE),
    (
     61, DEF_NAME, None, SELECT_TUPLE),
    (
     62, DEF_NAME, None, SELECT_TUPLE)))}, 
 'StringStudio':{'bankGroups':(0, 4, 6, 8, 10, 11, 14), 
  'params':(
   (
    (
     1, DEF_NAME, 'TENSION', SELECT_TUPLE),
    (
     2, DEF_NAME, None, INT_VALUE),
    (
     3, DEF_NAME, None, INT_VALUE),
    (
     4, DEF_NAME, None, INT_VALUE),
    (5, 'FineTune'),
    (
     6, 'Key Prio', None, SELECT_TUPLE),
    EMPTY_PARAM,
    (
     97, DEF_NAME)),
   (
    (7, 'Uni On/O', 'UNISON', ('OFF', 'ON')),
    (
     8, 'Uni Voic', None, SELECT_TUPLE),
    (9, 'Uni Detu'),
    (10, 'Uni Dela'),
    (11, 'Stretch'),
    (12, 'Error')),
   ((13, 'Vib On/O', 'VIBRATO', ('OFF', 'ON')), (14, 'Vib Spee'), (15, 'Vib Fade'), (16, 'Vib Amou'),
 (17, 'Vib Erro'), (18, 'Vib Dela'), (19, 'Vib<ModW')),
   (
    (20, 'Port.On/O', 'PORTAMENT', ('OFF', 'ON')),
    (21, 'Port.Time'),
    (
     22, 'Port.Prop', None, SELECT_TUPLE),
    (
     23, 'Port.Leg', None, SELECT_TUPLE)),
   (
    (32, 'On/Off', 'EXICTER', ('OFF', 'ON')),
    (
     33, 'Type', None, SELECT_TUPLE),
    (34, 'Protrusi'),
    (37, 'Stiffnes'),
    (40, 'Velocity'),
    (24, 'Position'),
    (43, 'Damping'),
    (25, 'Fix Posi', None, ('OFF', 'ON'))),
   ((35, 'Prot<KEY', 'EXITE MD'), (36, 'Prot<V'), (38, 'Stif<KEY'), (39, 'Stif<V'), (41, 'Vel<KEY'),
 (42, 'Vel<V'), (26, 'Pos<KEY'), (27, 'Pos<V')),
   ((46, 'On/OFF', 'DAMPER', ('OFF', 'ON')), (47, 'Mass'), (49, 'Stiffnes'), (51, 'Velocity'),
 (28, 'Position'), (53, 'Damping'), (29, 'FIX POS', None, ('OFF', 'ON')), (54, ' Gated', None, ('OFF', 'ON'))),
   ((48, 'Mass<KEY', 'DAMPER MD'), (50, 'Stiff<KE'), (52, 'Velo<KEY'), (30, 'Pos<Key'),
 (31, 'Pos<Vel')),
   ((44, 'On/Off', 'PICK', ('OFF', 'ON')), (45, 'Position'), (61, 'On/Off', 'TREMOLO', ('OFF', 'ON')),
 (62, 'Fng.Stiff'), (63, 'Mass'), (64, 'Mas<Key'), (65, 'Mas<Vel'), (66, 'Frt.Stf')),
   (
    (55, 'Dampin', 'STRING'),
    (57, 'Decay'),
    (59, 'DecyRate'),
    (60, 'Inharmon'),
    EMPTY_PARAM,
    EMPTY_PARAM,
    (56, 'Damp<KEY', 'STR MOD'),
    (58, 'Decay<KE')),
   (
    (67, 'LFO.On/Of', 'LFO', ('OFF', 'ON')),
    (
     68, 'LFO.Shape', None, SELECT_TUPLE),
    (70, 'LFO.SyncO', None, ('OFF', 'ON')),
    (
     69, 'LF.SynRat', None, SELECT_TUPLE),
    (71, 'LFO Dela'),
    (72, 'LFO Spd'),
    (73, 'LFO Fade')),
   (
    (74, 'On/Off', 'FILTER', ('OFF', 'ON')),
    (
     75, 'Type', None, SELECT_TUPLE),
    (76, 'Freq'),
    (80, 'Reso')),
   ((77, 'FRQ<Key', 'FILTER MD'), (78, 'FRQ<LFO'), (79, 'FRQ<Env'), (81, 'Res<Key'), (82, 'Res<LFO'),
 (83, 'Res<Env')),
   ((84, 'On/Off', 'FEG', ('OFF', 'ON')), (85, 'Attack'), (86, 'Decay'), (87, 'Sustain'),
 (88, 'Release'), (89, 'Att<Vel'), (90, 'FEG<Vel')),
   (
    (91, 'On/Off', 'BODY', ('OFF', 'ON')),
    (
     92, 'Type', None, SELECT_TUPLE),
    (
     93, 'Size', None, SELECT_TUPLE),
    (94, 'Decay'),
    (95, 'Lo Cut'),
    (96, 'Hi Cut'),
    (98, 'Mix')))}, 
 'MidiArpeggiator':(
  (
   (
    1, 'Style', 'ARP', SELECT_TUPLE),
   (
    2, 'Offset', None, INT_VALUE),
   (
    3, 'Repeats', None, INT_VALUE),
   (
    4, 'Sync On', None, SELECT_TUPLE),
   (
    5, 'Sync RT', None, SELECT_TUPLE),
   (
    6, 'Groove', None, SELECT_TUPLE),
   (7, 'Free Rat'),
   (8, 'Gate')),
  (
   (
    9, 'Retr.Mode', 'RETRIG', SELECT_TUPLE),
   (
    10, 'Ret. Int', None, INT_VALUE),
   (
    11, 'Hold On', 'HOLD', SELECT_TUPLE),
   (
    12, 'Trns Mod', 'TRANSPOSE', SELECT_TUPLE),
   (
    13, 'Trns Key', None, INT_VALUE),
   (14, 'Trns Ste'),
   (15, 'Trns Dist')),
  (
   (
    16, 'Velo On', 'Velocity', SELECT_TUPLE),
   (
    17, 'Vel.Retri', None, SELECT_TUPLE),
   (
    18, 'Vel.Decay', None, INT_VALUE),
   (
    19, 'Vel.Targe', None, SELECT_TUPLE))), 
 'MidiChord':(
  (
   (
    1, DEF_NAME, 'NOTE 1', INT_VALUE),
   (2, 'Velocity'),
   (
    3, DEF_NAME, 'NOTE 2', INT_VALUE),
   (4, 'Velocity'),
   (
    5, DEF_NAME, 'NOTE 3', INT_VALUE),
   (6, 'Velocity'),
   (
    7, DEF_NAME, 'NOTE 4', INT_VALUE),
   (8, 'Velocity')),
  (
   (
    9, DEF_NAME, 'NOTE 5', INT_VALUE),
   (10, 'Velocity'),
   (
    11, DEF_NAME, 'NOTE 6', INT_VALUE),
   (12, 'Velocity'))), 
 'MidiEffectGroupDevice':(
  (
   (
    1, DEF_NAME),
   (
    2, DEF_NAME),
   (
    3, DEF_NAME),
   (
    4, DEF_NAME),
   (
    5, DEF_NAME),
   (
    6, DEF_NAME),
   (
    7, DEF_NAME),
   (
    8, DEF_NAME)),
  (
   (
    9, 'ChainSel', None, INT_VALUE),
   None)), 
 'MidiNoteLength':(
  (
   (
    1, 'Trig Mod', None, SELECT_TUPLE),
   (
    2, DEF_NAME, None, SELECT_TUPLE),
   (
    3, 'Synced L', None, SELECT_TUPLE),
   (4, 'Time Len'),
   (5, 'Gate'),
   (6, 'On/Off-B'),
   (7, 'Dcy Time'),
   (8, 'Dcy Key ')),
  None), 
 'MidiPitcher':(
  (
   (
    1, DEF_NAME, None, INT_VALUE),
   (
    2, DEF_NAME, None, INT_VALUE),
   (
    3, DEF_NAME, None, INT_VALUE)),
  None), 
 'MidiRandom':(
  (
   (
    1, DEF_NAME),
   (
    2, DEF_NAME, None, INT_VALUE),
   (
    3, DEF_NAME, None, INT_VALUE),
   (
    4, DEF_NAME, None, SELECT_TUPLE),
   (
    5, DEF_NAME, None, SELECT_TUPLE)),
  None), 
 'MidiScale':(
  (
   (
    1, DEF_NAME, None, INT_VALUE),
   (
    2, 'Transpos', None, INT_VALUE),
   (
    3, DEF_NAME, None, SELECT_TUPLE),
   (
    4, DEF_NAME, None, INT_VALUE),
   (
    5, DEF_NAME, None, INT_VALUE)),
  (
   (
    6, 'Map 1', 'C', SELECT_TUPLE),
   (
    7, 'Map 2', 'C#', SELECT_TUPLE),
   (
    8, 'Map 3', 'D', SELECT_TUPLE),
   (
    9, 'Map 4', 'D#', SELECT_TUPLE),
   (
    10, 'Map 5', 'E', SELECT_TUPLE),
   (
    11, 'Map 6', 'F', SELECT_TUPLE)),
  (
   (
    12, 'Map 7', 'G', SELECT_TUPLE),
   (
    13, 'Map 8', 'G#', SELECT_TUPLE),
   (
    14, 'Map 9', 'A', SELECT_TUPLE),
   (
    15, 'Map 10', 'A#', SELECT_TUPLE),
   (
    16, 'Map 11', 'B', SELECT_TUPLE),
   (
    17, 'Map 12', 'C', SELECT_TUPLE))), 
 'MidiVelocity':(
  (
   (
    1, DEF_NAME),
   (
    2, DEF_NAME),
   (
    3, DEF_NAME, None, SELECT_TUPLE),
   (
    4, DEF_NAME, None, SELECT_TUPLE),
   (
    5, 'Operatio', None, SELECT_TUPLE),
   (
    6, DEF_NAME, None, INT_VALUE),
   (
    7, DEF_NAME, None, INT_VALUE),
   (
    8, DEF_NAME, None, INT_VALUE)),
  (
   (
    9, DEF_NAME, None, INT_VALUE),
   None))}
# okay decompiling scripts/ParameterUtil.pyc
