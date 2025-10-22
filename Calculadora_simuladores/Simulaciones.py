import tkinter as tk
from tkinter import ttk
import numpy as np
import random
import threading
import time
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.colors

# ==================== CLASES DE SIMULACIÓN ====================
class GameOfLife2D:
    def __init__(self, rows=50, cols=50):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)

    def randomize(self, p=0.2):
        self.grid = (np.random.random((self.rows, self.cols)) < p).astype(int)

    def step(self):
        new = np.zeros_like(self.grid)
        for r in range(self.rows):
            for c in range(self.cols):
                total = np.sum(self.grid[max(0, r-1):r+2, max(0, c-1):c+2]) - self.grid[r, c]
                if self.grid[r, c] == 1:
                    if total in (2, 3):
                        new[r, c] = 1
                else:
                    if total == 3:
                        new[r, c] = 1
        self.grid = new

class GameOfLife1D:
    def __init__(self, length=200, rule=30):
        self.length = length
        self.rule = rule
        self.rule_map = self._rule_to_map(rule)
        self.state = np.zeros(length, dtype=int)
        self.state[length // 2] = 1

    def _rule_to_map(self, rule):
        bits = [(rule >> i) & 1 for i in range(8)]
        triplets = [(1,1,1),(1,1,0),(1,0,1),(1,0,0),(0,1,1),(0,1,0),(0,0,1),(0,0,0)]
        return {triplets[i]: bits[7-i] for i in range(8)}

    def step(self):
        new = np.zeros_like(self.state)
        for i in range(self.length):
            left = self.state[(i-1) % self.length]
            center = self.state[i]
            right = self.state[(i+1) % self.length]
            new[i] = self.rule_map[(left, center, right)]
        self.state = new

    def reset(self):
        self.state = np.zeros(self.length, dtype=int)
        self.state[self.length // 2] = 1

class CovidSimulation:
    def __init__(self, rows=60, cols=60, init_infected=5, p_infect=0.3, p_recover=0.02, p_die=0.005):
        self.rows = rows
        self.cols = cols
        self.grid = np.ones((rows, cols), dtype=int)  # 1 = susceptible
        self.t = 0
        self.p_infect = p_infect
        self.p_recover = p_recover
        self.p_die = p_die
        for _ in range(init_infected):
            r = random.randrange(rows)
            c = random.randrange(cols)
            self.grid[r, c] = 2  # infected

    def step(self):
        new = self.grid.copy()
        for r in range(self.rows):
            for c in range(self.cols):
                state = self.grid[r, c]
                if state == 1:  # susceptible
                    neigh = self.grid[max(0, r-1):r+2, max(0, c-1):c+2]
                    infected_neighbors = np.sum(neigh == 2)
                    if infected_neighbors > 0:
                        p = 1 - ((1 - self.p_infect) ** infected_neighbors)
                        if random.random() < p:
                            new[r, c] = 2
                elif state == 2:  # infected
                    if random.random() < self.p_die:
                        new[r, c] = 4  # dead
                    elif random.random() < self.p_recover:
                        new[r, c] = 3  # recovered
        self.grid = new
        self.t += 1

    def counts(self):
        unique, counts = np.unique(self.grid, return_counts=True)
        d = {0:0, 1:0, 2:0, 3:0, 4:0}
        for u, c in zip(unique, counts):
            d[int(u)] = int(c)
        return d

# ==================== INTERFAZ PRINCIPAL ====================
class AppSimulaciones:
    def __init__(self, root):
        self.root = root
        root.title('Simulaciones: Juego de la Vida + COVID-19')
        root.geometry('1100x700')
        root.configure(bg='#e0f7ff')

        # Estilo azul/celeste
        style = ttk.Style()
        style.theme_use('clam')
        bg_color = '#e0f7ff'
        btn_color = '#87ceeb'
        btn_active = '#00bfff'
        text_color = '#003366'

        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=text_color, font=("Arial", 10))
        style.configure("TButton",
                        background=btn_color,
                        foreground="black",
                        font=("Arial", 10, "bold"),
                        padding=6)
        style.map("TButton",
                  background=[("active", btn_active)],
                  foreground=[("active", "white")])
        style.configure("TNotebook", background=bg_color, borderwidth=0)
        style.configure("TNotebook.Tab",
                        background=btn_color,
                        foreground=text_color,
                        padding=[12, 6],
                        font=("Arial", 10, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", btn_active)],
                  foreground=[("selected", "white")])
        style.configure("TEntry", fieldbackground="white", foreground="black")

        self.nb = ttk.Notebook(root)
        self.nb.pack(fill='both', expand=True, padx=10, pady=10)

        self._build_gameoflife_tab()
        self._build_gameoflife1d_tab()
        self._build_covid_tab()

    # ---------------- Juego de la Vida 2D ----------------
    def _build_gameoflife_tab(self):
        tab = ttk.Frame(self.nb)
        self.nb.add(tab, text='Juego de la Vida Variable')

        left = ttk.Frame(tab)
        left.pack(side='left', fill='y', padx=10, pady=10)
        right = ttk.Frame(tab)
        right.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        self.g2_rows = tk.IntVar(value=50)
        self.g2_cols = tk.IntVar(value=50)
        self.g2_p = tk.DoubleVar(value=0.2)

        ttk.Label(left, text='Filas:').pack(anchor='w', pady=(0,5))
        ttk.Entry(left, textvariable=self.g2_rows).pack(fill='x', pady=(0,10))
        ttk.Label(left, text='Columnas:').pack(anchor='w', pady=(0,5))
        ttk.Entry(left, textvariable=self.g2_cols).pack(fill='x', pady=(0,10))
        ttk.Label(left, text='Prob. inicial:').pack(anchor='w', pady=(0,5))
        ttk.Entry(left, textvariable=self.g2_p).pack(fill='x', pady=(0,10))

        ttk.Button(left, text='Crear aleatorio', command=self._g2_create_random).pack(fill='x', pady=5)
        ttk.Button(left, text='Paso', command=self._g2_step).pack(fill='x', pady=5)
        ttk.Button(left, text='Ejecutar/Parar', command=self._g2_toggle_run).pack(fill='x', pady=5)
        ttk.Button(left, text='Limpiar', command=self._g2_clear).pack(fill='x', pady=5)

        fig = Figure(figsize=(6,6), facecolor='#e0f7ff')
        self.g2_ax = fig.add_subplot(111)
        self.g2_ax.set_facecolor('#e0f7ff')
        self.g2_canvas = FigureCanvasTkAgg(fig, master=right)
        self.g2_canvas.get_tk_widget().pack(fill='both', expand=True)

        self.g2 = None
        self.g2_running = False

    def _g2_create_random(self):
        try:
            rows = max(5, int(self.g2_rows.get()))
            cols = max(5, int(self.g2_cols.get()))
            p = float(self.g2_p.get())
            self.g2 = GameOfLife2D(rows=rows, cols=cols)
            self.g2.randomize(p=p)
            self._g2_draw()
        except Exception as e:
            print(f"Error en Juego 2D: {e}")

    def _g2_draw(self):
        self.g2_ax.clear()
        self.g2_ax.set_facecolor('#e0f7ff')
        cmap = matplotlib.colors.ListedColormap(['white', 'black'])
        self.g2_ax.imshow(self.g2.grid, cmap=cmap, interpolation='nearest')
        self.g2_ax.set_title('Juego de la Vida Variable', color='#003366')
        self.g2_canvas.draw()

    def _g2_step(self):
        if self.g2 is None:
            self._g2_create_random()
        self.g2.step()
        self._g2_draw()

    def _g2_toggle_run(self):
        self.g2_running = not self.g2_running
        if self.g2_running:
            self._g2_run_loop()

    def _g2_run_loop(self):
        def loop():
            while self.g2_running:
                time.sleep(0.1)
                self.root.after(0, self._g2_step)
        threading.Thread(target=loop, daemon=True).start()

    def _g2_clear(self):
        if self.g2:
            self.g2.grid.fill(0)
            self._g2_draw()

    # ---------------- Juego de la Vida 1D ----------------
    def _build_gameoflife1d_tab(self):
        tab = ttk.Frame(self.nb)
        self.nb.add(tab, text='Juego de la Vida Reglas de Conway')

        left = ttk.Frame(tab)
        left.pack(side='left', fill='y', padx=10, pady=10)
        right = ttk.Frame(tab)
        right.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        self.g1_length = tk.IntVar(value=300)
        self.g1_rule = tk.IntVar(value=30)

        ttk.Label(left, text='Longitud:').pack(anchor='w', pady=(0,5))
        ttk.Entry(left, textvariable=self.g1_length).pack(fill='x', pady=(0,10))
        ttk.Label(left, text='Regla (0-255):').pack(anchor='w', pady=(0,5))
        ttk.Entry(left, textvariable=self.g1_rule).pack(fill='x', pady=(0,10))

        ttk.Button(left, text='Crear', command=self._g1_create).pack(fill='x', pady=5)
        ttk.Button(left, text='Siguiente', command=self._g1_step).pack(fill='x', pady=5)
        ttk.Button(left, text='Ejecutar/Parar', command=self._g1_toggle_run).pack(fill='x', pady=5)
        ttk.Button(left, text='Limpiar', command=self._g1_clear).pack(fill='x', pady=5)

        fig = Figure(figsize=(8,5), facecolor='#e0f7ff')
        self.g1_ax = fig.add_subplot(111)
        self.g1_ax.set_facecolor('#e0f7ff')
        self.g1_canvas = FigureCanvasTkAgg(fig, master=right)
        self.g1_canvas.get_tk_widget().pack(fill='both', expand=True)

        self.g1 = None
        self.g1_history = []
        self.g1_running = False

    def _g1_create(self):
        try:
            length = max(10, int(self.g1_length.get()))
            rule = min(255, max(0, int(self.g1_rule.get())))
            self.g1 = GameOfLife1D(length=length, rule=rule)
            self.g1.reset()
            self.g1_history = [self.g1.state.copy()]
            self._g1_draw()
        except Exception as e:
            print(f"Error en Juego 1D: {e}")

    def _g1_step(self):
        if self.g1 is None:
            self._g1_create()
        self.g1.step()
        self.g1_history.append(self.g1.state.copy())
        if len(self.g1_history) > 200:
            self.g1_history.pop(0)
        self._g1_draw()

    def _g1_draw(self):
        self.g1_ax.clear()
        self.g1_ax.set_facecolor('#e0f7ff')
        img = np.array(self.g1_history)
        cmap = matplotlib.colors.ListedColormap(['white', 'black'])
        self.g1_ax.imshow(img, aspect='auto', cmap=cmap, interpolation='nearest')
        self.g1_ax.set_title(f'Autómata 1D (Regla {self.g1.rule})', color='#003366')
        self.g1_canvas.draw()

    def _g1_toggle_run(self):
        self.g1_running = not self.g1_running
        if self.g1_running:
            self._g1_run_loop()

    def _g1_run_loop(self):
        def loop():
            while self.g1_running:
                time.sleep(0.05)
                self.root.after(0, self._g1_step)
        threading.Thread(target=loop, daemon=True).start()

    def _g1_clear(self):
        if self.g1 is not None:
            self.g1.reset()
            self.g1_history = [self.g1.state.copy()]
            self._g1_draw()

    # ---------------- Simulación COVID ----------------
    def _build_covid_tab(self):
        tab = ttk.Frame(self.nb)
        self.nb.add(tab, text='Simulación COVID (grid)')

        left = ttk.Frame(tab)
        left.pack(side='left', fill='y', padx=10, pady=10)
        right = ttk.Frame(tab)
        right.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        self.cv_rows = tk.IntVar(value=60)
        self.cv_cols = tk.IntVar(value=60)
        self.cv_init = tk.IntVar(value=5)
        self.cv_pinf = tk.DoubleVar(value=0.25)
        self.cv_prec = tk.DoubleVar(value=0.02)
        self.cv_pdie = tk.DoubleVar(value=0.005)

        fields = [
            ('Filas:', self.cv_rows),
            ('Columnas:', self.cv_cols),
            ('Infectados iniciales:', self.cv_init),
            ('P(infectar por vecino):', self.cv_pinf),
            ('P(recuperar por paso):', self.cv_prec),
            ('P(morir por paso):', self.cv_pdie),
        ]

        for label, var in fields:
            ttk.Label(left, text=label).pack(anchor='w', pady=(0,5))
            ttk.Entry(left, textvariable=var).pack(fill='x', pady=(0,10))

        ttk.Button(left, text='Crear simulación', command=self._cv_create).pack(fill='x', pady=5)
        ttk.Button(left, text='Paso', command=self._cv_step).pack(fill='x', pady=5)
        ttk.Button(left, text='Ejecutar/Parar', command=self._cv_toggle_run).pack(fill='x', pady=5)
        ttk.Button(left, text='Limpiar', command=self._cv_clear).pack(fill='x', pady=5)

        fig = Figure(figsize=(7,6), facecolor='#e0f7ff')
        self.cv_ax_grid = fig.add_subplot(211)
        self.cv_ax_grid.set_facecolor('#e0f7ff')
        self.cv_ax_chart = fig.add_subplot(212)
        self.cv_ax_chart.set_facecolor('#e0f7ff')
        self.cv_canvas = FigureCanvasTkAgg(fig, master=right)
        self.cv_canvas.get_tk_widget().pack(fill='both', expand=True)

        self.cv = None
        self.cv_running = False
        self.cv_history = []

    def _cv_create(self):
        try:
            rows = max(5, int(self.cv_rows.get()))
            cols = max(5, int(self.cv_cols.get()))
            init = max(1, int(self.cv_init.get()))
            pinf = float(self.cv_pinf.get())
            prec = float(self.cv_prec.get())
            pdie = float(self.cv_pdie.get())
            self.cv = CovidSimulation(rows=rows, cols=cols, init_infected=init,
                                      p_infect=pinf, p_recover=prec, p_die=pdie)
            self.cv_history = [self.cv.counts()]
            self._cv_draw()
        except Exception as e:
            print(f"Error en simulación COVID: {e}")

    def _cv_draw(self):
        self.cv_ax_grid.clear()
        self.cv_ax_chart.clear()
        self.cv_ax_grid.set_facecolor('#e0f7ff')
        self.cv_ax_chart.set_facecolor('#e0f7ff')

        cmap = matplotlib.colors.ListedColormap(['white','lightgreen','red','lightblue','black'])
        bounds = [0,1,2,3,4,5]
        norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
        self.cv_ax_grid.imshow(self.cv.grid, cmap=cmap, norm=norm, interpolation='nearest')
        self.cv_ax_grid.set_title(f'COVID Sim (t={self.cv.t})', color='#003366')

        times = list(range(len(self.cv_history)))
        s = [h[1] for h in self.cv_history]
        i = [h[2] for h in self.cv_history]
        r = [h[3] for h in self.cv_history]
        d = [h[4] for h in self.cv_history]
        self.cv_ax_chart.plot(times, s, label='Susceptibles', color='green')
        self.cv_ax_chart.plot(times, i, label='Infectados', color='red')
        self.cv_ax_chart.plot(times, r, label='Recuperados', color='blue')
        self.cv_ax_chart.plot(times, d, label='Muertos', color='black')
        self.cv_ax_chart.legend()
        self.cv_canvas.draw()

    def _cv_step(self):
        if self.cv is None:
            self._cv_create()
        self.cv.step()
        self.cv_history.append(self.cv.counts())
        self._cv_draw()

    def _cv_toggle_run(self):
        self.cv_running = not self.cv_running
        if self.cv_running:
            self._cv_run_loop()

    def _cv_run_loop(self):
        def loop():
            while self.cv_running:
                time.sleep(0.1)
                self.root.after(0, self._cv_step)
        threading.Thread(target=loop, daemon=True).start()

    def _cv_clear(self):
        if self.cv is not None:
            self._cv_create()

# ==================== EJECUCIÓN ====================
def main():
    root = tk.Tk()
    AppSimulaciones(root)
    root.mainloop()

if __name__ == '__main__':
    main()