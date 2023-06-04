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
from gui.settingsDialogs import SettingsPanel
import html
import inputCore
import itertools
import json
import keyboardHandler
import locationHelper
from logHandler import log
import math
import mouseHandler
import NVDAHelper
from NVDAObjects import behaviors, NVDAObject
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.UIA import UIA
from NVDAObjects.window import winword
import nvwave
import operator
import os
import re
from scriptHandler import script, willSayAllResume
import speech
from speech.priorities import SpeechPriority
import string
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
            f = open(LOG_FILE_NAME, "a", encoding='utf-8')
            print(s, file=f)
            #f.write(s.encode('UTF-8'))
            #f.write('\n')
            f.close()
else:
    def mylog(*arg, **kwarg):
        pass

def myAssert(condition):
    if not condition:
        raise RuntimeError("Assertion failed")

try:
    REASON_CARET = controlTypes.REASON_CARET
except AttributeError:
    REASON_CARET = controlTypes.OutputReason.CARET

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

defaultLangMap = '''
en:[a-zA-Z]
ru:[а-яА-Я]
zh_CN:[⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]
'''.strip()

module = "tonysEnhancements"
def initConfiguration():
    confspec = {
        "blockDoubleInsert" : "boolean( default=False)",
        "blockDoubleCaps" : "boolean( default=False)",
        "blockScrollLock" : "boolean( default=False)",
        "nvdaVolume" : "integer( default=100, min=0, max=100)",
        "appsVolume" : "integer( default=100, min=0, max=100)",
        "soundSplitLeft" : "boolean( default=False)",
        "soundSplit" : "boolean( default=False)",
        "busyBeep" : "boolean( default=False)",
        "dynamicKeystrokesTable" : f"string( default='{defaultDynamicKeystrokes}')",
        "fixWindowNumber" : "boolean( default=False)",
        "detectInsertMode" : "boolean( default=False)",
        "suppressUnselected" : "boolean( default=False)",
        "enableLangMap" : "boolean( default=False)",
        "langMap" : f"string( default='{defaultLangMap}')",
        "quickSearch1" : f"string( default='')",
        "quickSearch2" : f"string( default='')",
        "quickSearch3" : f"string( default='')",
        "priority" : "integer( default=0, min=0, max=3)",
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
            kb = keyboardHandler.KeyboardInputGesture.fromName(tokens[1]).identifiers[0]
        except (KeyError, IndexError):
            raise ValueError(f"Invalid kb shortcut {tokens[1]} ")
        result.add((app, kb))
    return result

dynamicKeystrokes = None
def reloadDynamicKeystrokes():
    global dynamicKeystrokes
    dynamicKeystrokes = parseDynamicKeystrokes(getConfig("dynamicKeystrokesTable"))


def parseLangMap(s):
    result = {}
    for line in s.splitlines():
        tokens = line.strip().split(":")
        if (len(tokens) == 0) or (len(line) == 0):
            continue
        if len(tokens) != 2:
            raise ValueError(f"LangMap configuration: invalid line: {line}")
        lang = tokens[0]
        try:
            r = re.compile(tokens[1])
        except  Exception as e:
            raise ValueError(f"Invalid regex for language {lang}: {tokens[1]}: {e}")
        result[lang] = r
    return result
langMap = None
def reloadLangMap():
    global langMap
    langMap = parseLangMap(getConfig("langMap"))

priorityNames = _("Normal,Above normal,High,Realtime").split(",")
priorityValues = [
    # https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setpriorityclass?redirectedfrom=MSDN
    0x00000020,
    0x00008000,
    0x00000080,
    0x00000100
]

def updatePriority():
    index = getConfig("priority")
    priority = priorityValues[index]
    result = ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), priority)
    if result == 0:
        gui.messageBox(_("Failed to set process priority to %s.") % priorityNames[index], _("Tony's enhancement add-on encountered an error"), wx.OK|wx.ICON_WARNING, None)

addonHandler.initTranslation()
initConfiguration()

