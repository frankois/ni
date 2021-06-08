# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/_NativeInstruments/Messages.py
# Compiled at: 2021-05-19 16:21:05
# Size of source mod 2**32: 9435 bytes
from . import OSC
from . import Helpers
from .Types import TrackType, PlayingStatus, typeToString
from .Logger import log

def sizeInfo():
    """Returns the current song number of visible tracks, scenes and return channels"""
    address = '/live/size'
    numberOfVisibleTracks = len(Helpers.song().visible_tracks)
    numberOfScenes = len(Helpers.song().scenes)
    numberOfReturns = len(Helpers.song().return_tracks)
    return OSC.OSCMessage(address, (numberOfVisibleTracks, numberOfScenes, numberOfReturns))


def sessionAutomationRecord():
    """Returns the current state of session automation record"""
    address = '/live/session_automation_record'
    return OSC.OSCMessage(address, int(Helpers.song().session_automation_record))


def currentTrackIndex():
    """
    Returns the current track type and index
    (track type, track index)
    """
    address = '/live/track'
    selected_track = Helpers.song().view.selected_track
    if selected_track == Helpers.song().master_track:
        return OSC.OSCMessage(address, (TrackType.MASTER, 0, ''))
    for index, track in enumerate(Helpers.visibleTracks()):
        if track == selected_track:
            trackType = track.has_audio_input and TrackType.AUDIO or TrackType.MIDI
            if track.is_foldable:
                trackType = TrackType.GROUP
            return OSC.OSCMessage(address, (trackType, index, str(Helpers.checkForKKInstance(index))))

    for index, track in enumerate(Helpers.returnTracks()):
        if track == selected_track:
            return OSC.OSCMessage(address, (TrackType.RETURN, index, ''))

    log('currentTrackIndex: The track does not exist')


def currentSceneIndex():
    """
    Returns the current scene index
    (scene index)
    """
    address = '/live/scene'
    for index, scene in enumerate(Helpers.scenes()):
        if scene == Helpers.song().view.selected_scene:
            return OSC.OSCMessage(address, index)

    log('currentSceneIndex: The scene does not exist')


def trackVolume(trackType, trackIndex):
    """Returns the track volume"""
    address = '/live/volume'
    track = Helpers.track(trackType, trackIndex)
    if track is not None:
        return OSC.OSCMessage(address, (trackType, trackIndex, track.mixer_device.volume.value))
    log('trackVolume: The track does not exist (' + typeToString(trackType, TrackType) + ', ' + str(trackIndex) + ')')


def trackPan(trackType, trackIndex):
    """Returns the track pan"""
    address = '/live/pan'
    track = Helpers.track(trackType, trackIndex)
    if track is not None:
        return OSC.OSCMessage(address, (trackType, trackIndex, track.mixer_device.panning.value))
    log('trackPan: The track does not exist (' + typeToString(trackType, TrackType) + ', ' + str(trackIndex) + ')')


def trackSolo(trackType, trackIndex):
    """Returns the track solo state"""
    address = '/live/solo'
    track = Helpers.track(trackType, trackIndex)
    if track is not None:
        if trackType is not TrackType.MASTER:
            return OSC.OSCMessage(address, (trackType, trackIndex, track.solo))
    log('trackSolo: The track does not exist (' + typeToString(trackType, TrackType) + ', ' + str(trackIndex) + ')')


def trackMute(trackType, trackIndex):
    """Returns the track mute state"""
    address = '/live/mute'
    track = Helpers.track(trackType, trackIndex)
    if track is not None:
        if trackType is not TrackType.MASTER:
            return OSC.OSCMessage(address, (trackType, trackIndex, track.mute))
    log('trackMute: The track does not exist (' + typeToString(trackType, TrackType) + ', ' + str(trackIndex) + ')')


def trackSend(trackType, trackIndex, sendIndex):
    """Returns the track send level for the selected track and the selected send index"""
    address = '/live/send'
    track = Helpers.track(trackType, trackIndex)
    if track is not None:
        if len(track.mixer_device.sends) > sendIndex:
            if trackType is not TrackType.MASTER:
                sendValue = track.mixer_device.sends[sendIndex].value
                return OSC.OSCMessage(address, (trackType, trackIndex, sendIndex, sendValue))
    log('trackSend: The track or send index does not exist (' + typeToString(trackType, TrackType) + ', ' + str(trackIndex) + ', ' + str(sendIndex) + ')')


