# PumpCalc: decisiones de diseño que faltan por definir

**Estado:** inventario de decisiones abiertas. Este documento no aprueba una interfaz nueva ni cambia los requisitos hidráulicos. Recoge la crítica a la interfaz implementada para que el siguiente diseño se decida antes de modificar el software.

## Qué se entendió de la revisión

- La barra lateral actual agrupa demasiado trabajo bajo **Cálculo** y no ayuda a distinguir las tareas que realiza la persona.
- Los formularios se ven como una sucesión de cuadros con comentarios. La ayuda ocupa espacio, pero no guía bien la captura.
- Los resultados parecen texto impreso dentro de cuadros. Falta una composición visual que permita entender primero la respuesta y luego examinar los detalles.
- El problema señalado es de **estructura, presentación e interacción**, además del aspecto gráfico. Cambiar solamente colores o bordes no resolvería lo anterior.

Los documentos existentes detallan el problema de la finca, los datos, el cálculo y las funciones esperadas. Dejan menos definida la experiencia visual. La decisión anterior de tener solo **Cálculo** y **Escenarios** en la barra lateral debe revisarse a la luz de esta observación; no se considera cerrada para el rediseño.

## Decisiones principales

| Tema | Lo que falta definir | Pregunta concreta que debe resolverse |
| --- | --- | --- |
| **1. Mapa de navegación** | Qué tareas merecen una entrada propia en la barra lateral y cuáles son pasos dentro de una tarea. | ¿La barra separa, por ejemplo, preparación de datos, instalación, bomba, resultados y escenarios? ¿Qué ve la persona al abrir la aplicación? |
| **2. Recorrido principal** | Orden en que una persona crea un escenario, consigue datos, calcula y compara; forma de avanzar y volver. | ¿Es un recorrido guiado por pasos o puede entrar libremente en cualquier sección? ¿Cómo se ve el progreso sin bloquear a quien ya tiene los datos? |
| **3. Pantalla inicial** | Una vista que explique qué puede hacer la aplicación y el estado del trabajo actual. | ¿Debe mostrar un resumen del escenario, tareas pendientes, cálculos recientes o accesos directos? |
| **4. Jerarquía de la información** | Qué debe llamar la atención primero en cada pantalla y qué debe quedar en un segundo nivel. | En Resultados, ¿la primera lectura es «alcanza la meta», los dos caudales, la gráfica o una comparación de condiciones? |
| **5. Diseño de formularios** | Agrupación de campos, distribución en columnas, longitud de cada sección y controles apropiados. | ¿Qué datos se completan juntos? ¿Qué campos requieren tabla, selector o entrada numérica en vez de texto libre? |
| **6. Ayuda para capturar datos** | Forma de explicar significado, unidad y procedencia sin convertir cada campo en un bloque de comentario. | ¿Qué ayuda está siempre visible y cuál aparece al pedirla? ¿Cómo se muestra un ejemplo sin confundirlo con datos reales? |
| **7. Entrada de la curva de bomba** | Diseño de la tabla de pares, edición de filas y vista previa de la curva. | ¿Cómo agrega, corrige y elimina puntos una persona? ¿Dónde ve la unidad original y la conversión a m³/h? |
| **8. Presentación de resultados** | Composición específica para las dos condiciones, cifras principales, pérdidas y estados. | ¿Se usa una comparación lado a lado, una tabla o secciones separadas? ¿Cómo se distinguen entradas, estimaciones y conclusión? |
| **9. Gráfica** | Su papel en la lectura, tamaño, leyenda, etiquetas, colores y comportamiento ante datos incompletos. | ¿Qué curvas y puntos se muestran a la vez? ¿Cómo se señala el cruce o la ausencia de cruce de cada condición sin depender solo del color? |
| **10. Escenarios y comparación** | Vista de biblioteca, selección, duplicación y comparación de alternativas. | ¿Qué datos aparecen en cada escenario? ¿Qué diferencias se resaltan al comparar y cómo se identifican resultados desactualizados? |
| **11. Estados de pantalla** | Diseño para borrador, campos faltantes, error, cálculo vigente, desactualizado y sin cruce. | ¿Qué ve exactamente la persona en cada estado y cuál es la siguiente acción disponible? |
| **12. Sistema visual** | Tipografía, tamaños, espaciado, colores, iconos, bordes y densidad de información. | ¿Qué estilo visual busca el proyecto y qué reglas comunes mantendrán consistentes todas las pantallas? |

## Detalles que también necesitan una decisión

### Captura y edición

- **Valores de demostración:** decidir si la aplicación abre vacía, con un ejemplo que se carga mediante una acción explícita o con otro tratamiento visual. Debe ser imposible confundir el ejemplo académico con una finca medida.
- **Procedencia de datos:** definir cómo se registran y se ven datos medidos, tomados de una ficha y supuestos. Falta decidir si la procedencia corresponde a cada campo o a grupos de campos.
- **Unidades:** definir dónde se seleccionan, cómo se visualiza una conversión y qué ocurre si se cambia la unidad después de escribir los puntos.
- **Validación:** especificar el aspecto de un campo incorrecto, la ubicación del mensaje, el foco y la conservación de lo que ya se escribió.
- **Guardado:** definir señales de cambios sin guardar, nombre de un borrador, confirmación al salir y recuperación de un escenario.

### Lectura e interpretación

- **Comparación con la meta:** decidir cómo se expresan «ambas», «solo una», «ninguna» y «no concluyente» en la interfaz, incluyendo cuál condición cumple cuando solo una lo hace.
- **Ausencia de cruce:** definir una presentación distinta para altura insuficiente a caudal cero y para una curva incompleta, sin dar a ambas el mismo aspecto de error.
- **Advertencia de succión:** decidir dónde aparece y qué prominencia tiene cuando la bomba está por encima del agua. Debe acompañar el resultado sin esconder la respuesta principal.
- **Precisión visible:** acordar cifras decimales, redondeo, unidades y texto que recuerde que se trata de una estimación con coeficientes aproximados.
- **Explicación técnica:** decidir qué parte de las pérdidas y del método numérico se ve de inmediato y qué parte se abre para quien quiera examinarla.

### Uso de la ventana

- **Tamaños y desplazamiento:** definir ancho mínimo, comportamiento al reducir la ventana y qué se desplaza cuando una sección es larga. La barra lateral y las acciones importantes deben seguir localizables.
- **Acceso por teclado:** definir orden de tabulación, foco visible, acciones de botones y lectura de errores y estados sin depender solo del color.
- **Lenguaje:** elegir nombres breves y consistentes para las tareas y condiciones. Conviene comprobar que una persona responsable de la finca entienda «desnivel», «curva», «escenario» y «punto de operación» o disponga de una explicación cercana.

## Qué conviene acordar antes de redibujar la aplicación

1. **Mapa de pantallas y barra lateral:** nombres de secciones, propósito de cada una y recorrido entre ellas.
2. **Bocetos de baja fidelidad:** pantalla inicial, captura de instalación, curva de bomba, resultados y comparación de escenarios.
3. **Ejemplos de cada estado:** datos faltantes, error, dos cruces, un cruce, ningún cruce y resultado desactualizado.
4. **Reglas de presentación:** jerarquía de cifras, gráfica, ayuda, advertencias y sistema visual básico.
5. **Criterios de aceptación de interfaz:** tareas observables que permitan decir si el nuevo diseño es claro, además de comprobar que el cálculo funciona.

Hasta decidir esos puntos, los requisitos funcionales permiten programar comportamientos, pero no bastan para afirmar que la organización y la apariencia de la interfaz sean las adecuadas.
