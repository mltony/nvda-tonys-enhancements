# Tony's enhancements (Mejoras de Tony) #

Este complemento aporta una serie de pequeñas mejoras para el lector de
pantalla NVDA, insignificantes por sí solas para merecer complementos
independientes.

Este complemento es compatible con NVDA versión 2024.2 o posterior

## Descargas

Instala la versión más reciente desde la tienda de complementos de NVDA.

## Órdenes mejoradas de navegación por tablas
* NVDA+control+dígitos del 1 al 0 - Saltar a la primera, segunda,
  tercera... décima columna de la tabla.
* NVDA+alt+dígitos del 1 al 0 - Saltar a la primera, segunda,
  tercera... décima fila de la tabla.

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

## Cambio automático de idioma
Permite cambiar automáticamente el idioma del sintetizador según el conjunto
de caracteres. En la ventana de preferencias de este complemento se pueden
configurar expresiones regulares para cada idioma. Asegúrate de que el
sintetizador soporta todos los idiomas que te interesan. No se soporta de
momento cambiar entre dos idiomas con caracteres latinos o conjuntos de
caracteres similares.

## Órdenes de búsqueda rápida

A partir de la versión 1.18, las órdenes de búsqueda rápida se han movido al
[complemento IndentNav](https://github.com/mltony/nvda-indent-nav).

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

A partir de la versión 1.18, las órdenes de mostrar y ocultar se han movido
al [complemento Task
Switcher](https://github.com/mltony/nvda-task-switcher).

## Pitar cuando NVDA esté ocupado

Marca esta opción para que NVDA proporcione retroalimentación de audio
cuando esté ocupado. El hecho de que NVDA esté ocupado no significa que haya
un problema necesariamente, pero sirve como señal al usuario de que las
órdenes que se envíen a NVDA no se procesarán inmediatamente.

## Ajuste de volumen de la aplicación

Esta función se ha integrado en el núcleo de NVDA y está disponible en NVDA
v2024.3 o posterior.

## Silenciar micrófono

Este complemento proporciona una orden para alternar el micrófono. No hay
gesto asignado a esta orden por defecto, pero puedes asignarla desde el
diálogo "Gestos de entrada" de NVDA si fuera necesario.

## División de sonido

Esta función se ha integrado en el núcleo de NVDA y está disponible en NVDA
v2024.2 o posterior.

## Funciones mejoradas del ratón

* Alt+dividir del teclado numérico: lleva el puntero al objeto actual y hace
  clic.
* Alt+multiplicar del teclado numérico: lleva el puntero al objeto actual y
  hace clic con el botón derecho del ratón.
* Alt+suprimir del teclado numérico: mueve el puntero del ratón a la esquina
  superior izquierda de la pantalla. Esto puede ser útil para evitar
  desplazamientos no deseados en ventanas de ciertas aplicaciones.

La funcionalidad de desplazamiento de la rueda del ratón se ha integrado en
el núcleo de NVDA y está disponible en NVDA v2024.3 o posterior.

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

## Bloqueo del atajo de bloqueo de mayúsculas doble

En NVDA, cuando el bloqueo de mayúsculas se configura como tecla de NVDA,
conmuta entre mayúsculas y minúsculas al pulsarla rápidamente dos veces. Sin
embargo, esto a veces puede causar una alternancia no intencionada entre
estos modos. Ya que el comportamiento de esta tecla es único y no se puede
deshabilitar en las opciones, este complemento ofrece un método para
bloquear este atajo de teclado concreto. Cuando se bloquea la doble
pulsación del bloqueo de mayúsculas, se puede cambiar entre mayúsculas y
minúsculas pulsando NVDA+f2, seguido de la tecla bloqueo mayúsculas.

Esta opción viene desactivada por defecto y debe activarse desde la
configuración.

## Prioridad del proceso de NVDA en el sistema

Esto permite acelerar la prioridad del proceso de NVDA en el sistema, que
puede aumentar el rendimiento, especialmente si la carga de la CPU es alta.

## Corrección de un fallo cuando el foco se atasca en la barra de tareas al pulsar windows+números

Esta función se ha eliminado a partir de la versión 1.18. Si necesitas una
funcionalidad de alternancia entre tareas más fiable, plantéate usar [el
complemento Task Switcher](https://github.com/mltony/nvda-task-switcher).

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=tonysEnhancements
