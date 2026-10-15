# PumpCalc — primera versión

Aplicación de escritorio para estimar el punto de operación de **una bomba, una tubería de diámetro constante y agua**. La ventana tiene un menú lateral para introducir la instalación y la curva de la bomba, y ver el resultado con ambas curvas.

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

- Instalación: longitud (m), diámetro interior (mm), material, desnivel (m) y cantidades de codos de 90°, válvulas de compuerta abiertas y válvulas de retención.
- Bomba: pares de caudal (m³/h) y altura (m), un par por línea, separados por `;`. Los caudales deben aumentar y las alturas disminuir o mantenerse.
- Resultados: caudal y altura de operación, velocidad del agua, pérdida en la tubería y pérdida en accesorios. Si no hay intersección dentro del intervalo dado para la bomba, se informa sin extrapolar.

La comparación inicial consiste en cambiar los datos y recalcular. Se muestra el resultado anterior para facilitar la comparación inmediata. No se guardan configuraciones.

## Modelo y alcance

El módulo [`pumpcalc/hydraulics.py`](pumpcalc/hydraulics.py) no tiene importaciones. Calcula la pérdida de tubería con Hazen–Williams en unidades SI:

`h_f = 10.67 · L · Q^1.852 / (C^1.852 · D^4.871)`

Las pérdidas de accesorios son `ΣK · v² / (2g)`. Los coeficientes iniciales son: PVC `C=150`, acero `C=120`, hierro fundido `C=100`; codo de 90° `K=0.9`, compuerta abierta `K=0.15` y retención `K=2.5`. Son valores aproximados para esta primera versión. La curva de la bomba se interpola linealmente entre los pares introducidos. El cruce de las curvas se obtiene mediante bisección en el segmento que cambia de signo.

El modelo supone tubería llena, agua, flujo estacionario y una única línea principal. No considera redes ramificadas, varias bombas, transitorios ni cambios de diámetro. Es una estimación académica; los coeficientes y la curva deben corresponder a la instalación real para usar el resultado en una decisión técnica.
