import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.path import Path
from utils.tsp import TSP
from typing import Optional


class RouteVisualizationWindow:
    """
    Window for visualizing the route with an option to open settings.
    """

    def __init__(self, master: tk.Tk, controller):
        self.master = master
        self.controller = controller
        self.master.title("Визуализация маршрута")

        ttk.Label(master, text="Построение маршрута доставки").pack(side=tk.TOP, pady=10)

        self.fig = Figure(figsize=(6, 6))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0, 1000)
        self.ax.set_ylim(0, 1000)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.route_length_label = ttk.Label(master, text="Длина маршрута: 0 м")
        self.route_length_label.pack(side=tk.TOP, pady=10)

        self.tsp: Optional[TSP] = None

        # self.settings_button = ttk.Button(master, text="Изменение параметров", command=self.controller.open_settings)
        # self.settings_button.pack(side=tk.TOP, pady=10)

    def update_route(self, path: Path, tsp: Optional[TSP]) -> None:
        """Updates the route graph and the route length label."""
        self.tsp = tsp
        self.tsp._paths = [Path(indx=path.indx, leng=path.leng, name="ACO Path")]
        km, m = divmod(path.leng, 1000)
        if km > 0:
            self.route_length_label.config(text=f"Длина маршрута: {int(km)}км {m:.0f}м")
        else:
            self.route_length_label.config(text=f"Длина маршрута: {path.leng:.0f} м")
        self.update_plot()

    def update_plot(self) -> None:
        """Updates the matplotlib plot with the current TSP solution."""
        if self.tsp:
            self.tsp.show(self.ax)
            self.canvas.draw_idle()
