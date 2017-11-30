"""usage: vangers-utils vmc [options] <in> <out>

    Decode, in=level *.ini
    -y, --ysize=size    y size of map
    -d, --decode        decode level
    -e, --encode        encode level
    -h, --help
"""

from typing import Dict

import docopt
import numpy as np
from PIL import Image

from vangers_utils.height_map import read_map


def _decode(in_filename: str, out_filename: str, y_size: int):
    arr1, arr3 = read_map(in_filename, y_size)
    arr1 = np.log2(arr1)
    arr1[np.isneginf(arr1)] = 0
    arr1 = (arr1 - np.min(arr1)) / (np.max(arr1) - np.min(arr1)) * 255
    arr1 = arr1.astype(np.uint8)
    img = Image.fromarray(arr1)
    img.save(out_filename)


def _encode(in_filename, out_filename):
    raise NotImplementedError()


def main(args: Dict[str, str]):
    in_filename = args['<in>']
    out_filename = args['<out>']
    if args['--decode']:
        _decode(in_filename, out_filename, int(args['--ysize']))
    elif args['--encode']:
        _encode(in_filename, out_filename)
    else:
        raise docopt.DocoptExit('Choose: -e or -d')
