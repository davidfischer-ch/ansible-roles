==================
Role ansible-tower
==================

------
Status
------

Alpha


-------
Example
-------

Inventory
=========

hosts:

```
[tower-group]
local-tower-server

[vagrant-group]
localhost
```

group_vars/all:

```
ansible_ssh_private_key_file: "{{ lookup('env', 'HOME') }}/.ssh/id_rsa"
```

group_vars/local:

```
ansible_port: 22
ansible_user: vagrant
ansible_ssh_pass: vagrant
ansible_become_pass: vagrant
ansible_ssh_common_args: '-o StrictHostKeyChecking=no'

ssh_authorized_keys:
  - "{{ lookup('env', 'HOME') }}/.ssh/id_rsa.pub"

locale: fr_CH.UTF-8
timezone: Etc/UTC

mounts: {}

desktop_package: null
upgrade_packages_async: '{{ omit }}'  # FIXME https://github.com/ansible/ansible/issues/14568

register_ssh_host: yes
```

host_vars/localhost:

```
ansible_connection: local

ssh_authorized_keys: []

vagrant_machines:
  tower:
    cpus: 2
    memory: 2048
    host_public: 192.168.56.2
    name: ubuntu/trusty64
    provider: virtualbox
```

host_vars/local-tower-server:

```
ansible_host: 192.168.56.2

python_versions: []

ansible_tower_admin_password: ****
ansible_tower_cache_password: ****
ansible_tower_database_password: ****
ansible_tower_instance_name: tower-test
ansible_tower_version: 3.0.3
```

PlayBook
========

```
---

# Provisioning

- hosts:
    - vagrant-group
  roles:
    - vagrant

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

# DevOps Services

- hosts:
    - tower-group
  roles:
    - ansible-tower
```
