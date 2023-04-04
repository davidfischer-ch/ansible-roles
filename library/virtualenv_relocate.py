import fnmatch, itertools, os, re, shutil

from ansible.module_utils.basic import AnsibleModule

# FIXME report changed only if content changed when operation is 'none'.

DOCUMENTATION = r"""
---
module: virtualenv_relocate
author: "David Fischer (@davidfischer-ch)"
short_description: Copy or move a Python virtualenv directory without breaking it.
description:
  - This module will copy or move source directory to/as destination directory.
  - This module will update Python resources in destination (replace source by destination path).
options:
  source:
    required: true
    description:
      - The source Python virtualenv.
  destination:
    required: true
    default: null
    description:
      - The destination, must not exist.
  operation:
    required: true
    choices: [copy, move, none]
    description:
      - The operation to do just before fixing paths.
      - copy means you want the source to be copied to destination.
      - move means you want the source to me moved to destination.
      - none means you only need to fix an already duplicated venv.
  encoding:
    required: false
    default: 'utf-8'
    description:
      - Paths are converted from string of given encoding to bytes.
"""

EXAMPLES = r"""
- virtualenv_relocate:
    source: /var/app/my-app/test
    destination: /var/app/releases/alpha
    operation: copy
"""


def main():
    module = AnsibleModule(
        argument_spec=dict(
            source=dict(required=True, type='path'),
            destination=dict(required=True, type='path'),
            operation=dict(required=True, choice=['copy', 'move', 'none']),
            encoding=dict(default='utf-8')
        ),
        supports_check_mode=True
    )
    source, destination, operation, encoding = (
        module.params[k] for k in ('source', 'destination', 'operation', 'encoding')
    )
    if operation == 'none':
        if not os.path.exists(destination):
            module.fail_json(msg='Destination does not exist.')
    else:
        if not os.path.exists(source):
            module.fail_json(msg='Source does not exist.')
        if os.path.exists(destination):
            module.fail_json(msg='Destination already exist.')
    if not module.check_mode:
        if operation == 'copy':
            shutil.copytree(source, destination, symlinks=True)
        elif operation == 'move':
            shutil.move(source, destination)
        relocate(source, destination, encoding)
    module.exit_json(changed=True)


def find_recursive(directory, patterns):
    """Simplified version of https://github.com/davidfischer-ch/pytoolbox/blob/master/pytoolbox/filesystem.py#L34."""
    patterns = [re.compile(fnmatch.translate(p)) for p in patterns]
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if any(p.match(filename) for p in patterns):
                yield os.path.join(dirpath, filename)


def relocate(source_directory, destination_directory, encoding='utf-8'):
    """Modified version of https://github.com/davidfischer-ch/pytoolbox/blob/master/pytoolbox/virtualenv.py."""
    b_source_directory = source_directory.encode(encoding)
    b_destination_directory = destination_directory.encode(encoding)

    for path in itertools.chain.from_iterable([
        find_recursive(destination_directory, ['*.egg-link', '*.pth', '*.pyc', 'RECORD']),
        find_recursive(os.path.join(destination_directory, 'bin'), ['*']),
        find_recursive(os.path.join(destination_directory, 'src'), ['*.so'])
    ]):
        if os.path.islink(path):
            continue  # Do not follow symbolic links
        with open(path, 'r+b') as f:
            content = f.read()
            updated_content = content.replace(b_source_directory, b_destination_directory)
            if updated_content != content:
                f.seek(0)
                f.write(updated_content)
                f.truncate()


if __name__ == '__main__':
    main()
