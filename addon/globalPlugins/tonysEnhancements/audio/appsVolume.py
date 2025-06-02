# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited, Tony Malykh, Bill Dengler
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import config
import globalVars
from logHandler import log
from pycaw.utils import AudioSession
import ui
from dataclasses import dataclass
from threading import Lock
from typing import NamedTuple
from .utils import AudioSessionCallback, DummyAudioSessionCallback
from comtypes import COMError


class VolumeAndMute(NamedTuple):
    volume: float
    mute: bool


_appVolumesCache: dict[int, VolumeAndMute] = {}
_appVolumesCacheLock = Lock()
_activeCallback: DummyAudioSessionCallback | None = None


def initialize() -> None:
    volume = config.conf["tonysEnhancements"]["applicationsSoundVolume"]
    muted = config.conf["tonysEnhancements"]["applicationsSoundMuted"]
    if muted:
        # Muted flag should not be persistent.
        config.conf["tonysEnhancements"]["applicationsSoundMuted"] = False
        muted = False
    _updateAppsVolumeImpl(volume / 100.0, muted, state=None)


def terminate():
    global _activeCallback
    if _activeCallback is not None:
        _activeCallback.unregister()
        _activeCallback = None


@dataclass(unsafe_hash=True)
class VolumeSetter(AudioSessionCallback):
    volumeAndMute: VolumeAndMute | None = None

    def getOriginalVolumeAndMute(self, pid: int) -> VolumeAndMute:
        try:
            with _appVolumesCacheLock:
                originalVolumeAndMute = _appVolumesCache[pid]
                del _appVolumesCache[pid]
        except KeyError:
            originalVolumeAndMute = VolumeAndMute(volume=1.0, mute=False)
        return originalVolumeAndMute

    def onSessionUpdate(self, session: AudioSession) -> None:
        pid = session.ProcessId
        simpleVolume = session.SimpleAudioVolume
        with _appVolumesCacheLock:
            if pid not in _appVolumesCache:
                _appVolumesCache[pid] = VolumeAndMute(
                    volume=simpleVolume.GetMasterVolume(),
                    mute=simpleVolume.GetMute(),
                )
        if pid != globalVars.appPid:
            simpleVolume.SetMasterVolume(self.volumeAndMute.volume, None)
            simpleVolume.SetMute(self.volumeAndMute.mute, None)

    def onSessionTerminated(self, session: AudioSession) -> None:
        pid = session.ProcessId
        simpleVolume = session.SimpleAudioVolume
        originalVolumeAndMute = self.getOriginalVolumeAndMute(pid)
        try:
            simpleVolume.SetMasterVolume(originalVolumeAndMute.volume, None)
            simpleVolume.SetMute(originalVolumeAndMute.mute, None)
        except (COMError, RuntimeError) as e:
            log.exception(f"Could not restore master volume of process {pid} upon exit: {e}")


def _updateAppsVolumeImpl(
    volume: float,
    muted: bool,
    state=None,
):
    global _activeCallback
    #if state.calculated() == AppsVolumeAdjusterFlag.DISABLED:
    if False:
        newCallback = DummyAudioSessionCallback()
        runTerminators = True
    else:
        newCallback = VolumeSetter(
            volumeAndMute=VolumeAndMute(
                volume=volume,
                mute=muted,
            ),
        )
        runTerminators = False
    if _activeCallback is not None:
        _activeCallback.unregister(runTerminators=runTerminators)
    _activeCallback = newCallback
    _activeCallback.register()


_VOLUME_ADJUSTMENT_DISABLED_MESSAGE: str = _(
    # Translators: error message when applications' volume is disabled
    "Application volume control disabled",
)


def _adjustAppsVolume(
    volumeAdjustment: int | None = None,
):
    volume: int = config.conf["tonysEnhancements"]["applicationsSoundVolume"]
    muted: bool = config.conf["tonysEnhancements"]["applicationsSoundMuted"]
    #state = config.conf["tonysEnhancements"]["applicationsVolumeMode"]
    volume += volumeAdjustment
    volume = max(0, min(100, volume))
    log.debug(f"Adjusting applications volume by {volumeAdjustment}% to {volume}%")
    config.conf["tonysEnhancements"]["applicationsSoundVolume"] = volume

    # We skip running terminators here to avoid application volume spiking to 100% for a split second.
    _updateAppsVolumeImpl(volume / 100.0, muted, state=None)
    # Translators: Announcing new applications' volume message
    msg = _("{} percent application volume").format(volume)
    ui.message(msg)


def _toggleAppsVolumeMute():
    state = config.conf["tonysEnhancements"]["applicationsVolumeMode"]
    volume: int = config.conf["tonysEnhancements"]["applicationsSoundVolume"]
    muted: bool = config.conf["tonysEnhancements"]["applicationsSoundMuted"]
    muted = not muted
    config.conf["tonysEnhancements"]["applicationsSoundMuted"] = muted
    _updateAppsVolumeImpl(volume / 100.0, muted, state)
    if muted:
        # Translators: Announcing new applications' mute status message
        msg = _("Muted other applications")
    else:
        # Translators: Announcing new applications' mute status message
        msg = _("Unmuted other applications")
    ui.message(msg)
