import tkinter as tk
from tkinter import ttk
from typing import Optional, Any


class AddressSelectionWindow:
    """
    Window for selecting addresses and their coordinates.
    """

    def __init__(self, master: tk.Tk, controller: Any) -> None:
        self.master = master
        self.controller = controller
        self.master.title("Выбор адресов")

        ttk.Label(master, text="Выберите адреса доставки из списка").pack(side=tk.TOP, pady=10)

        self.tree = ttk.Treeview(master, columns=("name", "x", "y"), show="headings", selectmode="extended")
        self.tree.heading('name', text='Название')
        self.tree.heading('x', text='X')
        self.tree.heading('y', text='Y')
        self.tree.column('name', width=200, anchor='w')
        self.tree.column('x', width=50, anchor='center')
        self.tree.column('y', width=50, anchor='center')
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_selection_change)

        self.addresses: list[tuple[str, int, int]] = self.controller.address_list
        for address in self.addresses:
            self.tree.insert("", "end", values=address)

        self.selected_count_label = ttk.Label(master, text="Выбрано адресов: 0")
        self.selected_count_label.pack(side=tk.BOTTOM, pady=10)

    def on_selection_change(self, event: Optional[tk.Event] = None) -> None:
        """Sends the selected addresses to the controller to update the route."""
        selected_items = self.tree.selection()
        selected_points = [self.tree.item(item, 'values') for item in selected_items]
        self.selected_count_label.config(text=f"Выбрано адресов: {len(selected_items)}")
        self.controller.update_points(selected_points)
