from tkinter import Y, TOP, LEFT, Listbox, StringVar, OptionMenu, IntVar, BOTH
from tkinter.ttk import Frame, Label, Checkbutton
from typing import List

from vangers_utils.gui.palettes_view import PalettesView
from vangers_utils.image.palette import list_palette_names


class ImageSettingsView(Frame):
    _filetypes: List[str] = ['auto', 'bmp', 'xbm']
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self._init_view()
        self.on_change = None
        # header_label = Label(self, text='Image settings')
        # header_label.config(font=("Arial", 12))
        # header_label.pack(side=TOP)



        settings_grid = Frame(self)
        settings_grid.pack(side=TOP)

        filetype_label = Label(settings_grid, text='Filetype')
        filetype_label.grid(column=0, row=0, sticky=('w', ))

        value = StringVar(value=['auto'])
        self._filetype_select = OptionMenu(settings_grid, value, *self._filetypes, command=self._on_filetype_select)
        self._filetype_select.grid(column=1, row=0, sticky=('w',))
        self._filetype_select.value = value

        value = StringVar(value='off')
        self._bml_bmp_check = Checkbutton(settings_grid, text='BML BMP flag', variable=value, onvalue='on', offvalue='off',
                                          command=self._on_bml_bmp_change)
        self._bml_bmp_check.grid(column=0, row=1, sticky=('w', ))
        self._bml_bmp_check.value = value

        value = StringVar(value='off')
        self._bml_bg_check = Checkbutton(settings_grid, text='BML BG flag', variable=value, onvalue='on', offvalue='off',
                                         command=self._on_bml_bg_change)
        self._bml_bg_check.grid(column=0, row=2, sticky=('w', ))
        self._bml_bg_check.value = value

        palettes_label = Label(self, text='Palettes')
        palettes_label.pack(side=TOP)

        self._palettes_view = PalettesView(self, palettes=list_palette_names(), on_select=self._on_palette_select)
        self._palettes_view.widget.pack(side=TOP, fill=BOTH, expand=True)

    @property
    def filetype(self)->str:
        return self._filetype_select.value.get()

    @property
    def bml_bg(self)->bool:
        return self._bml_bg_check.value.get() == 'on'

    @property
    def bml_bmp(self)->bool:
        return self._bml_bmp_check.value.get() == 'on'

    @property
    def palette(self)->str:
        return self._palettes_view.current_item

    def _on_bml_bg_change(self, *args):
        self.on_change()

    def _on_bml_bmp_change(self, *args):
        self.on_change()

    def _on_filetype_select(self, *args):
        self.on_change()

    def _init_view(self):
        pass

    def _on_palette_select(self, pal: str):
        self.on_change()