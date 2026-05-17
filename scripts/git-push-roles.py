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

    for cmd in (['git', 'push'], ['git', 'push', '--tags']):
        result = run(cmd)
        output = (result.stdout + result.stderr).decode('utf-8').strip()
        label = ' '.join(cmd[1:]) or 'push'
        print()
        print(termcolor.colored(f'Git {label} {name}', 'cyan'))
        if output:
            print(output)