class MultilineEditTextDialog(wx.Dialog):
    def __init__(self, parent, text, title_string, onTextComplete):
        super(MultilineEditTextDialog, self).__init__(parent, title=title_string)
        self.text = text
        self.onTextComplete = onTextComplete
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        sHelper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)

        self.textCtrl = wx.TextCtrl(self, size=(-1, 150), style=wx.TE_MULTILINE|wx.TE_DONTWRAP)
        self.textCtrl.Bind(wx.EVT_CHAR, self.onChar)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyUP)
        sHelper.addItem(self.textCtrl, flag=wx.EXPAND)
        self.textCtrl.SetValue(text)

        buttonGroup = gui.guiHelper.ButtonHelper(wx.HORIZONTAL)
        self.OkButton = buttonGroup.addButton(self, label=_('OK'))
        self.OkButton.Bind(wx.EVT_BUTTON, self.onOk)
        self.cancelButton = buttonGroup.addButton(self, label=_('Cancel'))
        self.cancelButton.Bind(wx.EVT_BUTTON, self.onCancel)
        sHelper.addItem(buttonGroup)

        mainSizer.Add(sHelper.sizer, border=10, flag=wx.ALL|wx.EXPAND, proportion=1)
        self.SetSizer(mainSizer)

        self.SetFocus()

    def onChar(self, event):
        control = event.ControlDown()
        shift = event.ShiftDown()
        alt = event.AltDown()
        keyCode = event.GetKeyCode()
        if event.GetKeyCode() == 1:
            # Control+A
            self.textCtrl.SetSelection(-1,-1)
        elif event.GetKeyCode() == wx.WXK_HOME:
            if not any([control, shift, alt]):
                curPos = self.textCtrl.GetInsertionPoint()
                lineNum = len(self.textCtrl.GetRange( 0, self.textCtrl.GetInsertionPoint() ).split("\n")) - 1
                colNum = len(self.textCtrl.GetRange( 0, self.textCtrl.GetInsertionPoint() ).split("\n")[-1])
                lineText = self.textCtrl.GetLineText(lineNum)
                m = re.search("^\s*", lineText)
                if not m:
                    raise Exception("This regular expression must match always.")
                indent = len(m.group(0))
                if indent == colNum:
                    newColNum = 0
                else:
                    newColNum = indent
                self.textCtrl.SetInsertionPoint(curPos - colNum + newColNum)
            else:
                event.Skip()
        else:
            event.Skip()


    def OnKeyUP(self, event):
        keyCode = event.GetKeyCode()
        if keyCode == wx.WXK_ESCAPE:
            self.text = self.textCtrl.GetValue()
            self.EndModal(wx.ID_CANCEL)
            wx.CallAfter(lambda: self.onTextComplete(wx.ID_CANCEL, self.text, None))
        event.Skip()

    def onOk(self, evt):
        self.text = self.textCtrl.GetValue()
        self.EndModal(wx.ID_OK)
        wx.CallAfter(lambda: self.onTextComplete(wx.ID_OK, self.text, None))

    def onCancel(self, evt):
        self.text = self.textCtrl.GetValue()
        self.EndModal(wx.ID_CANCEL)
        wx.CallAfter(lambda: self.onTextComplete(wx.ID_CANCEL, self.text, None))



class SettingsDialog(SettingsPanel):
    # Translators: Title for the settings dialog
    title = _("Tony's enhancements  settings")

    def makeSettings(self, settingsSizer):
        self.dynamicKeystrokesTable = getConfig("dynamicKeystrokesTable")
        self.langMap = getConfig("langMap")
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
      # Apps  volume slider
        sizer=wx.BoxSizer(wx.HORIZONTAL)
        # Translators: slider to select Apps   volume
        label=wx.StaticText(self,wx.ID_ANY,label=_("Applications volume"))
        slider=wx.Slider(self, wx.NewId(), minValue=0,maxValue=100)
        slider.SetValue(getConfig("appsVolume"))
        sizer.Add(label)
        sizer.Add(slider)
        settingsSizer.Add(sizer)
        self.appsVolumeSlider = slider
      # checkbox Enable sound split
        # Translators: Checkbox for sound split
        label = _("Split NVDA sound and applications' sounds into left and right channels.")
        self.soundSplitCheckbox = sHelper.addItem(wx.CheckBox(self, label=label))
        self.soundSplitCheckbox.Value = getConfig("soundSplit")
      # checkbox switch left and rright during sound split
        # Translators: Checkbox for switching left and right sound split
        label = _("Switch left and right during sound split.")
        self.soundSplitLeftCheckbox = sHelper.addItem(wx.CheckBox(self, label=label))
        self.soundSplitLeftCheckbox.Value = getConfig("soundSplitLeft")

      # Dynamic keystrokes table
        # Translators: Label for dynamic keystrokes table edit box
        label = _("Edit dynamic keystrokes table - see add-on documentation for more information")
        #self.dynamicKeystrokesEdit = gui.guiHelper.LabeledControlHelper(self, _("Dynamic keystrokes table - see add-on documentation for more information"), wx.TextCtrl, style=wx.TE_MULTILINE).control
        #self.dynamicKeystrokesEdit.Value = getConfig("dynamicKeystrokesTable")
        self.dynamicButton = sHelper.addItem (wx.Button (self, label = label))
        self.dynamicButton.Bind(wx.EVT_BUTTON, self.onDynamicClick)
      # LangMap checkbox and multiline edit button
        label = _("Enable automatic language switching based on character set")
        self.langMapCheckbox = sHelper.addItem(wx.CheckBox(self, label=label))
        self.langMapCheckbox.Value = getConfig("enableLangMap")
        label = _('Edit language map')
        self.langMapButton = sHelper.addItem (wx.Button (self, label = label))
        self.langMapButton.Bind(wx.EVT_BUTTON, self.onLangMapClick)
      # QuickSearch regexp text edit
        label = _("QuickSearch1 regexp (assigned to PrintScreen)")
        self.quickSearchEdit = sHelper.addLabeledControl(label, wx.TextCtrl)
        self.quickSearchEdit.Value = getConfig("quickSearch1")
      # QuickSearch2 regexp text edit
        label = _("QuickSearch2 regexp (assigned to ScrollLock))")
        self.quickSearch2Edit = sHelper.addLabeledControl(label, wx.TextCtrl)
        self.quickSearch2Edit.Value = getConfig("quickSearch2")
      # QuickSearch3 regexp text edit
        label = _("QuickSearch3 regexp (assigned to Pause)")
        self.quickSearch3Edit = sHelper.addLabeledControl(label, wx.TextCtrl)
        self.quickSearch3Edit.Value = getConfig("quickSearch3")
      # checkbox block scroll lock
        # Translators: Checkbox for blocking scroll lock
        label = _("Suppress scroll lock mode announcements")
        self.blockScrollLockCheckbox = sHelper.addItem(wx.CheckBox(self, label=label))
        self.blockScrollLockCheckbox.Value = getConfig("blockScrollLock")
      # System priority Combo box
        # Translators: Label for system priority combo box
        label = _("NVDA process system priority:")
        self.priorityCombobox = sHelper.addLabeledControl(label, wx.Choice, choices=priorityNames)
        index = getConfig("priority")
        self.priorityCombobox.Selection = index

    def dynamicCallback(self, result, text, keystroke):
        if result == wx.ID_OK:
            try:
                parseDynamicKeystrokes(text)
            except Exception as e:
                gui.messageBox(f"Error parsing dynamic keystrokes table: {e}",
                    _("Error"),wx.OK|wx.ICON_INFORMATION,self)
                self.popupDynamic(text=text)

                return

            self.dynamicKeystrokesTable = text

    def onDynamicClick(self, evt):
        self.popupDynamic(text=self.dynamicKeystrokesTable)

    def popupDynamic(self, text):
        title = _('Edit dynamic keystrokes table')
        gui.mainFrame.prePopup()
        dialog = MultilineEditTextDialog(self,
            text=text,
            title_string=title,
            onTextComplete=lambda result, text, keystroke: self.dynamicCallback(result, text, keystroke)
        )
        result = dialog.ShowModal()
        gui.mainFrame.postPopup()
    def langMapCallback(self, result, text, keystroke):
        if result == wx.ID_OK:
            try:
                parseLangMap(text)
            except Exception as e:
                gui.messageBox(f"Error parsing language map: {e}",
                    _("Error"),wx.OK|wx.ICON_INFORMATION,self)
                self.popupLangMap(text=text)
                return

            self.langMap = text

    def onLangMapClick(self, evt):
        self.popupLangMap(text=self.langMap)

    def popupLangMap(self, text):
        title = _('Edit language map')
        gui.mainFrame.prePopup()
        dialog = MultilineEditTextDialog(self,
            text=text,
            title_string=title,
            onTextComplete=lambda result, text, keystroke: self.langMapCallback(result, text, keystroke)
        )
        result = dialog.ShowModal()
        gui.mainFrame.postPopup()


    def onSave(self):
        try:
            parseDynamicKeystrokes(self.dynamicKeystrokesTable)
        except Exception as e:
            self.dynamicButton.SetFocus()
            ui.message(f"Error parsing dynamic keystrokes table: {e}")
            return

        setConfig("blockDoubleInsert", self.blockDoubleInsertCheckbox.Value)
        setConfig("blockDoubleCaps", self.blockDoubleCapsCheckbox.Value)
        setConfig("busyBeep", self.busyBeepCheckbox.Value)
        setConfig("fixWindowNumber", self.fixWindowNumberCheckbox.Value)
        setConfig("suppressUnselected", self.suppressUnselectedCheckbox.Value)
        setConfig("detectInsertMode", self.detectInsertModeCheckbox.Value)
        setConfig("nvdaVolume", self.nvdaVolumeSlider.Value)
        setConfig("appsVolume", self.appsVolumeSlider.Value)
        setConfig("soundSplit", self.soundSplitCheckbox.Value)
        setConfig("soundSplitLeft", self.soundSplitLeftCheckbox.Value)
        setConfig("dynamicKeystrokesTable", self.dynamicKeystrokesTable)
        reloadDynamicKeystrokes()
        setConfig("enableLangMap", self.langMapCheckbox.Value)
        setConfig("langMap", self.langMap)
        reloadLangMap()
        setConfig("quickSearch1", self.quickSearchEdit.Value)
        setConfig("quickSearch2", self.quickSearch2Edit.Value)
        setConfig("quickSearch3", self.quickSearch3Edit.Value)
        setConfig("blockScrollLock", self.blockScrollLockCheckbox.Value)
        updateScrollLockBlocking()
        setConfig("priority", self.priorityCombobox.Selection)
        updatePriority()
        updateSoundSplitterMonitorThread()

class Memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}
    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.f(*args)
        #Warning: You may wish to do a deepcopy here if returning objects
        return self.memo[args]

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
        self.stopSignal = False



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

    @Memoize
    def prepareFancyBeep(self, chord, length, left=10, right=10):
        beepLen = length
        freqs = self.getChordFrequencies(chord)
        intSize = 8 # bytes
        bufSize = max([NVDAHelper.generateBeep(None,freq, beepLen, right, left) for freq in freqs])
        if bufSize % intSize != 0:
            bufSize += intSize
            bufSize -= (bufSize % intSize)
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
        return packed

    def fancyBeep(self, chord, length, left=10, right=10, repetitions=1 ):
        self.player.stop()
        buffer = self.prepareFancyBeep(self, chord, length, left, right)
        self.player.feed(buffer)
        repetitions -= 1
        if repetitions > 0:
            self.stopSignal = False
            # This is a crappy implementation of multithreading. It'll deadlock if you poke it.
            # Don't use for anything serious.
            def threadFunc(repetitions):
                for i in range(repetitions):
                    if self.stopSignal:
                        return
                    self.player.feed(buffer)
            t = threading.Thread(target=threadFunc, args=(repetitions,))
            t.start()

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
        self.stopSignal = True
        self.player.stop()


originalWaveOpen = None
originalWatchdogAlive = None
originalWatchdogAsleep = None

def preWaveOpen(selfself, *args, **kwargs):
    global originalWaveOpen
    result = originalWaveOpen(selfself, *args, **kwargs)
    volume = getConfig("nvdaVolume")
    volume2 = int(0xFFFF * (volume / 100))
    if not getConfig("soundSplit"):
        volume2 = volume2 | (volume2 << 16)
    else:
        if getConfig("soundSplitLeft"):
            pass
        else:
            volume2 = (volume2 << 16)
    winmm.waveOutSetVolume(selfself._waveout, volume2)
    return result

