#!/usr/bin/env python3

import functools, os, shutil, subprocess, tempfile, yaml
from pathlib import Path

roles = Path('roles').resolve()

with open(roles / 'requirements.yml') as f:
    requirements = yaml.safe_load(f.read())


for requirement in requirements:
    name = requirement['name']

    directory = roles / name
    run = functools.partial(subprocess.run, cwd=directory, capture_output=True)

    status = run(['git', 'status', '.']).stdout.decode('utf-8')
    if status.count(os.linesep) > 9:
        print()
        print(f'[{name}] Status')
        print(status)
