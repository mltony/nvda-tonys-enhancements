# Tony's enhancements (Mejoras de Tony) #

* Autores: Tony Malykh
* Descargar [versión estable][1]
* Compatibilidad con NVDA: 2022.4 y 2023.1

Este complemento aporta una serie de pequeñas mejoras para el lector de
pantalla NVDA, insignificantes por sí solas para merecer complementos
independientes.

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

Con los siguientes atajos se puede copiar una tabla entera, una fila o una
columna preservando el formato, de tal forma que se pueda pegar como una
tabla en editores de texto enriquecido como Microsoft Word o WordPad.

* NVDA+alt+t - Muestra un menú emergente con opciones para copiar la tabla o
  parte de ella.

Hay también scripts independientes para copiar tablas, filas, columnas y
celdas, pero no tienen atajos de teclado asignados por defecto. Se pueden
asignar atajos personalizados para ellos desde el diálogo Gestos de entrada
de NVDA.

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

Se puede ocultar la ventana actual, y mostrar todas las ventanas
ocultas. Esto puede ser útil al usar varias ventanas en la misma aplicación
(pongamos Chrome) cuando queremos reordenarlas.

* NVDA+Shift+-: ocultar ventana actual.
* NVDA+Shift+=: Mostrar todas las ventanas ocultas.

Ten en cuenta que si cierras NVDA mientras una ventana está oculta, no hay
forma de volver a mostrarla tras reiniciarlo.

## Mejoras de consola

Antes, este complemento incluía ciertas funciones relacionadas con la
consola. A partir de la versión 1.8, todas las funciones relacionadas con la
consola se han movido al [complemento Console
Toolkit](https://github.com/mltony/nvda-console-toolkit/). Concretamente:

* Salida de la consola en tiempo real
* Pitar cuando se actualiza la consola
* Reforzar control+v en las consolas

## Pitar cuando NVDA esté ocupado

Marca esta opción para que NVDA proporcione retroalimentación de audio
cuando esté ocupado. El hecho de que NVDA esté ocupado no significa que haya
un problema necesariamente, pero sirve como señal al usuario de que las
órdenes que se envíen a NVDA no se procesarán inmediatamente.

## Ajuste de volumen

* NVDA+control+retroceso y avance de página - Ajustar volumen de NVDA.
* NVDA+alt+retroceso y avance de página - Ajustar volumen de todas las
  aplicaciones excepto NVDA.

## División de sonido

En el modo de división de sonido, NVDA dirigirá todo el sonido saliente al
canal derecho, mientras que las aplicaciones reproducirán sus sonidos por el
canal izquierdo. Se pueden intercambiar los canales en las opciones.

* NVDA+alt+s conmuta el modo de división de sonido.

Ten en cuenta que en ciertas situaciones la salida de sonido de una
aplicación podría estar limitada a un canal incluso cuando NVDA no está en
ejecución. Por ejemplo, esto podría suceder si NVDA ha fallado mientras la
división de sonido estaba activa, o cuando NVDA se cerró limpiamente cuando
la aplicación en cuestión no estaba en ejecución. Ante esas situaciones,
reinicia NVDA y desactiva la división de sonido mientras la aplicación esté
en ejecución.

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
