# PumpCalc

Aplicación de escritorio para estimar el punto de operación de **una bomba, una tubería de diámetro constante y agua** con el tanque casi vacío y casi lleno. Compara los dos caudales estimados con una meta y permite guardar escenarios locales.

## Instalación y ejecución

El entorno `.venv` ya está creado **en esta carpeta**, con CustomTkinter instalado. Desde Git Bash, activa y ejecuta:

```bash
source .venv/Scripts/activate
python main.py
```

Desde PowerShell, la activación equivalente es `.\.venv\Scripts\Activate.ps1`.

Para recrear el entorno en este equipo, usa la instalación funcional de Python 3.13 (la instalación de Python 3.14 que aparece primero en `PATH` no tiene su biblioteca estándar):

```powershell
& 'C:\Users\Juan Manuel\AppData\Local\Programs\Python\Python313\python.exe' -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

## Datos y resultados

- Instalación: meta (m³/h), longitud (m), diámetro interior (mm), material, dos desniveles (m), posición de la bomba respecto a la fuente y cantidades de accesorios.
- Bomba: puntos de caudal y altura (m) en filas separadas. La unidad de caudal puede ser m³/h, L/min o US gpm. Los caudales deben aumentar y las alturas disminuir o mantenerse. Fabricante, modelo y referencia son datos opcionales para identificar la curva; no intervienen en el cálculo.
- Resultados: caudal y altura de operación, velocidad, pérdidas y curvas para cada condición. Si no hay intersección dentro del intervalo dado, se informa sin extrapolar. La succión no se evalúa.

La barra lateral lleva directamente a **Instalación**, **Curva de bomba**, **Resultados** y **Escenarios**. El formulario agrupa los datos por secciones y deja el contexto opcional plegado. Se pueden guardar borradores incompletos, abrirlos, duplicarlos y comparar dos escenarios. Los cálculos se marcan como desactualizados cuando cambian sus entradas. La base de datos local `pumpcalc_data.sqlite3` se crea junto a `main.py` y se excluye de Git. Los valores precargados son **datos de demostración**, no mediciones de una finca.

## Modelo y alcance

El módulo [`pumpcalc/hydraulics.py`](pumpcalc/hydraulics.py) no tiene importaciones. Calcula la pérdida de tubería con Hazen–Williams en unidades SI:

`h_f = 10.67 · L · Q^1.852 / (C^1.852 · D^4.871)`

Las pérdidas de accesorios son `ΣK · v² / (2g)`. Los coeficientes iniciales son: PVC `C=150`, acero `C=120`, hierro fundido `C=100`; codo de 90° `K=0.9`, compuerta abierta `K=0.15` y retención `K=2.5`. Son valores aproximados para esta primera versión. La curva de la bomba se interpola linealmente entre los pares introducidos. El cruce de las curvas se obtiene mediante bisección en el segmento que cambia de signo.

El modelo supone tubería llena, agua, flujo estacionario y una única línea principal. No considera redes ramificadas, varias bombas, transitorios ni cambios de diámetro. Es una estimación académica; los coeficientes y la curva deben corresponder a la instalación real para usar el resultado en una decisión técnica.

## Documentos de evolución

- [Necesidad y requisitos del producto](NECESIDAD_Y_REQUERIMIENTOS.md): usuario principal de la finca, recorrido, funciones actuales y propuestas, e historias de usuario.
- [Caso de finca y validación](CASO_FINCA_Y_VALIDACION.md): interpretación de las dos condiciones del tanque, límites del modelo y datos pendientes para contrastarlo con una finca real.

Los documentos de evolución se redactaron antes de esta implementación. Sus columnas de «estado actual» describen la línea base previa; este README describe la funcionalidad presente. La validación de campo y la alerta de velocidad elevada siguen pendientes.
