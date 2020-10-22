"""usage: vangers-utils bmp [options] <in> <out>

    -d, --decode          decode image from bmp
    -e, --encode          encode image to bmp
    -p, --palette PALETTE palette name  [default: default]
"""
import os
import re
from typing import Dict

import docopt
import yaml
from PIL import Image

from vangers_utils.image.bmp.decode import decode_image
from vangers_utils.image.bmp.encode import encode_image
from vangers_utils.image.misc import get_meta_filename
from vangers_utils.image.palette import read_palette


def _decode(in_filename: str, out_filename: str, palette: str):
    palette = read_palette(palette)
    bmp_image = decode_image(
        file_name=in_filename,
        palette=palette
    )
    meta_filename = get_meta_filename(out_filename)
    with open(meta_filename, 'w') as f:
        yaml.dump(bmp_image.meta, f, default_flow_style=False)

    if len(bmp_image.images) == 1:
        bmp_image.images[0].save(out_filename)
    else:
        for n, image in enumerate(bmp_image.images):
            f = re.sub(r'^(.*)\.(\w+)$', r'\g<1>.{}.\g<2>'.format(n), out_filename)
            image.save(f)


def _encode(in_filename: str, out_filename: str, palette: str):
    palette = read_palette(palette)

    meta_filename = get_meta_filename(in_filename)
    meta = None
    if os.path.exists(meta_filename):
        with open(meta_filename) as f:
            meta = yaml.load(f)
    image = Image.open(in_filename)  # type: Image
    bytes_res = encode_image(image, meta, pal=palette)
    with open(out_filename, 'wb') as f:
        f.write(bytes_res)


def main(args: Dict[str, str]):
    in_filename = args['<in>']
    out_filename = args['<out>']
    palette_name = args.get('--palette', 'default')

    if args['--decode']:
        _decode(
            in_filename=in_filename,
            out_filename=out_filename,
            palette=palette_name
        )
    elif args['--encode']:
        _encode(in_filename, out_filename, palette_name)
    else:
        raise docopt.DocoptExit('Choose: -e or -d')
