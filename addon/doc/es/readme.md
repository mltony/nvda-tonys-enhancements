# Tony's enhancements (Mejoras de Tony) #

Este complemento aporta una serie de pequeñas mejoras para el lector de
pantalla NVDA, insignificantes por sí solas para merecer complementos
independientes.

This add-on is compatible with NVDA versions 2022.4 and 2024.1.

## Downloads

Please install the latest version from NVDA add-on store.

## Órdenes mejoradas de navegación por tablas
* NVDA+control+dígitos del 1 al 0 - Saltar a la primera, segunda,
  tercera... décima columna de la tabla.
* NVDA+alt+dígitos del 1 al 0 - Saltar a la primera, segunda,
  tercera... décima fila de la tabla.

## Órdenes de navegación por tablas eliminadas

Se han eliminado las siguientes órdenes de navegación por tablas porque se
han integrado en la versión más reciente del núcleo de NVDA.

* Saltar a la primera o última columna de la tabla.
* Saltar a la primera o la última fila de la tabla.
* Leer la columna actual de la tabla empezando desde la celda actual hacia
  abajo.
* Leer la fila actual de la tabla empezando desde la celda actual.
* Leer la columna actual de la tabla empezando por la parte superior.
* Leer la fila actual de la tabla empezando por el principio de la fila.

Nota: para aprender los gestos por defecto de NVDA para estas funciones,
consulta la guía de usuario de NVDA.

## Copiar tablas al portapapeles

With the following shortcuts you can copy either the whole table or current
row or current column in a formatted way, so that you can paste it as a
table to rich text editors, such as Microsoft Word or WordPad.  - NVDA+Alt+T
- shows popup menu with options to copy table or part of it.  There are also
separate scripts for copying tables, rows, columns and cells, but they don't
have keyboard shortcuts assigned by default, custom keyboard shortcuts cfor
them can be assigned in InputGestures dialog of NVDA.

## Órdenes mejoradas de navegación por palabras

