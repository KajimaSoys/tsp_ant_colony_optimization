from random import randint
from numpy import array
from matplotlib.lines import Line2D
from utils.path import Path


def generate_problem(count: int, canvas_size: int = 1000) -> list[tuple[int]]:
    """Generates a list of random 2D points."""
    return [(randint(0, canvas_size), randint(0, canvas_size)) for _ in range(count)]


class TSP:
    """
    Allows to visualize the Traveling Salesman Problem and paths.
    """
    CLR_POINT = "#eb343a"
    CLR_PATH = [
        "#eb343a",
        "#db34eb",
        "#5b34eb",
        "#34b4eb",
        "#34eb4c",
        "#ebe534",
        "#eb9234",
    ]

    def __init__(self, points: list[tuple[int]], paths: list[Path] = None):
        """Initializes the problem with points and paths, if any."""
        self._points = points
        self._paths = paths if paths is not None else []

    def get_points(self) -> list[tuple[int]]:
        """Returns the list of 2D points of the initialized problem."""
        return self._points

    def get_paths(self) -> list[Path]:
        """Returns the list of paths of the initialized problem."""
        return self._paths

    def show(self, ax) -> None:
        """Visualizes the TSP data using the given axes."""
        ax.clear()
        self.__draw_points(ax)
        lines = self.__draw_paths(ax)
        self.__draw_legend(ax, lines)
        ax.figure.canvas.draw()

    def __draw_points(self, ax) -> None:
        """Draws 2D points on the given axes."""
        ax.scatter(*array(self._points).T, zorder=1, color=self.CLR_POINT, label=f"Points ({len(self._points)})")
        for i, p in enumerate(self._points):
            ax.annotate(i + 1, p, ha="center", textcoords="offset points", xytext=(0, 4), fontsize=8)
            ax.annotate(f"({p[0]}; {p[1]})", p, ha="center", va="top", textcoords="offset points", xytext=(0, -4), fontsize=6)

    def __draw_paths(self, ax) -> list[Line2D]:
        """Draws all given paths on the given axes."""
        lines = []
        for i, path in enumerate(self._paths):
            points = [self._points[idx] for idx in path.indx]
            (line,) = ax.plot(*array(points).T, ls="--", zorder=0, color=self.CLR_PATH[i % len(self.CLR_PATH)],
                              label=f"{path.name} ({path.leng:.2f})")
            lines.append(line)
        return lines

    def __draw_legend(self, ax, lines: list[Line2D]) -> None:
        """Draws the legend on the given axes, with interactive toggle for paths."""
        if lines:
            legend = ax.legend()
            lined = {legline: origline for legline, origline in zip(legend.get_lines(), lines)}

            def on_pick(event):
                legline = event.artist
                origline = lined[legline]
                visible = not origline.get_visible()
                origline.set_visible(visible)
                legline.set_alpha(1.0 if visible else 0.2)
                ax.figure.canvas.draw()
            ax.figure.canvas.mpl_connect("pick_event", on_pick)
        else:
            ax.legend()
