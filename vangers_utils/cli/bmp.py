"""usage: vangers-utils bmp [options] <in> <out>

    -d, --decode        decode image from bmp
    -e, --encode        encode image to bmp
"""

import re
from typing import Dict

import docopt
import yaml

import vangers_utils.image.palette
from vangers_utils.image.bmp.decode import decode_image
from vangers_utils.image.bmp.encode import encode_image
from vangers_utils.image.misc import get_meta_filename


def _decode(in_filename: str, out_filename: str):
    bmp_image = decode_image(
        file_name=in_filename,
        palette=vangers_utils.image.palette.PALETTE
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


def _encode(in_filename: str, out_filename: str):
    meta_filename = get_meta_filename(in_filename)
    with open(meta_filename) as f:
        meta = yaml.load(f)

    bytes_res = encode_image(in_filename, meta, pal=vangers_utils.image.palette.PALETTE)
    with open(out_filename, 'wb') as f:
        f.write(bytes_res)


def main(args: Dict[str, str]):
    in_filename = args['<in>']
    out_filename = args['<out>']

    if args['--decode']:
        _decode(
            in_filename=in_filename,
            out_filename=out_filename
        )
    elif args['--encode']:
        _encode(in_filename, out_filename)
    else:
        raise docopt.DocoptExit('Choose: -e or -d')
