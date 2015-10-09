#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
    Cleanup Ubuntu Phone packages.

    :author: David Fischer <david.fischer.ch@gmail.com>
    :copyright: (c) 2015 David Fischer. All rights reserved.
"""

import argparse, re
from subprocess import check_output

__all__ = ('cleanup', 'main')

PACKAGE_REGEX = re.compile(r'^(?P<package>^\S+)\s+install$', re.MULTILINE)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     epilog='Cleanup Ubuntu Phone packages.')
    parser.add_argument('-k', '--keyboards', type=csv_list)
    args = parser.parse_args()
    print(' '.join(cleanup(args.keyboards or [])))


def cleanup(keyboards):
    keyboards.append('data')
    keyboards = {'ubuntu-keyboard-{0}'.format(k) for k in keyboards}
    extra_keyboards = sorted(set(p for p in get_packages() if p.startswith('ubuntu-keyboard-')) - keyboards)
    extra_keyboards = []  # FIXME Ubuntu Touch requires all keyboard packages...
    if extra_keyboards:
        check_output(['apt-get', 'remove'] + extra_keyboards)
    return extra_keyboards


def csv_list(value):
    return value.split(',')


def get_packages():
    return PACKAGE_REGEX.findall(check_output(['dpkg', '--get-selections']).decode('utf-8'))


if __name__ == '__main__':
    main()
