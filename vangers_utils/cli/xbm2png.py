"""usage: vangers-utils xbm2png [options] <in> <out>

    -W, --width WIDTH   image width [default: 800]
    -H, --height HEIGHT image height  [default: 600]
"""

from typing import Dict
from vangers_utils.image.xbm import read_image


def main(args: Dict[str, str]):
    width = int(args['--width'])
    height = int(args['--height'])
    xbm_image = read_image(
        file_name=args['<in>'],
        screen_width=width,
        screen_height=height,
    )
    print(xbm_image.meta)
    xbm_image.image.save(args['<out>'])



