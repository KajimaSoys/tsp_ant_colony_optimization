import tkinter as tk
from tkinter import ttk


class ToolTip(object):
    """
    Class to create and manage tooltips for Tkinter widgets.
    """
    def __init__(self, widget: tk.Widget, text: str = 'widget info') -> None:
        """
        Initialize the tooltip with a widget.

        Args:
        widget (tk.Widget): The widget to which the tooltip is attached.
        text (str): The text displayed by the tooltip.
        """
        self.widget = widget
        self.text = text
        self.tipwindow: tk.Toplevel | None = None
        self.id: str | None = None
        self.x = self.y = 0
        self.create_tooltip()

    def create_tooltip(self) -> None:
        """Bind mouse events for showing and hiding the tooltip."""
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event: tk.Event | None = None) -> None:
        """Schedule the tooltip to be shown after a delay when the mouse enters the widget."""
        self.schedule()

    def leave(self, event: tk.Event | None = None) -> None:
        """Unschedule and hide the tooltip when the mouse leaves the widget."""
        self.unschedule()
        self.hide_tip()

    def schedule(self) -> None:
        """Schedule the tooltip to appear after a delay."""
        self.unschedule()
        self.id = self.widget.after(500, self.show_tip)  # Delay in milliseconds

    def unschedule(self) -> None:
        """Cancel the scheduled appearance of the tooltip if any."""
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def show_tip(self, event: tk.Event | None = None) -> None:
        """Display the tooltip near the widget."""
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20

        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT, background="#ffffe0", relief=tk.SOLID, borderwidth=1, font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self) -> None:
        """Destroy the tooltip window."""
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def create_tooltip_icon(master: tk.Widget, text: str, row: int, column: int) -> None:
    """
    Create a tooltip icon (a label with a '?') that shows a tooltip when hovered.

    Args:
    master (tk.Widget): The master Tkinter widget.
    text (str): The tooltip text.
    row (int): The grid row to place the tooltip icon.
    column (int): The grid column to place the tooltip icon.
    """
    icon = ttk.Label(master, text='?', font=('Arial', 12, 'bold'), foreground='black')
    icon.grid(row=row, column=column, sticky='sw', ipadx=30)
    ToolTip(icon, text=text)
