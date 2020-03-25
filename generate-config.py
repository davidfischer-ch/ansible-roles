#!/usr/bin/env python

import argparse, collections, datetime, subprocess, yaml

import jinja2

OPTIONS_BLACKLIST = {
    'CONNECTION_FACTS_MODULES',
    'DEFAULT_HANDLER_INCLUDES_STATIC',  # Deprecated even if not marked as deprecated...
    'DEFAULT_SQUASH_ACTIONS',           # Deprecated even if not marked as deprecated...
    'DEFAULT_TASK_INCLUDES_STATIC',     # Deprecated even if not marked as deprecated...
}
OPTIONS_DISABLED = {
    'DEFAULT_VAULT_IDENTITY_LIST',  # Default value is broken, at least using this tool
}

TEMPLATE = """# Generator: ./generate-config.py
# Date: {{ date }}
{% for section, options in config.items()|sort %}
[{{ section }}]
{%- for key, default, name, description, enabled in options|sort %}
{% for line in description %}
# {{ line }}
{%- endfor %}
{% if enabled %}{{ key }} = {{ default }}{% else %}# {{ key }} ={% endif -%}
{%- endfor %}
{% endfor -%}"""


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     epilog='Generate ansible.cfg based on ansible-config.')
    parser.add_argument('-o', '--filename', default='ansible.cfg.generated')
    args = parser.parse_args()

    config = collections.defaultdict(set)
    for section, key, meta, enabled in get_options():
        default, description, name = (
            globals()[f'clean_{k}'](meta.get(k))
            for k in ('default', 'description', 'name')
        )
        config[section].add((key, default, name, description, enabled and default is not None))

    templates = jinja2.Environment(loader=jinja2.BaseLoader).from_string(TEMPLATE)
    content = templates.render(config=config, date=datetime.datetime.utcnow())

    with open(args.filename, 'w') as f:
        f.write(content)


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
        if 'deprecatd' in meta or 'deprecated' in ini:
            continue
        key, section = (ini[k] for k in ('key', 'section'))
        if env_name not in OPTIONS_BLACKLIST:
            yield section, key, meta, env_name not in OPTIONS_DISABLED


if __name__ == '__main__':
    main()
