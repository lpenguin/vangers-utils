import argparse
from vangers_utils.script.convert import Converter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('in_')
    parser.add_argument('out')

    args = parser.parse_args()
    Converter(args.in_, args.out).convert()


