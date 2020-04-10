# -*- coding: UTF-8 -*-
#A part of  Tony's Enhancements addon for NVDA
#Copyright (C) 2019 Tony Malykh
#This file is covered by the GNU General Public License.
#See the file COPYING.txt for more details.

import addonHandler
import api
import bisect
import collections
import config
import controlTypes
import core
import copy
import ctypes
from ctypes import create_string_buffer, byref
import documentBase
import editableText
import globalPluginHandler
import gui
from gui import guiHelper, nvdaControls
import inputCore
import itertools
import json
import keyboardHandler
from logHandler import log
import NVDAHelper
from NVDAObjects import behaviors
from NVDAObjects.window import winword
import nvwave
import operator
import os
import re
import sayAllHandler
from scriptHandler import script, willSayAllResume
import speech
import struct
import textInfos
import threading
import time
import tones
import types
import ui
import watchdog
import wave
import winUser
import wx

winmm = ctypes.windll.winmm


debug = False
if debug:
    import threading
    LOG_FILE_NAME = "C:\\Users\\tony\\Dropbox\\1.txt"
    f = open(LOG_FILE_NAME, "w")
    f.close()
    LOG_MUTEX = threading.Lock()
    def mylog(s):
        with LOG_MUTEX:
            f = open(LOG_FILE_NAME, "a")
            print(s, file=f)
            f.close()
else:
    def mylog(*arg, **kwarg):
        pass

def myAssert(condition):
    if not condition:
        raise RuntimeError("Assertion failed")

defaultDynamicKeystrokes = """
*:F1
*:F2
*:F3
*:F4
*:F5
*:F6
*:F7
*:F8
*:F9
*:F9
*:F10
*:F11
*:F12
code:Alt+DownArrow
code:Alt+UpArrow
code:Alt+Home
code:Alt+End
code:Alt+PageUp
code:Alt+PageDown
""".strip()

module = "tonysEnhancements"
def initConfiguration():
    confspec = {
        "blockDoubleInsert" : "boolean( default=False)",
        "blockDoubleCaps" : "boolean( default=False)",
        "consoleRealtime" : "boolean( default=False)",
        "consoleBeep" : "boolean( default=False)",
        "nvdaVolume" : "integer( default=100, min=0, max=100)",
        "busyBeep" : "boolean( default=False)",
        "dynamicKeystrokesTable" : f"string( default='{defaultDynamicKeystrokes}')",
        "fixWindowNumber" : "boolean( default=False)",
        "detectInsertMode" : "boolean( default=False)",
        "overrideMoveByWord" : "boolean( default=False)",
        "suppressUnselected" : "boolean( default=False)",
    }
    config.conf.spec[module] = confspec

def getConfig(key):
    value = config.conf[module][key]
    return value
def setConfig(key, value):
    config.conf[module][key] = value


def parseDynamicKeystrokes(s):
    result = set()
    for line in s.splitlines():
        tokens = line.strip().split(":")
        if (len(tokens) == 0) or (len(line) == 0):
            continue
        if len(tokens) != 2:
            raise ValueError(f"Dynamic shortcuts configuration: invalid line: {line}")
        app = tokens[0]
        try:
            kb = keyboardHandler.KeyboardInputGesture.fromName(tokens[1]).normalizedIdentifiers[0]
        except (KeyError, IndexError):
            raise ValueError(f"Invalid kb shortcut {tokens[1]} ")
        result.add((app, kb))
    return result

dynamicKeystrokes = None
def reloadDynamicKeystrokes():
    global dynamicKeystrokes
    dynamicKeystrokes = parseDynamicKeystrokes(getConfig("dynamicKeystrokesTable"))

addonHandler.initTranslation()
initConfiguration()
reloadDynamicKeystrokes()

