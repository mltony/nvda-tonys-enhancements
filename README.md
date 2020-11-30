# nvda-tonys-enhancements
This add-on contains a number of small improvements to NVDA screenreader, each of them too small to deserve a separate add-on.

This add-on is only compatible with NVDA versions 2019.3 and above.

## Downloads

[Tony's enhancements latest stable version](https://github.com/mltony/nvda-tonys-enhancements/releases/latest/download/tonysEnhancements.nvda-addon)

## Enhanced table navigation commands
* Control+Alt+Home/End - jump to the first/last column in the table.
* Control+Alt+PageUp/PageDown - jump to the first/last row in the table.
* NVDA+Control+digit - jump to 1st/2nd/3rd/... 10th column in the table.
* NVDA+Alt+digit - jump to 1st/2nd/3rd/... 10th row in the table.
* NVDA+Shift+DownArrow - read current column in the table starting from current cell down.

## Enhanced word navigation commands

As of version 1.8 this functionality has been moved to [WordNav add-on](https://github.com/mltony/nvda-word-nav/).

## Automatic language switching
Allows to automatically switch the language of your synthesizer by character set. Refgular expression for every language can be configured in the preferences window for this add-on. Please make sure that your synthesizer supports all the languages you're interested in. Switching between two Latin-based languages or two languages whose character sets are similar is not supported at this time.

## Suppress unwanted 'unselected' speech from NVDA

Suppose you have some text selected in text editors. Then you press a key, such as Home, or UpArrow, that is supposed to take you to another part of the document. NVDA would announce 'unselected' and then speak the former selection, which can be inconvenient at times. This feature prevents NVDA from speaking formerly selected text in situations like this.

## Dynamic keystrokes

You can assign certain keystrokes to be dynamic. After issuing such a keystroke, NVDA will be checking currently focused window for any updates and if the line is updated, NVDA will speak it automatically. For example, certain keystrokes in text editors should be marked dynamic, such as Jump to bookmark, jump to another line and debugging keystrokes,such as step into/step over.

The format of dynamic keystrokes table is simple: every line contains a rule in the following format:
```
appName keystroke
```
where `appName` is the name of the application where this keystroke is marked dynamic (or `*` to b marked dynamic in all applications), and`keystroke` is a keystroke in NVDA format, for example, `control+alt+shift+pagedown`.

## Real-time console output

This option is disabled by default and must be enabled in the settings.

This option makes NVDA to speak new lines immediately as they appear in console output, instead of queueing new speech utterances.

There is also an option to beep on command line updates - this would give you a better idea when new lines are printed in the console.

## Beep when NVDA is busy

Check this option for NVDA to provide audio feedback when NVDA is busy. NVDA being busy does not necessarily indicate a problem with NVDA, but rather this is a signal to the user that any NVDA commands will not be processed immediately.

## NVDA volume

* NVDA+Control+PageUp/PageDown - adjust NVDA volume.

This option controls the volume of NVDA speech as well as all the other sounds and beeps produced by NVDA. The advantage of this option compared to adjusting volume of a speech synthesizer, is that it affects the volume of all the beeps proportionally.

## Detecting insert mode in text editors

If this option is enabled, NVDA will beep when it detects insert mode in text editors.

## Blocking double insert keystroke

In NVDA pressing Insert key twice in a row toggles insert mode in applications. However, sometimes it happens accidentally and it triggers insert mode. Since this is a special keystroke, it cannot be disabled in the settings. This add-on provides a way to block this keyboard shortcut. When double insert is blocked, insert mode can stil be toggled by pressing NVDA+F2 and then Insert. 

This option is disabled by default and must be enabled in the settings.

## Fixing a bug when focus gets stuck in the taskbar when pressing Windows+Numbers

There is a bug in Windows 10, and possibly in other versions. When switching between applications using Windows+number shortcut sometimes the focus gets stuck in the taskbar area instead of jumping to the window being switched to. Since trying to report this bug to Microsoft is hopeless, a workaround has been implemented in this add-on. The add-on detects this situation and plays a short low-pitch beep when this situation is detected, then the add-on fixes it automatically.