def setAppsVolume(volumes=None):
    from . pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, IChannelAudioVolume
    if volumes is not None:
        leftVolume, rightVolume = volumes
    else:
        volume = getConfig("appsVolume")
        if getConfig("soundSplit"):
            if getConfig("soundSplitLeft"):
                leftVolume = 0
                rightVolume = volume
            else:
                leftVolume = volume
                rightVolume = 0
        else:
            leftVolume = rightVolume = volume

    leftVolume /= 100.0
    rightVolume /= 100.0

    audioSessions = AudioUtilities.GetAllSessions()
    for s in audioSessions:
        if s.Process is not None and 'nvda' in s.Process.name().lower():
            continue
        channelVolume = s._ctl.QueryInterface(IChannelAudioVolume)
        if channelVolume.GetChannelCount() == 2:
            channelVolume.SetChannelVolume(0, leftVolume, None)
            channelVolume.SetChannelVolume(1, rightVolume, None)

soundSplitterMonitorCounter = 0
def soundSplitterMonitorThread(localSoundSplitterMonitorCounter):
    global soundSplitterMonitorCounter
    while localSoundSplitterMonitorCounter == soundSplitterMonitorCounter:
        if not getConfig("soundSplit"):
            return
        setAppsVolume()
        #time.sleep(1)
        yield 1000

def updateSoundSplitterMonitorThread(exit=False):
    global soundSplitterMonitorCounter
    soundSplitterMonitorCounter += 1
    if exit:
        setAppsVolume((100,100))
        return
    ss = getConfig("soundSplit")
    if ss:
        executeAsynchronously(soundSplitterMonitorThread(soundSplitterMonitorCounter))
    else:
        setAppsVolume()


def findTableCell(selfself, gesture, movement="next", axis=None, index = 0):
    from scriptHandler import isScriptWaiting
    if isScriptWaiting():
        return
    formatConfig=config.conf["documentFormatting"].copy()
    formatConfig["reportTables"]=True
    try:
        origCell = selfself._getTableCellCoords(selfself.selection)
        info = selfself._getTableCellAt(origCell.tableID, selfself.selection, origCell.row, origCell.col)
    except LookupError:
        # Translators: The message reported when a user attempts to use a table movement command
        # when the cursor is not within a table.
        ui.message(_("Not in a table cell"))
        return

    MAX_TABLE_DIMENSION = 500

    edgeFound = False
    for attempt in range(MAX_TABLE_DIMENSION):
        origCell = selfself._getTableCellCoords(info)
        try:
            info = selfself._getNearestTableCell(info, origCell, movement, axis)
        except LookupError:
            edgeFound = True
            break
    if not edgeFound:
        ui.message(_("Cannot find edge of table in this direction"))
        info = self._getTableCellAt(origCell.tableID, self.selection, origCell.row, origCell.col)
        info.collapse()
        self.selection = info
        return

    if index > 1:
        inverseMovement = "next" if movement == "previous" else "previous"
        for i in range(1, index):
            origCell = selfself._getTableCellCoords(info)
            try:
                info = selfself._getNearestTableCell(selfself.selection, origCell, inverseMovement, axis)
            except LookupError:
                ui.message(_("Cannot find {axis} with index {index} in this table").format(**locals()))
                return

    speech.speakTextInfo(info,formatConfig=formatConfig,reason=REASON_CARET)
    info.collapse()
    selfself.selection = info

def deferredMessage(s):
    def func():
        speech.cancelSpeech()
        ui.message(s, speechPriority=SpeechPriority.NOW)
    core.callLater(100, func)

def copyTableToClipboard(table):
    htmlText = "\n".join([
        "<tr>" +
        "".join([
            f"<td>{html.escape(cell)}</td>"
            for cell in row
        ])
        + "</tr>"
        for row in table
    ])
    htmlText = f"<table>\n{htmlText}\n</table>"
    htmlDataObject = wx.HTMLDataObject()
    htmlDataObject.SetHTML(htmlText)

    def processPlainText(s):
        return (
            s.replace("\r\n", " ")
                .replace("\r", " ")
                .replace("\n", " ")
                .replace("\t", " ")
        )
    plainText = "\n".join([
        "\t".join([
            processPlainText(cell)
            for cell in row
        ])
        for row in table
    ])
    plainTextObject = wx.TextDataObject()
    plainTextObject.SetText(plainText)

    composite = wx.DataObjectComposite()
    composite.Add(htmlDataObject)
    composite.Add(plainTextObject)
    wx.TheClipboard.Open()
    wx.TheClipboard.SetData(composite)
    wx.TheClipboard.Close()


def copyRowImpl(selfself, tableID, startPos, row, colRange):
    result = []
    for col in colRange:
        try:
            info = selfself._getTableCellAt(tableID,startPos,row,col)
        except LookupError:
            return result
        result.append(info.text)
    return result

def copyTableImpl(selfself, currentRow=False, currentColumn=False, partial=False):
    try:
        origCell = selfself._getTableCellCoords(selfself.selection)
    except LookupError:
        deferredMessage(_("Not in a table!"))
        return
    startPos = selfself.selection
    result = []
    api.origCell = origCell
    rowRange = range(origCell.row, origCell.row+1) if currentRow else range(origCell.row if partial else 1, 200)
    colRange = range(origCell.col, origCell.col+1) if currentColumn else range(origCell.col if partial else 1, 200)
    for row in rowRange:
        row = copyRowImpl(selfself, origCell.tableID, startPos, row, origCell.col if currentColumn else None)
        if len(row) > 0:
            result.append(row)
        else:
            return result
    return result

