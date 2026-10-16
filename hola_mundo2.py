"""
Riuada de nassos - Juego solidario para la campaña #Riuadadenassos
a favor de Pallapupas (payasos de hospital).

Cómo jugar: haz clic en las narices rojas antes de que lleguen abajo.
Cada nariz atrapada = 1 rialla (risa). Tienes 30 segundos.

Requisitos: Python 3 (tkinter viene incluido).
Ejecutar:   python riuada_de_nassos.py
"""

import random
import tkinter as tk

# ---------- Ajustes fáciles de cambiar ----------
ANCHO, ALTO = 600, 450
DURACION = 30            # segundos de partida
PROB_NARIZ = 0.06        # probabilidad de que aparezca una nariz en cada "tick"
TICK_MS = 30             # milisegundos entre cada actualización
COLOR_FONDO = "#FFF4D6"
COLOR_NARIZ = "#E3201B"
HASHTAG = "#Riuadadenassos"
MENSAJE_FINAL = "Cada rialla compta! Ajuda els Pallapupas a seguir portant somriures als hospitals."


class Juego:
    def __init__(self, root):
        self.root = root
        root.title(f"Riuada de nassos {HASHTAG}")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=ANCHO, height=ALTO,
                                bg=COLOR_FONDO, highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.al_hacer_clic)

        self.jugando = False
        self.pantalla_inicio()

    # ---------- Pantallas ----------
    def pantalla_inicio(self):
        self.canvas.delete("all")
        self.canvas.create_text(ANCHO / 2, 110, text="Riuada de nassos",
                                font=("Helvetica", 34, "bold"), fill=COLOR_NARIZ)
        self.canvas.create_text(ANCHO / 2, 160, text=HASHTAG,
                                font=("Helvetica", 16), fill="#444")
        self.canvas.create_text(
            ANCHO / 2, 230,
            text="Atrapa todos los narices que puedas\nantes de que se acabe el tiempo.",
            font=("Helvetica", 14), fill="#333", justify="center")
        self.dibujar_nariz(ANCHO / 2, 310, 30)
        self.boton_texto("Començar!", ANCHO / 2, 385, self.empezar)

    def pantalla_final(self):
        self.jugando = False
        self.canvas.delete("all")
        self.canvas.create_text(ANCHO / 2, 90, text="Temps!",
                                font=("Helvetica", 32, "bold"), fill=COLOR_NARIZ)
        self.canvas.create_text(ANCHO / 2, 160,
                                text=f"Has aconseguit {self.puntos} rialles",
                                font=("Helvetica", 20, "bold"), fill="#222")
        self.canvas.create_text(ANCHO / 2, 235, text=MENSAJE_FINAL,
                                font=("Helvetica", 13), fill="#333",
                                width=ANCHO - 100, justify="center")
        self.canvas.create_text(ANCHO / 2, 300, text=HASHTAG,
                                font=("Helvetica", 18, "bold"), fill=COLOR_NARIZ)
        self.boton_texto("Tornar a jugar", ANCHO / 2, 380, self.empezar)

    def boton_texto(self, texto, x, y, accion):
        """Botón sencillo dibujado en el canvas."""
        rect = self.canvas.create_rectangle(x - 90, y - 24, x + 90, y + 24,
                                            fill=COLOR_NARIZ, outline="")
        label = self.canvas.create_text(x, y, text=texto, fill="white",
                                        font=("Helvetica", 15, "bold"))
        for item in (rect, label):
            self.canvas.tag_bind(item, "<Button-1>", lambda e: accion())

    # ---------- Lógica del juego ----------
    def empezar(self):
        self.canvas.delete("all")
        self.puntos = 0
        self.tiempo_restante = DURACION
        self.jugando = True
        self.marcador = self.canvas.create_text(
            10, 10, anchor="nw", font=("Helvetica", 16, "bold"), fill="#222")
        self.cronometro = self.canvas.create_text(
            ANCHO - 10, 10, anchor="ne", font=("Helvetica", 16, "bold"), fill="#222")
        self.actualizar_marcadores()
        self.cuenta_atras()
        self.bucle()

    def cuenta_atras(self):
        if not self.jugando:
            return
        if self.tiempo_restante <= 0:
            self.pantalla_final()
            return
        self.actualizar_marcadores()
        self.tiempo_restante -= 1
        self.root.after(1000, self.cuenta_atras)

    def actualizar_marcadores(self):
        self.canvas.itemconfig(self.marcador, text=f"Rialles: {self.puntos}")
        self.canvas.itemconfig(self.cronometro, text=f"Temps: {self.tiempo_restante}s")

    def dibujar_nariz(self, x, y, r):
        """Dibuja una nariz de payaso (círculo rojo con brillo). Devuelve sus ids."""
        cuerpo = self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                         fill=COLOR_NARIZ, outline="#9B1410", width=2,
                                         tags="nariz")
        brillo = self.canvas.create_oval(x - r * 0.5, y - r * 0.6,
                                         x - r * 0.1, y - r * 0.2,
                                         fill="#FFB3B0", outline="", tags="nariz")
        return cuerpo, brillo

    def nueva_nariz(self):
        r = random.randint(18, 32)
        x = random.randint(r, ANCHO - r)
        cuerpo, brillo = self.dibujar_nariz(x, -r, r)
        velocidad = random.uniform(2, 5)
        # Guardamos la velocidad en una etiqueta propia de cada nariz
        self.canvas.addtag_withtag(f"vel:{velocidad:.2f}", cuerpo)
        self.canvas.addtag_withtag(f"par:{brillo}", cuerpo)

    def bucle(self):
        if not self.jugando:
            return

        if random.random() < PROB_NARIZ:
            self.nueva_nariz()

        # Mover las narices y borrar las que salen por abajo
        for cuerpo in self.canvas.find_withtag("nariz"):
            etiquetas = self.canvas.gettags(cuerpo)
            vel = next((float(t[4:]) for t in etiquetas if t.startswith("vel:")), None)
            if vel is None:
                continue  # es un brillo; se mueve junto a su nariz
            par = next(int(t[4:]) for t in etiquetas if t.startswith("par:"))
            self.canvas.move(cuerpo, 0, vel)
            self.canvas.move(par, 0, vel)
            if self.canvas.coords(cuerpo)[1] > ALTO:
                self.canvas.delete(cuerpo)
                self.canvas.delete(par)

        self.root.after(TICK_MS, self.bucle)

    def al_hacer_clic(self, evento):
        if not self.jugando:
            return
        # Buscar la nariz que está bajo el cursor
        for item in reversed(self.canvas.find_overlapping(
                evento.x, evento.y, evento.x, evento.y)):
            etiquetas = self.canvas.gettags(item)
            if "nariz" not in etiquetas:
                continue
            if any(t.startswith("par:") for t in etiquetas):
                cuerpo = item
                par = next(int(t[4:]) for t in etiquetas if t.startswith("par:"))
            else:
                # Se hizo clic en el brillo: localizar su nariz
                cuerpo = next((c for c in self.canvas.find_withtag("nariz")
                               if f"par:{item}" in self.canvas.gettags(c)), None)
                if cuerpo is None:
                    continue
                par = item
            self.canvas.delete(cuerpo)
            self.canvas.delete(par)
            self.puntos += 1
            self.actualizar_marcadores()
            break


if __name__ == "__main__":
    ventana = tk.Tk()
    Juego(ventana)
    ventana.mainloop()