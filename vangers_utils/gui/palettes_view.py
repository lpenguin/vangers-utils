import tkinter
from tkinter import Widget, Listbox
from typing import List, Callable, Optional


class PalettesView:
    def __init__(self, parent: Widget, palettes=List[str], on_select: Callable[[str], None] = None):
        self._palettes = palettes
        self._list_box = Listbox(parent, exportselection=0 )
        # self._list_box.grid(column=0, row=0, sticky=(N, W, E, S))
        self._list_box.bind('<<ListboxSelect>>', self._on_list_box_select, )
        # s = ttk.Scrollbar(parent, orient=VERTICAL, command=self._list_box.yview)
        # s.place()
        # self._list_box['yscrollcommand'] = s.set
        # self._list_box.yscrollbar = s
        # self._s = s

        self._on_select = on_select
        self._fill_list_box()
        self._list_box.selection_set(0, 0)

    @property
    def widget(self)->Widget:
        return self._list_box

    @property
    def current_item(self) -> Optional[str]:
        indices = self._list_box.curselection()
        if len(indices) != 1:
            return None
        index = int(indices[0])
        name = self._list_box.get(index)
        return name

    def _fill_list_box(self):
        self._list_box.delete(0, tkinter.END)

        for name in self._palettes:
            self._list_box.insert('end', name)

    def _on_list_box_select(self, *args):
        current_palette = self.current_item
        if current_palette is not None and self._on_select is not None:
            self._on_select(current_palette)
