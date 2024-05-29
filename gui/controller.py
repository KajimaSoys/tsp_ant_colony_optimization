import tkinter as tk
from gui.address_selection import AddressSelectionWindow
from gui.route_visualization import RouteVisualizationWindow
from gui.settings import SettingsWindow
from utils.path import Path
from ant_colony import ACO
from utils.tsp import TSP
from typing import Optional


class ApplicationController:
    """
    The controller for the application, coordinating interactions between windows and data processing logic.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root2 = tk.Toplevel(self.root)
        self.address_window = AddressSelectionWindow(self.root, self)
        self.visualization_window = RouteVisualizationWindow(self.root2, self)
        self.settings_window = None

        self.ants = 100
        self.iterations = 20
        self.alpha = 1.5
        self.beta = 1.2
        self.p = 0.6
        self.q = 10

        self.points: Optional[list[tuple[int, int]]] = None
        self.tsp: Optional[TSP] = None
        self.aco: Optional[ACO] = None

    def run(self) -> None:
        """Starts the main event loop of tkinter."""
        self.root.mainloop()

    def update_points(self,  points: list[tuple[str]]) -> None:
        """Updates the points and creates a new TSP problem."""
        self.points = [(int(x), int(y)) for x, y in points]
        self.tsp = TSP(self.points)
        self.update_route()

    def update_settings(self, ants: int, iter: int, a: float, b: float, p: float, q: float) -> None:
        """Updates ACO algorithm parameters and recalculates the route."""
        self.ants = ants
        self.iterations = iter
        self.alpha = a
        self.beta = b
        self.p = p
        self.q = q
        self.update_route()

    def update_route(self) -> None:
        """Updates the route in the visualization window."""
        if self.points and len(self.points) > 1:
            best_path = self.perform_calculation()
            if best_path:
                print('Best Path:', best_path)
                self.visualization_window.update_route(best_path, self.tsp)

    def perform_calculation(self) -> Optional[Path]:
        """Perform the ACO calculation and update the plot."""
        if self.points and len(self.points) > 1:
            self.aco = ACO(ants=self.ants, iter=self.iterations, a=self.alpha, b=self.beta, p=self.p, q=self.q)
            best_path = self.aco.run(self.points)
            return best_path
        return None

    def open_settings(self):
        """Opens the settings window"""
        if not self.settings_window:
            self.settings_window = tk.Toplevel(self.root2)
            SettingsWindow(self.settings_window, self)
            self.settings_window.protocol("WM_DELETE_WINDOW", self.on_settings_close)

    def on_settings_close(self):
        """Change the settings_window to None to allow reopening of the settings window."""
        self.settings_window.destroy()
        self.settings_window = None
