#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import collections, itertools, json, os, subprocess

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r"""
---
module: drupal_toggle_modules
author: "David Fischer (@davidfischer-ch)"
short_description: Toggle Drupal modules.
options:
  path:
    required: true
    description:
      - The web root.
  enable:
    required: false
  disable:
    required: false
  drush:
    required: false
    default: vendor/bin/drush
"""

EXAMPLES = r"""
- drupal_toggle_modules: path=/var/www/my-site enable=admin_menu,content_access disable=ctools
"""


def main():
    module = AnsibleModule(
        argument_spec=dict(
            drush=dict(required=False, type='path', default='vendor/bin/drush'),
            path=dict(required=True, type='path'),
            enable=dict(required=False, type='list'),
            disable=dict(required=False, type='list')
        ),
        supports_check_mode=True
    )
    drush, path, enable, disable = (
        module.params[k] for k in ('drush', 'path', 'enable', 'disable')
    )
    try:
        updated_modules = toggle_drupal_modules(
            drush,
            path,
            enable=enable,
            disable=disable,
            simulate=module.check_mode)
    except MissingModuleError as e:
        module.fail_json(msg=str(e))
    module.exit_json(changed=bool(updated_modules), diff=updated_modules)


class MissingModuleError(RuntimeError):
    pass


def get_drupal_modules(drush, directory):
    return json.loads(
        subprocess.check_output(
            [drush, 'pm-list', '--format=json'],
            cwd=directory,
            env=get_drush_environment())
    )


def get_drush_environment():
    if not get_drush_environment.env:
        get_drush_environment.env = os.environ.copy()  # https://github.com/drush-ops/drush/issues/2025
        get_drush_environment.env['PATH'] = '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
    return get_drush_environment.env
get_drush_environment.env = None


def toggle_drupal_modules(drush, directory, enable=None, disable=None, simulate=False):
    modules = get_drupal_modules(drush, directory)
    toggle_modules, updated_modules = collections.defaultdict(list), []
    for module, state in itertools.chain(
        ((m, 'enabled') for m in enable),
        ((m, 'disabled') for m in disable)
    ):
        if module not in modules:
            raise MissingModuleError('Module {0} is not installed.'.format(module))
        status = modules[module]['status'].lower()
        if status != state:
            toggle_modules[state].append(module)
            updated_modules.append({
                'after': state + os.linesep, 'after_header': module,
                'before': status + os.linesep, 'before_header': module
            })
    if not simulate:
        for state, action in ('disabled', 'dis'), ('enabled', 'en'):
            modules_for_action = toggle_modules[state]
            if modules_for_action:
                subprocess.check_call([drush, action, '-y'] + modules_for_action, cwd=directory)
    return updated_modules


if __name__ == '__main__':
    main()
