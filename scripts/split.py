#!/usr/bin/env python3

import glob, os, subprocess
from pathlib import Path

from pytoolbox import filesystem
from pytoolbox.subprocess import rsync
from requests import post, put

ANSIBLE_ROLES_DIRECTORY = Path('ansible-roles').absolute()
ROLES_SOURCE_DIRECTORY = ANSIBLE_ROLES_DIRECTORY / 'roles'
ROLES_TARGET_DIRECTORY = Path('roles').absolute()
README_TEMPLATE = Path('README.md').absolute()

GITHUB_API = 'https://api.github.com'
GITHUB_USER = 'davidfischer-ch'
GITHUB_AUTH = (GITHUB_USER, 'a4***')

MESSAGE = 'Extract role from library'

PATHS = [
    '.gitattributes',
    'ansible.cfg',
    'ansible.cfg.orig',
    'check-syntax.py',
    'common.yml',
    'devices.yml',
    'django-stack.yml',
    'elk-stack.yml',
    'example',
    'examples',
    'inventory',
    'library',
    'playbooks',
    'plugins',
    'README.md',
    'README.rst',
    'requirements.pip2',
    'requirements.pip3',
    'requirements.txt',
    'roles/ansible-fork',
    'roles/celery',
    'roles/requirements',
    'roles_todo',
    'sharing-servers.yml',
    'site.yml',
    'TODO.rst'
]


def main():
    roles = {Path(p).name for p in glob.glob(str(ROLES_SOURCE_DIRECTORY / '*'))}
    ROLES_TARGET_DIRECTORY.mkdir(exist_ok=True)
    for role in sorted(roles):
        process_role(role, roles)
    print('OK')


def create_github_repo(role):
    post(
        f'{GITHUB_API}/user/repos',
        auth=GITHUB_AUTH,
        json={
            'name': f'ansible-role-{role}',
            'description': f'Ansible role for {role}',
            'homepage': f'https://github.com/{GITHUB_USER}/ansible-roles',
            'private': False,
            'has_issues': True,
            'has_projects': True,
            'has_wiki': True
        })
    put(
        f'{GITHUB_API}/repos/{GITHUB_USER}/ansible-role-{role}/topics',
        auth=GITHUB_AUTH,
        json={'names': ['ansible', role]})
    return f'git@github.com:{GITHUB_USER}/ansible-role-{role}.git'


def process_role(role, roles):
    directory = ROLES_TARGET_DIRECTORY / f'ansible-role-{role}'
    if not directory.exists():
        print('Create role', role)
        try:
            rsync(ANSIBLE_ROLES_DIRECTORY, directory, destination_is_dir=True)
            os.chdir(directory)
            paths = PATHS + [f'roles/{r}' for r in roles - {role}]
            print('\tFiltering')
            subprocess.check_output([
                'git', 'filter-branch', '--force', '--index-filter',
                f"git rm --cached --ignore-unmatch -r {' '.join(paths)}",
                '--prune-empty', '--tag-name-filter', 'cat', '--', '--all'
            ])
            for path in (Path('roles') / role).glob('*'):
                print('\tMove directory', path.name)
                subprocess.check_output(['git', 'mv', path, path.name])
            subprocess.check_output(['git', 'clean', '-f', '-d'])
            print('\tGenerate README')
            filesystem.from_template(README_TEMPLATE, 'README.md', values={
                'has_meta': Path('meta').exists(),
                'role': role
            }, jinja2=True)
            subprocess.check_output(['git', 'add', 'README.md'])
            subprocess.check_output(['git', 'commit', '-m', MESSAGE])
            print('\tJob done!')
        except Exception:
            filesystem.remove(directory, recursive=True)
            raise
    print('Push role', role)
    os.chdir(directory)
    url = create_github_repo(role)
    subprocess.check_call(['git', 'remote', 'remove', 'origin'])
    subprocess.check_call(['git', 'remote', 'add', 'origin', url])
    subprocess.check_call(['git', 'push', '--all'])


if __name__ == '__main__':
    main()
