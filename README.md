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
Most text editors support Control+LeftArrow/RightArrow commands for word navigation. However the definition of the word changes from one program to another. This is especially true of modern web-based text editors, such as Monaco. NVDA should know the definition of word in given program in order to speak words correctly. If NVDA doesn't know the exact definition, then either words are going to be skipped, or pronounced multiple times. Moreover, some web-based text editors position the cursor in the end of the word, instead of the beginning, making editing much harder for visually impaired users. In order to combat this problem I have created enhanced word navigation commands, that take the word definition from Notepad++ and they do not rely on program's definition of words, but rather parse lines into words on NVDA's side. The Control+LeftArrow/RightArrow gesture is not even sent to the program, thus ensuring the consistency of the speech.
* Control+Windows+LeftArrow/RightArrow - jump to previous/next word on the line

Currently the drawback of this approach is that sometimes it is not able to advance to next/previous line in some text editors, such as VSCode, since due to its internal optimizations, VSCode presents only a few lines of file contents at a time.

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
