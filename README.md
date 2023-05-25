# Ansible Library

Library of Ansible plugins and roles for deploying various services.

This library is covering multiple use-cases:

* Deploying a full Django stack
* Deploying a full LAMP stack
* Deploying an ELK stack (work in progress)
* Deploying an Ampache server
* Deploying a GitLab server using Omnibus
* Deploying an ownCloud server or client
* Deploying a SeaFile server or client
* Installing a {development, multimedia, ...} computer under Debian/Ubuntu
* Tweaking an Ubuntu Phone (never install nfs-client!)
* ...

The roles are generic enough to be usable as-is.

## Scripts

### Development Tools

- [check-syntax.py](scripts/check-syntax.py) : Check YAML syntax of a whole file tree.
- [git-init-roles.py](scripts/git-init-roles.py) : Convert roles from "ansible-galaxy copies" to proprer "git clones". Useful when working on roles.
- [git-status-roles.py](scripts/git-status-roles.py) : Show the git status of roles when its meaningful (something changed). Useful when working on roles.
- [git-update-roles.py](scripts/git-update-roles.py) : Iterate over all roles and do `git pull`. Usefull when working on roles.
- [happy-new-year.py](scripts/happy-new-year.py) : Iterate over all roles and refresh end-year with current year. Usefull or not, that is the question.
- [refresh-roles.sh](scripts/refresh-roles.sh) : Use ansible-galaxy to install/update roles in roles/ directory. Roles are listed in [requirements.yml](roles/requirements.yml).

### Legacy

- [generate-config.py](scripts/generate-config.py) : Generate `ansible.cfg` with `ansible-config`.
- [split/](scripts/split/) : Scripts used to split this library in many repositories.


## Examples

### An Ubuntu Desktop Computer

#### PlayBook

```
---

- import_playbook: roles-df/playbooks/devices.yml

- hosts:
    - seafile-client
  roles:
    - seafile-client
```

#### Inventory

```
[gaming]
my-computer

[laptop]
my-computer

[seafile-client]
my-computer
```

#### Variables

```
ansible_connection: local
ansible_host: 127.0.0.1
ansible_port: 22
ansible_user: me
ssh_port: 22
user: '{{ ansible_user }}'
group: '{{ ansible_user }}'
desktop_package: ubuntu-desktop
java_packages:
  - icedtea-8-plugin
  - openjdk-8-jre
extra_apt_repositories:
  - ppa:nilarimogard/webupd8
extra_packages:
  - nvidia-prime
  - prime-indicator
```

### Django Development Server

See django-site role's [README](https://github.com/davidfischer-ch/ansible-role-django-site/blob/master/README.md) and [example](examples/django-dev/).

### Mounting a S3 bucket with s3fs

See s3fs role's [README](https://github.com/davidfischer-ch/ansible-role-s3fs/blob/master/README.md).

### Seafile Professional Server

See:

* seafile role's [README](https://github.com/davidfischer-ch/ansible-role-seafile/blob/master/README.md) and [example](examples/seafile-vm/).

### Setup a PostgreSQL server with an application DB

See:

* postgresql role's [README](https://github.com/davidfischer-ch/ansible-role-postgresql/blob/master/README.md).
* postgresql-databases role's [README](https://github.com/davidfischer-ch/ansible-role-postgresql-databases/blob/master/README.md).

### Installing AWS utilities

See cloudwatch-logs-agent role's [README](https://github.com/davidfischer-ch/ansible-role-cloudwatch-logs-agent/blob/master/README.md).

## Versioning

Convention: `v<MAJOR>.<MINOR>.<PATCH>`

### MAJOR Upgrade

Breaking change that cannot be applied as-is on hosts setup using a previous version of the role.
It may requires a migration procedure or some additional code.

Examples:

- A deprecated feature is now removed
- More to come

### MINOR Upgrade

Non-breaking change that cannot be applied as-is without updating the automation using the role.

Requires some changes in the code using the role.

Examples:

- A default value defined in the role is changed or removed
- A variable is renamed or its data scheme is modified
- More to come

### PATCH Upgrade

An update that is assumed to be safe to be applied.

Examples:

- Some bug fixes
- Code or templates refactoring
- There is a new feature (disabled by default)
- There is a new action available (you have to call it)
- Enhanced support of the hundreds Linux distributions

2014-2022 - David Fischer
