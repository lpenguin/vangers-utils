"""usage: vangers-utils bmp2png [options] <in> <out>

    --palette <palette=value>
"""

from typing import Dict

from vangers_utils.bmp import read_image


def main(args: Dict[str, str]):
    xbm_image = read_image(
        file_name=args['<in>'],
        pal=args['--palette']
    )
    xbm_image.save(args['<out>'])


