import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.tsp import TSP, generate_problem
from utils.path import Path
from utils.tooltip import create_tooltip_icon
from ant_colony import ACO


class TSPGUI:
    def __init__(self, master):
        self.master = master
        master.title("Задача коммивояжёра - оптимизация муравьиной колонией")

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=9, column=0, columnspan=6)

        self.points = None
        self.tsp = None
        self.aco = None

        self.setup_widgets()

    def setup_widgets(self):
        row_start = 0
        ttk.Label(self.master, text="Количество точек (points):").grid(row=row_start, column=0, sticky='se', ipady=4)
        self.points_count = tk.Scale(self.master, from_=1, to=100, orient='horizontal')
        self.points_count.set(20)
        self.points_count.grid(row=row_start, column=1, sticky='we')
        ttk.Button(self.master, text="Сгенерировать задачу", command=self.generate_task).grid(row=row_start, column=3, columnspan=1, sticky='swe')

        row_start += 1
        ttk.Label(self.master, text="Количество муравьёв (ants):").grid(row=row_start, column=0, sticky='se', ipady=4)
        self.ants_scale = tk.Scale(self.master, from_=1, to=200, orient='horizontal')
        self.ants_scale.set(100)
        self.ants_scale.grid(row=row_start, column=1, sticky='we')
        create_tooltip_icon(self.master, "Общее количество агентов (муравьев), задействованных в одной итерации.", row_start, 2)
        ttk.Button(self.master, text="Расчёт", command=self.perform_calculation).grid(row=row_start, column=3, columnspan=1, sticky='swe')

        row_start += 1
        ttk.Label(self.master, text="Количество итераций (iter):").grid(row=row_start, column=0, sticky='se', ipady=4)
        self.iter_scale = tk.Scale(self.master, from_=1, to=100, orient='horizontal')
        self.iter_scale.set(20)
        self.iter_scale.grid(row=row_start, column=1, sticky='we')
        create_tooltip_icon(self.master, "Максимальное количество итераций алгоритма.", row_start, 2)

        row_start += 1
        ttk.Label(self.master, text="Альфа (α):").grid(row=row_start, column=0, sticky='se', ipady=4)
        self.alpha_scale = tk.Scale(self.master, from_=0.0, to=3.0, orient='horizontal', resolution=0.1)
        self.alpha_scale.set(1.5)
        self.alpha_scale.grid(row=row_start, column=1, sticky='we')
        create_tooltip_icon(self.master, "Коэффициент, контролирующий влияние феромона на ребре.", row_start, 2)

        row_start += 1
        ttk.Label(self.master, text="Бета (β):").grid(row=row_start, column=0, sticky='se', ipady=4)
        self.beta_scale = tk.Scale(self.master, from_=0.0, to=3.0, orient='horizontal', resolution=0.1)
        self.beta_scale.set(1.2)
        self.beta_scale.grid(row=row_start, column=1, sticky='we')
        create_tooltip_icon(self.master, "Коэффициент, контролирующий влияние привлекательности маршрута.", row_start, 2)

        row_start += 1
        ttk.Label(self.master, text="Коэффициент испарения феромона (ρ):").grid(row=row_start, column=0, sticky='se', ipady=4)
        self.p_scale = tk.Scale(self.master, from_=0.0, to=1.0, orient='horizontal', resolution=0.1)
        self.p_scale.set(0.6)
        self.p_scale.grid(row=row_start, column=1, sticky='we')
        create_tooltip_icon(self.master, "Отражает степень взаимного влияния между муравьями, предотвращает бесконечное накопление феромона.", row_start, 2)

        row_start += 1
        ttk.Label(self.master, text="Интенсивность феромона (q):").grid(row=row_start, column=0, sticky='se', ipady=4)
        self.q_scale = tk.Scale(self.master, from_=1, to=100, orient='horizontal')
        self.q_scale.set(10)
        self.q_scale.grid(row=row_start, column=1, sticky='we')
        create_tooltip_icon(self.master, "Общее количество феромонов, влияющее на скорость сходимости алгоритма.", row_start, 2)

    def generate_task(self):
        self.points = generate_problem(int(self.points_count.get()))
        self.tsp = TSP(self.points)
        self.update_plot()

    def perform_calculation(self, event=None):
        if self.points:
            ants = int(self.ants_scale.get())
            iterations = int(self.iter_scale.get())
            alpha = float(self.alpha_scale.get())
            beta = float(self.beta_scale.get())
            p = float(self.p_scale.get())
            q = float(self.q_scale.get())
            self.aco = ACO(ants=ants, iter=iterations, a=alpha, b=beta, p=p, q=q)
            best_path = self.aco.run(self.points)
            print('Best Path:', best_path)
            self.tsp._paths = [Path(indx=best_path.indx, leng=best_path.leng, name="ACO Path")]
            self.update_plot()

    def update_plot(self):
        if self.tsp:
            self.ax.clear()
            self.tsp.show(self.ax)
            self.canvas.draw_idle()


if __name__ == "__main__":
    root = tk.Tk()
    app = TSPGUI(root)
    root.mainloop()
