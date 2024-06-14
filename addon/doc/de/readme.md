# Tonys Verbesserungen #

Diese NVDA-Erweiterung enthält eine Reihe kleinerer Verbesserungen, von
denen jede zu klein ist, um ein eigene NVDA-Erweiterung daraus zu machen.

This add-on is compatible with NVDA version 2024.2 or later

## Downloads

Please install the latest version from NVDA add-on store.

## Erweiterte Tabellen-Navigationsbefehle
* NVDA+Steuerung+Ziffer - springe zu Spalte 1, 2, 3 bis 10 in einer Tabelle.
* NVDA+Alt+Ziffer - springe zu Reihe 1, 2, 3 bis 10 in einer Tabelle.

## Kopieren von Tabellen in die Zwischenablage

With the following shortcuts you can copy either the whole table or current
row or current column in a formatted way, so that you can paste it as a
table to rich text editors, such as Microsoft Word or WordPad.

* NVDA+Alt+T - shows popup menu with options to copy table or part of it.

There are also separate scripts for copying tables, rows, columns and cells,
but they don't have keyboard shortcuts assigned by default, custom keyboard
shortcuts cfor them can be assigned in InputGestures dialog of NVDA.

## Automatische Sprachumschaltung
Ermöglicht es, die Sprache der Sprachausgabe automatisch nach Zeichensatz
umzuschalten. Reflektierende Ausdrücke für jede Sprache können im
Einstellungsfenster für dieser NVDA-Erweiterung konfiguriert werden. Bitte
vergewissern Sie sich, dass die Sprachausgabe alle Sprachen unterstützt, an
denen Sie interessiert sind. Das Umschalten zwischen zwei lateinisch
basierten Sprachen oder zwei Sprachen mit ähnlichen Zeichensätzen wird
derzeit nicht unterstützt.

## Befehle für die Schnellsuche

