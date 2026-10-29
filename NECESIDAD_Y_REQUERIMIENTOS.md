# PumpCalc: necesidad real, alcance y requisitos del producto

**Estado:** especificación de la evolución. La columna «Estado» de la tabla conserva la situación de la línea base previa a la implementación descrita en README.md; no es un inventario actualizado del código.

## 1. La decisión que necesita tomar una persona

La persona responsable de una finca quiere llevar agua desde una fuente, como un aljibe o un pozo, hasta un tanque abierto. Necesita saber si una bomba y una instalación propuestas pueden entregar el caudal que requiere. La ficha de la bomba describe su comportamiento a diferentes caudales; la tubería, el desnivel y los accesorios imponen una resistencia. El caudal esperable en esa combinación no se obtiene leyendo un único valor de la caja de la bomba: se estima donde se cruzan la curva de la bomba y la curva de la instalación.

PumpCalc responde una pregunta acotada: **«Con el tanque casi vacío y casi lleno, ¿qué caudal se estima para esta bomba y alcanza mi meta en ambos casos?»** Su utilidad principal es comparar alternativas antes de comprar o montar componentes, o comprender por qué una configuración ya planteada no parece suficiente. El resultado es una estimación del modelo, no una garantía de rendimiento en campo ni una aprobación técnica de la bomba.

### Personas afectadas y necesidades

| Persona | Situación y necesidad | Decisión que busca apoyar |
| --- | --- | --- |
| **Principal: responsable de la finca** | Conoce el tanque y la cantidad de agua que necesita, pero puede desconocer la curva de bomba o el diámetro interior de la tubería. | Saber si la configuración merece seguir considerándose, incluso cuando cambia el nivel del tanque. |
| **Secundaria: instalador o vendedor que asesora** | Puede medir el recorrido y consultar fichas de equipos; ayuda a traducir la necesidad a datos técnicos. | Comparar alternativas y explicar al responsable de la finca qué cambia. |

Estudiantes y docentes forman parte del **contexto del curso**, no son un tercer perfil de uso con el mismo peso. El producto debe servir primero a quien toma la decisión práctica; la explicación académica sigue disponible, pero no debe ser un requisito previo para usar la aplicación.

## 2. El obstáculo anterior al cálculo: conseguir los datos

El usuario no empieza con una tabla completa de parámetros. Parte de una necesidad cotidiana y debe traducirla a datos de instalación y de una bomba específica. Si no puede obtenerlos, el flujo se detiene antes de pulsar **Calcular**.

| Dato | Fuente razonable | Lo que debe quedar claro en la interfaz |
| --- | --- | --- |
| Caudal mínimo deseado | Necesidad de uso; por ejemplo, volumen del tanque dividido entre el tiempo disponible para llenarlo. | Es una meta del usuario, no un resultado hidráulico. Si se necesitan 6.500 L en una hora, la meta es 6,5 m³/h. |
| Longitud de tubería | Plano, trazado previsto o medición del recorrido completo. | Se pide la longitud a lo largo de la tubería, no la distancia en línea recta. |
| Diámetro interior y material | Especificación del tubo existente o del producto propuesto. | El diámetro interior no se debe confundir con el nominal o el exterior. |
| Desnivel con el tanque casi vacío y casi lleno | Diferencia entre la superficie del agua en la fuente y la superficie del tanque en cada condición, medida o estimada en la finca. | Son **dos condiciones** de la misma instalación. Si también cambia el nivel de la fuente, hay que reflejarlo en cada desnivel. La versión actual solo admite desniveles no negativos. |
| Posición de la bomba respecto al agua de origen | Observación de la ubicación y del nivel mínimo esperado de la fuente. | Permite contextualizar una advertencia: PumpCalc no verifica si la succión de esa bomba es viable. |
| Cantidades de accesorios | Plano o inspección del recorrido. | Se cuentan los tipos admitidos por el modelo; sus coeficientes son aproximaciones incorporadas en la aplicación. |
| Puntos caudal–altura de la bomba | Curva de la ficha del fabricante correspondiente al modelo y condición de operación elegidos. | Cada línea representa un par de la misma curva. La ficha puede estar dibujada y usar L/min o galones por minuto; deben identificarse las unidades y, en este último caso, el tipo de galón. |

Los valores que aparezcan precargados en un ejemplo deben identificarse como **datos de demostración**. No representan automáticamente la instalación del usuario. Si falta una curva confiable de la bomba o se desconoce el diámetro interior, el resultado puede tener una apariencia de precisión que los datos no justifican.

## 3. Alcance de la solución

### Caso que sí representa esta etapa

