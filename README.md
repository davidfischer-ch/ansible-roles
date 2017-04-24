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

- include: roles-df/playbooks/devices.yml

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

See django-site role's [README](roles/django-sites/README.md).

### Mounting a S3 bucket with s3fs

See s3fs role's [README](roles/s3fs/README.md).

### Installing AWS utilities

#### PlayBook

```
- hosts:
    - all:!localhost
  roles:
    - cloudwatch-logs-agent
    - cloudwatch-mon-scripts
```

#### Variables

```
cloudwatch_logs_agent_default_buffer_duration: 10000
cloudwatch_logs_agent_default_group_name: production
cloudwatch_logs_agent_default_initial_position: start
cloudwatch_logs_agent_logs:

  fail2ban:
    name: fail2ban
    file: /var/log/fail2ban.log
    datetime_format: '%Y-%m-%d %H:%M:%S,%f'  # e.g. 2017-03-28 07:50:45
    stream_name: 'fail2ban {instance_id}'

  nginx-default-access:
    name: nginx-default-access
    file: /var/log/nginx/access.log
    datetime_format: '%d/%b/%Y:%H:%M:%S %z'  # e.g. 27/Mar/2017:15:26:29 +0000
    stream_name: 'nginx default access {instance_id}'

  nginx-default-error:
    name: nginx-default-error
    file: /var/log/nginx/error.log
    datetime_format: '%Y/%m/%d %H:%M:%S'  # e.g. 2017/03/28 07:50:45
    stream_name: 'nginx default error {instance_id}'

  nginx-application-access:
    name: nginx-application-access
    file: /var/log/nginx/application/access.log
    datetime_format: '%d/%b/%Y:%H:%M:%S %z'  # e.g. 27/Mar/2017:15:26:29 +0000
    stream_name: 'nginx application access {instance_id}'

  nginx-application-error:
    name: nginx-application-error
    file: /var/log/nginx/application/error.log
    datetime_format: '%Y/%m/%d %H:%M:%S'  # e.g. 2017/03/28 07:50:45
    stream_name: 'nginx application error {instance_id}'
```

2014-2017 - David Fischer
