# -*- coding: UTF-8 -*-
#A part of  Tony's Enhancements addon for NVDA
#Copyright (C) 2019 Tony Malykh
#This file is covered by the GNU General Public License.
#See the file COPYING.txt for more details.

import addonHandler
import api
import bisect
import config
import controlTypes
import core
import copy
import ctypes
from ctypes import create_string_buffer, byref
import documentBase
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
import ui
import watchdog
import wave
import winUser
import wx

winmm = ctypes.windll.winmm

debug = True
if debug:
    f = open("C:\\Users\\tony\\Dropbox\\2.txt", "w")
def mylog(s):
    if debug:
        print(str(s), file=f)
        f.flush()

def myAssert(condition):
    if not condition:
        raise RuntimeError("Assertion failed")

defaultDynamicKeystrokes = """
* F1
* F2
* F3
* F4
* F5
* F6
* F7
* F8
* F9
* F9
* F10
* F11
* F12
code Alt+DownArrow
code Alt+UpArrow
code Alt+Home
code Alt+End
code Alt+PageUp
code Alt+PageDown
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
        tokens = line.strip().split()
        if len(tokens) == 0:
            continue
        if len(tokens) != 2:
            raise ValueError(f"INvalid line: {line}")
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
        setConfig("nvdaVolume", self.nvdaVolumeSlider.Value)
        setConfig("dynamicKeystrokesTable", self.dynamicKeystrokesEdit.Value)
        reloadDynamicKeystrokes()
        super(SettingsDialog, self).onOk(evt)

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
            speech.cancelSpeech()
            speech.speakTextInfo(textInfo)
            return
    elapsed = time.time() - originalTimestamp
    if not spokenAnyway and elapsed > speakAnywayAfter:
        speech.speakTextInfo(textInfo)
        spokenAnyway = True
    if elapsed < 1.0:
        sleepTime = 25 # ms
    elif elapsed < 10:
        sleepTime = 1000 # ms
    else:
        sleepTime = 5000
    core.callLater(sleepTime, checkUpdate, localGestureCounter, attempt+1, originalTimestamp, spokenAnyway=spokenAnyway)



class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = _("Tony's Enhancements")

    def __init__(self, *args, **kwargs):
        super(GlobalPlugin, self).__init__(*args, **kwargs)
        self.createMenu()
        self.injectHooks()
        self.injectTableFunctions()
        self.lastConsoleUpdateTime = 0

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
        global originalWaveOpen, originalWatchdogAlive, originalWatchdogAsleep
        self.originalExecuteGesture = inputCore.InputManager.executeGesture
        inputCore.InputManager.executeGesture = lambda selfself, gesture, *args, **kwargs: self.preExecuteGesture(selfself, gesture, *args, **kwargs)
        self.originalCalculateNewText = behaviors.LiveText._calculateNewText
        behaviors.LiveText._calculateNewText = lambda selfself, *args, **kwargs: self.preCalculateNewText(selfself, *args, **kwargs)
        originalWaveOpen = nvwave.WavePlayer.open
        nvwave.WavePlayer.open = preWaveOpen
        originalWatchdogAlive = watchdog.alive
        watchdog.alive = preWatchdogAlive
        originalWatchdogAsleep = watchdog.asleep
        watchdog.asleep = preWatchdogAsleep
        self.myWatchdog = MyWatchdog()
        self.myWatchdog.setDaemon(True)
        self.myWatchdog.start()

    def  removeHooks(self):
        global originalWaveOpen
        inputCore.InputManager.executeGesture = self.originalExecuteGesture
        behaviors.LiveText._calculateNewText = self.originalCalculateNewText
        nvwave.WavePlayer.open = originalWaveOpen
        watchdog.alive = originalWatchdogAlive
        watchdog.asleep = originalWatchdogAsleep
        self.myWatchdog.terminate()

    def preExecuteGesture(self, selfself, gesture, *args, **kwargs):
        global gestureCounter
        gestureCounter += 1
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
        #mylog(str(kb))
        #mylog(dynamicKeystrokes)
        if len(kb) == 0:
            #tones.beep(500, 50)
            pass
        else:
            kb = kb[0]
        focus = api.getFocusObject()
        appName = focus.appModule.appName
        if(
            ("*", kb) in dynamicKeystrokes
            or (appName, kb) in dynamicKeystrokes
        ):
        #if gesture.normalizedIdentifiers == keyboardHandler.KeyboardInputGesture.fromName("Alt+Home").normalizedIdentifiers:
            #tones.beep(700, 50)
            #mylog(str(gesture.normalizedIdentifiers))
            core.callLater(0,
                checkUpdate,
                gestureCounter, 0, time.time(), gesture
            )
            pass
        return self.originalExecuteGesture(selfself, gesture, *args, **kwargs)

    def preCalculateNewText(self, selfself, *args, **kwargs):
        outLines =   self.originalCalculateNewText(selfself, *args, **kwargs)
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
