#!/usr/bin/env python

import collections, datetime, subprocess, yaml

import jinja2

OPTIONS_BLACKLIST = {
    'CONNECTION_FACTS_MODULES',
    'DEFAULT_HANDLER_INCLUDES_STATIC',
    'DEFAULT_REMOTE_PORT',
    'DEFAULT_SQUASH_ACTIONS',
    'DEFAULT_TASK_INCLUDES_STATIC',
}

TEMPLATE = """
# Generator: ./generate-config.py
# Date: {{ date }}
{% for section, options in config.items()|sort %}
[{{ section }}]
{%- for key, default, name, description in options|sort %}
{% for line in description %}
# {{ line }}
{%- endfor %}
{{ key }}={{ default }}
{%- endfor %}
{% endfor -%}
"""


def main():
    'Generate ansible.cfg based on ansible-config.'

    config = collections.defaultdict(set)
    for section, key, meta in get_options():
        default, description, name = (
            globals()[f'clean_{k}'](meta.get(k))
            for k in ('default', 'description', 'name')
        )
        config[section].add((key, default, name, description))

    templates = jinja2.Environment(loader=jinja2.BaseLoader).from_string(TEMPLATE)
    with open('ansible.cfg', 'w') as f:
        f.write(templates.render(config=config, date=datetime.datetime.utcnow()))


def clean_default(value):
    return ','.join(sorted(value)) if isinstance(value, (list, set, tuple)) else value


def clean_description(value):
    return (value, ) if isinstance(value, str) else tuple(value)


def clean_name(value):
    return value or ''


def get_options():
    content = yaml.safe_load(subprocess.check_output(['ansible-config', 'list']))
    for env_name, meta in content.items():
        try:
            ini = meta['ini'][0]
        except KeyError:
            continue  # This option cannot be defined in the ini file
        if 'deprecated' in ini:
            continue
        key, section = (ini[k] for k in ('key', 'section'))
        if env_name not in OPTIONS_BLACKLIST:
            yield section, key, meta


if __name__ == '__main__':
    main()

