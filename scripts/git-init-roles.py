#!/usr/bin/env python3

import functools, shutil, subprocess, tempfile, yaml
from pathlib import Path

roles = Path('roles').resolve()

with open(roles / 'requirements.yml') as f:
    requirements = yaml.safe_load(f.read())

for requirement in requirements:
    name = requirement['name']
    url = requirement['src']
    version = requirement['version']

    url = url.replace('https://', 'git@').replace('github.com/', 'github.com:') + '.git'
    target = roles / name
    target_git = target / '.git'

    run = functools.partial(subprocess.run, cwd=target, capture_output=True)

    if target_git.exists():
        print(f'[{name}] Remove {target_git}')
        shutil.rmtree(target_git)

    with tempfile.TemporaryDirectory() as source:
        source_git = Path(source) / '.git'
        print(f'[{name}] Cloning version {version} from {url}')
        run(['git', 'clone', url, source, '--branch', version])
        # bugs.python.org/issue32689
        shutil.move(str(source_git), target_git)
