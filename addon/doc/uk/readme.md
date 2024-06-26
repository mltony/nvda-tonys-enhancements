# Tony's enhancements #

Цей додаток містить низку невеликих поліпшень екранного читача NVDA, кожне з
яких є занадто малим, щоб заслуговувати на окремий додаток.

This add-on is compatible with NVDA version 2024.2 or later

## Downloads

Please install the latest version from NVDA add-on store.

## Поліпшені команди навігації у таблиці
* NVDA+Control+цифра – перейти до першого/другого/третього/десятого
  стовпчика таблиці.
* NVDA+Alt+цифра – перейти до першого/другого/третього/десятого рядка
  таблиці.

## Копіювання таблиць у буфер обміну

За допомогою наведених нижче комбінацій клавіш ви можете скопіювати або всю
таблицю, або поточний рядок, або поточний стовпець у відформатованому
вигляді, щоб потім вставити його як таблицю в текстові редактори, такі як
Microsoft Word або WordPad.

* NVDA+Alt+T — показує спливаюче меню з параметрами копіювання таблиці або
  її частини.

There are also separate scripts for copying tables, rows, columns and cells,
but they don't have keyboard shortcuts assigned by default, custom keyboard
shortcuts cfor them can be assigned in InputGestures dialog of NVDA.

## Автоматичне перемикання мов
Дозволяє автоматично перемикати мову вашого синтезатора за набором
символів. Регулярний вираз для кожної мови можна налаштувати у діалозі
налаштувань додатка. Будь ласка, переконайтеся, що ваш синтезатор підтримує
всі мови, які вас цікавлять. Перемикання між двома мовами на основі латиниці
або двома мовами зі схожими наборами символів наразі не підтримується.

## Команди швидкого пошуку

As of version v1.18, QuickSearch commands have been moved to [IndentNav
add-on](https://github.com/mltony/nvda-indent-nav).

## Приглушення промовляння NVDA небажаної фрази «не виділено»

Уявімо, що ви виділили якийсь текст у текстовому редакторі. Потім ви
натискаєте клавішу, наприклад, «на початок» або «стрілка вгору», яка має
перенести вас до іншої частини документа. NVDA промовить «не виділено», а
потім промовить попереднє виділення, що іноді може бути незручно. Ця функція
запобігає тому, щоб NVDA озвучувала раніше виділений текст у подібних
ситуаціях.

## Динамічні комбінації клавіш

Ви можете призначити деякі команди як динамічні. Після виконання такої
команди NVDA відстежуватиме активне вікно на будь-які оновлення і, якщо
рядок був оновлений, NVDA автоматично його промовить. Наприклад, як
динамічні можуть бути позначені деякі команди в текстовому редакторі, як-от
перехід на закладку, перехід на інший рядок та команди налагодження, такі як
step into/step over.

Формат таблиці динамічних команд – простий: кожен рядок містить правило в
такому форматі:
```
appName keystroke
```
де `appName` – ім’я програми, в якій команда позначена як динамічна, або `*`
для позначення команди як динамічної в усіх програмах, а keystroke – команда
у форматі NVDA, наприклад: `control+alt+shift+сторінка вниз`.

Щоб визначити appName для вашої програми, виконайте такі дії:

1. Перейдіть до своєї програми.
2. 2. Відкрийте Консоль Python nvda, натиснувши комбінацію клавіш
   NVDA+Shift+Z.
3. Введіть focus.appModule.appName і натисніть enter.
4. Натисніть F6, щоб перейти до панелі виведення та знайти значення appName
   в останньому рядку.

## Показ і приховування вікон

As of version v1.18 show/hide commands have been moved to [Task Switcher
add-on](https://github.com/mltony/nvda-task-switcher).

## Сигнал, коли NVDA зайнята

Позначте цей параметр, щоб отримувати звуковий зворотний зв’язок, коли NVDA
зайнята. Зайнятість NVDA не обов’язково означає проблему з нею. Це радше
сигнал для користувача, що певні команди NVDA будуть виконані не відразу.

## Application Volume adjustment

This functionality has been merged into NVDA core and is available in NVDA
v2024.3 or later.

## Mute microphone

This add-on provides a command for switching the microphone. There is no
gesture assigned to this command by default, you can assign a gesture in
NVDA's "Input Gestures" dialog if needed.

## Розділення звуку

This functionality has been merged into NVDA core and is available in NVDA
v2024.2 or later.

## Покращені функції миші

* Alt+додатковий знак ділення: наводить курсор миші на поточний об’єкт і
  натискає його.
* Alt+додатковий знак множення: наводить курсор миші на поточний об’єкт і
  натискає на ньому правою кнопкою миші.
* Alt+додатковий деліт: переміщає курсор миші у верхній лівий кут екрана. Це
  може бути корисним для запобігання небажаному наведенню курсора на вікна в
  певних програмах.

The functionality for mouse wheel scrolling has been merged into NVDA core
and is available in NVDA v2024.3 or later.

## Виявлення режиму вставки у текстових редакторах

Якщо цей параметр увімкнено, NVDA подаватиме звуковий сигнал, коли виявить
режим вставки в текстових редакторах.

## Блокувати подвійний Insert

При використанні NVDA подвійне натискання клавіші insert вмикає в деяких
програмах режим вставки. Причому іноді це відбувається раптово. Оскільки це
спеціальна команда, то її не можна вимкнути у налаштуваннях. Однак цей
додаток надає можливість заблокувати цю комбінацію клавіш. Коли подвійний
insert заблоковано, режим вставки і надалі можна вмикати натисканням NVDA+F2
і потім insert.

Цей параметр початково вимкнено, його можна увімкнути в налаштуваннях.

## Blocking double Caps Lock keystroke

In NVDA, when Caps Lock is set as an NVDA key, pressing it twice in a row
toggles between uppercase and lowercase input modes. However, this can
sometimes cause unintentional switching between these modes. Since this
key’s behavior is unique and cannot be disabled through settings, this
add-on offers a method to block this specific keyboard shortcut. When the
double Caps Lock key press is blocked, you can still switch between
uppercase and lowercase input modes by pressing NVDA+F2 followed by the Caps
Lock key.

Цей параметр початково вимкнено, його можна увімкнути в налаштуваннях.

## Системний пріоритет процесу NVDA

Це дозволяє підвищити системний пріоритет процесу NVDA, що може покращити
швидкість відгуку NVDA, особливо при високому навантаженні на процесор.

## Виправлено помилку, коли фокус застрягав на панелі завдань при натисканні комбінації клавіш Windows+Цифри

This feature has been removed as of version v1.18. If you need a more
reliable task switching functionality, please consider using [Task Switcher
add-on](https://github.com/mltony/nvda-task-switcher).

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=tonysEnhancements
