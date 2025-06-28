# nvda-tonys-enhancements
This add-on contains a number of small improvements to NVDA screenreader, each of them too small to deserve a separate add-on.

This add-on is compatible with NVDA version 2024.2 or later

## Downloads

Please install the latest version from NVDA add-on store.

## Enhanced table navigation commands
* NVDA+Control+digit - jump to 1st/2nd/3rd/... 10th column in the table.
* NVDA+Alt+digit - jump to 1st/2nd/3rd/... 10th row in the table.

## Copying tables to clipboard

With the following shortcuts you can copy either the whole table or current row or current column in a formatted way, so that you can paste it as a table to rich text editors, such as Microsoft Word or WordPad.
- NVDA+Alt+T - shows popup menu with options to copy table or part of it.
There are also separate scripts for copying tables, rows, columns and cells, but they don't have keyboard shortcuts  assigned by default, custom keyboard shortcuts cfor them can be assigned in InputGestures dialog of NVDA.

## Clipboard history

As of NVDA v2024.4 built-in Windows clipboard history feature works poorly with NVDA. As a drop-in replacement, this add-on provides a fully accessible clipboard history feature. It is bound to `Windows+V` by default, so it replaces the built-in feature.

## Automatic language switching
Allows to automatically switch the language of your synthesizer by character set. Refgular expression for every language can be configured in the preferences window for this add-on. Please make sure that your synthesizer supports all the languages you're interested in. Switching between two Latin-based languages or two languages whose character sets are similar is not supported at this time.

## Quicksearch commands

As of version v1.18, QuickSearch commands have been moved to [IndentNav add-on](https://github.com/mltony/nvda-indent-nav).

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

As of version v1.18 show/hide commands have been moved to [Task Switcher add-on](https://github.com/mltony/nvda-task-switcher).

## Beep when NVDA is busy

Check this option for NVDA to provide audio feedback when NVDA is busy. NVDA being busy does not necessarily indicate a problem with NVDA, but rather this is a signal to the user that any NVDA commands will not be processed immediately.

## Application Volume adjustment

This feature allows you to adjust the volume of NVDA and other applications independently. The following commands are available:

* NVDA+Ctrl+PageUp: Increases the volume of NVDA.
* NVDA+Ctrl+PageDown: Decreases the volume of NVDA.
* NVDA+Alt+PageUp: Increases the volume of other applications.
* NVDA+Alt+PageDown: Decreases the volume of other applications.
* Mute or unmute other applications: This command does not have a default gesture assigned. You can assign a custom one in NVDA's "Input Gestures" dialog.

## Mute microphone

This add-on provides a command for switching the microphone. There is no gesture assigned to this command by default, you can assign a gesture in NVDA's "Input Gestures" dialog if needed.

## Sound split

This functionality has been merged into NVDA core and is available in NVDA v2024.2 or later.

## Enhanced mouse functions

* Alt+NumPadDivide: Point mouse cursor at current object and click it.
* Alt+NumPadMultiply: Point mouse cursor at current object and right mouse button click on it.
* Alt+NumPadDelete: Move mouse cursor out of the way to top left corner of the screen. This can be useful to prevent unwanted hover over windows in certain applications.

The functionality for mouse wheel scrolling has been merged into NVDA core and is available in NVDA v2024.3 or later.

## Detecting insert mode in text editors

If this option is enabled, NVDA will beep when it detects insert mode in text editors.

## Blocking double insert keystroke

In NVDA pressing Insert key twice in a row toggles insert mode in applications. However, sometimes it happens accidentally and it triggers insert mode. Since this is a special keystroke, it cannot be disabled in the settings. This add-on provides a way to block this keyboard shortcut. When double insert is blocked, insert mode can stil be toggled by pressing NVDA+F2 and then Insert. 

This option is disabled by default and must be enabled in the settings.

## Blocking double Caps Lock keystroke

In NVDA, when Caps Lock is set as an NVDA key, pressing it twice in a row toggles between uppercase and lowercase input modes. However, this can sometimes cause unintentional switching between these modes. Since this key’s behavior is unique and cannot be disabled through settings, this add-on offers a method to block this specific keyboard shortcut. When the double Caps Lock key press is blocked, you can still switch between uppercase and lowercase input modes by pressing NVDA+F2 followed by the Caps Lock key. 

This option is disabled by default and must be enabled in the settings.

## System priority of NVDA process

This allows to boost system priority of NVDA process, that might improve NVDA responsiveness, especially when CPU load is high.

## Fixing a bug when focus gets stuck in the taskbar when pressing Windows+Numbers

This feature has been removed as of version v1.18. If you need a more reliable task switching functionality, please consider using [Task Switcher add-on](https://github.com/mltony/nvda-task-switcher).
