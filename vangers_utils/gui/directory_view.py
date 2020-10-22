import os
import tkinter
from os import getcwd, listdir
from os.path import isdir, join, isfile, basename
from tkinter import Widget, Listbox, ttk, VERTICAL, S, E, W, N, SE, NE
from typing import Callable, Optional


class DirectoryView:
    def __init__(self, parent: Widget, initial_dir: str = None, height: int = 25,
                 on_select: Callable[[str], None] = None):
        self._current_dir = initial_dir or getcwd()
        self._list_box = Listbox(parent)
        # self._list_box.grid(column=0, row=0, sticky=(N, W, E, S))
        self._list_box.bind('<<ListboxSelect>>', self._on_list_box_select)
        self._list_box.bind('<Double-1>', self._on_list_box_double_click)

        # s = ttk.Scrollbar(parent, orient=VERTICAL, command=self._list_box.yview)
        # s.place()
        # self._list_box['yscrollcommand'] = s.set
        # self._list_box.yscrollbar = s
        # self._s = s

        self._on_select = on_select
        self._fill_list_box()

    @property
    def widget(self) -> Widget:
        return self._list_box

    def change_dir(self, directory: str):
        self._current_dir = directory
        self._fill_list_box()

    def _fill_list_box(self):
        names = listdir(self._current_dir)
        names = [
            join(self._current_dir, name)
            for name in names
        ]
        names = ['..'] + list(sorted(names, key=isdir, reverse=True))

        self._list_box.delete(0, tkinter.END)

        for name in names:
            if name != '..':
                if isdir(name):
                    name = basename(name) + os.sep
                else:
                    name = basename(name)
            self._list_box.insert('end', name)
        self._list_box.selection_set(0, 0)

    @property
    def current_item(self) -> Optional[str]:
        indices = self._list_box.curselection()
        if len(indices) != 1:
            return None
        index = int(indices[0])
        name = self._list_box.get(index)
        return join(self._current_dir, name.rstrip(os.sep))

    def _on_list_box_select(self, *args):
        current_fn = self.current_item
        if isfile(current_fn) and self._on_select is not None:
            self._on_select(current_fn)

    def _on_list_box_double_click(self, *args):
        current_fn = self.current_item

        if isdir(current_fn):
            self.change_dir(current_fn)

