import errno, os, re, sys

from ansible.module_utils.basic import AnsibleModule

PY2 = sys.version_info[0] < 3
if PY2:
    import ConfigParser as configparser, io
else:
    import configparser

DOCUMENTATION = r"""
---
module: kernel_facts
author: "David Fischer (@davidfischer-ch)"
short_description: Gather facts about the GNU/Linux Kernel configuration.
options:
  release:
    required: false
    default: null
    description:
      - Release to scan, defaults to active Kernel.
"""

EXAMPLES = r"""
- kernel_facts:
"""

CONFIG_PREFIX = re.compile(r'^config_')
DRIVER_IN_KERNEL = 'y'
DRIVER_HAS_MODULE = 'm'


def main():
    module = AnsibleModule(
        argument_spec=dict(
            release=dict(default=None)
        ),
        supports_check_mode=True
    )
    module.exit_json(
        changed=False,
        ansible_facts=dict(
            kernel_config=get_kernel_config()
        )
    )


def get_kernel_config(release=None):
    # Using index on os.uname() to be retro-compatible with old python releases
    try:
        with open('/boot/config-{0}'.format(release or os.uname()[2])) as f:
            config = configparser.ConfigParser()
            config_string = '[kernel]' + f.read()
            config.readfp(io.BytesIO(config_string)) if PY2 else config.read_string(config_string)
    except IOError as e:
        if e.errno == errno.ENOENT:
            return {}
        raise
    return {CONFIG_PREFIX.sub('', k): v for k, v in config.items('kernel')}


if __name__ == '__main__':
    main()
