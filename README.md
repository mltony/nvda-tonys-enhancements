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

## Real-time console output

This option is disabled by default and must be enabled in the settings.

This option makes NVDA to speak new lines immediately as they appear in console output, instead of queueing new speech utterances.

There is also an option to beep on command line updates - this would give you a better idea when new lines are printed in the console.

## Master volume

* NVDA+Control+PageUp/PageDown - adjust NVDA master volume.

This option controls the volume of NVDA speech as well as all the other sounds and beeps produced by NVDA. The advantage of this option compared to adjusting volume of a speech synthesizer, is that it affects the volume of all the beeps proportionally.

## Blocking double insert keystroke

In NVDA pressing Insert key twice in a row toggles insert mode in applications. However, sometimes it happens accidentally and it triggers insert mode. Since this is a special keystroke, it cannot be disabled in the settings. This add-on provides a way to block this keyboard shortcut. When double insert is blocked, insert mode can stil be toggled by pressing NVDA+F2 and then Insert. 

This option is disabled by default and must be enabled in the settings.
