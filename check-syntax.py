#!/usr/bin/env python

import yaml

from pytoolbox import filesystem

for filename in sorted(filesystem.find_recursive('.', '*.yml')):
    print(filename)
    with open(filename) as f:
        yaml.load(f)
