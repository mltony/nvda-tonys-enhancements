# Tonys Verbesserungen #

Diese NVDA-Erweiterung enthält eine Reihe kleinerer Verbesserungen, von
denen jede zu klein ist, um ein eigene NVDA-Erweiterung daraus zu machen.

This add-on is compatible with NVDA versions 2022.4 and 2024.1.

## Downloads

Please install the latest version from NVDA add-on store.

## Erweiterte Tabellen-Navigationsbefehle
* NVDA+Steuerung+Ziffer - springe zu Spalte 1, 2, 3 bis 10 in einer Tabelle.
* NVDA+Alt+Ziffer - springe zu Reihe 1, 2, 3 bis 10 in einer Tabelle.

## Befehle zur Tabellen-Navigation wurden entfernt

Die folgenden Tabellen-Navigationsbefehle wurden entfernt, da sie bereits in
NVDA integriert wurden.

* Sprung zur ersten/letzten Spalte in der Tabelle.
* Sprung zur ersten/letzten Zeile in der Tabelle.
* Aktuelle Spalte in der Tabelle ab der aktuellen Zelle abwärts vorlesen.
* Aktuelle Zeile in der Tabelle ab der aktuellen Zelle vorlesen.
* Aktuelle Spalte in der Tabelle von oben nach unten vorlesen.
* Aktuelle Zeile in der Tabelle, beginnend mit dem Anfang der Zeile,
  vorlesen.

Hinweis: Informationen zu den Standard-Tastenbefehlen in NVDA für diese
Funktionen finden Sie im NVDA-Benutzerhandbuch.

## Kopieren von Tabellen in die Zwischenablage

With the following shortcuts you can copy either the whole table or current
row or current column in a formatted way, so that you can paste it as a
table to rich text editors, such as Microsoft Word or WordPad.  - NVDA+Alt+T
- shows popup menu with options to copy table or part of it.  There are also
separate scripts for copying tables, rows, columns and cells, but they don't
have keyboard shortcuts assigned by default, custom keyboard shortcuts cfor
them can be assigned in InputGestures dialog of NVDA.

## Verbesserte Wort-Navigationsbefehle

Ab Version 1.8 wurde diese Funktionalität in die NVDA-Erweiterung
[WordNav](https://github.com/mltony/nvda-word-nav/) ausgelagert.

## Automatische Sprachumschaltung
Ermöglicht es, die Sprache der Sprachausgabe automatisch nach Zeichensatz
umzuschalten. Reflektierende Ausdrücke für jede Sprache können im
Einstellungsfenster für dieser NVDA-Erweiterung konfiguriert werden. Bitte
vergewissern Sie sich, dass die Sprachausgabe alle Sprachen unterstützt, an
denen Sie interessiert sind. Das Umschalten zwischen zwei lateinisch
basierten Sprachen oder zwei Sprachen mit ähnlichen Zeichensätzen wird
derzeit nicht unterstützt.

## Befehle für die Schnellsuche

Sie können bis zu drei Slots für konfigurierbare reguläre Ausdrücke haben,
nach denen Sie häufig in Eingabefeldern suchen. Standardmäßig sind sie den
Schaltflächen "Bildschirm drucken", "Bildschirm sperren" und "Pause"
zugewiesen. Sie können eine Vorwärts- oder Rückwärtssuche durchführen, indem
Sie die Umschalttaste in Kombination mit diesen Tasten betätigen.

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
You can hide current window, and you can show all currently hidden
windows. This might be useful if you use multiple windows in the same app
(say Chrome) and you would like to rearrange them.  - NVDA+Shift+-: hide
current window.  - NVDA+Shift+=: Show all currently closed windows.

Bitte beachten Sie, dass es derzeit keine Möglichkeit gibt, ein
ausgeblendetes Fenster nach einem Neustart von NVDA wieder einzublenden,
sobald Sie NVDA beendet haben.

## Erweiterungen der Konsole

Zuvor enthielt diese NVDA-Erweiterung eine Reihe von konsolenbezogenen
Funktionen. Ab Version 1.8 wurden alle konsolenbezogenen Funktionen in die
NVDA-Erweiterung [Werkzeug für die
Konsole](https://github.com/mltony/nvda-console-toolkit/) ausgelagert. Im
Einzelnen:

- Konsolen-Ausgabe in Echtzeit
- Signalton bei Konsolen-Aktualisierungen
- Erzwingt Strg+V in Konsolen

## Signalisiere, wenn NVDA ausgelastet ist

Aktivieren Sie diese Option, wenn NVDA signalisieren soll, dass es
beschäftigt ist. In diesem Fall gibt es nicht unbedingt ein Problem mit
NVDA, zeigt dem Nutzer jedoch an, dass der nächste NVDA-Befehl nicht sofort
ausgeführt wird.

## Einstellung der Lautstärke

Due to compatibility issues with the WASAPI added in NVDA-2023.2, the volume
adjustment have been temporarily removed, but may be restored in the future.

## Sound-Aufteilung

As of version 1.16 this functionality has been moved to [soundSplitter
add-on](https://github.com/opensourcesys/soundSplitter/) maintained by Luke.

## Verbesserte Maus-Funktionen

* Alt+Nummernblock-Schrägstrich: Zeigt mit dem Mauszeiger auf das aktuelle
  Objekt und führt darauf einen normalen Klick aus.
* Alt+Nummernblock-Stern: Zeigt mit dem Mauszeiger auf das aktuelle Objekt
  und führt mit der Maustaste darauf einen Rechtsklick aus.
* Alt+Nummernblock-Plus/Nummernblock-Minus: Den Mauszeiger auf das aktuelle
  Objekt ziehen und nach unten/oben blättern. Dies ist nützlich für endlos
  scrollende Webseiten und Webseiten, die beim Scrollen mehr Inhalt laden.
* Alt+Nummernblock-Entf: Zieht den Mauszeiger aus dem Weg in die linke obere
  Ecke des Bildschirms. Dies kann nützlich sein, um unerwünschte
  überlappende Fenster in bestimmten Anwendungen zu vermeiden.


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

## System-Priorität des NVDA-Prozesses

Dies ermöglicht es, die System-Priorität des NVDA-Prozesses zu erhöhen, was
die Reaktionsfähigkeit von NVDA verbessern kann, insbesondere bei hoher
CPU-Last.

## Behebung eines Fehlers, bei dem der Fokus in der Taskleiste hängen bleibt, wenn man Windows+Zahl drückt

Es gibt einen Fehler in Windows 10 und möglicherweise auch in anderen
Versionen. Beim Umschalten zwischen Anwendungen mit der Tastenkombination
Windows+Zahl bleibt der Fokus manchmal im Bereich der Taskleiste hängen,
anstatt zu dem Fenster zu springen, zu dem gewechselt wird. Da es
aussichtslos ist, diesen Fehler an Microsoft zu melden, wurde in dieser
NVDA-Erweiterung ein Workaround implementiert. Das Add-on erkennt diese
Situation und gibt einen kurzen, tiefen Piepton ab, wenn diese Situation
erkannt wird, und behebt sie dann automatisch.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=tonysEnhancements