def copyCell(selfself, gesture):
    cells = copyTableImpl(selfself, currentRow=True, currentColumn=True)
    if cells is not None:
        api.copyToClip(cells[0][0])
        deferredMessage(_("Cell copied"))


def copyRow(selfself, gesture):
    cells = copyTableImpl(selfself, currentRow=True)
    if cells is not None:
        copyTableToClipboard(cells)
        deferredMessage(_("Row copied"))

def copyRowPartial(selfself, gesture):
    cells = copyTableImpl(selfself, currentRow=True, partial=True)
    if cells is not None:
        copyTableToClipboard(cells)
        deferredMessage(_("Partial row copied"))

def copyColumn(selfself, gesture):
    cells = copyTableImpl(selfself, currentColumn=True)
    if cells is not None:
        copyTableToClipboard(cells)
        deferredMessage(_("Column copied"))

def copyColumnPartial(selfself, gesture):
    cells = copyTableImpl(selfself, currentColumn=True, partial=True)
    if cells is not None:
        copyTableToClipboard(cells)
        deferredMessage(_("Partial column copied"))

def copyTable(selfself, gesture):
    cells = copyTableImpl(selfself)
    if cells is not None:
        copyTableToClipboard(cells)
        deferredMessage(_("Table copied"))

def copyTablePopup(selfself,gesture):
    try:
        origCell = selfself._getTableCellCoords(selfself.selection)
    except LookupError:
        deferredMessage(_("Not in a table!"))
        return

    gui.mainFrame.prePopup()
    try:
        frame = wx.Frame(None, -1,"Fake popup frame")
        menu = wx.Menu()
        for func, menuStr  in [
            (copyCell, _("Copy ce&ll")),
            (copyColumn, _("Copy &column")),
            (copyColumnPartial, _("Copy column from current cell &down")),
            (copyRow, _("Copy &row")),
            (copyRowPartial, _("Copy row from current cell to the ri&ght")),
            (copyTable, _("Copy &table")),
        ]:
            item = menu.Append(wx.ID_ANY, menuStr)
            frame.Bind(
                wx.EVT_MENU,
                lambda evt, func=func: func(selfself, gesture),
                item,
            )

        frame.Bind(
            wx.EVT_MENU_CLOSE,
            lambda evt: frame.Close()
        )
        frame.Show()

        wx.CallAfter(lambda: frame.PopupMenu(menu))
    finally:
        gui.mainFrame.postPopup()

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


originalSpeechSpeak = None
def processLanguages(command):
    if isinstance(command, speech.commands.LangChangeCommand):
        return
    if not isinstance(command, str):
        yield command
        return
    s = command
    global langMap
    if False:
        langMap = {
            'en': re.compile(r'[a-zA-Z]'),
            'ru': re.compile(r'[а-яА-Я]'),
        }
    curLang = None
    i = -1
    prev = 0
    while i+1 < len(s):
        minIndex = None
        minLang = None
        for lang, r in langMap.items():
            if lang == curLang:
                continue
            m = r.search(s, pos=i+1)
            if m is not None:
                if minIndex is None or m.start(0) < minIndex:
                    minIndex = m.start(0)
                    minLang = lang
        if minLang is not None:
            if minIndex > prev:
                yield s[prev:minIndex]
            yield speech.commands.LangChangeCommand(minLang)
            curLang = minLang
            i = minIndex
            prev = minIndex
        else:
            break
    if i < len(s):
        i = max(i, 0)
        yield s[i:]

def newSpeechSpeak(speechSequence, *args, **kwargs):
    sequence = speechSequence
    if getConfig('enableLangMap'):
        sequence = [subcommand for command in sequence for subcommand in processLanguages(command)]
        #mylog(str(sequence))
    return originalSpeechSpeak(sequence, *args, **kwargs)


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

def updateScrollLockBlocking():
    doBlock = getConfig("blockScrollLock")
    TOGGLE_KEYS = {
        winUser.VK_CAPITAL,
        winUser.VK_NUMLOCK,
    }
    if not doBlock:
        TOGGLE_KEYS.add(winUser.VK_SCROLL)
    keyboardHandler.KeyboardInputGesture.TOGGLE_KEYS = frozenset(TOGGLE_KEYS)

class NoLocationException(Exception):
    pass

class ReleaseControlModifier:
    AttachThreadInput = winUser.user32.AttachThreadInput
    GetKeyboardState = winUser.user32.GetKeyboardState
    SetKeyboardState = winUser.user32.SetKeyboardState

    def __init__(self, obj=None):
        if obj is None:
            obj = api.getFocusObject()
        self.obj = obj
    def __enter__(self):
        hwnd =  self.obj.windowHandle
        processID,ThreadId = winUser.getWindowThreadProcessID(hwnd)
        self.ThreadId = ThreadId
        self.AttachThreadInput(ctypes.windll.kernel32.GetCurrentThreadId(), ThreadId, True)
        PBYTE256 = ctypes.c_ubyte * 256
        pKeyBuffers = PBYTE256()

        pKeyBuffers_old = PBYTE256()
        self.GetKeyboardState( ctypes.byref(pKeyBuffers_old ))
        self.pKeyBuffers_old = pKeyBuffers_old

        self.SetKeyboardState( ctypes.byref(pKeyBuffers) )
        return self
    def __exit__(self, *args, **kwargs):
        self.SetKeyboardState( ctypes.byref(self.pKeyBuffers_old) )
        self.AttachThreadInput(ctypes.windll.kernel32.GetCurrentThreadId(), self.ThreadId, False)

