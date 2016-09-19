import argparse
from vangers_utils.xbm import read_image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('in_')
    parser.add_argument('out')
    parser.add_argument('--width', '-W', default=800, required=False, type=int)
    parser.add_argument('--height', '-H', default=600, required=False, type=int)

    args = parser.parse_args()
    print(args.in_)
    xbm_image = read_image(
        file_name=args.in_,
        screen_width=args.width,
        screen_height=args.height
    )
    print(xbm_image.meta)
    xbm_image.image.save(args.out)


