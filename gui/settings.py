import tkinter as tk
from tkinter import ttk
from utils.tooltip import create_tooltip_icon
from typing import Optional


class SettingsWindow:
    """
    Window for algorithm settings with sliders to adjust parameters.
    """
    def __init__(self, master: tk.Tk, controller) -> None:
        self.master = master
        self.controller = controller
        self.master.title("Настройки алгоритма")

        self.setup_widgets()

    def setup_widgets(self) -> None:
        """Set up interactive widgets for the GUI."""

        # ants parameter
        row_start = 0
        ttk.Label(self.master, text="Количество муравьёв (ants):").grid(row=row_start, column=0, sticky='se', ipady=4)
        self.ants_scale = tk.Scale(self.master, from_=1, to=200, orient='horizontal')
        self.ants_scale.set(self.controller.ants)
        self.ants_scale.grid(row=row_start, column=1, sticky='we')
        self.ants_scale.config(command=self.apply_changes)
        create_tooltip_icon(self.master, "Общее количество агентов (муравьев), задействованных в одной итерации.", row_start, 2)

        # iter parameter
        row_start += 1
        ttk.Label(self.master, text="Количество итераций (iter):").grid(row=row_start, column=0, sticky='se', ipady=4)
        self.iter_scale = tk.Scale(self.master, from_=1, to=100, orient='horizontal')
        self.iter_scale.set(self.controller.iterations)
        self.iter_scale.grid(row=row_start, column=1, sticky='we')
        self.iter_scale.config(command=self.apply_changes)
        create_tooltip_icon(self.master, "Максимальное количество итераций алгоритма.", row_start, 2)

        # alpha parameter
        row_start += 1
        ttk.Label(self.master, text="Альфа (α):").grid(row=row_start, column=0, sticky='se', ipady=4)
        self.alpha_scale = tk.Scale(self.master, from_=0.0, to=3.0, orient='horizontal', resolution=0.1)
        self.alpha_scale.set(self.controller.alpha)
        self.alpha_scale.grid(row=row_start, column=1, sticky='we')
        self.alpha_scale.config(command=self.apply_changes)
        create_tooltip_icon(self.master, "Коэффициент, контролирующий влияние феромона на ребре.", row_start, 2)

        # beta parameter
        row_start += 1
        ttk.Label(self.master, text="Бета (β):").grid(row=row_start, column=0, sticky='se', ipady=4)
        self.beta_scale = tk.Scale(self.master, from_=0.0, to=3.0, orient='horizontal', resolution=0.1)
        self.beta_scale.set(self.controller.beta)
        self.beta_scale.grid(row=row_start, column=1, sticky='we')
        self.beta_scale.config(command=self.apply_changes)
        create_tooltip_icon(self.master, "Коэффициент, контролирующий влияние привлекательности маршрута.", row_start, 2)

        # p(Ro) parameter
        row_start += 1
        ttk.Label(self.master, text="Коэффициент испарения феромона (ρ):").grid(row=row_start, column=0, sticky='se', ipady=4, padx=(30, 0))
        self.p_scale = tk.Scale(self.master, from_=0.0, to=1.0, orient='horizontal', resolution=0.1)
        self.p_scale.set(self.controller.p)
        self.p_scale.grid(row=row_start, column=1, sticky='we')
        self.p_scale.config(command=self.apply_changes)
        create_tooltip_icon(self.master, "Отражает степень взаимного влияния между муравьями, предотвращает бесконечное накопление феромона.", row_start, 2)

        # q parameter
        row_start += 1
        ttk.Label(self.master, text="Интенсивность феромона (q):").grid(row=row_start, column=0, sticky='se', ipady=4)
        self.q_scale = tk.Scale(self.master, from_=1, to=100, orient='horizontal')
        self.q_scale.set(self.controller.q)
        self.q_scale.grid(row=row_start, column=1, sticky='we')
        self.q_scale.config(command=self.apply_changes)
        create_tooltip_icon(self.master, "Общее количество феромонов, влияющее на скорость сходимости алгоритма.", row_start, 2)

    def apply_changes(self, event: Optional[tk.Event] = None) -> None:
        """Updates the values of the settings in the controller."""
        ants = self.ants_scale.get()
        iter = self.iter_scale.get()
        a = self.alpha_scale.get()
        b = self.beta_scale.get()
        p = self.p_scale.get()
        q = self.q_scale.get()
        self.controller.update_settings(ants, iter, a, b, p, q)