- Agua, flujo estacionario, una bomba y una sola línea principal de diámetro interior constante.
- Una curva caudal–altura suministrada mediante puntos ordenados por caudal.
- Dos condiciones representativas con desnivel no negativo: tanque casi vacío y casi lleno. Se calculan por separado con la misma bomba, tubería y accesorios.
- Estimación del punto de operación de cada condición dentro del intervalo de la curva ingresada; no se extrapola.
- Comparación de alternativas independientes, como cambiar el diámetro o la bomba, mediante escenarios guardados.

### Casos que esta etapa no representa

- Redes ramificadas, varias bombas o distintos diámetros en un mismo recorrido.
- Evolución continua del caudal y cálculo exacto del tiempo total de llenado. Las dos condiciones son fotografías del inicio y del final, no una simulación de todo el proceso.
- Destinos que exigen una presión residual determinada, como ciertos sistemas de riego presurizado.
- Verificación de succión, cavitación, potencia, consumo, eficiencia, costo o región de operación recomendada por el fabricante.
- Certificación de una instalación o elección automática de la bomba que se debe comprar.

Estas exclusiones son límites del modelo actual. Que ambas condiciones superen la meta significa únicamente que **la superan en las estimaciones bajo los datos y supuestos indicados**. La succión no verificada debe indicarse junto a los resultados, especialmente si la bomba está por encima del nivel del agua de origen.

## 4. Recorrido principal del usuario

1. Define la meta de caudal y comprueba si su caso de finca corresponde al alcance de PumpCalc.
2. Obtiene o estima los datos de la instalación, los dos desniveles representativos y la curva de una bomba concreta.
3. Completa los paneles **Instalación** y **Curva de bomba** dentro del espacio de **Cálculo**.
4. Calcula y consulta **Resultados** para el tanque casi vacío y casi lleno: punto de operación, pérdidas, gráfica y relación con la meta en cada condición.
5. Guarda la configuración como **Escenario** con un nombre y la procedencia de la curva.
6. Duplica el escenario para cambiar una alternativa y compara ambos resultados sin perder el original.

La barra lateral tendrá dos destinos estables: **Cálculo** y **Escenarios**. Dentro de Cálculo, las **tres tarjetas** de Instalación, Curva de bomba y Resultados abrirán paneles en la misma ventana; el usuario podrá volver sin perder lo que escribió. Las tres tarjetas estarán siempre visibles. Esta estructura fue aceptada por el responsable del proyecto en la conversación de diseño para mantener juntas las partes de un mismo cálculo.

## 5. Concepto central: escenario

Un **escenario** es una configuración identificable de instalación y bomba. Guarda un nombre, las entradas completas, los desniveles de las dos condiciones del tanque, la meta de caudal, la referencia de la curva utilizada y el estado de **cada** cálculo. Cada resultado se asocia a las entradas exactas con las que fue obtenido. La ausencia de cruce en una o ambas condiciones también se puede conservar.

Al cambiar una entrada que afecta el cálculo, el resultado anterior deja de describir la configuración en pantalla: debe mostrarse como **desactualizado** hasta recalcular. Duplicar un escenario crea una alternativa independiente para comparar cambios, en vez de reemplazar los datos originales. Los dos resultados de un mismo escenario muestran la variación por nivel del tanque; la duplicación permite comparar cambios de bomba o tubería.

## 6. Requisitos funcionales

**Estado actual** describe lo que ya ofrece el código; **propuesto** describe trabajo pendiente. El orden P0/P1 refleja valor para el problema, no un compromiso de implementación inmediata.

