"""usage: vangers-utils xbm [options] <in> <out>

    -d, --decode          decode image from xbm
    -e, --encode          encode image to xbm
    -W, --width WIDTH     image width [default: 800]
    -H, --height HEIGHT   image height [default: 600]
    -p, --palette PALETTE palette name  [default: default]
"""

from typing import Dict

import docopt
import yaml

from vangers_utils.image.misc import get_meta_filename
from vangers_utils.image.xbm.decode import decode_image
from vangers_utils.image.xbm.encode import encode_image
from vangers_utils.image.xbm.image import XbmImage
from vangers_utils.image.palette import read_palette


def _decode(in_filename: str, out_filename: str, width: int, height: int, palette_name: str):
    palette = read_palette(palette_name)
    xbm_image = decode_image(
        file_name=in_filename,
        screen_width=width,
        screen_height=height,
        palette=palette,
    )

    out_filename = out_filename
    xbm_image.image.save(out_filename)
    meta_file_name = get_meta_filename(out_filename)
    with open(meta_file_name, 'w') as f:
        yaml.dump(xbm_image.meta.to_dict(), f, default_flow_style=False)


def _encode(in_filename: str, out_filename: str, palette_name: str):
    palette = read_palette(palette_name)
    if not in_filename.endswith('.bmp'):
        raise docopt.DocoptExit("Only BMP files supported")

    meta_file_name = get_meta_filename(in_filename)
    with open(meta_file_name) as f:
        meta = XbmImage.Meta.from_dict(yaml.load(f))

    encode_image(meta, in_filename, out_filename, palette)


def main(args: Dict[str, str]):
    width = int(args['--width'])
    height = int(args['--height'])
    in_filename = args['<in>']
    out_filename = args['<out>']
    palette_name = args.get('--palette', 'default')

    if args['--decode']:
        _decode(in_filename, out_filename, width, height, palette_name)
    elif args['--encode']:
        _encode(in_filename, out_filename, palette_name)
    else:
        raise docopt.DocoptExit('Choose: -e or -d')
