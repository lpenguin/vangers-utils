from glob import glob
from os.path import join, basename, isfile
from tkinter import Tk, ttk, Listbox, StringVar, Label, BOTH, LEFT, RAISED, TOP, Y, BOTTOM, RIGHT, X
from tkinter.filedialog import askopenfile, askdirectory
from tkinter.ttk import Button
from typing import Optional, List, Dict, Tuple

from PIL import ImageTk
from PIL.Image import Image

from vangers_utils.gui.directory_view import DirectoryView
from vangers_utils.gui.image_settings_view import ImageSettingsView
from vangers_utils.gui.palettes_view import PalettesView
from vangers_utils.image.bmp.decode import decode_image as _decode_image_bmp
from vangers_utils.image.xbm.decode import decode_image as _decode_image_xbm

from vangers_utils.image.palette import read_palette, list_palette_names


def decode_bmp(filepath: str, palette: List[int], is_bg: bool=False, is_bml: bool=False) -> Tuple[Dict, List[Image]]:
    bmp_image = _decode_image_bmp(filepath, palette, read_palette('objects'))
    return (bmp_image.meta, bmp_image.images)


def decode_xbm(filepath: str, palette: List[int], *args, **kwargs) -> Tuple[Dict, List[Image]]:
    xbm_image = _decode_image_xbm(filepath, palette)
    return (xbm_image.meta.to_dict(), [xbm_image.image])


class ConvertApp:
    _current_dir: Optional[str]
    _cur_images: List

    def __init__(self):
        self._root = Tk()
        # self._root.pack(fill=BOTH, expand=True)

        main_frame = ttk.Frame(self._root, padding=(5, 5, 12, 0))
        main_frame.pack(side=TOP, fill=BOTH)

        directory_frame = ttk.Frame(main_frame, padding=(5, 5, 12, 0), relief=RAISED, borderwidth=1)
        directory_frame.pack(fill=Y, side=LEFT)

        self._dir_view = DirectoryView(parent=directory_frame, on_select=self._on_file_select)
        self._dir_view.widget.pack(side=TOP, fill=Y, expand=True)

        button = Button(directory_frame, text='Change directory', command=self._on_change_directory)
        button.pack(side=TOP)

        self._images_frame = ttk.Frame(main_frame, borderwidth=1, relief=RAISED)
        self._images_frame.pack(fill=BOTH, side=LEFT)

        self._image_labels = []

        self._image_settings = ImageSettingsView(main_frame, borderwidth=1, relief=RAISED)
        self._image_settings.pack(fill=Y, side=RIGHT)
        self._image_settings.on_change = self._on_settings_change

        self._image_meta_label = ttk.Label(self._root, text='Meta: ')
        self._image_meta_label.pack(side=TOP, fill=X)
        # self._palettes_frame =  ttk.Frame(self._root, borderwidth=1, relief=RAISED)
        # self._palettes_frame.pack(fill=Y, side=RIGHT)

        # self._image_label = Label(self._root)

    def _on_settings_change(self):
        self._on_file_select(self._dir_view.current_item)

    def _on_change_directory(self, *args):
        dir = askdirectory()
        self._dir_view.change_dir(dir)

    def _on_palette_select(self, palette: str):
        self._on_file_select(self._dir_view.current_item)

    def _decode_image(self, filepath: str, palette: List[int]) ->Tuple[Dict, List[Image]]:
        filetype = self._image_settings.filetype
        decodef = decode_bmp

        if filetype == 'auto':
            if filepath.endswith('.bml') or filepath.endswith('.bmo') or filepath.endswith('.bmp'):
                decodef = decode_bmp
            else:
                decodef = decode_xbm
        elif filetype == 'bmp':
            decodef = decode_bmp
        elif filetype == 'xbm':
            decodef = decode_xbm

        return decodef(filepath, palette)

    def _on_file_select(self, filepath: str):
        palette = read_palette(self._image_settings.palette)
        if self._image_settings.palette != 'default':
            palette = [
                min(p * 2, 255)
                for p in palette
            ]

        meta, images = self._decode_image(filepath, palette)

        for label in self._image_labels:
            label.pack_forget()
            label.destroy()
        self._image_meta_label['text'] = str(meta)
        self._image_labels = []
        self._cur_images = []

        for image in images:
            label = Label(self._images_frame)
            img = ImageTk.PhotoImage(image)
            self._cur_images.append(img)
            self._image_labels.append(label)
            label['image'] = img
            label.pack()

    def run(self):
        self._root.mainloop()