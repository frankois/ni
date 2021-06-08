# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/_NativeInstruments/Helpers.py
# Compiled at: 2021-05-19 16:16:29
# Size of source mod 2**32: 6820 bytes
import Live
from .Types import TrackType
from .Logger import log
PARAM_PREFIX_KK = 'NIKB'
PLUGIN_PREFIX_KK = 'Komplete Kontrol'
PLUGIN_CLASS_NAME_VST = 'PluginDevice'
PLUGIN_CLASS_NAME_AU = 'AuPluginDevice'

def song():
    """Returns the current song instance"""
    return Live.Application.get_application().get_document()


def scenes():
    """Returns a list of scenes"""
    return song().scenes


def scene(index):
    """Returns the selected scene (index) or None"""
    ss = scenes()
    if index < len(ss):
        return ss[index]


def visibleTracks():
    """Returns a list of visible tracks"""
    return song().visible_tracks


def returnTracks():
    """Returns a list of the return tracks"""
    return song().return_tracks


def masterTrack():
    return song().master_track


def returnTrack(index):
    """Returns the return track at the selected index or None if the index does not exist"""
    tracks = returnTracks()
    if index < len(tracks):
        return tracks[index]


def genericTrack(index):
    """Returns the track at the selected index or None if the index does not exist"""
    tracks = visibleTracks()
    if index < len(tracks):
        return tracks[index]


def track(trackType, index):
    """Returns the track of the selected type at the selected index or None if the index does not exist for the type"""
    if trackType == TrackType.MASTER:
        return masterTrack()
    if trackType == TrackType.RETURN:
        return returnTrack(index)
    if trackType != TrackType.EMPTY:
        return genericTrack(index)


def armTrack(index, state):
    """Sets the arm flag for the selected track"""
    t = genericTrack(index)
    if t is not None:
        if state is 1 or state is 0:
            t.arm = state


def muteTrack(trackType, index, state):
    """Sets the mute flag for the selected track of the selected type"""
    t = track(trackType, index)
    if t is not None:
        if trackType is not TrackType.MASTER:
            if state is 1 or state is 0:
                t.mute = state


def soloTrack(trackType, index, state):
    """Sets the solo flag for the selected track of the selected type"""
    t = track(trackType, index)
    if t is not None:
        if trackType is not TrackType.MASTER:
            if state is 1 or state is 0:
                t.solo = state


def tracksClipSlots():
    """Returns the list of each track clip slots in the song"""
    tracksClipSlots = []
    for track in Live.tracks():
        tracksClipSlots.append(track.clip_slots)

    return tracksClipSlots


def clips():
    """Returns a bidimensional list of all the clips in the song"""
    tracks = []
    for track in tracksClipSlots():
        trackClips = []
        for clipSlot in track:
            trackClips.append(clipSlot.clip)

        tracks.append(trackClips)

    return tracks


def clip(column, row):
    """Returns the clip at scene (s) in track (t) or None"""
    t = genericTrack(column)
    if t is not None:
        if len(t.clip_slots) > row:
            return t.clip_slots[row].clip


def clipName(t, s):
    """Returns the clip name or an empty string if the clip does not exist"""
    clip = Live.clip(t, s)
    if clip is not None:
        return str(clip.name)
    return ''


def fireClip(t, s):
    """Launches clip number (s) in track number (t)"""
    clip = Live.clip(t, s)
    if clip is not None:
        clip.fire()


def stopClip(t, s):
    """Stops clip number (s) in track (t)"""
    clip = Live.clip(t, s)
    if clip is not None:
        clip.stop()


def tempo():
    """Returns the current song tempo"""
    return song().tempo


def setTempo(tempo):
    """Sets the current song tempo"""
    if tempo is not None:
        song().tempo = tempo


def currentSongTime():
    """Returns the current song time"""
    return song().current_song_time


def setCurrentSongTime(time):
    """Sets the current song time"""
    if time is not None:
        song().current_song_time = time


def findInstrumentInDeviceList(devicelist):
    """Returns the instrument in the list of devices or None"""
    for device in devicelist:
        instr = findInstrument(device)
        if instr:
            return instr


def findInstrumentInChain(chain):
    """Returns the instrument in the device chain or None"""
    for device in chain.devices:
        instr = findInstrument(device)
        if instr:
            return instr


def findInstrument(device):
    """Returns the instrument for the selected device or None"""
    if device.type == 1:
        if device.can_have_chains:
            chains = device.chains
            for chain in chains:
                instr = findInstrumentInChain(chain)
                if instr:
                    return instr

        else:
            if device.class_name == PLUGIN_CLASS_NAME_VST or device.class_name == PLUGIN_CLASS_NAME_AU:
                if device.class_display_name.startswith(PLUGIN_PREFIX_KK):
                    parms = device.parameters
                    if parms:
                        if len(parms) > 1:
                            pn = parms[1].name
                            if pn.startswith(PARAM_PREFIX_KK):
                                return (
                                 str(device.class_display_name), str(pn))
        return (
         device.class_display_name, None)
    return


def checkForKKInstance(trackIndex):
    """Returns the Komplete Kontrol instance name if an instance is found, otherwise an empty string"""
    tracks = visibleTracks()
    if trackIndex < len(tracks):
        devices = tracks[trackIndex].devices
        instr = findInstrumentInDeviceList(devices)
        if instr:
            if instr[1] is not None:
                log('Selecting ' + str(instr[0]) + '[' + str(instr[1]) + '] on track[' + str(trackIndex) + ']')
                return str(instr[1])
    log('Selecting non KK track[' + str(trackIndex) + ']')
    return ''


def recordQuantizeGrid(grid):
    """Returns the current record quantization value"""
    if grid == Live.Clip.GridQuantization.g_eighth:
        return Live.Song.RecordingQuantization.rec_q_eight
    if grid == Live.Clip.GridQuantization.g_quarter:
        return Live.Song.RecordingQuantization.rec_q_quarter
    if grid == Live.Clip.GridQuantization.g_thirtysecond:
        return Live.Song.RecordingQuantization.rec_q_thirtysecond
    return Live.Song.RecordingQuantization.rec_q_sixtenth


def quantizeCurrentClip():
    """Quantize the current clip"""
    clip = song().view.detail_clip
    if clip is not None:
        grid = clip.view.grid_quantization
        if grid is not None:
            clip.quantize(recordQuantizeGrid(grid), 1.0)
# okay decompiling src/_NativeInstruments/Helpers.pyc
