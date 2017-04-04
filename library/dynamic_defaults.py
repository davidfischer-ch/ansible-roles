#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re

from ansible.module_utils.basic import AnsibleModule

LOOKUP_KEYS = [
    '{ansible_distribution}-{ansible_distribution_version}',
    '{ansible_distribution}',
    '{ansible_system}'
]

DOCUMENTATION = r"""
---
module: dynamic_defaults
author: "David Fischer (@davidfischer-ch)"
short_description: Set variables based on operating system.
description:
  - Set variables to defaults using the lookup keys in lower-case and with / replaced by -.
  - Set a variable dynamic_defaults_outputs to a list of (keys, resulting facts).
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
  lookup_keys:
    required: false
    default: %s
    description:
      - Keys used to retrieve defaults, order matters.
  must_match:
    required: false
    default: false
    description:
      - Force that at least of the lookup keys is matched.
""" % (LOOKUP_KEYS, )

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
            lookup_keys=dict(required=False, default=LOOKUP_KEYS, type='list'),
            must_match=dict(required=False, default=False, type='bool')
        ),
        supports_check_mode=True
    )
    hostvars, defaults, lookup_keys, must_match = (
        module.params[k] for k in ('hostvars', 'defaults', 'lookup_keys', 'must_match')
    )
    lookup_keys = tuple(k.format(**hostvars).replace('/', '-').lower() for k in lookup_keys)
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
    outputs = facts.get('dynamic_defaults_outputs', [])
    outputs.append([lookup_keys, facts.copy()])
    facts['dynamic_defaults_outputs'] = outputs
    module.exit_json(ansible_facts=facts, changed=False)

if __name__ == '__main__':
    main()
