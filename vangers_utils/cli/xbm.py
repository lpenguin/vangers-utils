"""usage: vangers-utils xbm [options] <in> <out>

    -d, --decode        decode image from xbm [default: True]
    -e, --encode        encode image to xbm
    -W, --width WIDTH   image width [default: 800]
    -H, --height HEIGHT image height  [default: 600]
"""

from typing import Dict

import docopt
import yaml
import re

from vangers_utils.image.xbm.decode import decode_image
from vangers_utils.image.xbm.encode import encode_image
from vangers_utils.image.xbm.image import XbmImage


def _decode(in_filename: str, out_filename: str, width: int, height: int):
    xbm_image = decode_image(
        file_name=in_filename,
        screen_width=width,
        screen_height=height,
    )

    out_filename = out_filename
    xbm_image.image.save(out_filename)
    meta_file_name = re.sub(r'^(.*)\.\w+$', r'\g<1>.meta.yaml', out_filename)
    with open(meta_file_name, 'w') as f:
        yaml.dump(xbm_image.meta.to_dict(), f, default_flow_style=False)


def _encode(in_filename: str, out_filename: str):
    if not in_filename.endswith('.bmp'):
        raise docopt.DocoptExit("Only BMP files supported")

    meta_file_name = re.sub(r'^(.*)\.\w+$', r'\g<1>.meta.yaml', in_filename)
    with open(meta_file_name) as f:
        meta = XbmImage.Meta.from_dict(yaml.load(f))

    encode_image(meta, in_filename, out_filename)


def main(args: Dict[str, str]):
    width = int(args['--width'])
    height = int(args['--height'])
    in_filename = args['<in>']
    out_filename = args['<out>']

    if args['--decode']:
        _decode(in_filename, out_filename, width, height)
    elif args['--encode']:
        _encode(in_filename, out_filename)
    else:
        raise docopt.DocoptExit('Must choose: -e or -d')


