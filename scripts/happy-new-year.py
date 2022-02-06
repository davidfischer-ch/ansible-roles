#!/usr/bin/env python3

import datetime, functools, re, subprocess, sys, yaml
from pathlib import Path

YEAR_REGEX = re.compile(r'2014-(\d+) - David Fischer')
YEAR = str(datetime.datetime.today().year)

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
    target_readme = target / 'README.md'

    if not target_readme.exists():
        continue

    run = functools.partial(subprocess.run, cwd=target, capture_output=True)

    print(f'[{name}] Set year to {YEAR}')
    if not target_git.exists():
        sys.exit(f'[{name}] Error: {target_git} is missing, run git-init-roles.py first')

    with target_readme.open('r') as f:
        content = f.read()

    assert content
    content = YEAR_REGEX.sub(f'2014-{YEAR} - David Fischer', content)
    print(content)

    with target_readme.open('w') as f:
        f.write(content)

    run(['git', 'add', 'README.md'])
    run(['git', 'commit', 'README.md', '-m', f'Happy {YEAR}'])
    run(['git', 'push'], capture_output=False)
