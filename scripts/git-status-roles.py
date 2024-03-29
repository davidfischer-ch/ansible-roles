#!/usr/bin/env python3

from pathlib import Path
import functools, os, subprocess, yaml

import termcolor

roles = Path('roles').resolve()
requirements = yaml.safe_load((roles / 'requirements.yml').read_text(encoding='utf-8'))

for requirement in requirements:
    name = requirement['name']

    directory = roles / name
    run = functools.partial(subprocess.run, cwd=directory, capture_output=True)

    status = run(['git', 'status', '.']).stdout.decode('utf-8')
    if status.count(os.linesep) > 9:
        print()
        print(termcolor.colored(f'Status of {name}', 'cyan'))
        print(status)

