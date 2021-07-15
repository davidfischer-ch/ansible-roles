#!/usr/bin/env python

import argparse, yaml

from pytoolbox import filesystem
from pytoolbox.argparse import is_dir, FullPaths


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     epilog='Check YAML syntax of a whole file tree.')
    parser.add_argument('directory', action=FullPaths, nargs='?', type=is_dir, default='.')
    args = parser.parse_args()
    check(args.directory)


def check(directory):
    for filename in sorted(filesystem.find_recursive(directory, '*.yml')):
        print(filename)
        with open(filename) as f:
            yaml.load(f)


if __name__ == '__main__':
    main()