WS_EX_TOPMOST = 0x0008
HWND_BOTTOM = ctypes.wintypes.HWND(1)
HWND_NOTOPMOST = ctypes.wintypes.HWND(-2)
HWND_TOP = ctypes.wintypes.HWND(0)
HWND_TOPMOST = ctypes.wintypes.HWND(-1)

def isWindowTopmost(hwnd):
    exStyle = winUser.getExtendedWindowStyle(hwnd)
    return exStyle & WS_EX_TOPMOST != 0

def setWindowTopmost(hwnd, level):
    winUser.user32.SetWindowPos(
        hwnd,
        level,
        0, 0, 0, 0,
        winUser.SWP_NOACTIVATE | winUser.SWP_NOMOVE | winUser.SWP_NOSIZE
    )


_getParent = ctypes.windll.user32.GetParent
def getWindowParent(hwnd):
    return _getParent(hwnd)

def getTopLevelWindow(hwnd):
    result = []
    while hwnd != 0:
        result.append(hwnd)
        hwnd = getWindowParent(hwnd)
    return result[-1]

def getTopLevelWindowNVDA(obj):
    result = []
    desktop = api.getDesktopObject()
    while obj is not None and obj != desktop:
        result.append(obj.windowHandle)
        obj = obj.simpleParent
    return result[-1]

_windowFromPoint = ctypes.windll.user32.WindowFromPoint
lastPoint = None
class MousePointerHover:
    def getBestLocation(self):
        reviewInfo = api.getReviewPosition()
        startObj = reviewInfo.NVDAObjectAtStart
        if startObj is not None and startObj.isFocusable:
            p= startObj.location
            self.kind = _("focusable object")
        else:
            try:
                p = reviewInfo._getBoundingRectFromOffset(t._startOffset)
                self.kind = _("current review character")
            except:
                try:
                    left,top = reviewInfo.pointAtStart
                    width = height = 0
                    p = locationHelper.RectLTWH(left, top, width, height)
                    self.kind = _("current review character")
                except:
                    try:
                        p = api.getNavigatorObject().location
                        self.kind = _("navigator object")
                    except:
                        raise NoLocationException()
        self.x = p.left + p.width // 2
        self.y = p.top + p.height //2
        return (self.x, self.y)

    def __enter__(self):
        global lastPoint
        focus = api.getFocusObject()
        currentNVDAWindowHandle = getTopLevelWindowNVDA(focus)
        x,y = self.getBestLocation()
        p = winUser.getCursorPos()
        self.oldPos = p
        winUser.setCursorPos(x,y)
        for counter in range(100):
            hwnd = _windowFromPoint(ctypes.wintypes.POINT(x,y))
            if counter == 0 and hwnd == 0:
                (x,y) = lastPoint
                mouseHandler.executeMouseMoveEvent(x,y)
                self.kind = _("repeat")
                return
            topHwnd = getTopLevelWindow(hwnd)
            if topHwnd == currentNVDAWindowHandle:
                mouseHandler.executeMouseMoveEvent(x,y)
                lastPoint = (x,y)
                return self
            tones.beep(500, 50)
            setWindowTopmost(topHwnd, HWND_BOTTOM)
        raise Exception("Infinite loop!")

    def __exit__(self, *argc, **argv):
        x,y = tuple(self.oldPos)
        winUser.setCursorPos(x, y)
        mouseHandler.executeMouseMoveEvent(x,y)

        pass


