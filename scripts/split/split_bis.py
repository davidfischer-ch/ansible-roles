#!/usr/bin/env python3

from pathlib import Path

from pytoolbox import filesystem

SCRIPTS_DIRECTORY = Path(__file__).absolute().parent.parent
LIBRARY_DIRECTORY = SCRIPTS_DIRECTORY.parent
ROLES_SOURCE_DIRECTORY = LIBRARY_DIRECTORY / 'roles'
ROLES_TARGET_DIRECTORY = LIBRARY_DIRECTORY.parent
README_TEMPLATE = SCRIPTS_DIRECTORY / 'README.md'
REQUIREMENTS_TEMPLATE = SCRIPTS_DIRECTORY / 'requirements.yml'
REQUIREMENTS_FILENAME = ROLES_SOURCE_DIRECTORY / 'requirements.yml'

GITHUB_USER = 'davidfischer-ch'


def main():
    roles = {Path(p).name for p in ROLES_SOURCE_DIRECTORY.glob('*')}
    filesystem.from_template(
        REQUIREMENTS_TEMPLATE,
        REQUIREMENTS_FILENAME,
        values={
            'GITHUB_USER': GITHUB_USER,
            'roles': roles
        },
        jinja2=True)
    print('OK')


if __name__ == '__main__':
    main()
