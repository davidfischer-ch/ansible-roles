#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os, re, shutil

from ansible.module_utils.basic import AnsibleModule

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
  ok_flag:
    required: false
    default: null
    description:
      - A file inside the release directory that flags the release as complete.
      - WARNING: All releases without the flag will ALWAYS be removed!
      - Default value means this feature is disabled.
  regexp:
    required: true
    description:
      - The regular expression to look for in the name of the releases directories.
        Uses Python regular expressions; see U(http://docs.python.org/2/library/re.html).
"""

EXAMPLES = r"""
- cleanup_releases: directory=/var/app/releases keep=3 regexp=release-[0-9]{3}
- cleanup_releases: directory=/var/app/releases keep=3 ok_flag=ok.flag regexp=[0-9]{8}T[0-9]{6}
"""


def main():
    module = AnsibleModule(
        argument_spec=dict(
            directory=dict(required=True, type='path'),
            keep=dict(default=None, type='int'),
            ok_flag=dict(default=None),
            regexp=dict(required=True)
        ),
        supports_check_mode=True
    )
    directory, keep, ok_flag, regexp = (module.params[k] for k in ('directory', 'keep', 'ok_flag', 'regexp'))
    regexp = re.compile(regexp)
    if keep is not None and keep < 1:
        module.fail_json(msg="'keep' should be a positive number")

    releases, remove_releases = set(os.path.join(directory, r) for r in os.listdir(directory) if regexp.match(r)), set()
    if ok_flag is not None:
        remove_releases = set(r for r in releases if not os.path.exists(os.path.join(r, ok_flag)))
        releases = releases - remove_releases
    if keep is not None:
        remove_releases.update(sorted(releases, reverse=True)[keep:])
    remove_releases = sorted(remove_releases, reverse=True)  # For cosmetic reasons
    diff = [{'after': 'absent', 'after_header': r, 'before': get_state(r), 'before_header': r} for r in remove_releases]
    if not module.check_mode:
        for release in remove_releases:
            if os.path.isdir(release):
                shutil.rmtree(release)
            else:
                os.remove(release)
    module.exit_json(changed=bool(remove_releases), diff=diff)


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

if __name__ == '__main__':
    main()
