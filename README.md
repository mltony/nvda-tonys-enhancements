# nvda-tonys-enhancements
This add-on contains a number of small improvements to NVDA screenreader, each of them too small to deserve a separate add-on.

This add-on is compatible with NVDA versions 2022.4 and 2023.1, but it is not compatible with NVDA-Alpha or version 2023.2.

## Downloads

[Tony's enhancements latest stable version](https://github.com/mltony/nvda-tonys-enhancements/releases/latest/download/tonysEnhancements.nvda-addon)

## Enhanced table navigation commands
* NVDA+Control+digit - jump to 1st/2nd/3rd/... 10th column in the table.
* NVDA+Alt+digit - jump to 1st/2nd/3rd/... 10th row in the table.

## Removed table navigation commands

The following table navigation commands have been Removed as they have been integrated into the latest version of NVDA core.

* Jump to the first/last column in the table.
* Jump to the first/last row in the table.
* Read current column in the table starting from current cell down.
* Read current row in the table starting from current cell.
* Read current column in the table starting from the top.
* Read current row in the table starting from the beginning of the row.

Note: To learn about NVDA's default gestures for these features, please refer to the NVDA user guide.

## Copying tables to clipboard

With the following shortcuts you can copy either the whole table or current row or current column in a formatted way, so that you can paste it as a table to rich text editors, such as Microsoft Word or WordPad.
- NVDA+Alt+T - shows popup menu with options to copy table or part of it.
There are also separate scripts for copying tables, rows, columns and cells, but they don't have keyboard shortcuts  assigned by default, custom keyboard shortcuts cfor them can be assigned in InputGestures dialog of NVDA.

## Enhanced word navigation commands

As of version 1.8 this functionality has been moved to [WordNav add-on](https://github.com/mltony/nvda-word-nav/).

## Automatic language switching
Allows to automatically switch the language of your synthesizer by character set. Refgular expression for every language can be configured in the preferences window for this add-on. Please make sure that your synthesizer supports all the languages you're interested in. Switching between two Latin-based languages or two languages whose character sets are similar is not supported at this time.

## Quicksearch commands

You can have up to three slots for configurable regular expressions that you frequencly search for in editables. By default they are assigned to `PrintScreen`, `ScrollLock` and `Pause` buttons. You can perform forward search, or backward search by pressing `Shift` combined with these buttons.

## Suppress unwanted 'unselected' speech from NVDA

Suppose you have some text selected in text editors. Then you press a key, such as Home, or UpArrow, that is supposed to take you to another part of the document. NVDA would announce 'unselected' and then speak the former selection, which can be inconvenient at times. This feature prevents NVDA from speaking formerly selected text in situations like this.

## Dynamic keystrokes

You can assign certain keystrokes to be dynamic. After issuing such a keystroke, NVDA will be checking currently focused window for any updates and if the line is updated, NVDA will speak it automatically. For example, certain keystrokes in text editors should be marked dynamic, such as Jump to bookmark, jump to another line and debugging keystrokes,such as step into/step over.

The format of dynamic keystrokes table is simple: every line contains a rule in the following format:
```
appName keystroke
```
where `appName` is the name of the application where this keystroke is marked dynamic (or `*` to b marked dynamic in all applications), and`keystroke` is a keystroke in NVDA format, for example, `control+alt+shift+pagedown`.

In order to figure out appName for your application, do this:

1. Switch to your application.
2. Open NVDA Python Console by pressing NVDA+Shift+Z.
3. Type `focus.appModule.appName` and hit enter.
4. Press F6 to go to output pane and find appName value in the last line.

## Showing and hiding windows
You can hide current window, and you can show all currently hidden windows. This might be useful if you use multiple windows in the same app (say Chrome) and you would like to rearrange them.
- NVDA+Shift+-: hide current window.
- NVDA+Shift+=: Show all currently closed windows.

Please note, that if you quit NVDA while a window is hidden, there is currently no way to show it after NVDA is restarted.

## Console enhancements

Previously this add-on included a number of console-related features. As of version 1.8, all console-related features have been moved to [Console Toolkit add-on](https://github.com/mltony/nvda-console-toolkit/). Specifically:

- Real-time console output
- Beep on console updates
- Enforce Control+V in consoles

## Beep when NVDA is busy

Check this option for NVDA to provide audio feedback when NVDA is busy. NVDA being busy does not necessarily indicate a problem with NVDA, but rather this is a signal to the user that any NVDA commands will not be processed immediately.

## Volume adjustment

* NVDA+Control+PageUp/PageDown - adjust NVDA volume.
* NVDA+Alt+PageUp/PageDown - adjust volume of all applications except for NVDA.

## Sound split

In Sound split mode NVDA will direct all sound output to the right channel, while applications will play their sounds in the left channel. Channels can be switched in settings.

* NVDA+Alt+S toggles sound split mode. 

Please note, that in certain situations sound output from an application might be limited to one channel even when NVDA is not running. For example, this could happen if NVDA has crashed while sound split was on, or when NVDA exited cleanly while the app in question was not running. In those situations, please restart NVDA,  and turn off sound split while the app in question is running.

## Enhanced mouse functions

* Alt+NumPadDivide: Point mouse cursor at current object and click it.
* Alt+NumPadMultiply: Point mouse cursor at current object and right mouse button click on it.
* Alt+NumPadPlus/NumPadMinus: Point mouse cursor at current object and scroll down/up. THis is useful for infinite scroll webpages and webpages that load more content on scroll.
* Alt+NumPadDelete: Move mouse cursor out of the way to top left corner of the screen. This can be useful to prevent unwanted hover over windows in certain applications.


## Detecting insert mode in text editors

If this option is enabled, NVDA will beep when it detects insert mode in text editors.

## Blocking double insert keystroke

In NVDA pressing Insert key twice in a row toggles insert mode in applications. However, sometimes it happens accidentally and it triggers insert mode. Since this is a special keystroke, it cannot be disabled in the settings. This add-on provides a way to block this keyboard shortcut. When double insert is blocked, insert mode can stil be toggled by pressing NVDA+F2 and then Insert. 

This option is disabled by default and must be enabled in the settings.

## System priority of NVDA process

This allows to boost system priority of NVDA process, that might improve NVDA responsiveness, especially when CPU load is high.

## Fixing a bug when focus gets stuck in the taskbar when pressing Windows+Numbers

There is a bug in Windows 10, and possibly in other versions. When switching between applications using Windows+number shortcut sometimes the focus gets stuck in the taskbar area instead of jumping to the window being switched to. Since trying to report this bug to Microsoft is hopeless, a workaround has been implemented in this add-on. The add-on detects this situation and plays a short low-pitch beep when this situation is detected, then the add-on fixes it automatically.
