"""usage: vangers-utils scb [options] <in> <out>

    -d, --decode        decode image from scb
    -e, --encode        encode image to scb
    -v, --verbose       verbose encode
    -h, --help
"""

from typing import Dict

import docopt

from vangers_utils.scb.decode.decoder import ScbToYamlDecoder
from vangers_utils.scb.encode.convert import YamlToScbConverter


def _decode(in_filename: str, out_filename: str):
    with open(in_filename, 'rb') as in_f:
        with open(out_filename, 'wt') as out_f:
            ScbToYamlDecoder(in_f, out_f).convert()


def _encode(in_filename: str, out_filename: str, verbose: bool):
    YamlToScbConverter(in_filename, out_filename).convert(verbose)


def main(args: Dict[str, str]):
    in_filename = args['<in>']
    out_filename = args['<out>']
    if args['--decode']:
        _decode(in_filename, out_filename)
    elif args['--encode']:
        _encode(in_filename, out_filename, bool(args['--verbose']))
    else:
        raise docopt.DocoptExit('Choose: -e or -d')