| ID | Prioridad | Requisito | Estado |
| --- | --- | --- | --- |
| RF-01 | P0 | Explicar el caso de finca que representa el cálculo, qué datos requiere y de dónde puede obtenerse cada uno. | Propuesto |
| RF-02 | P0 | Registrar una meta mínima de caudal en m³/h. | Propuesto |
| RF-03 | P0 | Registrar longitud, diámetro interior, material y cantidades de accesorios admitidos. | Actual |
| RF-04 | P0 | Registrar dos desniveles no negativos que representen el tanque casi vacío y casi lleno, considerando el nivel de la fuente en cada condición. | Propuesto; hoy solo se registra un desnivel |
| RF-05 | P0 | Registrar al menos dos pares de la misma curva de bomba, con caudal creciente y altura no creciente. | Actual |
| RF-06 | P0 | Convertir caudales de fichas expresados en L/min o GPM estadounidense a m³/h, identificando la unidad de origen. | Propuesto |
| RF-07 | P0 | Validar formato y rangos de entradas antes de calcular; señalar el campo que necesita corrección. | Parcial: hay validación, pero el mensaje se muestra en la barra lateral |
| RF-08 | P0 | Calcular el punto de operación por separado para las dos condiciones mediante el módulo numérico existente, sin extrapolar. | Propuesto; hoy se calcula una sola condición |
| RF-09 | P0 | Mostrar para cada condición caudal, altura, velocidad, pérdidas y curvas; distinguir resultados de datos introducidos. | Parcial: las salidas actuales corresponden a una sola condición |
| RF-10 | P0 | Comparar cada caudal estimado con la meta y distinguir «ambas condiciones», «solo una», «ninguna» y «no concluyente» cuando falten datos para decidir. | Propuesto |
| RF-11 | P0 | Mostrar junto a los resultados que la succión no fue evaluada; destacar el aviso cuando la bomba esté por encima del nivel mínimo de la fuente. | Propuesto |
| RF-12 | P0 | Diferenciar la ausencia de cruce según lo que realmente permiten concluir los extremos de la curva; no afirmar una causa que los datos no demuestran. | Propuesto; hoy hay un mensaje único |
| RF-13 | P0 | Guardar y volver a abrir escenarios con las dos condiciones, las entradas y el estado de cada cálculo. | Propuesto |
| RF-14 | P0 | Marcar ambos resultados como desactualizados cuando cambien las entradas que los produjeron. | Propuesto |
| RF-15 | P1 | Duplicar escenarios y comparar sus entradas y resultados principales. | Propuesto |
| RF-16 | P1 | Registrar fabricante, modelo, condición de operación y referencia de la curva utilizada. | Propuesto |
| RF-17 | P1 | Mantener la barra lateral con Cálculo y Escenarios, y usar tres tarjetas para los paneles del cálculo. | Propuesto; estructura aceptada por el responsable del proyecto |
| RF-18 | P2 | Avisar sobre velocidades elevadas cuando exista un criterio técnico aplicable y documentado para el caso. | Propuesto; criterio aún no definido |

## 7. Requisitos no funcionales y reglas de confianza

| ID | Requisito |
| --- | --- |
| RNF-01 | Conservar `pumpcalc/hydraulics.py` y su lógica matemática **sin ningún cambio**. Las dos condiciones se obtienen mediante llamadas separadas al módulo existente; la interfaz, la persistencia y la comparación con la meta se construyen fuera de él. |
| RNF-02 | Mantener una aplicación de escritorio utilizable sin conexión a Internet para calcular y consultar escenarios locales. |
| RNF-03 | Guardar escenarios sin perder la relación entre cada condición, sus entradas y su resultado; una edición nunca debe presentar un resultado anterior como vigente. |
| RNF-04 | Mostrar unidades junto a cada entrada y salida; identificar los datos de demostración y declarar que los coeficientes de material y accesorios son aproximados. |
| RNF-05 | Permitir completar el recorrido principal mediante teclado y mantener visibles las etiquetas, errores y estado seleccionado. |
| RNF-06 | Verificar los flujos de dos condiciones, guardar, abrir, duplicar, recalcular y manejar casos sin cruce, además de conservar las pruebas numéricas existentes. |
| RNF-07 | Identificar por separado datos medidos, datos de ficha y supuestos. No presentar el ejemplo académico como validación de campo ni afirmar una precisión que todavía no se ha medido. |

## 8. Historias de usuario prioritarias

### HU-01 — Saber qué datos necesito

**Como** responsable de una finca, **quiero** saber qué datos pide PumpCalc y de dónde obtenerlos **para** preparar el cálculo sin tomar los ejemplos como medidas de mi instalación.

**Criterios de aceptación:** cada entrada indica unidad, significado y fuente habitual; los valores de demostración se identifican; el alcance del modelo se muestra antes de interpretar resultados.

### HU-02 — Definir mi necesidad de agua

**Como** responsable de una finca, **quiero** indicar el caudal mínimo que necesito **para** contrastarlo con los caudales estimados.

**Criterios de aceptación:** puedo introducir una meta positiva en m³/h; se conserva dentro del escenario y se distingue visualmente de los caudales calculados.

### HU-03 — Describir el recorrido y los niveles del agua

**Como** responsable de una finca, **quiero** registrar la tubería, los accesorios y los desniveles con el tanque casi vacío y casi lleno **para** representar dos condiciones relevantes de la misma instalación.

**Criterios de aceptación:** registro longitud, diámetro interior, material, cantidades de accesorios y dos desniveles no negativos; se indica que el nivel de la fuente también puede cambiar; un error identifica el campo que debe corregirse.

### HU-04 — Registrar la curva de una bomba concreta

**Como** instalador o vendedor que asesora a la finca, **quiero** ingresar los pares caudal–altura de una ficha e identificar su origen **para** evaluar una bomba reconocible.