class SettingsDialog(gui.SettingsDialog):
    # Translators: Title for the settings dialog
    title = _("Tony's enhancements  settings")

    def __init__(self, *args, **kwargs):
        super(SettingsDialog, self).__init__(*args, **kwargs)

    def makeSettings(self, settingsSizer):
        sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

      # checkbox Detect insert mode
        # Translators: Checkbox for insert mode detection
        label = _("Detect insert mode in text documents and beep on every keystroke when insert mode is on.")
        self.detectInsertModeCheckbox = sHelper.addItem(wx.CheckBox(self, label=label))
        self.detectInsertModeCheckbox.Value = getConfig("detectInsertMode")


      # checkbox block double insert
        # Translators: Checkbox for block double insert
        label = _("Block double insert")
        self.blockDoubleInsertCheckbox = sHelper.addItem(wx.CheckBox(self, label=label))
        self.blockDoubleInsertCheckbox.Value = getConfig("blockDoubleInsert")
      # checkbox block double caps
        # Translators: Checkbox for block double caps
        label = _("Block double Caps Lock")
        self.blockDoubleCapsCheckbox = sHelper.addItem(wx.CheckBox(self, label=label))
        self.blockDoubleCapsCheckbox.Value = getConfig("blockDoubleCaps")
      # checkbox console realtime
        # Translators: Checkbox for realtime console
        label = _("Speak console output in realtime")
        self.consoleRealtimeCheckbox = sHelper.addItem(wx.CheckBox(self, label=label))
        self.consoleRealtimeCheckbox.Value = getConfig("consoleRealtime")
      # checkbox console beep
        # Translators: Checkbox for console beep on update
        label = _("Beep on update in consoles")
        self.consoleBeepCheckbox = sHelper.addItem(wx.CheckBox(self, label=label))
        self.consoleBeepCheckbox.Value = getConfig("consoleBeep")
      # checkbox Busy beep
        # Translators: Checkbox for busy beep
        label = _("Beep when NVDA is busy")
        self.busyBeepCheckbox = sHelper.addItem(wx.CheckBox(self, label=label))
        self.busyBeepCheckbox.Value = getConfig("busyBeep")
      # checkbox fix windows+Number
        # Translators: Checkbox for windows_Number
        label = _("Fix focus being stuck in the taskbar when pressing Windows+Number")
        self.fixWindowNumberCheckbox = sHelper.addItem(wx.CheckBox(self, label=label))
        self.fixWindowNumberCheckbox.Value = getConfig("fixWindowNumber")

      # checkbox override move by word
        # Translators: Checkbox for override move by word
        label = _("Use enhanced move by word commands for control+LeftArrow/RightArrow in editables.")
        self.overrideMoveByWordCheckbox = sHelper.addItem(wx.CheckBox(self, label=label))
        self.overrideMoveByWordCheckbox.Value = getConfig("overrideMoveByWord")

      # checkbox suppress unselected
        # Translators: Checkbox for suppress unselected
        label = _("Suppress saying of 'unselected'.")
        self.suppressUnselectedCheckbox = sHelper.addItem(wx.CheckBox(self, label=label))
        self.suppressUnselectedCheckbox.Value = getConfig("suppressUnselected")

      # NVDA volume slider
        sizer=wx.BoxSizer(wx.HORIZONTAL)
        # Translators: slider to select NVDA  volume
        label=wx.StaticText(self,wx.ID_ANY,label=_("NVDA volume"))
        slider=wx.Slider(self, wx.NewId(), minValue=0,maxValue=100)
        slider.SetValue(getConfig("nvdaVolume"))
        sizer.Add(label)
        sizer.Add(slider)
        settingsSizer.Add(sizer)
        self.nvdaVolumeSlider = slider
      # Dynamic keystrokes table
        # Translators: Label for dynamic keystrokes table edit box
        self.dynamicKeystrokesEdit = gui.guiHelper.LabeledControlHelper(self, _("Dynamic keystrokes table - see add-on documentation for more information"), wx.TextCtrl, style=wx.TE_MULTILINE).control
        self.dynamicKeystrokesEdit.Value = getConfig("dynamicKeystrokesTable")

    def onOk(self, evt):
        try:
            parseDynamicKeystrokes(self.dynamicKeystrokesEdit.Value)
        except Exception as e:
            self.dynamicKeystrokesEdit.SetFocus()
            ui.message(f"Error parsing dynamic keystrokes table: {e}")
            return

        setConfig("blockDoubleInsert", self.blockDoubleInsertCheckbox.Value)
        setConfig("blockDoubleCaps", self.blockDoubleCapsCheckbox.Value)
        setConfig("consoleRealtime", self.consoleRealtimeCheckbox.Value)
        setConfig("consoleBeep", self.consoleBeepCheckbox.Value)
        setConfig("busyBeep", self.busyBeepCheckbox.Value)
        setConfig("fixWindowNumber", self.fixWindowNumberCheckbox.Value)
        setConfig("overrideMoveByWord", self.overrideMoveByWordCheckbox.Value)
        setConfig("suppressUnselected", self.suppressUnselectedCheckbox.Value)
        setConfig("detectInsertMode", self.detectInsertModeCheckbox.Value)
        setConfig("nvdaVolume", self.nvdaVolumeSlider.Value)
        setConfig("dynamicKeystrokesTable", self.dynamicKeystrokesEdit.Value)
        reloadDynamicKeystrokes()
        super(SettingsDialog, self).onOk(evt)

