# PumpCalc: caso de finca, interpretación y validación

**Estado:** decisiones de análisis y plan de validación. Aún no hay mediciones de una finca incorporadas al proyecto; README.md describe los dos cálculos por condición ya implementados.

Este documento reúne los supuestos físicos, la interpretación de resultados y la evidencia necesaria para contrastar PumpCalc con una finca real. Las necesidades, los requisitos y las historias de usuario están en [NECESIDAD_Y_REQUERIMIENTOS.md](NECESIDAD_Y_REQUERIMIENTOS.md). El módulo `pumpcalc/hydraulics.py` y su lógica matemática permanecen intactos.

## Decisiones de alcance

| Decisión | Tratamiento en esta etapa |
| --- | --- |
| Dos condiciones del tanque | Requisito prioritario: dos llamadas al cálculo vigente, con entradas y resultados identificados por condición. |
| Succión | Advertencia visible junto al resultado; no se calcula su viabilidad. |
| Ausencia de cruce | Mensajes basados en los extremos de la curva; cuando estos no bastan, se informa que faltan datos. |
| Material y accesorios | Se declaran los coeficientes empíricos actuales como aproximaciones, con su procedencia exacta pendiente. |
| Tiempo total de llenado | Fuera del alcance de las dos condiciones; no se infiere de sus dos caudales. |
| Rango por variación de `C` | Análisis posterior, separado del cambio de nivel del tanque; necesita valores justificables. |
| Validación en finca real | Pendiente de mediciones; el ejemplo académico conserva la etiqueta de demostración. |

## 1. Condiciones del tanque que representará cada escenario

Un escenario de finca describirá **la misma bomba, tubería y accesorios** bajo dos condiciones:

| Condición | Dato que cambia | Pregunta que responde |
| --- | --- | --- |
| Tanque casi vacío | Desnivel entre la superficie del agua en la fuente y la superficie del agua en el tanque al inicio. | ¿Qué caudal se estima al comenzar el llenado? |
| Tanque casi lleno | El mismo desnivel cuando el tanque se acerca al nivel final. | ¿Qué caudal se estima cerca del final? |

