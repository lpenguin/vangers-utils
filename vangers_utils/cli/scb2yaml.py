"""usage: vangers-utils scb2yml [options] <in> <out>

    -h, --help
"""
from typing import Dict

from vangers_utils.scb.decode.convert import ScbToYamlEncoder


def _decode(in_filename: str, out_filename: str):
    with open(in_filename, 'rb') as in_f:
        with open(out_filename, 'wt') as out_f:
            ScbToYamlEncoder(in_f, out_f).convert()


def main(args: Dict[str, str]):
    in_filename = args['<in>']
    out_filename = args['<out>']
    _decode(in_filename, out_filename)
