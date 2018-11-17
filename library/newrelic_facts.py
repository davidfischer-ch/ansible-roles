#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import multiprocessing

import psutil
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r"""
---
module: newrelic_facts
author: "David Fischer (@davidfischer-ch)"
short_description: Gather facts about host such as New Relic CU for pricing purposes. Requires psutil python module.
options:
  hours:
    required: false
    default: 730
    description:
      - Number of hours per month the host is running.
      - Default value is average hours per month (365 * 24 / 12).
"""

EXAMPLES = r"""
- newrelic_facts:
"""


def main():
    # See https://newrelic.com/infrastructure/pricing (CPU Cores + GB RAM) x hours used
    module = AnsibleModule(
        argument_spec=dict(
            hours=dict(default=730, type='int')
        ),
        supports_check_mode=True
    )
    module.exit_json(changed=False, ansible_facts=dict(
        newrelic_cu=(
            multiprocessing.cpu_count() + psutil.virtual_memory().total // 1000 ** 3
        ) * module.params['hours']
    ))


if __name__ == '__main__':
    main()
