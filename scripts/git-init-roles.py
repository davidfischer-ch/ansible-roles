#!/usr/bin/env python3

from pathlib import Path
import functools, shutil, subprocess, tempfile, yaml

import termcolor

roles = Path('roles').resolve()
requirements = yaml.safe_load((roles / 'requirements.yml').read_text(encoding='utf-8'))

for requirement in requirements:
    name = requirement['name']
    url = requirement['src']
    version = requirement['version']

    url = url.replace('https://', 'git@').replace('github.com/', 'github.com:') + '.git'
    target = roles / name
    target_git = target / '.git'

    run = functools.partial(subprocess.run, cwd=target, capture_output=True)

    print()
    print(termcolor.colored(f'Git init {name}', 'cyan'))

    if target_git.exists():
        shutil.rmtree(target_git)

    with tempfile.TemporaryDirectory() as source:
        source_git = Path(source) / '.git'
        print(f'Cloning version {version} from {url}')
        run(['git', 'clone', url, source, '--branch', version])
        # bugs.python.org/issue32689
        shutil.move(str(source_git), target_git)

