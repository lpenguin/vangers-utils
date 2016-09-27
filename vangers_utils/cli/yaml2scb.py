"""usage: vangers-utils yml2scb [options] <in> <out>

    -h, --help
    -v, --verbose   Dump binary
"""

from typing import Dict
from vangers_utils.scb.yaml2scb.convert import YamlToScbConverter


def main(args: Dict[str, str]):
    verbose = bool(args['--verbose'])
    YamlToScbConverter(args['<in>'], args['<out>']).convert(verbose)

