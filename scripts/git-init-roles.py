#!/usr/bin/env python3

import functools, os, shutil, subprocess, tempfile, yaml
from pathlib import Path

roles = Path('roles').resolve()

with open(roles / 'requirements.yml') as f:
    requirements = yaml.safe_load(f.read())


for requirement in requirements:
    name = requirement['name']
    src = requirement['src']
    version = requirement['version']

    directory = roles / name
    git_directory = directory / 'git'
    run = functools.partial(subprocess.run, cwd=directory, capture_output=True)

    if git_directory.exists():
        print(f'[{name}] Remove {git_directory}')
        shutil.rmtree(git_directory)

    with tempfile.TemporaryDirectory() as tmp:
        print(f'[{name}] Cloning version {version} from {src}')
        run(['git', 'clone', src, tmp, '--branch', version])
        shutil.move(Path(tmp) / '.git', git_directory)