**Criterios de aceptación:** se exigen al menos dos pares de la misma curva, con caudal creciente y altura no creciente; se registra modelo y fuente; se identifican y convierten L/min o GPM estadounidense antes de calcular en m³/h; no se extrapola.

### HU-05 — Ver el comportamiento al inicio y al final

**Como** responsable de una finca, **quiero** ver el punto de operación para el tanque casi vacío y casi lleno **para** entender cómo cambia el caudal al llenarse.

**Criterios de aceptación:** para cada condición se muestran caudal, altura, velocidad, pérdidas y curvas; si no hay cruce en una condición, se informa sin inventar un caudal; los dos resultados se identifican por su condición.

### HU-06 — Saber cuándo alcanzo mi meta

**Como** responsable de una finca, **quiero** comparar ambos caudales con mi meta **para** distinguir si la alcanzo en las dos condiciones, solo en una o en ninguna.

**Criterios de aceptación:** el mensaje diferencia esos casos e identifica cuál condición cumple cuando solo cumple una; usa «no concluyente» si los datos no permiten decidir y distingue el caso en que la bomba no vence la altura aun en caudal cero; no promete un tiempo total de llenado ni declara la bomba apta en todos sus aspectos.

### HU-07 — Conocer la limitación de la succión

**Como** responsable de una finca, **quiero** ver junto al resultado que la succión no fue verificada **para** no confundir el caudal estimado con una garantía de funcionamiento de una bomba ubicada sobre el agua.

**Criterios de aceptación:** el aviso aparece junto a ambos resultados; si se indica que la bomba está por encima del nivel mínimo de la fuente, el aviso se destaca sin afirmar automáticamente que la bomba fallará.

### HU-08 — Retomar un escenario

**Como** responsable de una finca, **quiero** guardar y abrir una configuración **para** continuar el análisis sin introducir todos los datos de nuevo.

**Criterios de aceptación:** el escenario tiene un nombre; al abrirlo recupero entradas, meta y estado de las dos condiciones; al editar una entrada que afecta el cálculo, los resultados previos quedan desactualizados hasta recalcular.

### HU-09 — Comparar alternativas

**Como** responsable de una finca, **quiero** duplicar un escenario y cambiar una bomba o tubería **para** comparar alternativas sin perder la configuración original.

**Criterios de aceptación:** la copia se edita de forma independiente; ambas configuraciones se conservan; la comparación muestra el dato modificado y los resultados inicial y final de cada alternativa.

## 9. Ejemplo que une problema y solución

**Datos de demostración, no mediciones de una finca:** una persona necesita **6,5 m³/h**. En el ejemplo académico documentado, una bomba con la curva indicada, 40 m de tubería PVC, 12 m de desnivel y diámetro interior de 32 mm produce una estimación de **6,064 m³/h**. Al cambiar únicamente el diámetro interior a 40 mm, la estimación pasa a **6,616 m³/h**. El ejemplo ayuda a entender la comparación de alternativas, pero usa un solo desnivel y no valida el comportamiento de un tanque que se llena.

El caso de finca real queda **pendiente de medición**. Para presentarlo como ejemplo y validación se necesitan la identificación y curva de la bomba, el recorrido y diámetro interior de la tubería, los accesorios, los niveles de agua de origen y tanque en cada condición y mediciones de caudal comparables. No se completarán esos valores con supuestos inventados. El plan de medición y los criterios de interpretación están en [CASO_FINCA_Y_VALIDACION.md](CASO_FINCA_Y_VALIDACION.md).

## 10. Referencias para el alcance y los datos

- [Hydraulic Institute: curvas de bomba y de sistema](https://datatool.pumps.org/pump-fundamentals/combined.html). Describe el punto de operación como intersección de curvas.
- [Hydraulic Institute: curvas del sistema](https://datatool.pumps.org/pump-fundamentals/sys-curves). Explica la contribución de altura estática, presión y fricción.
- [Grundfos: cómo obtener una curva de bomba](https://www.grundfos.com/us/support/how-to-guides/how-to-get-a-pump-curve-quickly). Muestra la búsqueda de curvas por producto y modelo.
- [EPA: manual de EPANET 2.2](https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=P10113EM.TXT). Documenta las propiedades de tuberías y bombas que requiere un modelo hidráulico y el carácter empírico de la rugosidad.
- [NIST: factores de conversión](https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8). Distingue el galón estadounidense del imperial y documenta la conversión de GPM.

La descripción del cálculo vigente y sus supuestos detallados están en [DOCUMENTO_PROYECTO.md](DOCUMENTO_PROYECTO.md). Este documento define las necesidades y el comportamiento esperado del producto; no sustituye la explicación matemática.
