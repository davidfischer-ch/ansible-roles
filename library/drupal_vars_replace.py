#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json, os, re, subprocess

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r"""
---
module: drupal_vars_replace
author: "David Fischer (@davidfischer-ch)"
short_description: Update Drupal variables replacing a pattern by a value. Recurse into (dict, list) data structures.
options:
  path:
    required: true
    description:
      - The web root.
  pattern:
    required: true
  value:
    required: true
"""

EXAMPLES = r"""
- drupal_vars_replace: path=/var/www/my-site pattern=my-old-domain.com value=my-new-domain.com
"""


def get_drupal_variables(directory):
    return json.loads(subprocess.check_output(
        ['drush', '-r', directory, 'vget', '--format=json'], env=get_drush_environment()
    ).decode('utf-8'))


def get_drush_environment():
    if not get_drush_environment.env:
        get_drush_environment.env = os.environ.copy()  # https://github.com/drush-ops/drush/issues/2025
        get_drush_environment.env['PATH'] = '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
    return get_drush_environment.env
get_drush_environment.env = None


def replace_drupal_variables(directory, pattern, string, simulate=False):
    updated_variables = []
    regexp = re.compile(pattern)

    def update(value):
        if isinstance(value, dict):
            return {k: update(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [update(v) for v in value]
        return regexp.sub(string, value) if isinstance(value, unicode) else value

    for name, value in get_drupal_variables(directory).items():
        updated_value = update(value)
        if updated_value != value:
            if not simulate:
                set_drupal_variable(directory, name, updated_value)
            updated_variables.append({
                'after': updated_value, 'after_header': name, 'before': value, 'before_header': name
            })
    return updated_variables


def set_drupal_variable(directory, name, value):
    process = subprocess.Popen(['drush', '-r', directory, 'vset', '--format=json', name, json.dumps(value)],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=get_drush_environment())
    (stdout, stderr), returncode = process.communicate(), process.poll()
    if returncode:
        raise ValueError(name, value, stdout, stderr)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(required=True, type='path'),
            pattern=dict(required=True),
            value=dict(required=True)
        ),
        supports_check_mode=True
    )
    path, pattern, value = (module.params[k] for k in ('path', 'pattern', 'value'))
    updated_variables = replace_drupal_variables(path, pattern, value, simulate=module.check_mode)
    module.exit_json(changed=bool(updated_variables), diff=updated_variables)

if __name__ == '__main__':
    main()