class Beeper:
    BASE_FREQ = speech.IDT_BASE_FREQUENCY
    def getPitch(self, indent):
        return self.BASE_FREQ*2**(indent/24.0) #24 quarter tones per octave.

    BEEP_LEN = 10 # millis
    PAUSE_LEN = 5 # millis
    MAX_CRACKLE_LEN = 400 # millis
    MAX_BEEP_COUNT = MAX_CRACKLE_LEN // (BEEP_LEN + PAUSE_LEN)

    def __init__(self):
        self.player = nvwave.WavePlayer(
            channels=2,
            samplesPerSec=int(tones.SAMPLE_RATE),
            bitsPerSample=16,
            outputDevice=config.conf["speech"]["outputDevice"],
            wantDucking=False
        )



    def fancyCrackle(self, levels, volume):
        levels = self.uniformSample(levels, self.MAX_BEEP_COUNT )
        beepLen = self.BEEP_LEN
        pauseLen = self.PAUSE_LEN
        pauseBufSize = NVDAHelper.generateBeep(None,self.BASE_FREQ,pauseLen,0, 0)
        beepBufSizes = [NVDAHelper.generateBeep(None,self.getPitch(l), beepLen, volume, volume) for l in levels]
        bufSize = sum(beepBufSizes) + len(levels) * pauseBufSize
        buf = ctypes.create_string_buffer(bufSize)
        bufPtr = 0
        for l in levels:
            bufPtr += NVDAHelper.generateBeep(
                ctypes.cast(ctypes.byref(buf, bufPtr), ctypes.POINTER(ctypes.c_char)),
                self.getPitch(l), beepLen, volume, volume)
            bufPtr += pauseBufSize # add a short pause
        self.player.stop()
        self.player.feed(buf.raw)

    def simpleCrackle(self, n, volume):
        return self.fancyCrackle([0] * n, volume)


    NOTES = "A,B,H,C,C#,D,D#,E,F,F#,G,G#".split(",")
    NOTE_RE = re.compile("[A-H][#]?")
    BASE_FREQ = 220
    def getChordFrequencies(self, chord):
        myAssert(len(self.NOTES) == 12)
        prev = -1
        result = []
        for m in self.NOTE_RE.finditer(chord):
            s = m.group()
            i =self.NOTES.index(s)
            while i < prev:
                i += 12
            result.append(int(self.BASE_FREQ * (2 ** (i / 12.0))))
            prev = i
        return result

    def fancyBeep(self, chord, length, left=10, right=10):
        beepLen = length
        freqs = self.getChordFrequencies(chord)
        intSize = 8 # bytes
        bufSize = max([NVDAHelper.generateBeep(None,freq, beepLen, right, left) for freq in freqs])
        if bufSize % intSize != 0:
            bufSize += intSize
            bufSize -= (bufSize % intSize)
        self.player.stop()
        bbs = []
        result = [0] * (bufSize//intSize)
        for freq in freqs:
            buf = ctypes.create_string_buffer(bufSize)
            NVDAHelper.generateBeep(buf, freq, beepLen, right, left)
            bytes = bytearray(buf)
            unpacked = struct.unpack("<%dQ" % (bufSize // intSize), bytes)
            result = map(operator.add, result, unpacked)
        maxInt = 1 << (8 * intSize)
        result = map(lambda x : x %maxInt, result)
        packed = struct.pack("<%dQ" % (bufSize // intSize), *result)
        self.player.feed(packed)

    def uniformSample(self, a, m):
        n = len(a)
        if n <= m:
            return a
        # Here assume n > m
        result = []
        for i in range(0, m*n, n):
            result.append(a[i  // m])
        return result
    def stop(self):
        self.player.stop()


originalWaveOpen = None
originalWatchdogAlive = None
originalWatchdogAsleep = None

def preWaveOpen(selfself, *args, **kwargs):
    global originalWaveOpen
    result = originalWaveOpen(selfself, *args, **kwargs)
    volume = getConfig("nvdaVolume")
    volume2 = int(0xFFFF * (volume / 100))
    volume2 = volume2 | (volume2 << 16)
    winmm.waveOutSetVolume(selfself._waveout, volume2)
    return result

def findTableCell(selfself, gesture, movement="next", axis=None, index = 0):
    from scriptHandler import isScriptWaiting
    if isScriptWaiting():
        return
    formatConfig=config.conf["documentFormatting"].copy()
    formatConfig["reportTables"]=True
    try:
        tableID, origRow, origCol, origRowSpan, origColSpan = selfself._getTableCellCoords(selfself.selection)
        info = selfself._getTableCellAt(tableID, selfself.selection,origRow, origCol)
    except LookupError:
        # Translators: The message reported when a user attempts to use a table movement command
        # when the cursor is not within a table.
        ui.message(_("Not in a table cell"))
        return

    MAX_TABLE_DIMENSION = 500

    edgeFound = False
    for attempt in range(MAX_TABLE_DIMENSION):
        tableID, origRow, origCol, origRowSpan, origColSpan = selfself._getTableCellCoords(info)
        try:
            info = selfself._getNearestTableCell(tableID, info, origRow, origCol, origRowSpan, origColSpan, movement, axis)
        except LookupError:
            edgeFound = True
            break
    if not edgeFound:
        ui.message(_("Cannot find edge of table in this direction"))
        info = self._getTableCellAt(tableID, self.selection,origRow, origCol)
        info.collapse()
        self.selection = info
        return

    if index > 1:
        inverseMovement = "next" if movement == "previous" else "previous"
        for i in range(1, index):
            tableID, origRow, origCol, origRowSpan, origColSpan = selfself._getTableCellCoords(info)
            try:
                info = selfself._getNearestTableCell(tableID, selfself.selection, origRow, origCol, origRowSpan, origColSpan, inverseMovement, axis)
            except LookupError:
                ui.message(_("Cannot find {axis} with index {index} in this table").format(**locals()))
                return

    speech.speakTextInfo(info,formatConfig=formatConfig,reason=controlTypes.REASON_CARET)
    info.collapse()
    selfself.selection = info


def speakColumn(selfself, gesture):
    movement = "next"
    axis = "row"
    from scriptHandler import isScriptWaiting
    if isScriptWaiting():
        return
    formatConfig=config.conf["documentFormatting"].copy()
    formatConfig["reportTables"]=True
    try:
        tableID, origRow, origCol, origRowSpan, origColSpan = selfself._getTableCellCoords(selfself.selection)
        info = selfself._getTableCellAt(tableID, selfself.selection,origRow, origCol)
    except LookupError:
        # Translators: The message reported when a user attempts to use a table movement command
        # when the cursor is not within a table.
        ui.message(_("Not in a table cell"))
        return

    MAX_TABLE_DIMENSION = 500
    for attempt in range(MAX_TABLE_DIMENSION):
        speech.speakTextInfo(info, formatConfig=formatConfig, reason=controlTypes.REASON_CARET)
        tableID, origRow, origCol, origRowSpan, origColSpan = selfself._getTableCellCoords(info)
        try:
            info = selfself._getNearestTableCell(tableID, info, origRow, origCol, origRowSpan, origColSpan, movement, axis)
        except LookupError:
            break

wdTime = 0
wdAsleep = False
wdTimeout = 0.3 # seconds
def             preWatchdogAlive():
    global wdTime, wdAsleep
    current = time.time()
    delta = current - wdTime
    wdTime = current
    wdAsleep = False
    originalWatchdogAlive()

def             preWatchdogAsleep():
    global wdTime, wdAsleep
    current = time.time()
    delta = current - wdTime
    wdTime = current
    wdAsleep = True
    originalWatchdogAsleep()
    wdAsleep = True

class     MyWatchdog(threading.Thread):
    def __init__(self):
        super().__init__()
        self.stopSignal = False

    def run(self):
        global wdTime, wdAsleep, wdTimeout
        time.sleep(5)
        while not self.stopSignal:
            if getConfig("busyBeep"):
                while not wdAsleep and (time.time() - wdTime) > wdTimeout:
                    tones.beep(150, 10, left=25, right=25)
                    #time.sleep(0.01)
            time.sleep(0.1)

    def terminate(self):
        self.stopSignal = True

gestureCounter = 0
storedText = None
speakAnywayAfter = 0.1 # seconds
def checkUpdate(localGestureCounter, attempt, originalTimestamp, gesture=None, spokenAnyway=False):
    global gestureCounter, storedText
    if gestureCounter != localGestureCounter:
        return
    try:
        focus = api.getFocusObject()
        textInfo = focus.makeTextInfo(textInfos.POSITION_CARET)
        textInfo.expand(textInfos.UNIT_LINE)
        text = textInfo.text
    except Exception as e:
        log.warning(f"Error retrieving text during dynamic keystroke handling: {e}")
        return
    if attempt == 0:
        storedText = text
    else:
        if text != storedText:
            if spokenAnyway:
                speech.cancelSpeech()
            speech.speakTextInfo(textInfo, unit=textInfos.UNIT_LINE)
            return
    elapsed = time.time() - originalTimestamp
    if not spokenAnyway and elapsed > speakAnywayAfter:
        speech.speakTextInfo(textInfo, unit=textInfos.UNIT_LINE)
        spokenAnyway = True
    if elapsed < 1.0:
        sleepTime = 25 # ms
    elif elapsed < 10:
        sleepTime = 1000 # ms
    else:
        sleepTime = 5000
    core.callLater(sleepTime, checkUpdate, localGestureCounter, attempt+1, originalTimestamp, spokenAnyway=spokenAnyway)

allModifiers = [
    winUser.VK_LCONTROL, winUser.VK_RCONTROL,
    winUser.VK_LSHIFT, winUser.VK_RSHIFT, winUser.VK_LMENU,
    winUser.VK_RMENU, winUser.VK_LWIN, winUser.VK_RWIN,
]


def executeAsynchronously(gen):
    """
    This function executes a generator-function in such a manner, that allows updates from the operating system to be processed during execution.
    For an example of such generator function, please see GlobalPlugin.script_editJupyter.
    Specifically, every time the generator function yilds a positive number,, the rest of the generator function will be executed
    from within wx.CallLater() call.
    If generator function yields a value of 0, then the rest of the generator function
    will be executed from within wx.CallAfter() call.
    This allows clear and simple expression of the logic inside the generator function, while still allowing NVDA to process update events from the operating system.
    Essentially the generator function will be paused every time it calls yield, then the updates will be processed by NVDA and then the remainder of generator function will continue executing.
    """
    if not isinstance(gen, types.GeneratorType):
        raise Exception("Generator function required")
    try:
        value = gen.__next__()
    except StopIteration:
        return
    l = lambda gen=gen: executeAsynchronously(gen)
    core.callLater(value, executeAsynchronously, gen)

class SpeechChunk:
    def __init__(self, text, now):
        self.text = text
        self.timestamp = now
        self.spoken = False
        self.nextChunk = None

    def speak(self):
        def callback():
            global currentSpeechChunk, latestSpeechChunk
            with speechChunksLock:
                if self != currentSpeechChunk:
                    # This can happen when this callback has already been scheduled, but new speech has arrived
                    # and this chunk was cancelled due to timeout.
                    return
                myAssert(
                    (
                        currentSpeechChunk == latestSpeechChunk
                        and self.nextChunk is None
                    )
                    or (
                        currentSpeechChunk != latestSpeechChunk
                        and self.nextChunk is not  None
                    )
                )

                currentSpeechChunk = self.nextChunk
                if self.nextChunk is not None:
                    self.nextChunk.speak()
                else:
                    latestSpeechChunk = None
        speech.speak([
            self.text,
            speech.commands.CallbackCommand(callback),
        ])

currentSpeechChunk = None
latestSpeechChunk = None
speechChunksLock = threading.Lock()
originalReportNewText = None
def newReportConsoleText(selfself, line, *args, **kwargs):
    global currentSpeechChunk, latestSpeechChunk
    if getConfig("consoleBeep"):
        tones.beep(100, 5)
    if not getConfig("consoleRealtime"):
        return originalReportNewText(selfself, line, *args, **kwargs)
    now = time.time()
    threshold = now - 1
    newChunk = SpeechChunk(line, now)
    with speechChunksLock:
        myAssert((currentSpeechChunk is not None) == (latestSpeechChunk is not None))
        if latestSpeechChunk is not None:
            latestSpeechChunk.nextChunk = newChunk
            latestSpeechChunk = newChunk
            if currentSpeechChunk.timestamp < threshold:
                speech.cancelSpeech()
                while currentSpeechChunk.timestamp < threshold:
                    currentSpeechChunk = currentSpeechChunk.nextChunk
                currentSpeechChunk.speak()
        else:
            currentSpeechChunk = latestSpeechChunk = newChunk
            newChunk.speak()

originalSpeakSelectionChange = None
originalCaretMovementScriptHelper = None
performingShiftGesture = False
def preSpeakSelectionChange(oldInfo, newInfo, *args, **kwargs):
    if getConfig('suppressUnselected') and not performingShiftGesture:
        # Setting speakUnselected to false if user is not intending to select/unselect things
        if len(args) >= 2:
            args[1] = False
        else:
            kwargs['speakUnselected'] = False
    return originalSpeakSelectionChange(oldInfo, newInfo, *args, **kwargs)
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = _("Tony's Enhancements")

    def __init__(self, *args, **kwargs):
        super(GlobalPlugin, self).__init__(*args, **kwargs)
        self.createMenu()
        self.injectHooks()
        self.injectTableFunctions()
        self.lastConsoleUpdateTime = 0
        self.beeper = Beeper()

    def createMenu(self):
        def _popupMenu(evt):
            gui.mainFrame._popupSettingsDialog(SettingsDialog)
        self.prefsMenuItem = gui.mainFrame.sysTrayIcon.preferencesMenu.Append(wx.ID_ANY, _("Tony's enhancements..."))
        gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, _popupMenu, self.prefsMenuItem)


    def terminate(self):
        self.removeHooks()
        prefMenu = gui.mainFrame.sysTrayIcon.preferencesMenu
        prefMenu.Remove(self.prefsMenuItem)


    def injectHooks(self):
        global originalWaveOpen, originalWatchdogAlive, originalWatchdogAsleep, originalReportNewText, originalSpeakSelectionChange, originalCaretMovementScriptHelper
        self.originalExecuteGesture = inputCore.InputManager.executeGesture
        inputCore.InputManager.executeGesture = lambda selfself, gesture, *args, **kwargs: self.preExecuteGesture(selfself, gesture, *args, **kwargs)
        #self.originalCalculateNewText = behaviors.LiveText._calculateNewText
        #behaviors.LiveText._calculateNewText = lambda selfself, *args, **kwargs: self.preCalculateNewText(selfself, *args, **kwargs)
        originalReportNewText = behaviors.LiveText._reportNewText
        behaviors.LiveText._reportNewText = newReportConsoleText

        originalWaveOpen = nvwave.WavePlayer.open
        nvwave.WavePlayer.open = preWaveOpen
        originalWatchdogAlive = watchdog.alive
        watchdog.alive = preWatchdogAlive
        originalWatchdogAsleep = watchdog.asleep
        watchdog.asleep = preWatchdogAsleep
        self.myWatchdog = MyWatchdog()
        self.myWatchdog.setDaemon(True)
        self.myWatchdog.start()
        self.originalMoveByWord = editableText.EditableText.script_caret_moveByWord
        editableText.EditableText.script_caret_moveByWord = lambda selfself, gesture, *args, **kwargs: self.script_caretMoveByWord(selfself, gesture, *args, **kwargs)
        originalSpeakSelectionChange = speech.speakSelectionChange
        speech.speakSelectionChange = preSpeakSelectionChange

    def  removeHooks(self):
        global originalWaveOpen, originalReportNewText
        inputCore.InputManager.executeGesture = self.originalExecuteGesture
        #behaviors.LiveText._calculateNewText = self.originalCalculateNewText
        behaviors.LiveText._reportNewText = originalReportNewText
        nvwave.WavePlayer.open = originalWaveOpen
        watchdog.alive = originalWatchdogAlive
        watchdog.asleep = originalWatchdogAsleep
        self.myWatchdog.terminate()
        editableText.EditableText.script_caret_moveByWord = self.originalMoveByWord
        speech.speakSelectionChange = originalSpeakSelectionChange

    windowsSwitchingRe = re.compile(r':\d\+windows$')
    typingKeystrokeRe = re.compile(r':(shift\+)?[A-Za-z0-9](\+shift)?$')
    def preExecuteGesture(self, selfself, gesture, *args, **kwargs):
        global gestureCounter, editorMovingCaret, performingShiftGesture
        gestureCounter += 1
        editorMovingCaret = False
        if (
            getConfig("blockDoubleInsert")  and
            gesture.vkCode == winUser.VK_INSERT and
            not gesture.isNVDAModifierKey
        ):
            tones.beep(500, 50)
            return
        if (
            getConfig("blockDoubleCaps")  and
            gesture.vkCode == winUser.VK_CAPITAL and
            not gesture.isNVDAModifierKey
        ):
            tones.beep(500, 50)
            return

        kb = gesture.normalizedIdentifiers
        if len(kb) == 0:
            pass
        else:
            kb = kb[0]
        focus = api.getFocusObject()
        appName = focus.appModule.appName
        if(
            dynamicKeystrokes is not None and (
                ("*", kb) in dynamicKeystrokes
                or (appName, kb) in dynamicKeystrokes
            )
        ):
            core.callLater(0,
                checkUpdate,
                gestureCounter, 0, time.time(), gesture
            )
        if getConfig("fixWindowNumber") and self.windowsSwitchingRe.search(kb):
            executeAsynchronously(self.asyncSwitchWindowHandler(gestureCounter))
        if getConfig("detectInsertMode") and self.typingKeystrokeRe.search(kb):
            text = None
            caret = None
            executeAsynchronously(self.insertModeDetector(gestureCounter, text, caret))
        if (
            (winUser.VK_SHIFT, False) in gesture.modifiers
            or (winUser.VK_LSHIFT, False) in gesture.modifiers
            or (winUser.VK_RSHIFT, False) in gesture.modifiers
        ):
            performingShiftGesture = True
        else:
            performingShiftGesture = False
        return self.originalExecuteGesture(selfself, gesture, *args, **kwargs)

    def asyncSwitchWindowHandler(self, thisGestureCounter):
        global gestureCounter
        timeout = time.time() + 2
        yield 1
      # step 1. wait for all modifiers to be released
        while True:
            if time.time() > timeout:
                return
            if gestureCounter != thisGestureCounter:
                return
            status = [
                winUser.getKeyState(k) & 32768
                for k in allModifiers
            ]
            if not any(status):
                break
            yield 1
      # Step 2
        #for i in range(100):
        yield 50
        if gestureCounter != thisGestureCounter:
            return
        if True:
            focus = api.getFocusObject()
            if focus.appModule.appName == "explorer":
                if focus.windowClassName == "TaskListThumbnailWnd":
                    kbdEnter = keyboardHandler.KeyboardInputGesture.fromName("Enter")
                    kbdEnter.send()
                    tones.beep(100, 20)
                    return

    def getCurrentLineAndCaret(self):
        focus = api.getFocusObject()
        caretInfo = focus.makeTextInfo(textInfos.POSITION_SELECTION)
        if len(caretInfo.text) > 0:
            return "", -10
        lineInfo = caretInfo.copy()
        lineInfo.expand(textInfos.UNIT_LINE)
        lineText = lineInfo.text
        # Command line prompt reports every line containing ~120 whitespaces, therefore it appears as if insert mode is on and is overwriting spaces.
        # To work around that, stripping whitespaces  from the right
        lineText = lineText.rstrip()
        lineInfo.setEndPoint(caretInfo, 'endToEnd')
        caretOffset = len(lineInfo.text)
        return lineText, caretOffset


    def insertModeDetector(self, thisGestureCounter, originalText, originalCaret):
        global gestureCounter
        timeout = time.time() + 0.5
        try:
            originalText, originalCaret = self.getCurrentLineAndCaret()
        except:
            return
        if originalCaret < 0:
            # Something is selected, never mind
            return
        yield 10

        while True:
            if gestureCounter != thisGestureCounter:
                return
            if time.time() > timeout:
                return
            try:
                text, caret = self.getCurrentLineAndCaret()
            except:
                return
            if (text != originalText) or (caret != originalCaret):
                # state has changed, we will check for signs of insert mode, but we won't be running this loop anymore
                if (caret == originalCaret + 1) and (len(text) == len(originalText)):
                    try:
                        if (text[:originalCaret] == originalText[:originalCaret]) and (text[originalCaret+1:] == originalText[originalCaret+1:]) and (text[originalCaret] != originalText[originalCaret]):
                            # Boom! Insert mode detected!
                            tones.beep(150, 30)
                    except IndexError:
                        pass
                return
            yield 10

    def preCalculateNewText(self, selfself, *args, **kwargs):
        outLines =   self.originalCalculateNewText(selfself, *args, **kwargs)
        return outLines
        if len(outLines) == 1 and len(outLines[0].strip()) == 1:
            # Only a single character has changed - in this case NVDA thinks that's a typed character, so it is not spoken anyway. Con't interfere.
            return outLines
        if len(outLines) == 0:
            return outLines
        if getConfig("consoleBeep"):
            tones.beep(100, 5)
        if getConfig("consoleRealtime"):
            #if time.time() > self.lastConsoleUpdateTime + 0.5:
                #self.lastConsoleUpdateTime = time.time()
            speech.cancelSpeech()
        return outLines

    def injectTableFunctions(self):
        self.injectTableFunction(
            scriptName="firstColumn",
            kb="Control+Alt+Home",
            doc="Move to the first column in table",
            movement="previous",
            axis="column",
        )
        self.injectTableFunction(
            scriptName="lastColumn",
            kb="Control+Alt+End",
            doc="Move to the last column in table",
            movement="next",
            axis="column",
        )
        self.injectTableFunction(
            scriptName="firstRow",
            kb="Control+Alt+PageUp",
            doc="Move to the first row in table",
            movement="previous",
            axis="row",
        )
        self.injectTableFunction(
            scriptName="lastRow",
            kb="Control+Alt+PageDown",
            doc="Move to the last row in table",
            movement="next",
            axis="row",
        )
        for i in range(1, 11):
            self.injectTableFunction(
                scriptName=f"jumpToColumn{i}",
                kb="NVDA+Control+%d" % (i%10),
                doc="Move to the %d-th column in table" % i,
                movement="previous",
                axis="column",
                index = i,
            )
            self.injectTableFunction(
                scriptName=f"jumpToRow{i}",
                kb="NVDA+Alt+%d" % (i%10),
                doc="Move to the %d-th row in table" % i,
                movement="previous",
                axis="row",
                index = i,
            )
        self.injectTableFunction(
            scriptName="readColumn",
            kb="NVDA+Shift+DownArrow",
            doc="Read column starting from current cell",
            function=speakColumn,
        )

    def injectTableFunction(self, scriptName, kb, doc, function=findTableCell, *args, **kwargs):
        cls = documentBase.DocumentWithTableNavigation
        funcName = "script_%s" % scriptName
        script = lambda self,gesture: function(self, gesture, *args, **kwargs)
        script.__doc__ = doc
        script.category = self.scriptCategory
        setattr(cls, funcName, script)
        cls._DocumentWithTableNavigation__gestures["kb:%s" % kb] = scriptName

    @script(description='Increase NVDA volume.', gestures=['kb:NVDA+control+PageUp'])
    def script_increaseVolume(self, gesture):
        self.adjustVolume(5)

    @script(description='Decrease NVDA volume.', gestures=['kb:NVDA+control+PageDown'])
    def script_decreaseVolume(self, gesture):
        self.adjustVolume(-5)

    def adjustVolume(self, increment):
        volume = getConfig("nvdaVolume")
        volume += increment
        if volume > 100:
            volume = 100
        if volume < 0:
            volume = 0
        setConfig("nvdaVolume", volume)
        message = _("NVDA volume %d") % volume
        ui.message(message)

    # Regular expression for the beginning of a word. Matches:
    #  1. End of string
    # 2. Beginning of any word: \b\w
    # 3. Punctuation mark preceded by non-punctuation mark: (?<=[\w\s])[^\w\s]
    # 4. Punctuation mark preceded by beginning of the string
    wordRe = re.compile(r'$|\b\w|(?<=[\w\s])[^\w\s]|^[^\w\s]')
    def script_caretMoveByWord(self, selfself, gesture):
        if not getConfig('overrideMoveByWord'):
            return self.originalMoveByWord(selfself, gesture)
        try:
            if 'leftArrow' == gesture.mainKeyName:
                direction = -1
            elif 'rightArrow' == gesture.mainKeyName:
                direction = 1
            else:
                return self.originalMoveByWord(selfself, gesture)
            focus = api.getFocusObject()
            caretInfo = focus.makeTextInfo(textInfos.POSITION_CARET)
            caretInfo.collapse(end=(direction > 0))
            lineInfo = caretInfo.copy()
            lineInfo.expand(textInfos.UNIT_PARAGRAPH)
            offsetInfo = lineInfo.copy()
            offsetInfo.setEndPoint(caretInfo, 'endToEnd')
            caret = len(offsetInfo.text)
            for lineAttempt in range(100):
                lineText = lineInfo.text.rstrip('\r\n')
                isEmptyLine = len(lineText.strip()) == 0
                boundaries = [m.start() for m in self.wordRe.finditer(lineText)]
                boundaries = sorted(list(set(boundaries)))
                if direction > 0:
                    newWordIndex = bisect.bisect_right(boundaries, caret)
                else:
                    newWordIndex = bisect.bisect_left(boundaries, caret) - 1
                if not isEmptyLine and (0 <= newWordIndex < len(boundaries)):
                    if lineAttempt == 0:
                        adjustment = boundaries[newWordIndex] - caret
                        newInfo = caretInfo
                        newInfo.move(textInfos.UNIT_CHARACTER, adjustment)
                    else:
                        newInfo = lineInfo
                        if direction > 0:
                            adjustment =  boundaries[newWordIndex]
                            newInfo.collapse(end=False)
                        else:
                            adjustment =  boundaries[newWordIndex] - len(lineInfo.text)
                            newInfo.collapse(end=True)
                        result = newInfo.move(textInfos.UNIT_CHARACTER, adjustment)
                    if newWordIndex + 1 < len(boundaries):
                        newInfo.move(
                            textInfos.UNIT_CHARACTER,
                            boundaries[newWordIndex + 1] - boundaries[newWordIndex],
                            endPoint='end',
                        )
                    newInfo.updateCaret()
                    speech.speakTextInfo(newInfo, unit=textInfos.UNIT_WORD, reason=controlTypes.REASON_CARET)
                    return
                else:
                    lineInfo.collapse()
                    result = lineInfo.move(textInfos.UNIT_PARAGRAPH, direction)
                    if result == 0:
                        self.beeper.fancyBeep('HF', 100, left=25, right=25)
                        return
                    lineInfo.expand(textInfos.UNIT_PARAGRAPH)
                    # now try to find next word again on next/previous line
                    if direction > 0:
                        caret = -1
                    else:
                        caret = len(lineInfo.text)
            #raise Exception('Failed to find next word')
            self.beeper.fancyBeep('HF', 100, left=25, right=25)
        except NotImplementedError:
            return self.originalMoveByWord(selfself, gesture)