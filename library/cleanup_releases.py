#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os, re

from ansible.module_utils.basic import AnsibleModule
from pytoolbox.filesystem import try_remove

DOCUMENTATION = r"""
---
module: cleanup_releases
author: "David Fischer (@davidfischer-ch)"
short_description: Remove oldest releases directories named according to an incremental pattern such as a date-time.
description:
  - This module will remove oldest releases directories found in a releases directory.
  - This module should be called at the end of the release process.
options:
  directory:
    required: true
    description:
      - The directory in which the releases directories are stored.
  keep:
    required: false
    default: null
    description:
      - Number of releases to keep.
      - Default value means keep all.
  regexp:
    required: false
    default: '[0-9]{8}T[0-9]{12}'
    description:
      - Default corresponds to a short ISO 8601 date-time.
      - The regular expression to look for in the name of the releases directories.
        Uses Python regular expressions; see U(http://docs.python.org/2/library/re.html).
"""

EXAMPLES = r"""
- cleanup_releases: directory=/var/app/releases keep=3
- cleanup_releases: directory=/var/app/releases keep=3 regexp='release-[0-9]{3}'
"""


def get_state(b_path):
    # https://github.com/ansible/ansible-modules-core/blob/bf5b3de83eae72e0602ce2418a1a547c023ed3fe/files/file.py
    if os.path.lexists(b_path):
        if os.path.islink(b_path):
            return 'link'
        if os.path.isdir(b_path):
            return 'directory'
        if os.stat(b_path).st_nlink > 1:
            return 'hard'
        # could be many other things, but defaulting to file
        return 'file'
    return 'absent'


def main():
    module = AnsibleModule(
        argument_spec=dict(
            directory=dict(required=True, type='path'),
            keep=dict(default=None, type='int'),
            regexp=dict(default=r'[0-9]{8}T[0-9]{12}')
        ),
        supports_check_mode=True
    )
    directory, keep, regexp = (module.params[k] for k in ('directory', 'keep', 'regexp'))
    regexp = re.compile(regexp)
    if keep is not None and keep < 1:
        module.fail_json(msg="'keep' should be a positive number")

    # FIXME first should be removed releases that don't have the "complete" flag
    releases = (os.path.join(directory, r) for r in os.listdir(directory) if regexp.match(r))
    oldest_releases = [] if keep is None else sorted(releases, reverse=True)[keep:]
    before = [{'path': r, 'state': get_state(r)} for r in oldest_releases]
    if not module.check_mode:
        for release in oldest_releases:
            try_remove(release, recursive=True)
    module.exit_json(changed=bool(oldest_releases), diff={
        'after': [{'path': r, 'state': 'absent'} for r in oldest_releases], 'before': before
    })

if __name__ == '__main__':
    main()