def trackSends(trackType, trackIndex):
    """Returns the track send levels for the selected track"""
    address = '/live/send'
    track = Helpers.track(trackType, trackIndex)
    if track is not None:
        if trackType is not TrackType.MASTER:
            bundle = OSC.OSCBundle()
            for sendIndex, send in enumerate(track.mixer_device.sends):
                sendValue = send.value
                bundle.append(address, (trackType, trackIndex, sendIndex, sendValue))

            return bundle
    log('trackSends: The track does not exist (' + typeToString(trackType, TrackType) + ', ' + str(trackIndex) + ')')


def trackInfo(trackType, trackIndex):
    """
    Return basic track information
    (track index, type, name, color, armed, solo, mute, volume, panning)
    """
    address = '/live/track/info'
    track = Helpers.track(trackType, trackIndex)
    if track is None:
        log('trackInfo: The track does not exist (' + typeToString(trackType, TrackType) + ', ' + str(trackIndex) + ')')
        return
    if trackType is TrackType.GENERIC:
        trackType = track.has_audio_input and TrackType.AUDIO or TrackType.MIDI
        if track.is_foldable:
            trackType = TrackType.GROUP
    arm = 0
    if trackType is TrackType.AUDIO or trackType is TrackType.MIDI:
        arm = track.arm and 1 or 0
    solo = track.solo and 1 or 0
    mute = track.mute and 1 or 0
    volume = track.mixer_device.volume.value
    panning = track.mixer_device.panning.value
    name = str(track.name)
    color = int(track.color)
    return OSC.OSCMessage(address, (trackType, trackIndex, name, color, arm, solo, mute, volume, panning))


def trackArm(trackIndex):
    """
    Return basic track information
    (track index, type, name, color, armed, solo, mute, volume, panning)
    """
    address = '/live/track/arm'
    arm = 0
    if not track.is_foldable:
        arm = track.arm and 1 or 0
    return OSC.OSCMessage(address, (trackIndex, arm))


def loop():
    """Return the current loop state"""
    address = '/live/loop'
    return OSC.OSCMessage(address, Helpers.song().loop and 1 or 0)


def clipInfo(trackIndex, sceneIndex):
    """
    Returns basic clip information
    (track index, scene index, clip name, clip color)
    """
    address = '/live/clip/info'
    clip = Helpers.clip(trackIndex, sceneIndex)
    if clip is None:
        log('clipInfo: The clip at (' + str(trackIndex) + ', ' + str(sceneIndex) + ') does not exist')
        return
    clipName = str(clip.name)
    clipColor = int(clip.color)
    return OSC.OSCMessage(address, (trackIndex, sceneIndex, clipName, clipColor))


def clipStatus(trackIndex, sceneIndex):
    """
    Returns clip status
    (track index, scene index, playing status, is looping, length, position, loop start, loop end)
    """
    address = '/live/clip/status'
    clip = Helpers.clip(trackIndex, sceneIndex)
    if clip is None:
        log('clipInfo: The clip at (' + str(trackIndex) + ', ' + str(sceneIndex) + ') does not exist')
        return
    playingStatus = PlayingStatus.READY
    if clip.is_triggered == 1:
        playingStatus = PlayingStatus.TRIGGERED
    if clip.is_playing == 1:
        playingStatus = PlayingStatus.PLAYING
    if clip.is_recording == 1:
        playingStatus = PlayingStatus.RECORDING
    length = clip.length
    position = clip.playing_position
    looping = clip.looping and 1 or 0
    warping = clip.is_audio_clip and clip.warping and 1 or 0
    loopStart = clip.loop_start
    loopEnd = clip.loop_end
    return OSC.OSCMessage(address, (
     trackIndex, sceneIndex, playingStatus, looping, warping, length, position, loopStart, loopEnd))


def clipRemoved(trackIndex, sceneIndex):
    """Returns the coordinates of the clip that was removed (track index, scene index)"""
    address = '/live/clip/removed'
    clip = Helpers.clip(trackIndex, sceneIndex)
    if clip is not None:
        log('clipRemoved: The clip at (' + str(trackIndex) + ', ' + str(sceneIndex) + ') has not been removed')
        return
    return OSC.OSCMessage(address, (trackIndex, sceneIndex))


def clipPitch(trackIndex, sceneIndex):
    """Returns the pitch of the selected clip"""
    address = '/live/clip/pitch'
    clip = Helpers.clip(trackIndex, sceneIndex)
    if clip is not None:
        return OSC.OSCMessage(address, (trackIndex, sceneIndex, clip.pitch_coarse, clip.pitch_fine))
    log('clipPitch: The clip does not exist (' + str(trackIndex) + ', ' + str(sceneIndex) + ')')


def tempo():
    """Returns the current song number of visible tracks, scenes and return channels"""
    address = '/live/tempo'
    return OSC.OSCMessage(address, Helpers.tempo())
# okay decompiling src/_NativeInstruments/Messages.pyc
