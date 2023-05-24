#!/usr/bin/env python3

from pathlib import Path
import functools, subprocess, yaml

import termcolor

roles = Path('roles').resolve()
requirements = yaml.safe_load((roles / 'requirements.yml').read_text(encoding='utf-8'))

for requirement in requirements:
    name = requirement['name']

    directory = roles / name
    run = functools.partial(subprocess.run, cwd=directory, capture_output=True)

    status = run(['git', 'pull']).stdout.decode('utf-8')
    print()
    print(termcolor.colored(f'Git pull {name}', 'cyan'))
    print(status)

