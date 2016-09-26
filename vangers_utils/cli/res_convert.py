import argparse
from vangers_utils.script.bin_convert import BinToYamlConverter
from vangers_utils.script.yaml_convert import YamlToBinConverter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('in_')
    parser.add_argument('out')

    args = parser.parse_args()
    YamlToBinConverter(args.in_, args.out).convert()
    # BinToYamlConverter(args.in_, args.out).convert()


