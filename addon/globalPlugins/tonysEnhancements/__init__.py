# -*- coding: UTF-8 -*-
#A part of  Tony's Enhancements addon for NVDA
#Copyright (C) 2019 Tony Malykh
#This file is covered by the GNU General Public License.
#See the file COPYING.txt for more details.

import addonHandler
import api
import config
import controlTypes
import core
import copy
import ctypes
from ctypes import create_string_buffer, byref
import documentBase
import globalPluginHandler
import gui
from gui.settingsDialogs import SettingsPanel
import html
import inputCore
import keyboardHandler
import locationHelper
from logHandler import log
import mouseHandler
import NVDAHelper
import nvwave
import operator
import re
from scriptHandler import script
import speech
from speech.priorities import SpeechPriority
import struct
import textInfos
import threading
import time
import tones
import types
import ui
import watchdog
import winUser
import wx
from . import audio
import globalVars

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
        "soundSplitState": "integer(default=0)",
        "includedSoundSplitModes": "int_list(default=list(0, 2, 3))",
        "applicationsSoundVolume": "integer(default=100, min=0, max=100)",
        "applicationsSoundMuted": "boolean(default=False)",
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
        keystroke = tokens[1].rstrip()
        try:
            kb = keyboardHandler.KeyboardInputGesture.fromName(keystroke).identifiers[0]
        except (KeyError, IndexError):
            raise ValueError(f"Invalid kb shortcut {keystroke}")
        except LookupError:
            log.error(f"Invalid kb shortcut {keystroke}")
            continue
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
      # checkbox suppress unselected
        # Translators: Checkbox for suppress unselected
        label = _("Suppress saying of 'unselected'.")
        self.suppressUnselectedCheckbox = sHelper.addItem(wx.CheckBox(self, label=label))
        self.suppressUnselectedCheckbox.Value = getConfig("suppressUnselected")
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
        setConfig("suppressUnselected", self.suppressUnselectedCheckbox.Value)
        setConfig("detectInsertMode", self.detectInsertModeCheckbox.Value)
        setConfig("dynamicKeystrokesTable", self.dynamicKeystrokesTable)
        reloadDynamicKeystrokes()
        setConfig("enableLangMap", self.langMapCheckbox.Value)
        setConfig("langMap", self.langMap)
        reloadLangMap()
        setConfig("blockScrollLock", self.blockScrollLockCheckbox.Value)
        updateScrollLockBlocking()
        setConfig("priority", self.priorityCombobox.Selection)
        updatePriority()

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
        try:
            outputDevice=config.conf["speech"]["outputDevice"]
        except KeyError:
            outputDevice=config.conf["audio"]["outputDevice"]
        self.player = nvwave.WavePlayer(
            channels=2,
            samplesPerSec=int(tones.SAMPLE_RATE),
            bitsPerSample=16,
            outputDevice=outputDevice,
            wantDucking=False,
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
        buffer = self.prepareFancyBeep(chord, length, left, right)
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

originalWatchdogAlive = None
originalWatchdogAsleep = None

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
    rowRange = range(origCell.row, origCell.row+1) if currentRow else range(origCell.row if partial else 1, 1000)
    colRange = range(origCell.col, origCell.col+1) if currentColumn else range(origCell.col if partial else 1, 1000)
    for row in rowRange:
        row = copyRowImpl(selfself, origCell.tableID, startPos, row, colRange)
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
    Specifically, every time the generator function yields a positive number,, the rest of the generator function will be executed
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

# For some reason Since some Windows update around March 2025 we cannot resolve keystrokes right away - this throws an exception.
# Doing it with a delay of 3 seconds.
#reloadDynamicKeystrokes()
core.callLater(5000, reloadDynamicKeystrokes)
reloadLangMap()
updatePriority()
updateScrollLockBlocking()

audio.initialize()

def getControlVGesture():
    try:
        return keyboardHandler.KeyboardInputGesture.fromName("Control+v")
    except LookupError:
        # This happens if vk code for letter V fails to resolve, when current keyboard layout is for example Russian
        # vk code for V key is 86
        return keyboardHandler.KeyboardInputGesture(modifiers={(winUser.VK_CONTROL, False)}, vkCode=86, scanCode=0, isExtended=False)

def ephemeralCopyToClip(text: str):
    """
    Copies string to clipboard without leaving an entry in clipboard history.
    """
    with winUser.openClipboard(gui.mainFrame.Handle):
        winUser.emptyClipboard()
        winUser.setClipboardData(winUser.CF_UNICODETEXT, text)
        ephemeralFormat = ctypes.windll.user32.RegisterClipboardFormatW("ExcludeClipboardContentFromMonitorProcessing")
        ctypes.windll.user32.SetClipboardData(ephemeralFormat,None)

class BackupClipboard:
    def __init__(self, text):
        try:
            self.backup = api.getClipData()
        except OSError:
            self.backup = ""
        self.text = text
    def __enter__(self):
        ephemeralCopyToClip(self.text)
        return self
    def __exit__(self, *args, **kwargs):
        core.callLater(300, self.restore)
    def restore(self):
        ephemeralCopyToClip(self.backup)

TEXT_FORMAT = "Text"
def getClipboardEntries(maxEntries=50):
    from .pywinsdk.relative import winsdk
    from .pywinsdk.relative.winsdk.windows.applicationmodel.datatransfer import Clipboard
    from .pywinsdk.relative.winsdk.windows.foundation import AsyncStatus
    
    def dummyAwait(result):
        while result.status == AsyncStatus.STARTED:
            wx.Yield()
        if result.status == AsyncStatus.COMPLETED:
            return result
        raise RuntimeError(f"Bad async status {result.status}")

    history = dummyAwait(Clipboard.get_history_items_async())
    items = history.get_results()
    itemTuples = []    
    result = []
    for i in range(maxEntries):
        try:
            item = items.items[i]
        except OSError:
            continue
        content = item.content
        avf = content.available_formats
        avf2 = [avf.get_at(j) for j in range(avf.size)]
        if TEXT_FORMAT not in avf2:
            continue
        itemTuples.append((item,content.get_text_async()))
    for item, text in itemTuples:
        text = dummyAwait(text)
        value = text.get_results()
        result.append(value)
    return result

def truncateLongString(s):
    MAX_LEN = 1000
    if len(s) > MAX_LEN:
        s = s[:MAX_LEN] + "..."
    return s

# Adapted from Frequent Text add-on
clipboardHistoryEntries = []
class ClipboardHistoryDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.title = _("Clipboard history")
        global clipboardHistoryEntries
        self.listBlocks = clipboardHistoryEntries
        self.listBlocksTruncated = [truncateLongString(s) for s in self.listBlocks]
        
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        listLabel = wx.StaticText(self, wx.ID_ANY, _("Entries"))
        sizer_1.Add(listLabel, 0, 0, 0)

        self.BlocksList = wx.ListBox(self, wx.ID_ANY, choices=self.listBlocksTruncated, style=wx.LB_SINGLE)
        self.BlocksList.SetFocus()
        if len(self.listBlocks) != 0:
            self.BlocksList.SetSelection(0)
        sizer_1.Add(self.BlocksList, 0, 0, 0)

        sizer_2 = wx.StdDialogButtonSizer()
        sizer_1.Add(sizer_2, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 4)

        self.pasteButton = wx.Button(self, wx.ID_ANY, _("&Paste"))
        if len(self.listBlocks) > 0:
            self.pasteButton.SetDefault()
        sizer_2.Add(self.pasteButton, 0, 0, 0)

        self.button_CLOSE = wx.Button(self, wx.ID_CLOSE, "")
        sizer_2.AddButton(self.button_CLOSE)

        if self.BlocksList.GetCount() == 0:
            self.pasteButton.Disable()

        sizer_2.Realize()

        self.SetSizer(sizer_1)
        sizer_1.Fit(self)

        self.SetEscapeId(self.button_CLOSE.GetId())

        self.Layout()
        self.Centre()

        self.Bind(wx.EVT_BUTTON, self.onPaste, self.pasteButton)
    
    def onPaste(self, evt):
        self.Hide()
        evt.Skip()
        # Get the name of selected block
        name = self.listBlocks[self.BlocksList.GetSelection()]
        pasteStr = name
        with BackupClipboard(pasteStr):
            focus = api.getFocusObject()
            if focus.windowClassName == "ConsoleWindowClass":
                # Windows console window - Control+V doesn't work here, so using an alternative method here
                WM_COMMAND = 0x0111
                watchdog.cancellableSendMessage(focus.windowHandle, WM_COMMAND, 0xfff1, 0)
            else:
                keyboardHandler.KeyboardInputGesture.fromName("Control+v").send()
        self.Destroy()

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
        from  pycaw.utils import AudioUtilities
        microphone = AudioUtilities.CreateDevice(AudioUtilities.GetMicrophone())
        if microphone is not None:
            microphone.EndpointVolume.SetMute(False, None)
        self.removeHooks()
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(SettingsDialog)

    def injectHooks(self):
        global originalWatchdogAlive, originalWatchdogAsleep,  originalSpeakSelectionChange, originalCaretMovementScriptHelper,  originalSpeechSpeak
        self.originalExecuteGesture = inputCore.InputManager.executeGesture
        inputCore.InputManager.executeGesture = lambda selfself, gesture, *args, **kwargs: self.preExecuteGesture(selfself, gesture, *args, **kwargs)
        originalWatchdogAlive = watchdog.alive
        watchdog.alive = preWatchdogAlive
        originalWatchdogAsleep = watchdog.asleep
        watchdog.asleep = preWatchdogAsleep
        self.myWatchdog = MyWatchdog()
        self.myWatchdog.setDaemon(True)
        self.myWatchdog.start()
        originalSpeakSelectionChange = speech.speakSelectionChange
        speech.speakSelectionChange = preSpeakSelectionChange
        originalSpeechSpeak = speech.speech.speak
        speech.speech.speak = newSpeechSpeak


    def  removeHooks(self):
        inputCore.InputManager.executeGesture = self.originalExecuteGesture
        watchdog.alive = originalWatchdogAlive
        watchdog.asleep = originalWatchdogAsleep
        self.myWatchdog.terminate()
        speech.speakSelectionChange = originalSpeakSelectionChange
        speech.speech.speak = originalSpeechSpeak

    typingKeystrokeRe = re.compile(r':((shift\+)?[A-Za-z0-9]|space)$')
    shiftSelectionKeystroke = re.compile(r':(control\+)?shift\+((up|down|left|right)Arrow|home|end|pageUp|pageDown)$')
    def preExecuteGesture(self, selfself, gesture, *args, **kwargs):
        global gestureCounter, editorMovingCaret, performingShiftGesture
        gestureCounter += 1
        editorMovingCaret = False
        # Check if gesture has the vkCode attribute
        if hasattr(gesture, 'vkCode'):
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
        if getConfig("detectInsertMode") and self.typingKeystrokeRe.search(kb):
            text = None
            caret = None
            executeAsynchronously(self.insertModeDetector(gestureCounter, text, caret))
        if getConfig('suppressUnselected') and self.shiftSelectionKeystroke.search(kb) is not None:
            performingShiftGesture = True
        else:
            performingShiftGesture = False
        return self.originalExecuteGesture(selfself, gesture, *args, **kwargs)

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
                doc=_("Move to the %d-th column in table") % i,
                movement="previous",
                axis="column",
                index = i,
            )
            self.injectTableFunction(
                scriptName=f"jumpToRow{i}",
                kb="NVDA+Alt+%d" % (i%10),
                doc=_("Move to the %d-th row in table") % i,
                movement="previous",
                axis="row",
                index = i,
            )
        self.injectTableFunction(
            scriptName="copyTableToClipboardPopup",
            kb="NVDA+Alt+T",
            doc=_("Show popup menu with copy table to clipboard commands."),
            function=copyTablePopup,
        )
        self.injectTableFunction(
            scriptName="copyCellToClipboard",
            kb=None,
            doc=_("Copy table cell to clipboard."),
            function=copyCell,
        )
        self.injectTableFunction(
            scriptName="copyColumnToClipboard",
            kb=None,
            doc=_("Copy table column to clipboard."),
            function=copyColumn,
        )
        self.injectTableFunction(
            scriptName="copyRowToClipboard",
            kb=None,
            doc=_("Copy table row to clipboard."),
            function=copyRow,
        )
        self.injectTableFunction(
            scriptName="copyTableToClipboard",
            kb=None,
            doc=_("Copy the whole table to clipboard."),
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

    @script(description=_("Toggle microphone mute."))
    def script_toggleMicrophoneMute(self, gesture):
        from  pycaw.utils import AudioUtilities, IAudioEndpointVolume
        microphone = AudioUtilities.CreateDevice(AudioUtilities.GetMicrophone())
        if microphone is None:
            ui.message(_("Default microphone not found."))
            return
        mm = bool(microphone.EndpointVolume.GetMute())
        mm = not mm
        microphone.EndpointVolume.SetMute(mm, None)
        msg = _("Muted microphone") if mm else _("Unmuted microphone")
        def announce():
            speech.cancelSpeech()
            ui.message(msg)
        core.callLater(100, announce)

    @script(description=_("Left click on current object."), gestures=['kb:Alt+NumPadDivide'])
    def script_leftClick(self, gesture):
        with ReleaseControlModifier():
            with MousePointerHover() as m:
                kind = m.kind
                ui.message(_("Left click on {kind}").format(kind=kind))
                mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_LEFTDOWN,0,0)
                mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_LEFTUP,0,0)

    @script(description=_("Right click on current object."), gestures=['kb:Alt+NumPadMultiply'])
    def script_rightClick(self, gesture):
        with ReleaseControlModifier():
            with MousePointerHover() as m:
                kind = m.kind
                ui.message(_("Left click on {kind}").format(kind=kind))
                mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_RIGHTDOWN,0,0)
                mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_RIGHTUP,0,0)

    @script(description=_("Move mouse pointer to top left corner."), gestures=['kb:Alt+NumPadDelete'])
    def script_mouseMoveToTopLeft(self, gesture):
        ui.message(_("Mouse pointer moved to top left corner. "))
        mouseHandler.executeMouseMoveEvent(0, 0)

    @script(description=_("Show clipboard history"), gestures=['kb:windows+v'])
    def script_showClipboardHistory(self, gesture):
        global clipboardHistoryEntries
        clipboardHistoryEntries = getClipboardEntries()
        gui.mainFrame.popupSettingsDialog(ClipboardHistoryDialog)

    @script(
        description=_(
            # Translators: Describes a command.
            "Increases the volume of other applications",
        ),
        gestures=['kb:NVDA+Alt+PageUp']
    )
    def script_increaseApplicationsVolume(self, gesture: "inputCore.InputGesture") -> None:
        audio.appsVolume._adjustAppsVolume(5)

    @script(
        description=_(
            # Translators: Describes a command.
            "Decreases the volume of other applications",
        ),
        gestures=['kb:NVDA+Alt+PageDown']
    )
    def script_decreaseApplicationsVolume(self, gesture: "inputCore.InputGesture") -> None:
        audio.appsVolume._adjustAppsVolume(-5)

    @script(
        description=_(
            # Translators: Describes a command.
            "Mutes or unmutes other applications",
        ),
    )
    def script_toggleApplicationsMute(self, gesture: "inputCore.InputGesture") -> None:
        appsVolume._toggleAppsVolumeMute()

    def findVolumeSetting(self):
        settings = [
            setting
            for setting in globalVars.settingsRing.settings
            if setting.setting.id == 'volume'
        ]
        return settings[0]
        


    @script(
        description=_("Increases the volume of NVDA",),
        gestures=("kb:NVDA+Control+PageUp",),
    )
    def script_increaseNVDAVolume(self, gesture):
        newVolume = self.findVolumeSetting().increase()
        msg = _("{} percent NVDA volume").format(newVolume)
        ui.message(msg)

    @script(
        description=_("Decreases the volume of NVDA",),
        gestures=("kb:NVDA+Control+PageDown",),
    )
    def script_decreaseNVDAVolume(self, gesture):
        newVolume = self.findVolumeSetting().decrease()
        msg = _("{} percent NVDA volume").format(newVolume)
        ui.message(msg)
