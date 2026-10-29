# PumpCalc: flujo, arquitectura e interfaz

**Estado:** definición de diseño para la evolución de PumpCalc. La estructura de archivos mostrada es orientativa; README.md describe la implementación presente.

## 1. Arquitectura elegida

PumpCalc seguirá siendo una sola aplicación de escritorio en Python: un **monolito modular con arquitectura limpia ligera**. La separación principal será entre interfaz, casos de uso, modelo y persistencia. La interfaz y la persistencia dependerán de las reglas de la aplicación, mientras que el cálculo hidráulico permanecerá independiente de ambas.

El módulo `pumpcalc/hydraulics.py` y su lógica matemática se conservan **sin ningún cambio**. El caso de uso de cálculo lo llamará por separado para las condiciones de tanque casi vacío y tanque casi lleno. La comparación con la meta, la interpretación de resultados y la advertencia de succión se harán fuera de ese módulo.

Estructura propuesta para incorporar conforme se desarrollen las funciones:

```text
main.py                    # inicia y conecta las piezas
pumpcalc/
  hydraulics.py            # matemática existente, sin cambios
  modelos.py               # escenario, entradas y resultados
  casos_uso.py              # calcular, comparar con la meta e interpretar
  persistencia.py           # guardar y recuperar escenarios con SQLite
  ui/
    app.py                 # ventana y barra lateral
    formulario.py          # captura de datos
    resultados.py          # presentación de resultados
    grafica.py             # dibujo de la gráfica
```

El recorrido interno será: **formulario → datos del escenario → caso de uso → `hydraulics.py` → resultado → pantalla**. Los casos de uso recibirán datos de Python, no controles de CustomTkinter. Solo la pieza de persistencia conocerá SQLite. No se prevén clases o capas adicionales por cada historia de usuario.

## 2. Patrón de interfaz

La ventana tendrá una barra lateral estable con **Cálculo** y **Escenarios**. La barra permanecerá visible al entrar en un panel y al volver. Las tareas de un mismo cálculo se agruparán dentro de Cálculo, sin convertir cada tarea en una pestaña de navegación.

La vista principal de **Cálculo** mostrará siempre tres tarjetas: **Instalación**, **Curva de bomba** y **Resultados**. Cada tarjeta abrirá un panel en el área principal de la misma ventana. El usuario podrá volver a las tarjetas sin perder lo escrito. Resultados también podrá abrirse antes de calcular; en ese caso mostrará qué datos faltan. Ninguna tarjeta se desbloqueará ni aparecerá de manera sorpresiva.

```text
┌────────────────┬──────────────────────────────────────────────┐
│ PumpCalc       │ Cálculo · Escenario sin guardar              │
│                │ ¿Qué datos necesito?                         │
│ ● Cálculo      │                                              │
│   Escenarios   │ [Instalación] [Curva de bomba] [Resultados]   │
│                │                                              │
│                │              [Calcular]                      │
└────────────────┴──────────────────────────────────────────────┘
```

| Espacio | Contenido previsto |
| --- | --- |
| **Instalación** | Meta de caudal; longitud, diámetro interior, material y accesorios; desniveles para tanque casi vacío y casi lleno; posición de la bomba respecto al agua de origen. Cada dato tendrá unidad y ayuda breve sobre cómo obtenerlo. |
| **Curva de bomba** | Fabricante, modelo y referencia de la ficha; unidad de caudal de la ficha; pares caudal–altura en una tabla. El ejemplo, si se carga, se identificará como demostración. |
| **Resultados** | Relación de cada condición con la meta, dos resultados comparables, detalle de pérdidas y velocidad, y gráfica de la bomba y las dos condiciones. La advertencia «succión no evaluada» aparecerá junto a la respuesta. |
| **Escenarios** | Configuraciones guardadas con nombre, fecha y estado. Desde aquí se podrá abrir un escenario en Cálculo, duplicarlo o elegir dos para compararlos. |

El botón **Calcular** estará en la vista principal de Cálculo. Los errores señalarán el campo correspondiente, explicarán cómo corregirlo y conservarán los demás datos. Al cambiar una entrada después de calcular, los resultados se mostrarán como **desactualizados** hasta recalcular. Los estados estarán escritos; el color no será su única indicación. La presentación priorizará la respuesta para la persona de la finca y dejará disponible el detalle técnico.

## 3. Flujo de un usuario en un escenario normal

1. **Abrir Cálculo.** La persona ve las tres tarjetas y la ayuda «¿Qué datos necesito?».
2. **Preparar los datos.** Define la meta de caudal a partir del agua que necesita y el tiempo disponible. Mide o consulta la tubería, el diámetro interior, los accesorios y los desniveles con el tanque casi vacío y casi lleno; consigue la curva de una bomba concreta.
3. **Completar Instalación.** Introduce la meta y las características físicas. La interfaz distingue claramente las dos condiciones del tanque y muestra unidades y ayudas junto a los campos.
4. **Completar Curva de bomba.** Identifica la bomba, selecciona la unidad usada en su ficha y transcribe los pares caudal–altura. Al volver a Cálculo, conserva lo escrito.
5. **Calcular.** Si falta un dato o hay un valor incorrecto, la aplicación abre el panel correspondiente, señala el campo y permite corregirlo sin borrar el resto.
6. **Leer Resultados.** Primero consulta si el caudal estimado alcanza la meta con el tanque casi vacío, casi lleno, en ambos casos o en ninguno; si faltan datos para decidir, verá «no concluyente». Después puede revisar las cifras, las pérdidas y la gráfica.
7. **Leer los límites del resultado.** La advertencia de succión aparece junto a la respuesta. Si no hay cruce dentro de la curva aportada, la interfaz explica lo que los datos permiten concluir o indica que faltan datos. Los dos caudales no se presentan como un cálculo del tiempo total de llenado.
8. **Guardar el escenario.** La persona le asigna un nombre reconocible y podrá encontrarlo en Escenarios con los datos que produjeron sus resultados.
9. **Comparar una alternativa, si lo necesita.** Duplica el escenario, cambia la bomba o la tubería, recalcula y compara las dos configuraciones. Mientras no recalcule, el resultado de la copia aparece como desactualizado.

## 4. Nombre del escenario y punto pendiente

**El nombre lo elige el usuario.** Al guardar un escenario, la interfaz le pedirá un nombre descriptivo, por ejemplo, «Tanque principal · bomba A». El sistema puede sugerir «Escenario nuevo» si el campo queda vacío, pero no debe elegir el nombre definitivo de las alternativas del usuario.

Queda **pendiente de decisión** permitir guardar un escenario incompleto como **borrador sin calcular**. Se planteó porque una persona puede necesitar salir a buscar la curva de la bomba o el diámetro interior y volver más tarde. El flujo normal anterior describe el caso en que dispone de los datos necesarios para calcular.