Si baja el nivel del aljibe o del pozo durante el bombeo, **también cambia el nivel de origen**. Por ello, los dos desniveles deben describir las superficies de agua en ambas condiciones; no basta con medir la altura de la bomba o la pared del tanque. Para depósitos abiertos, la altura estática depende de la diferencia entre niveles de agua. En instalaciones con presión exigida en el destino, esta versión no representa toda la altura requerida. [Hydraulic Institute: curvas del sistema](https://datatool.pumps.org/pump-fundamentals/sys-curves).

Cada condición llamaría una vez al cálculo existente con su propio desnivel. Si la bomba, la tubería, los coeficientes y el nivel de origen se mantienen iguales, el mayor desnivel del tanque casi lleno conduce a un caudal estimado menor o igual. El par de resultados es un **intervalo por cambio de nivel del agua**, no un intervalo estadístico de confianza. Si una condición queda fuera del intervalo de la curva de bomba, no se le asigna un caudal numérico.

Dos puntos de operación no calculan el **tiempo total de llenado**: el caudal cambia entre ambas condiciones. Calcular ese tiempo requeriría describir el volumen según el nivel del tanque y el comportamiento a lo largo del proceso. Por ahora, el tiempo total calculado queda fuera del alcance. Una medición de tiempo real puede registrarse como contexto, sin presentarla como una salida que el modelo actual predice.

## 2. Succión: advertencia que acompaña al resultado

La posición de la bomba respecto a la fuente debe quedar registrada como contexto, en especial si está sobre el nivel mínimo del agua. Los resultados deben indicar **«succión no evaluada»**. Cuando la bomba está por encima de la superficie del agua, la advertencia merece mayor visibilidad, pero no permite concluir por sí sola que la bomba fallará. La capacidad de trabajar con aspiración y el riesgo de cavitación dependen de la bomba y de las condiciones de entrada, que PumpCalc no calcula. [Hydraulic Institute: NPSH y regiones de operación](https://www.pumps.org/2022/12/07/the-basics-of-npsh-pump-operating-regions/).

La frase «alcanza la meta» se referirá únicamente al caudal **estimado por el modelo** para las condiciones indicadas. No verificará cebado, presión de succión, NPSH, potencia ni eficiencia.

## 3. Qué significa «no hay cruce»

El código calcula `F(Q) = H_bomba(Q) - H_instalación(Q)` y busca un cero dentro de los puntos suministrados. La interfaz actual muestra un único mensaje cuando `punto_operacion()` devuelve `None`. La interpretación futura debe respetar el tramo de caudales disponible y no extrapolar.

| Situación observada en la curva ingresada | Interpretación admisible |
| --- | --- |
| La curva incluye `Q = 0` y la altura de la bomba allí es menor que la altura estática requerida. | Bajo los supuestos del modelo y esa curva, la bomba no vence la altura aun sin flujo; no se obtiene caudal positivo. |
| En el último punto suministrado la bomba todavía entrega más altura que la que exige la instalación. | No hay cruce **dentro del intervalo ingresado**. Faltan datos para saber qué ocurre a caudales mayores; no se afirma que el cruce exista fuera del intervalo. |
| La curva comienza en un caudal mayor que cero y la bomba ya está por debajo de la altura requerida en ese primer punto. | No hay cruce en el intervalo ingresado. Podría faltar la parte de la curva de menores caudales; no se afirma que la bomba sea incapaz de vencer la altura en todo su rango. |

Estas distinciones pueden obtenerse al interpretar los extremos con las funciones existentes. Se apoyan en la validación actual de puntos de bomba con caudal creciente y altura no creciente, y en que la altura de la instalación aumenta con el caudal para los parámetros permitidos. No requieren modificar `hydraulics.py`.

Si el cálculo devuelve un cruce en `Q = 0`, existe un punto matemático en el extremo, pero **no satisface una meta positiva de caudal**.

## 4. Modelo de pérdidas y procedencia de los parámetros

La interfaz pide **material**. Según el material selecciona un valor fijo del coeficiente empírico `C` de Hazen–Williams. Ese coeficiente no es una medición de la tubería específica ni equivale al factor de fricción iterativo de Darcy–Weisbach. El modelo actual emplea Hazen–Williams para agua; esta fórmula se desarrolló para flujo turbulento y el coeficiente puede variar según la condición y antigüedad de la tubería. [EPA: manual de EPANET 2.2](https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=P10113EM.TXT).

| Parámetro del código actual | Valor | Estado de la evidencia |
| --- | ---: | --- |
| `C` para PVC | 150 | Valor inicial aproximado del proyecto; no medido en la finca. |
| `C` para acero | 120 | Valor inicial aproximado del proyecto; no medido en la finca. |
| `C` para hierro fundido | 100 | Valor inicial aproximado del proyecto; no medido en la finca. |
| `K` por codo de 90° | 0,9 | Valor inicial aproximado; no ligado a una pieza comercial concreta. |
| `K` por válvula de compuerta abierta | 0,15 | Valor inicial aproximado; no ligado a una pieza comercial concreta. |
| `K` por válvula de retención | 2,5 | Valor inicial aproximado; no ligado a una pieza comercial concreta. |

La procedencia de estos **valores exactos** todavía no está documentada con fichas de los componentes. Las tablas externas muestran valores orientativos y no deben presentarse como si certificaran los números elegidos para esta instalación. En el código, los `K` se multiplican por las cantidades ingresadas y se suman antes de calcular.

El diámetro interior de 32 mm del ejemplo académico no debe etiquetarse como un **límite inferior universal** de Hazen–Williams. Sí exige conocer el diámetro real: la pérdida de tubería en la fórmula implementada es muy sensible a ese dato. Una futura comparación de varios valores justificables de `C` sería un análisis de sensibilidad del **supuesto de material**, separado del intervalo causado por los niveles del tanque. No se fijará un rango numérico de incertidumbre sin datos que lo respalden.

El aviso de velocidad alta queda como mejora secundaria. La interfaz ya muestra la velocidad, pero no se incorporará un umbral de alerta sin indicar para qué tubería y criterio técnico aplica.

## 5. Curva de bomba y unidades

La versión actual exige **al menos dos pares** de caudal y altura, con caudal estrictamente creciente y altura no creciente. Eso es un mínimo para ejecutar la interpolación lineal, no una cantidad universalmente suficiente para representar cualquier ficha. Para transcribir una gráfica conviene usar los puntos legibles de la curva del modelo elegido y prestar especial atención al tramo donde se espera el cruce; no se establece una cifra fija de puntos recomendados sin ver la curva.

La ficha debe identificar fabricante, modelo y condición de operación de la curva. El caudal de entrada al módulo numérico seguirá en m³/h. Para facilitar la transcripción, la capa de interfaz podrá convertir:

| Unidad de la ficha | Equivalencia en m³/h |
| --- | ---: |
| 1 L/min | 0,06 m³/h |
| 1 galón **estadounidense** por minuto (US gpm) | 0,22712472 m³/h |

El galón imperial tiene otro volumen; si una gráfica solo dice «GPM» y no permite reconocer cuál usa, la unidad debe aclararse antes de convertir. [NIST: factores de conversión](https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8).

## 6. Fundamento numérico vigente, en breve

La función `altura_bomba()` interpola linealmente los pares ingresados. `altura_instalacion()` suma desnivel, pérdida por tubería y pérdidas por accesorios. `punto_operacion()` recorre cada tramo de la curva de bomba y aplica bisección cuando la diferencia entre ambas alturas cambia de signo. Comprueba primero los extremos y, en el tramo con cruce, realiza hasta **60 iteraciones**; termina antes si la diferencia de alturas es como máximo `1e-9 m` o si el ancho del intervalo de caudal es como máximo `1e-8 m³/h`. Si no halla cruce en el intervalo ingresado, devuelve `None`.

El código no calcula un factor de fricción iterativo. La explicación matemática completa permanece en [DOCUMENTO_PROYECTO.md](DOCUMENTO_PROYECTO.md); esta sección solo permite interpretar el comportamiento existente.

## 7. Caso de finca para validación: datos pendientes

No se llamará «caso real» al ejemplo académico de 40 m y 32 mm. Hasta disponer de mediciones, los números de [DOCUMENTO_PROYECTO.md](DOCUMENTO_PROYECTO.md) son **datos de demostración**. Para contrastar el modelo con una finca concreta se registrarán, como mínimo:

1. Identificación de la finca o un código anónimo, fecha y condiciones de la medición.
2. Fuente de agua, ubicación de la bomba y niveles del agua en fuente y tanque al inicio y cerca del final.
3. Longitud real del recorrido, diámetro **interior**, material, estado conocido de la tubería y accesorios presentes.
4. Identificación y curva de la bomba utilizada, con sus unidades y condición de operación.
5. Meta de caudal del responsable de la finca y mediciones de caudal obtenidas cerca de las dos condiciones. Si se registra volumen por tiempo, anotar el tramo de nivel al que corresponde y si hubo consumo simultáneo de agua.

La comparación se hará **condición por condición**: caudal estimado al inicio frente a caudal medido cerca del inicio, y lo mismo para el final. Se informará la diferencia observada sin declarar una tolerancia aceptable inventada. Un tiempo total de llenado medido puede describir la experiencia de la finca, pero no validará una predicción de tiempo total que esta versión no produce.

La validación de campo queda pendiente hasta contar con esos datos. No requiere alterar los cálculos matemáticos existentes; sí exige documentar claramente qué se midió y qué se supuso.
