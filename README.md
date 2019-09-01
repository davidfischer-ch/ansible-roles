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

See django-site role's [README](roles/django-site/README.md) and [example]/examples/django-dev/).

### Mounting a S3 bucket with s3fs

See s3fs role's [README](roles/s3fs/README.md).

### Seafile Professional Server

See:

* seafile role's [README](roles/seafile/README.md) and [example](examples/seafile-vm/).

### Setup a PostgreSQL server with an application DB

See:

* postgresql role's [README](roles/postgresql/README.md).
* postgresql-databases role's [README](roles/postgresql-databases/README.md).

### Installing AWS utilities

See cloudwatch-logs-agent role's [README](roles/cloudwatch-logs-agent/README.md).

2014-2019 - David Fischer
