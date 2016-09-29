"""usage: vangers-utils bmp [options] <in> <out>

    -d, --decode        decode image from bmp
    -e, --encode        encode image to bmp
    --no-bmp            BMP_FLAG
    --background        BG_FLAG
    --no-offsets        BML_NO_OFFSETS
"""

from typing import Dict

import docopt
import yaml

import vangers_utils.image.palette
from vangers_utils.image.bmp.decode import decode_image
from vangers_utils.image.bmp.encode import encode_image
from vangers_utils.image.misc import get_meta_filename


def _decode(in_filename: str, out_filename: str,
            is_bmp: bool = True, is_background: bool = False, is_no_offsets: bool = False):
    bmp_image = decode_image(
        file_name=in_filename,
        palette=vangers_utils.image.palette.PALETTE,
        is_bmp=is_bmp,
        is_background=is_background,
        is_no_offsets=is_no_offsets,
    )
    meta_filename = get_meta_filename(out_filename)
    with open(meta_filename, 'w') as f:
        yaml.dump(bmp_image.meta, f, default_flow_style=False)

    bmp_image.image.save(out_filename)


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
            out_filename=out_filename,
            is_bmp=not args['--no-bmp'],
            is_background=bool(args['--background']),
            is_no_offsets=bool(args['--no-offsets']),
        )
    elif args['--encode']:
        _encode(in_filename, out_filename)
    else:
        raise docopt.DocoptExit('Must choose: -e or -d')



