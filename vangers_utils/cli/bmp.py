import argparse
from vangers_utils.bmp import read_image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('in_')
    parser.add_argument('out')
    parser.add_argument('--palette')

    args = parser.parse_args()
    print(args.in_)
    xbm_image = read_image(
        file_name=args.in_,
        pal=args.palette
    )
    xbm_image.save(args.out)


