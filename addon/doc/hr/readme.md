# Tonijeva poboljšanja (Tony's Enhancements) #

Ovaj dodatak sadrži mnoga mala poboljšanja NVDA čitača ekrana, a svako od
tih poboljšanja je premaleno, da bi zaslužilo zaseban dodatak.

This add-on is compatible with NVDA versions 2022.4 and 2024.1.

## Downloads

Please install the latest version from NVDA add-on store.

## Poboljšani prečaci za kretanje po tablicama
* NVDA+kontrol+brojka – skoči na 1., 2., 3., … 10. stupac u tablici.
* NVDA+Alt+brojka – skoči na 1., 2., 3., … 10. redak u tablici.

## Uklonjene naredbe za kretanje po tablicama

Sljedeće naredbe za kretanje po tablicama su uklonjene jer su integrirane u
najnoviju verziju NVDA jezgre.

* Skoči na prvi/zadnji stupac u tablici.
* Skoči na prvi/zadnji redak u tablici.
* Čitaj trenutačni stupac u tablici prema dolje, počevši od trenutačne
  ćelije.
* Čitaj trenutačni stupac u tablici prema dolje, počevši od trenutačne
  ćelije.
* Čitaj trenutačni stupac u tablici prema dolje, počevši od trenutačne
  ćelije.
* Čitaj trenutačni stupac u tablici prema dolje, počevši od trenutačne
  ćelije.

Note: To learn about NVDA's default gestures for these features, please
refer to the NVDA user guide.

## Copying tables to clipboard

With the following shortcuts you can copy either the whole table or current
row or current column in a formatted way, so that you can paste it as a
table to rich text editors, such as Microsoft Word or WordPad.  - NVDA+Alt+T
- shows popup menu with options to copy table or part of it.  There are also
separate scripts for copying tables, rows, columns and cells, but they don't
have keyboard shortcuts assigned by default, custom keyboard shortcuts cfor
them can be assigned in InputGestures dialog of NVDA.

## Poboljšane naredbe za kretanje po riječima

As of version 1.8 this functionality has been moved to [WordNav
add-on](https://github.com/mltony/nvda-word-nav/).

## Automatic language switching
Allows to automatically switch the language of your synthesizer by character
set. Refgular expression for every language can be configured in the
preferences window for this add-on. Please make sure that your synthesizer
supports all the languages you're interested in. Switching between two
Latin-based languages or two languages whose character sets are similar is
not supported at this time.

## Quicksearch commands

You can have up to three slots for configurable regular expressions that you
frequencly search for in editables. By default they are assigned to
`PrintScreen`, `ScrollLock` and `Pause` buttons. You can perform forward
search, or backward search by pressing `Shift` combined with these buttons.

## Suppress unwanted 'unselected' speech from NVDA

Suppose you have some text selected in text editors. Then you press a key,
such as Home, or UpArrow, that is supposed to take you to another part of
the document. NVDA would announce 'unselected' and then speak the former
selection, which can be inconvenient at times. This feature prevents NVDA
from speaking formerly selected text in situations like this.

## Dinamični tipkovnički prečaci

Moguće je dodijeliti dinamične tipkovničke prečace. Nakon izdavanja takvog
prečaca, NVDA će provjeriti aktualiziranja trenutačno fokusiranog prozora i
ako je redak aktualiziran, NVDA će to automatski izgovoriti. Na primjer,
određeni prečaci u uređivačima teksta trebaju biti označeni kao dinamični,
kao što je skok na zabilješku, skok na jedan drugi redak te prečaci za
uklanjanja grešaka, kao što je ukoračiti/prijeći preko.

Format tablice dinamičkih prečaca je jednostavan: svaki redak sadrži pravilo
u sljedećem formatu:
```
appName keystroke
```
gdje je `appName` ime aplikacije u kojoj je ovaj prečac označen dinamičnim
(ili `*` za označavanje dinamičnosti u svim aplikacijama), a `keystroke` je
tipkovnički prečac u NVDA formatu, na primjer, `kontrol+alt+šift+stranica
dolje`.

In order to figure out appName for your application, do this:

1. Switch to your application.
2. Open NVDA Python Console by pressing NVDA+Shift+Z.
3. Type `focus.appModule.appName` and hit enter.
4. Press F6 to go to output pane and find appName value in the last line.

## Showing and hiding windows
You can hide current window, and you can show all currently hidden
windows. This might be useful if you use multiple windows in the same app
(say Chrome) and you would like to rearrange them.  - NVDA+Shift+-: hide
current window.  - NVDA+Shift+=: Show all currently closed windows.

Please note, that if you quit NVDA while a window is hidden, there is
currently no way to show it after NVDA is restarted.

## Console enhancements

Previously this add-on included a number of console-related features. As of
version 1.8, all console-related features have been moved to [Console
Toolkit
add-on](https://github.com/mltony/nvda-console-toolkit/). Specifically:

- Real-time console output - Beep on console updates - Enforce Control+V in
consoles

## Signaliziraj zvukom kad je NVDA zauzet

Označi ovu NVDA opciju za pružanje povratnih informacija zvukom kad je NVDA
zauzet. Zauzetost NVDA čitača ne mora nužno značiti problem s NVDA-om, već
je to signal korisniku, da se bilo koje NVDA naredbe neće odmah izvršiti.

## Volume adjustment

Due to compatibility issues with the WASAPI added in NVDA-2023.2, the volume
adjustment have been temporarily removed, but may be restored in the future.

## Sound split

As of version 1.16 this functionality has been moved to [soundSplitter
add-on](https://github.com/opensourcesys/soundSplitter/) maintained by Luke.

## Enhanced mouse functions

* Alt+NumPadDivide: Point mouse cursor at current object and click it.
* Alt+NumPadMultiply: Point mouse cursor at current object and right mouse
  button click on it.
* Alt+NumPadPlus/NumPadMinus: Point mouse cursor at current object and
  scroll down/up. THis is useful for infinite scroll webpages and webpages
  that load more content on scroll.
* Alt+NumPadDelete: Move mouse cursor out of the way to top left corner of
  the screen. This can be useful to prevent unwanted hover over windows in
  certain applications.


## Detecting insert mode in text editors

If this option is enabled, NVDA will beep when it detects insert mode in
text editors.

## Blokiranje dvostrukog unosa tipkovničkog prečaca

U NVDA čitaču, uzastopnim dvostrukim pritiskom na tipku „Insert”, mijenja
način umetanja u aplikacije. No, ponekad se to dogodi slučajno i pokreće
modus za umetanje. Budući da je ovo zaseban tipkovnički prečac, on se ne
može deaktivirati u postavkama. Ovaj dodatak omogućuje način blokiranja ovog
tipkovničkog prečaca. Kad je dvostruko umetanje blokirano, modus umetanja
može se mijenjati pritiskom na NVDA+F2, a zatim „Insert”.

Ova je opcija standardno deaktivirana i mora se aktivirati u postavkama.

## System priority of NVDA process

This allows to boost system priority of NVDA process, that might improve
NVDA responsiveness, especially when CPU load is high.

## Fixing a bug when focus gets stuck in the taskbar when pressing Windows+Numbers

There is a bug in Windows 10, and possibly in other versions. When switching
between applications using Windows+number shortcut sometimes the focus gets
stuck in the taskbar area instead of jumping to the window being switched
to. Since trying to report this bug to Microsoft is hopeless, a workaround
has been implemented in this add-on. The add-on detects this situation and
plays a short low-pitch beep when this situation is detected, then the
add-on fixes it automatically.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=tonysEnhancements
