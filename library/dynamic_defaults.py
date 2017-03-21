#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re

from ansible.module_utils.basic import AnsibleModule, get_platform, get_distribution, get_distribution_version

DOCUMENTATION = r"""
---
module: dynamic_defaults
author: "David Fischer (@davidfischer-ch)"
short_description: Set variables based on operating system.
description:
  - Set variables to defaults using the lookup keys in lower-case: {platform}, {distribution}, {distribution}-{version}.
options:
  hostvars:
    required: true
    description:
      - Simply set it to '{{ hostvars[inventory_hostname] }}'
      - Required to retrieve dynamic defaults and set destination variables only if missing.
  defaults:
    required: true
    description:
      - A dictionary with defaults values.
  must_match:
    required: false
    default: false
    description:
      - Force that at least of the lookup keys is matched.
"""

EXAMPLES = r"""
- dynamic_defaults:
    hostvars: '{{ hostvars[inventory_hostname] }}'
    defaults:
      macosx:
        python_versions:
          - 2.7
      ubuntu-14.04:
        ruby_packages:
          - ruby
          - ruby-dev
      ubuntu-16.04:
        python_versions:
          - 2.7
          - 3.5
"""


def main():
    # See https://newrelic.com/infrastructure/pricing (CPU Cores + GB RAM) x hours used
    module = AnsibleModule(argument_spec=dict(
            hostvars=dict(required=True, type='dict'),
            defaults=dict(required=True, type='dict'),
            must_match=dict(required=False, default=False, type='bool')
        ),
        supports_check_mode=True
    )
    hostvars, defaults, must_match = (module.params[k] for k in ('hostvars', 'defaults', 'must_match'))
    distribution = get_distribution()
    lookup_keys = tuple(k.replace('/', '-').lower() for k in (
        '-'.join([distribution, get_distribution_version()]), distribution, get_platform()
    ))
    facts, match = {}, False
    for lookup_key in lookup_keys:
        for key, variables in defaults.items():
            if re.match('^%s$' % key, lookup_key):
                match = True
                for name, value in variables.items():
                    if name not in hostvars:
                        facts.setdefault(name, value)
    if must_match and not match:
        module.fail_json(msg='No match found, lookup keys %s.' % (lookup_keys, ))
    module.exit_json(ansible_facts=facts, changed=True, diff={
        'before': {}, 'after': {'facts': facts, 'lookup_keys': lookup_keys}
    })

if __name__ == '__main__':
    main()
