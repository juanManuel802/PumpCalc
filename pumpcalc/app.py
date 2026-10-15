"""Interfaz de una sola ventana para PumpCalc."""

import tkinter as tk

import customtkinter as ctk

from pumpcalc.hydraulics import altura_bomba, altura_instalacion, punto_operacion


MATERIALES = {"PVC": 150, "Acero": 120, "Hierro fundido": 100}
ACCESORIOS = {
    "Codos de 90°": 0.9,
    "Válvulas de compuerta abiertas": 0.15,
    "Válvulas de retención": 2.5,
}


class PumpCalcApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("PumpCalc | Métodos numéricos")
        self.geometry("1100x760")
        self.minsize(980, 680)
        self.configure(fg_color="#f3f7fb")

        self.resultado = None
        self.resultado_anterior = None
        self.datos = None
        self.paginas = {}
        self.botones = {}

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._crear_menu()
        self._crear_contenido()
        self.mostrar_pagina("Instalación")

    def _crear_menu(self):
        menu = ctk.CTkFrame(self, width=215, corner_radius=0, fg_color="#10243a")
        menu.grid(row=0, column=0, sticky="nsew")
        menu.grid_propagate(False)
        menu.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            menu, text="PumpCalc", font=ctk.CTkFont(size=26, weight="bold"),
            text_color="white", anchor="w"
        ).grid(row=0, column=0, sticky="ew", padx=24, pady=(34, 2))
        ctk.CTkLabel(
            menu, text="Agua · una línea · una bomba", text_color="#a9bed1",
            font=ctk.CTkFont(size=12), anchor="w"
        ).grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 34))

        for fila, nombre in enumerate(("Instalación", "Curva de bomba", "Resultados"), 2):
            boton = ctk.CTkButton(
                menu, text=nombre, anchor="w", height=44, corner_radius=8,
                fg_color="transparent", hover_color="#1d3c5b",
                text_color="#d7e5f0", font=ctk.CTkFont(size=14),
                command=lambda pagina=nombre: self.mostrar_pagina(pagina)
            )
            boton.grid(row=fila, column=0, sticky="ew", padx=14, pady=4)
            self.botones[nombre] = boton

        ctk.CTkButton(
            menu, text="Calcular", height=46, corner_radius=8,
            fg_color="#19a888", hover_color="#148e73",
            font=ctk.CTkFont(size=15, weight="bold"), command=self.calcular
        ).grid(row=6, column=0, sticky="ew", padx=16, pady=(28, 8))
        self.mensaje = ctk.CTkLabel(
            menu, text="", wraplength=178, justify="left", text_color="#f7c4b8",
            font=ctk.CTkFont(size=12)
        )
        self.mensaje.grid(row=7, column=0, sticky="ew", padx=19, pady=5)

    def _crear_contenido(self):
        contenedor = ctk.CTkFrame(self, fg_color="transparent")
        contenedor.grid(row=0, column=1, sticky="nsew", padx=24, pady=22)
        contenedor.grid_columnconfigure(0, weight=1)
        contenedor.grid_rowconfigure(0, weight=1)

        for nombre in ("Instalación", "Curva de bomba", "Resultados"):
            pagina = ctk.CTkFrame(contenedor, fg_color="transparent")
            pagina.grid(row=0, column=0, sticky="nsew")
            self.paginas[nombre] = pagina

        self._pagina_instalacion(self.paginas["Instalación"])
        self._pagina_bomba(self.paginas["Curva de bomba"])
        self._pagina_resultados(self.paginas["Resultados"])

    def mostrar_pagina(self, nombre):
        self.paginas[nombre].tkraise()
        for titulo, boton in self.botones.items():
            boton.configure(
                fg_color="#1b4966" if titulo == nombre else "transparent",
                text_color="white" if titulo == nombre else "#d7e5f0",
            )

    def _titulo(self, parent, titulo, subtitulo):
        ctk.CTkLabel(
            parent, text=titulo, font=ctk.CTkFont(size=27, weight="bold"),
            text_color="#142b40", anchor="w"
        ).pack(fill="x", pady=(0, 3))
        ctk.CTkLabel(
            parent, text=subtitulo, font=ctk.CTkFont(size=13),
            text_color="#5b7183", anchor="w", wraplength=770, justify="left"
        ).pack(fill="x", pady=(0, 22))

    def _campo(self, parent, texto, valor, fila, columna=0):
        caja = ctk.CTkFrame(parent, fg_color="transparent")
        caja.grid(row=fila, column=columna, sticky="ew", padx=(0, 20), pady=(0, 16))
        ctk.CTkLabel(
            caja, text=texto, text_color="#324b60", anchor="w",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(fill="x", pady=(0, 6))
        entrada = ctk.CTkEntry(caja, height=38, border_color="#c6d5df")
        entrada.insert(0, valor)
        entrada.pack(fill="x")
        return entrada

    def _pagina_instalacion(self, pagina):
        self._titulo(
            pagina, "Instalación", "Introduce los datos de una sola tubería y sus accesorios principales."
        )
        tarjeta = ctk.CTkFrame(pagina, fg_color="white", corner_radius=14)
        tarjeta.pack(fill="x")
        interior = ctk.CTkFrame(tarjeta, fg_color="transparent")
        interior.pack(fill="x", padx=24, pady=24)
        interior.grid_columnconfigure((0, 1), weight=1)

        self.longitud = self._campo(interior, "Longitud de tubería (m)", "40", 0, 0)
        self.diametro = self._campo(interior, "Diámetro interior (mm)", "32", 0, 1)
        self.desnivel = self._campo(interior, "Desnivel vertical (m)", "12", 1, 0)

        material_caja = ctk.CTkFrame(interior, fg_color="transparent")
        material_caja.grid(row=1, column=1, sticky="ew", padx=(0, 20), pady=(0, 16))
        ctk.CTkLabel(
            material_caja, text="Material", text_color="#324b60", anchor="w",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(fill="x", pady=(0, 6))
        self.material = ctk.CTkOptionMenu(
            material_caja, values=list(MATERIALES), height=38,
            fg_color="#e7f0f5", button_color="#d3e4ee", button_hover_color="#bed8e7",
            text_color="#17374c"
        )
        self.material.pack(fill="x")
        self.material.set("PVC")

        ctk.CTkLabel(
            interior, text="Accesorios", text_color="#1b394f", anchor="w",
            font=ctk.CTkFont(size=17, weight="bold")
        ).grid(row=2, column=0, columnspan=2, sticky="ew", pady=(6, 14))
        self.accesorios = {}
        for indice, (nombre, k) in enumerate(ACCESORIOS.items()):
            valor = "2" if indice == 0 else "1"
            self.accesorios[nombre] = self._campo(
                interior, f"{nombre}  (K = {k:g} por unidad)", valor,
                3 + indice // 2, indice % 2
            )

        ctk.CTkLabel(
            pagina,
            text="Modelo: agua en tubería llena, flujo estacionario y un solo diámetro por cálculo.",
            text_color="#5b7183", anchor="w", font=ctk.CTkFont(size=12)
        ).pack(fill="x", pady=18)

    def _pagina_bomba(self, pagina):
        self._titulo(
            pagina, "Curva de bomba",
            "Escribe pares de la ficha técnica: caudal (m³/h); altura (m). Un par por línea, ordenado por caudal."
        )
        tarjeta = ctk.CTkFrame(pagina, fg_color="white", corner_radius=14)
        tarjeta.pack(fill="both", expand=True)
        ctk.CTkLabel(
            tarjeta, text="Puntos del fabricante", text_color="#1b394f", anchor="w",
            font=ctk.CTkFont(size=17, weight="bold")
        ).pack(fill="x", padx=24, pady=(24, 8))
        self.puntos_texto = ctk.CTkTextbox(
            tarjeta, height=260, font=ctk.CTkFont(family="Consolas", size=15),
            border_width=1, border_color="#c6d5df"
        )
        self.puntos_texto.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        self.puntos_texto.insert("1.0", "0; 38\n2; 35\n4; 29\n6; 19\n8; 5")
        ctk.CTkLabel(
            tarjeta,
            text="La altura se interpola entre estos puntos. No se estima el comportamiento fuera de este intervalo.",
            text_color="#5b7183", anchor="w", wraplength=700, justify="left"
        ).pack(fill="x", padx=24, pady=(0, 24))

    def _pagina_resultados(self, pagina):
        self._titulo(
            pagina, "Resultados", "El punto de operación es la intersección de las curvas."
        )
        self.resumen = ctk.CTkLabel(
            pagina, text="Completa los datos y pulsa Calcular.",
            font=ctk.CTkFont(size=18, weight="bold"), text_color="#153d56",
            anchor="w", justify="left", wraplength=760
        )
        self.resumen.pack(fill="x", pady=(0, 5))
        self.detalle = ctk.CTkLabel(
            pagina, text="", font=ctk.CTkFont(size=13), text_color="#526b7e",
            anchor="w", justify="left", wraplength=760
        )
        self.detalle.pack(fill="x", pady=(0, 14))
        self.comparacion = ctk.CTkLabel(
            pagina, text="", font=ctk.CTkFont(size=12), text_color="#147d70",
            anchor="w", justify="left", wraplength=760
        )
        self.comparacion.pack(fill="x", pady=(0, 10))

        grafica_tarjeta = ctk.CTkFrame(pagina, fg_color="white", corner_radius=14)
        grafica_tarjeta.pack(fill="both", expand=True)
        self.grafica = tk.Canvas(
            grafica_tarjeta, bg="white", highlightthickness=0, height=390
        )
        self.grafica.pack(fill="both", expand=True, padx=15, pady=12)
        self.grafica.bind("<Configure>", lambda _evento: self._dibujar_grafica())

    def _leer_datos(self):
        def numero(entrada):
            return float(entrada.get().strip().replace(",", "."))

        longitud = numero(self.longitud)
        diametro = numero(self.diametro)
        desnivel = numero(self.desnivel)
        if longitud <= 0 or diametro <= 0 or desnivel < 0:
            raise ValueError("Longitud y diámetro deben ser positivos; el desnivel no puede ser negativo.")

        suma_k = 0.0
        for nombre, entrada in self.accesorios.items():
            cantidad = int(entrada.get().strip())
            if cantidad < 0:
                raise ValueError("Las cantidades de accesorios no pueden ser negativas.")
            suma_k += cantidad * ACCESORIOS[nombre]

        puntos = []
        for linea in self.puntos_texto.get("1.0", "end").splitlines():
            if linea.strip():
                partes = linea.split(";")
                if len(partes) != 2:
                    raise ValueError("Cada punto de bomba debe tener el formato caudal; altura.")
                puntos.append(tuple(float(valor.strip().replace(",", ".")) for valor in partes))
        if len(puntos) < 2:
            raise ValueError("Introduce al menos dos puntos de la curva de bomba.")
        if any(q < 0 or h < 0 for q, h in puntos):
            raise ValueError("Los puntos de bomba no pueden ser negativos.")
        if any(puntos[i + 1][0] <= puntos[i][0] or puntos[i + 1][1] > puntos[i][1]
               for i in range(len(puntos) - 1)):
            raise ValueError("Ordena los puntos por caudal creciente y altura no creciente.")

        return {
            "longitud_m": longitud,
            "diametro_mm": diametro,
            "coeficiente_c": MATERIALES[self.material.get()],
            "desnivel_m": desnivel,
            "suma_k": suma_k,
            "puntos": puntos,
        }

    def calcular(self):
        try:
            datos = self._leer_datos()
        except ValueError as error:
            self.mensaje.configure(text=str(error))
            return

        self.mensaje.configure(text="")
        self.resultado_anterior = self.resultado
        self.datos = datos
        self.resultado = punto_operacion(
            datos["puntos"], datos["longitud_m"], datos["diametro_mm"],
            datos["coeficiente_c"], datos["desnivel_m"], datos["suma_k"]
        )

        if self.resultado is None:
            self.resumen.configure(text="No se encontró un punto de operación en la curva suministrada.")
            self.detalle.configure(text="Revisa los datos o introduce más puntos de la curva del fabricante.")
        else:
            r = self.resultado
            self.resumen.configure(
                text=f"Caudal de operación: {r['caudal_m3h']:.3f} m³/h    ·    Altura: {r['total_m']:.2f} m"
            )
            self.detalle.configure(
                text=(f"Velocidad: {r['velocidad_ms']:.2f} m/s    ·    "
                      f"Pérdida en tubería: {r['tuberia_m']:.2f} m    ·    "
                      f"Pérdida en accesorios: {r['accesorios_m']:.2f} m    ·    "
                      f"Desnivel: {datos['desnivel_m']:.2f} m")
            )

        if self.resultado_anterior is not None:
            anterior = self.resultado_anterior
            self.comparacion.configure(
                text=f"Cálculo anterior: {anterior['caudal_m3h']:.3f} m³/h y {anterior['total_m']:.2f} m."
            )
        else:
            self.comparacion.configure(text="")

        self.mostrar_pagina("Resultados")
        self._dibujar_grafica()

    def _dibujar_grafica(self):
        lienzo = self.grafica
        lienzo.delete("all")
        if self.datos is None:
            return
        ancho = max(lienzo.winfo_width(), 500)
        alto = max(lienzo.winfo_height(), 300)
        izquierda, derecha, arriba, abajo = 72, 24, 28, 58
        x0, x1 = izquierda, ancho - derecha
        y0, y1 = arriba, alto - abajo
        datos = self.datos
        puntos = datos["puntos"]
        q_min, q_max = puntos[0][0], puntos[-1][0]

        def sistema(q):
            return altura_instalacion(
                q, datos["longitud_m"], datos["diametro_mm"],
                datos["coeficiente_c"], datos["desnivel_m"], datos["suma_k"]
            )["total_m"]

        h_max = max(max(h for _, h in puntos), sistema(q_max), 1.0) * 1.1

        def x(q):
            return x0 + (q - q_min) * (x1 - x0) / (q_max - q_min)

        def y(h):
            return y1 - h * (y1 - y0) / h_max

        for indice in range(6):
            altura = h_max * indice / 5
            yy = y(altura)
            lienzo.create_line(x0, yy, x1, yy, fill="#e6edf2")
            lienzo.create_text(x0 - 10, yy, text=f"{altura:.0f}", anchor="e", fill="#64798b", font=("Arial", 10))
            caudal = q_min + (q_max - q_min) * indice / 5
            xx = x(caudal)
            lienzo.create_line(xx, y0, xx, y1, fill="#eef2f5")
            lienzo.create_text(xx, y1 + 15, text=f"{caudal:.1f}", fill="#64798b", font=("Arial", 10))

        lienzo.create_line(x0, y0, x0, y1, fill="#7f93a3", width=1)
        lienzo.create_line(x0, y1, x1, y1, fill="#7f93a3", width=1)
        lienzo.create_text((x0 + x1) / 2, alto - 15, text="Caudal (m³/h)", fill="#324b60", font=("Arial", 11))
        lienzo.create_text(20, (y0 + y1) / 2, text="Altura (m)", angle=90, fill="#324b60", font=("Arial", 11))

        for indice in range(len(puntos) - 1):
            q_a, h_a = puntos[indice]
            q_b, h_b = puntos[indice + 1]
            lienzo.create_line(x(q_a), y(h_a), x(q_b), y(h_b), fill="#1673b1", width=3)
        for q, h in puntos:
            radio = 4
            lienzo.create_oval(x(q) - radio, y(h) - radio, x(q) + radio, y(h) + radio,
                               fill="#1673b1", outline="white")

        anterior_q = q_min
        anterior_h = sistema(q_min)
        for indice in range(1, 121):
            q = q_min + (q_max - q_min) * indice / 120
            h = sistema(q)
            lienzo.create_line(x(anterior_q), y(anterior_h), x(q), y(h), fill="#e28c3f", width=3)
            anterior_q, anterior_h = q, h

        lienzo.create_line(x1 - 180, y0 + 5, x1 - 155, y0 + 5, fill="#1673b1", width=3)
        lienzo.create_text(x1 - 148, y0 + 5, text="Bomba", anchor="w", fill="#324b60", font=("Arial", 10))
        lienzo.create_line(x1 - 180, y0 + 24, x1 - 155, y0 + 24, fill="#e28c3f", width=3)
        lienzo.create_text(x1 - 148, y0 + 24, text="Instalación", anchor="w", fill="#324b60", font=("Arial", 10))

        if self.resultado is not None:
            q = self.resultado["caudal_m3h"]
            h = self.resultado["total_m"]
            lienzo.create_oval(x(q) - 7, y(h) - 7, x(q) + 7, y(h) + 7,
                               fill="#19a888", outline="white", width=2)
            lienzo.create_text(x(q) + 10, y(h) - 12, text="Punto de operación",
                               anchor="w", fill="#147d70", font=("Arial", 10, "bold"))