reloadDynamicKeystrokes()
reloadLangMap()
updatePriority()
updateSoundSplitterMonitorThread()
updateScrollLockBlocking()

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
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(SettingsDialog)

    def terminate(self):
        updateSoundSplitterMonitorThread(exit=True)
        from . pycaw.pycaw import AudioUtilities
        microphone = AudioUtilities.GetDefaultMicrophone()
        if microphone is not None:
            microphone.SetMute(False, None)
        self.removeHooks()
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(SettingsDialog)

    quickSearchGestures = ",PrintScreen,ScrollLock,Pause".split(",")
    def injectHooks(self):
        global originalWaveOpen, originalWatchdogAlive, originalWatchdogAsleep,  originalSpeakSelectionChange, originalCaretMovementScriptHelper,  originalSpeechSpeak
        self.originalExecuteGesture = inputCore.InputManager.executeGesture
        inputCore.InputManager.executeGesture = lambda selfself, gesture, *args, **kwargs: self.preExecuteGesture(selfself, gesture, *args, **kwargs)
        originalWaveOpen = nvwave.WavePlayer.open
        nvwave.WavePlayer.open = preWaveOpen
        originalWatchdogAlive = watchdog.alive
        watchdog.alive = preWatchdogAlive
        originalWatchdogAsleep = watchdog.asleep
        watchdog.asleep = preWatchdogAsleep
        self.myWatchdog = MyWatchdog()
        self.myWatchdog.setDaemon(True)
        self.myWatchdog.start()
        originalSpeakSelectionChange = speech.speakSelectionChange
        speech.speakSelectionChange = preSpeakSelectionChange
        originalSpeechSpeak = speech.speak
        speech.speak = newSpeechSpeak

        for i in [1,2,3]:
            configKey = f"quickSearch{i}"
            script = lambda selfself, gesture, configKey=configKey: self.script_quickSearch(selfself, gesture, getConfig(configKey))
            script.category = "Tony's Enhancements"
            script.__name__ = _("QuickSearch") + str(i)
            script.__doc__ = _("Performs QuickSearch back or forward in editables according to quickSearch{i} regexp").format(**locals())
            setattr(editableText.EditableText, f"script_quickSearch{i}", script)
            editableText.EditableText._EditableText__gestures[f"kb:{self.quickSearchGestures[i]}"] = f"quickSearch{i}"
            editableText.EditableText._EditableText__gestures[f"kb:Shift+{self.quickSearchGestures[i]}"] = f"quickSearch{i}"

    def  removeHooks(self):
        global originalWaveOpen
        inputCore.InputManager.executeGesture = self.originalExecuteGesture
        nvwave.WavePlayer.open = originalWaveOpen
        watchdog.alive = originalWatchdogAlive
        watchdog.asleep = originalWatchdogAsleep
        self.myWatchdog.terminate()
        speech.speakSelectionChange = originalSpeakSelectionChange
        speech.speak = originalSpeechSpeak
        for i in [1,2,3]:
            delattr(editableText.EditableText, f"script_quickSearch{i}")
            del editableText.EditableText._EditableText__gestures[f"kb:{self.quickSearchGestures[i]}"]
            del editableText.EditableText._EditableText__gestures[f"kb:Shift+{self.quickSearchGestures[i]}"]

    windowsSwitchingRe = re.compile(r':windows\+\d$')
    typingKeystrokeRe = re.compile(r':((shift\+)?[A-Za-z0-9]|space)$')
    shiftSelectionKeystroke = re.compile(r':(control\+)?shift\+((up|down|left|right)Arrow|home|end|pageUp|pageDown)$')
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

        kb = gesture.identifiers
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

        if getConfig("fixWindowNumber") and self.windowsSwitchingRe.search(kb) is not None:

            executeAsynchronously(self.asyncSwitchWindowHandler(gestureCounter))
        if getConfig("detectInsertMode") and self.typingKeystrokeRe.search(kb):
            text = None
            caret = None
            executeAsynchronously(self.insertModeDetector(gestureCounter, text, caret))
        if getConfig('suppressUnselected') and self.shiftSelectionKeystroke.search(kb) is not None:
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
        oldLines = args[1]
        newLines = args[0]
        if oldLines == newLines:
            return []
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
            scriptName="copyTableToClipboardPopup",
            kb="NVDA+Alt+T",
            doc="Show popup menu with copy table to clipboard commands.",
            function=copyTablePopup,
        )
        self.injectTableFunction(
            scriptName="copyCellToClipboard",
            kb=None,
            doc="Copy table cell to clipboard.",
            function=copyCell,
        )
        self.injectTableFunction(
            scriptName="copyColumnToClipboard",
            kb=None,
            doc="Copy table column to clipboard.",
            function=copyColumn,
        )
        self.injectTableFunction(
            scriptName="copyRowToClipboard",
            kb=None,
            doc="Copy table row to clipboard.",
            function=copyRow,
        )
        self.injectTableFunction(
            scriptName="copyTableToClipboard",
            kb=None,
            doc="Copy the whole table to clipboard.",
            function=copyTable,
        )


    def injectTableFunction(self, scriptName, kb, doc, function=findTableCell, *args, **kwargs):
        cls = documentBase.DocumentWithTableNavigation
        funcName = "script_%s" % scriptName
        script = lambda self,gesture: function(self, gesture, *args, **kwargs)
        script.__name__ = funcName
        script.__doc__ = doc
        script.category = self.scriptCategory
        setattr(cls, funcName, script)
        if kb is not None:
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

    @script(description='Increase applications volume.', gestures=['kb:NVDA+Alt+PageUp'])
    def script_increaseAppVolume(self, gesture):
        self.adjustAppVolume(5)

    @script(description='Decrease applications volume.', gestures=['kb:NVDA+Alt+PageDown'])
    def script_decreaseAppVolume(self, gesture):
        self.adjustAppVolume(-5)

    def adjustAppVolume(self, increment):
        volume = getConfig("appsVolume")
        volume += increment
        if volume > 100:
            volume = 100
        if volume < 0:
            volume = 0
        setConfig("appsVolume", volume)
        message = _("Applications volume %d") % volume
        ui.message(message)
        setAppsVolume()


    def script_quickSearch(self, selfself, gesture, regex):
        if "shift" in gesture._get_modifierNames():
            direction = -1
        else:
            direction = 1
        caretInfo = selfself.makeTextInfo(textInfos.POSITION_SELECTION)
        caretInfo.collapse(end=(direction > 0))
        info = selfself.makeTextInfo(textInfos.POSITION_ALL)
        info.setEndPoint(caretInfo, 'startToStart' if direction > 0 else 'endToEnd')
        text = info.text
        text = text.replace("\r\n", "\n") # Fix for Notepad++
        text = text.replace("\r", "\n") # Fix for AkelPad
        matches = list(re.finditer(regex, text, re.MULTILINE))
        if len(matches) == 0:
            self.beeper.fancyBeep('HF', 100, left=25, right=25)
            return
        if direction > 0:
            match = matches[0]
            #adjustment = match.start()
            preLines = text[:match.start()].split("\n")
            if len(preLines) > 1:
                # Go to the beginning of the line to avoid some inconsistent behavior
                caretInfo.expand(textInfos.UNIT_PARAGRAPH)
                caretInfo.collapse(end=False)
                caretInfo.move(textInfos.UNIT_PARAGRAPH, len(preLines) - 1)
                caretInfo.expand(textInfos.UNIT_PARAGRAPH)
                caretInfo.collapse(end=False)
            caretInfo.move(textInfos.UNIT_CHARACTER, len(preLines[-1]))
        else:
            match = matches[-1]
            #adjustment = match.start() - len(text)
            preLines = text[:match.start()].split("\n")
            postLines = text[match.start():].split("\n")
            if len(postLines) > 1:
                q = -len(postLines) + 1
                # Go to the beginning of the line to avoid some inconsistent behavior
                caretInfo.expand(textInfos.UNIT_PARAGRAPH)
                caretInfo.collapse(end=False)
                caretInfo.move(textInfos.UNIT_PARAGRAPH, -len(postLines) + 1)
            caretInfo.expand(textInfos.UNIT_PARAGRAPH)
            caretInfo.collapse(end=False)
            caretInfo.move(textInfos.UNIT_CHARACTER, len(preLines[-1]))
        caretInfo.move(textInfos.UNIT_CHARACTER, match.end() - match.start(), endPoint='end')
        caretInfo.updateSelection()
        mylog(f"1. {caretInfo.text}")
        lineInfo = caretInfo.copy()
        lineInfo.expand(textInfos.UNIT_PARAGRAPH)
        mylog(f"2. {lineInfo.text}")
        lineInfo.setEndPoint(caretInfo, 'startToStart')
        mylog(lineInfo.text)
        speech.speakTextInfo(lineInfo, unit=textInfos.UNIT_PARAGRAPH, reason=REASON_CARET)

    hiddenWindows = []
    @script(description='Hide current window.', gestures=['kb:NVDA+Shift+-'])
    def script_HideWindow(self, gesture):
        fg = api.getForegroundObject()
        handle = fg.windowHandle
        self.hiddenWindows.append(handle)
        winUser.user32.ShowWindow(handle, winUser.SW_HIDE)
        keyboardHandler.KeyboardInputGesture.fromName("Alt+Tab").send()
        #winUser.setForegroundWindow(api.getDesktopObject().windowHandle)
        def delayedSpeak():
            speech.cancelSpeech()
            ui.message(_("Hid current window. Now there are %d windows hidden.") % len(self.hiddenWindows))
        core.callLater(100, delayedSpeak)

    @script(description='Show hidden windows.', gestures=['kb:NVDA+Shift+='])
    def script_showWindows(self, gesture):
        if len(self.hiddenWindows) == 0:
            ui.message(_("No windows hidden or all hidden windows have been already shown."))
            return
        n = len(self.hiddenWindows)
        for handle in self.hiddenWindows:
            time.sleep(0.1)
            SW_SHOW = 5
            winUser.user32.ShowWindow(handle, SW_SHOW)
        winUser.setForegroundWindow(self.hiddenWindows[-1])
        def delayedSpeak():
            speech.cancelSpeech()
            ui.message(_("%d windows shown") % n)
        core.callLater(100, delayedSpeak)
        self.hiddenWindows = []

    @script(description='Toggle sound split.', gestures=['kb:NVDA+Alt+S'])
    def script_toggleSoundSplit(self, gesture):
        ss = getConfig("soundSplit")
        ss = not ss
        msg = _("Sound split enabled") if ss else _("Sound split disabled")
        setConfig("soundSplit", False)
        def updateSoundSplit():
            setConfig("soundSplit", ss)
            updateSoundSplitterMonitorThread()
        #core.callLater(100, updateSoundSplit)
        updateSoundSplit()
        ui.message(msg)

    @script(description='Toggle microphone mute.', gestures=['kb:NVDA+Delete'])
    def script_toggleMicrophoneMute(self, gesture):
        from . pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        microphone = AudioUtilities.GetDefaultMicrophone()
        if microphone is None:
            ui.message(_("Default microphone not found."))
            return
        mm = bool(microphone.GetMute())
        mm = not mm
        microphone.SetMute(mm, None)
        msg = _("Muted microphone") if mm else _("Unmuted microphone")
        def announce():
            speech.cancelSpeech()
            ui.message(msg)
        core.callLater(100, announce)

    @script(description='Left click on current object.', gestures=['kb:Alt+NumPadDivide'])
    def script_leftClick(self, gesture):
        with ReleaseControlModifier():
            with MousePointerHover() as m:
                kind = m.kind
                ui.message(_("Left click on {kind}").format(kind=kind))
                mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_LEFTDOWN,0,0)
                mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_LEFTUP,0,0)

    @script(description='Right click on current object.', gestures=['kb:Alt+NumPadMultiply'])
    def script_rightClick(self, gesture):
        with ReleaseControlModifier():
            with MousePointerHover() as m:
                kind = m.kind
                ui.message(_("Left click on {kind}").format(kind=kind))
                mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_RIGHTDOWN,0,0)
                mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_RIGHTUP,0,0)

    @script(description='Mouse wheel scroll down on current object.', gestures=['kb:Alt+NumPadPlus'])
    def script_scrollDown(self, gesture):
        with ReleaseControlModifier():
            with MousePointerHover() as m:
                ui.message(_("Scroll down"))
                mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_WHEEL,0,0, -1000)

    @script(description='Mouse wheel scroll up on current object.', gestures=['kb:Alt+NumPadMinus'])
    def script_scrollUp(self, gesture):
        with ReleaseControlModifier():
            with MousePointerHover() as m:
                ui.message(_("Scroll up"))
                mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_WHEEL,0,0, 1000)

    @script(description='Move mouse pointer to top left corner.', gestures=['kb:Alt+NumPadDelete'])
    def script_mouseMoveToTopLeft(self, gesture):
        ui.message(_("Mouse pointer moved to top left corner. "))
        mouseHandler.executeMouseMoveEvent(0, 0)