As of version v1.18, QuickSearch commands have been moved to [IndentNav
add-on](https://github.com/mltony/nvda-indent-nav).

## Unerwünschte "nicht ausgewählt"-Meldungen in NVDA unterdrücken

Angenommen, Sie haben einen Text in einem Text-Editor ausgewählt. Dann
drücken Sie eine Taste, z. B. Pos1 oder Pfeiltaste nach oben, die Sie zu
einem anderen Textbereich führen soll. NVDA würde "nicht ausgewählt"
mitteilen und dann die frühere Auswahl mitteilen, was manchmal unpraktisch
sein kann. Diese Funktion verhindert, dass NVDA in solchen Situationen den
zuvor ausgewählten Text vorliest.

## Dynamische Tastenkombinationen

Sie können bestimmte Tastenkombinationen dynamisch machen. Dies bedeutet,
dass NVDA nach solch einer Tastenkombination das Fenster der aktuellen
Anwendung auf Aktualisierungen prüft und die aktuelle Zeile vorliest, sofern
sich diese Geändert hat. Dies kann z. B. die Tastenkombination springe zu
Lesezeichen, springe zu einer bestimmten Zeile  in einem Editor sein.

Das Format der dynamischen Tastenkürzel ist einfach. Jede Zeile enthält eine
Regel in folgendem Format:
```
appName Tastendruck
```
Hier ist mit  "Anwendungsname" der Name der Anwendung gemeint, in welcher
die Tastenkombination dynamisch gemacht werden soll. Mit * wird die
Tastenkombination in allen Anwendungen dynamisch gemacht. Die
"Tastenkombination" muss im NVDA-Format geschrieben werden. Beispiel:
"control+alt+shift+pagedown" für Alt+Steuerung++UmschaltPfeil runter..

Um den appName für die Anwendung herauszufinden, gehen Sie folgendermaßen
vor:

1. Wechseln Sie zur Anwendung.
2. Öffnen Sie die NVDA Python-Konsole, indem Sie NVDA+Umschalt+Z drücken.
3. Geben Sie `focus.appModule.appName` ein und drücken Sie die Eingabetaste.
4. Drücken Sie F6, um zum Ausgabebereich zu gelangen, und suchen Sie den
   Wert appName in der letzten Zeile.

## Fenster ein- und ausblenden

As of version v1.18 show/hide commands have been moved to [Task Switcher
add-on](https://github.com/mltony/nvda-task-switcher).

## Signalisiere, wenn NVDA ausgelastet ist

Aktivieren Sie diese Option, wenn NVDA signalisieren soll, dass es
beschäftigt ist. In diesem Fall gibt es nicht unbedingt ein Problem mit
NVDA, zeigt dem Nutzer jedoch an, dass der nächste NVDA-Befehl nicht sofort
ausgeführt wird.

## Application Volume adjustment

This functionality has been merged into NVDA core and is available in NVDA
v2024.3 or later.

## Mute microphone

This add-on provides a command for switching the microphone. There is no
gesture assigned to this command by default, you can assign a gesture in
NVDA's "Input Gestures" dialog if needed.

## Sound-Aufteilung

This functionality has been merged into NVDA core and is available in NVDA
v2024.2 or later.

## Verbesserte Maus-Funktionen

* Alt+Nummernblock-Schrägstrich: Zeigt mit dem Mauszeiger auf das aktuelle
  Objekt und führt darauf einen normalen Klick aus.
* Alt+Nummernblock-Stern: Zeigt mit dem Mauszeiger auf das aktuelle Objekt
  und führt mit der Maustaste darauf einen Rechtsklick aus.
* Alt+Nummernblock-Entf: Zieht den Mauszeiger aus dem Weg in die linke obere
  Ecke des Bildschirms. Dies kann nützlich sein, um unerwünschte
  überlappende Fenster in bestimmten Anwendungen zu vermeiden.

The functionality for mouse wheel scrolling has been merged into NVDA core
and is available in NVDA v2024.3 or later.

## Erkennung des Einfügemodus in Text-Editoren

Wenn diese Option aktiviert ist, gibt NVDA einen Signalton wieder, sobald
der Einfügemodus in Text-Editoren erkannt wurde.

## Zweimaligen Druck der Taste einfügen blockieren

Während der Nutzung von NVDA bewirkt das zweimalige Drücken der
Einfügen-Taste hintereinander den Wechsel zwischen Einfügen und
Überschreiben, sofern die aktuelle Anwendung dies unterstützt. Manchmal
geschieht dies jedoch versehentlich und löst den Überschreibmodus aus. Da es
sich um einen speziellen Tastenanschlag handelt, kann er in den
Einstellungen nicht deaktiviert werden. Diese Erweiterung bietet eine
Möglichkeit, diese Tastenkombination zu blockieren. Wenn der Doppeldruck
blockiert ist, kann der Einfügemodus durch Drücken von NVDA+F2 und betätigen
der Einfügen-Taste umgeschaltet werden.

Diese Option ist standardmäßig ausgeshaltet und muss manuell in den
Einstellungen aktiviert werden.

## Blocking double Caps Lock keystroke

In NVDA, when Caps Lock is set as an NVDA key, pressing it twice in a row
toggles between uppercase and lowercase input modes. However, this can
sometimes cause unintentional switching between these modes. Since this
key’s behavior is unique and cannot be disabled through settings, this
add-on offers a method to block this specific keyboard shortcut. When the
double Caps Lock key press is blocked, you can still switch between
uppercase and lowercase input modes by pressing NVDA+F2 followed by the Caps
Lock key.

Diese Option ist standardmäßig ausgeshaltet und muss manuell in den
Einstellungen aktiviert werden.

## System-Priorität des NVDA-Prozesses

Dies ermöglicht es, die System-Priorität des NVDA-Prozesses zu erhöhen, was
die Reaktionsfähigkeit von NVDA verbessern kann, insbesondere bei hoher
CPU-Last.

## Behebung eines Fehlers, bei dem der Fokus in der Taskleiste hängen bleibt, wenn man Windows+Zahl drückt

This feature has been removed as of version v1.18. If you need a more
reliable task switching functionality, please consider using [Task Switcher
add-on](https://github.com/mltony/nvda-task-switcher).

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=tonysEnhancements