A partir de la versión 1.8, esta función se ha movido al [complemento
WordNav](https://github.com/mltony/nvda-word-nav/).

## Cambio automático de idioma
Permite cambiar automáticamente el idioma del sintetizador según el conjunto
de caracteres. En la ventana de preferencias de este complemento se pueden
configurar expresiones regulares para cada idioma. Asegúrate de que el
sintetizador soporta todos los idiomas que te interesan. No se soporta de
momento cambiar entre dos idiomas con caracteres latinos o conjuntos de
caracteres similares.

## Órdenes de búsqueda rápida

Se pueden tener hasta tres huecos con expresiones regulares configurables
buscadas frecuentemente en campos editables. Por defecto están asignadas a
las teclas `Imprimir pantalla`, `Bloquear desplazamiento` y `Pausa`. Se
pueden realizar búsquedas hacia adelante o hacia atrás pulsando `shift`
junto a estos botones.

## Eliminar el mensaje 'deseleccionado' no deseado de NVDA

Supón que tienes algo de texto seleccionado en editores de texto. Pulsas una
tecla, como inicio o flecha arriba, que se supone que te lleva a otra parte
del documento. NVDA anunciaría 'deseleccionado' y después verbalizaría el
texto que estaba seleccionado, y esto puede ser molesto a veces. Esta
función evita que NVDA verbalice el texto que estaba seleccionado en
situaciones como esta.

## Atajos de teclado dinámicos

Se pueden asignar ciertos atajos de teclado para que sean dinámicos. Después
de pulsar un atajo, NVDA revisará la ventana con el foco en búsqueda de
actualizaciones y si la línea se actualiza, NVDA la verbalizará
automáticamente. Por ejemplo, ciertos atajos en editores de texto deberían
marcarse como dinámicos, tales como saltar a marcador, saltar a otra línea y
atajos de teclado de depuración, tales como avanzar a la siguiente
instrucción o saltarla.

El formato de la tabla de atajos de teclado dinámicos es simple. Cada línea
contiene una regla que sigue el siguiente formato:
```
nombreAplicación atajo
```
donde `nombreAplicación` es el nombre de la aplicación donde se marca el
atajo como dinámico (o `*` para marcarlo como dinámico en todas las
aplicaciones), y `atajo` es un atajo en el formato de NVDA, por ejemplo
`control+alt+shift+pagedown`.

Para averiguar el nombre de tu aplicación, haz lo siguiente:

1. Cambia a tu aplicación.
2. Abre la consola Python de NVDA pulsando NVDA+control+z.
3. Teclea `focus.appModule.appName` y pulsa intro.
4. Pulsa f6 para ir al panel de salida y encuentra el nombre de la
   aplicación en la última línea.

## Mostrar y ocultar ventanas
You can hide current window, and you can show all currently hidden
windows. This might be useful if you use multiple windows in the same app
(say Chrome) and you would like to rearrange them.  - NVDA+Shift+-: hide
current window.  - NVDA+Shift+=: Show all currently closed windows.

Ten en cuenta que si cierras NVDA mientras una ventana está oculta, no hay
forma de volver a mostrarla tras reiniciarlo.

## Mejoras de consola

Antes, este complemento incluía ciertas funciones relacionadas con la
consola. A partir de la versión 1.8, todas las funciones relacionadas con la
consola se han movido al [complemento Console
Toolkit](https://github.com/mltony/nvda-console-toolkit/). Concretamente:

- Real-time console output - Beep on console updates - Enforce Control+V in
consoles

## Pitar cuando NVDA esté ocupado

Marca esta opción para que NVDA proporcione retroalimentación de audio
cuando esté ocupado. El hecho de que NVDA esté ocupado no significa que haya
un problema necesariamente, pero sirve como señal al usuario de que las
órdenes que se envíen a NVDA no se procesarán inmediatamente.

## Ajuste de volumen

Due to compatibility issues with the WASAPI added in NVDA-2023.2, the volume
adjustment have been temporarily removed, but may be restored in the future.

## División de sonido

As of version 1.16 this functionality has been moved to [soundSplitter
add-on](https://github.com/opensourcesys/soundSplitter/) maintained by Luke.

## Funciones mejoradas del ratón

* Alt+dividir del teclado numérico: lleva el puntero al objeto actual y hace
  clic.
* Alt+multiplicar del teclado numérico: lleva el puntero al objeto actual y
  hace clic con el botón derecho del ratón.
* Alt+más numérico o menos numérico: lleva el puntero del ratón al objeto
  actual y desplaza hacia arriba o hacia abajo. Esto es útil en páginas web
  con desplazamiento infinito y páginas web que cargan más contenido al
  desplazarse.
* Alt+suprimir del teclado numérico: mueve el puntero del ratón a la esquina
  superior izquierda de la pantalla. Esto puede ser útil para evitar
  desplazamientos no deseados en ventanas de ciertas aplicaciones.


## Detección del modo de inserción en editores de texto

Si esta opción está habilitada, NVDA pitará cuando detecte el modo de
inserción en editores de texto.

## Bloquear el atajo del doble insert

En NVDA, al pulsar la tecla Insert dos veces seguidas se conmuta el modo de
inserción en las aplicaciones. Sin embargo, a veces sucede por accidente y
dispara el modo de inserción. Dado que esta es una tecla especial, no se
puede desactivar en las opciones. Este complemento proporciona una manera de
bloquear este atajo de teclado. Cuando se bloquea el Insert doble, todavía
se puede conmutar el modo de inserción pulsando NVDA+f2 y luego insert.

Esta opción viene desactivada por defecto y debe activarse desde la
configuración.

## Prioridad del proceso de NVDA en el sistema

Esto permite acelerar la prioridad del proceso de NVDA en el sistema, que
puede aumentar el rendimiento, especialmente si la carga de la CPU es alta.

## Corrección de un fallo cuando el foco se atasca en la barra de tareas al pulsar windows+números

Hay un fallo en Windows 10, y posiblemente en otras versiones. Al cambiar
entre aplicaciones usando los atajos windows+números, a veces el foco se
atasca en la barra de tareas en lugar de saltar a la ventana a la que
queremos ir. No hay muchas esperanzas de que Microsoft arregle el fallo al
reportarlo, por lo que este complemento implementa una solución. El
complemento detecta esta situación y reproduce un breve pitido grave, tras
lo cuál la corrige automáticamente.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=tonysEnhancements
