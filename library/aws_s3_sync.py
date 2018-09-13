#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import subprocess

from ansible.module_utils.basic import AnsibleModule

EXTRA_OPTS = ['--sse', '--exact-timestamps']

DOCUMENTATION = r"""
---
module: aws_s3_sync
author: "David Fischer (@davidfischer-ch)"
short_description: Syncs directories and S3 prefixes.
description:
  - This module uses aws s3 sync.
options:
  source:
    required: true
    description:
      - The source bucket (syntax -> s3://<bucket>/<path>/) or directory.
  destination:
    required: true
    description:
      - The destination bucket (syntax -> s3://<bucket>/<path>/) or directory.
  region:
    required: false
    description:
      - AWS region name.
  delete:
    required: false
    default: false
    description:
      - Files that exist in the destination but not in the source are deleted during sync
  excludes:
    required: false
    description:
      - Exclude all files or objects from the command that matches the specified pattern.
  includes:
    required: false
    description:
      - Don't exclude files or objects in the command that match the specified pattern.
  rsync_patterns:
    required: false
    default: true
    description:
      - Set it to True if you are passing "rsync" expressions to excludes and includes.
  extra_opts:
    required: false
    default: %s
    description:
      - Specify additional "aws cli s3" options by passing in an array.
""" % (EXTRA_OPTS, )

EXAMPLES = r"""
- aws_s3_sync: source=s3://my-bucket/some/path/ destination=/local/path/ delete=yes
"""


def main():
    module = AnsibleModule(
        argument_spec=dict(
            source=dict(required=True),
            destination=dict(required=True),
            region=dict(default=None),
            delete=dict(default=False, type='bool'),
            excludes=dict(default=[], type='list'),
            includes=dict(default=[], type='list'),
            rsync_patterns=dict(default=False, type='bool'),
            extra_opts=dict(default=EXTRA_OPTS, type='list'),
        ),
        supports_check_mode=True
    )
    source, destination, region, delete, excludes, includes, rsync_patterns, extra_opts = (
        module.params[k] for k in
        (
            'source',
            'destination',
            'region',
            'delete',
            'excludes',
            'includes',
            'rsync_patterns',
            'extra_opts'
        )
    )

    command = ['aws', 's3', 'sync'] + extra_opts
    if module.check_mode:
        command.append('--dryrun')
    if delete:
        command.append('--delete')
    if region is not None:
        command.extend(['--region', region])

    def pattern(value):
        return (value.lstrip('/') + '*') if rsync_patterns else value

    command.extend('--exclude={0}'.format(pattern(e)) for e in excludes)
    command.extend('--include={0}'.format(pattern(i)) for i in includes)
    command.extend([source, destination])
    diff = subprocess.check_output(command)
    module.exit_json(changed=bool(diff), diff={'after': diff, 'before': ''})


if __name__ == '__main__':
    main()
