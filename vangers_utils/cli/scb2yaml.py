"""usage: vangers-utils scb2yml [options] <in> <out>

    -h, --help
"""
from typing import Dict
from vangers_utils.scb.scb2yaml.convert import ScbToYamlConverter


def main(args: Dict[str, str]):
    ScbToYamlConverter(args['<in>'], args['<out>']).convert()

