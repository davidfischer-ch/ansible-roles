================
Role django-site
================

------
Status
------

Alpha

Not (yet) implemented:

* Role actions such as configure, local-backup, local-restore, manage, ...
* Mounting the data directory. I think this roles should not take this responsibility. When deploying more than one web host, make sure your PlayBook mount the data directory prior to calling this role.

-------
Example
-------

Code Repository
===============

Structure:

```
website$ tree -L 3
.
├── config.yml
└── src
    └── myproject
        ├── myproject
        ├── contact
        ├── locale
        ├── manage.py
        ├── news
        ├── offices
        ├── pages
        ├── publications
        ├── requirements.install.pip2
        └── templates

8 directories, 3 files
```

Settings are templates that will be rendered with the Ansible `template` module:

```
website$ tree src/myproject/myproject/settings/
src/myproject/myproject/settings/
├── base.py.j2
├── develop.py.j2
├── __init__.py.j2
└── production.py.j2

0 directories, 4 files
```

Automation configuration file `config.yml`:

```
configuration_templates:
  - settings/__init__.py
  - settings/base.py
  - settings/develop.py
  - settings/production.py
custom_applications:
  - contact
  - news
  - offices
  - pages
  - publications
python_version: '3.5'
source_path: src/myproject
```

PlayBook
========

```
---

# Management

- hosts:
    - localhost
  roles:
    - register-ssh-hosts

# Common Services

- hosts:
    - all:!localhost
  roles:
    - bootstrap
    - fail2ban
    - ufw
    - miscellaneous
    - kernel
    - python
    - mounts
    - rsync

# Application Services

- hosts:
    - my-site-cache-group
  roles:
    - redis

- hosts:
    - my-site-db-group
  roles:
    - postgresql

- hosts:
    - my-site-storage-group
  roles:
    - nfs

# TODO: Mount shared storage

- hosts:
    - my-site-web-group
  roles:
    - django-site
    - nginx
    - uwsgi
  vars:
    djsite_role_action: setup
    djsite_sass_enabled: yes

    nginx_sites:
      site:
        name: '{{ djsite_instance_name }}'
        config_file: '{{ roles_directory }}/django-site/templates/example.nginx.config.conf.j2'
        debug: '{{ djsite_debug_enabled|bool }}'
        domain: '{{ djsite_domain }}'
        redirect_ssl: '{{ djsite_redirect_ssl|bool }}'
        with_dhparam: '{{ djsite_ssl_enabled|bool }}'
        with_ssl: '{{ djsite_ssl_enabled|bool }}'

    uwsgi_apps:
      application:
        name: '{{ djsite_instance_name }}'
        config_file: '{{ roles_directory }}/django-site/templates/example.uwsgi.app.xml.j2'
        user: '{{ djsite_daemon_user }}'
        group: '{{ djsite_daemon_group }}'
        path: '{{ djsite_app_directory }}/production'
        project: '{{ djsite_project }}'
        python_version: python
        limit_as: 2048
```
