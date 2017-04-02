===============
Ansible Library
===============

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

--------
Examples
--------

An Ubuntu Desktop Computer
==========================

PlayBook::

    ---

    - include: roles-df/playbooks/devices.yml

    - hosts:
        - seafile-client
      roles:
        - seafile-client

Inventory::

    [gaming]
    my-computer

    [laptop]
    my-computer

    [seafile-client]
    my-computer

Variables::

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

Django Development Server
=========================

Using the PlayBook ``playbooks/django-stack.yml``.

Inventory::

    [caching]
    a-django-dev-server

    [database]
    a-django-dev-server

    [messaging]
    a-django-dev-server

    [web]
    a-django-dev-server

    [worker]
    a-django-dev-server

Variables::

    ansible_host: 192.168.56.101
    ansible_port: 22
    ansible_user: vagrant

    ssh_port: 22

    user: '{{ ansible_user }}'
    group: '{{ ansible_user }}'

    locale: fr_CH.UTF-8
    timezone: 'Europe/Zurich'
    upgrade_packages_async: '{{ omit }}'
    upgrade_packages_poll: '{{ omit }}'

    mounts: {}

    python_versions:
      - 2.7
      - 3.4

    # Django Stack

    <my-application-settings-here>

    celery_services:
      default:
        name: my-django-application-celery-default-worker
        config_file: celery-default-worker.conf.j2
      beat:
        name: my-django-application-celery-beat
        config_file: celery-beat.conf.j2

    nginx_daemon_mode: supervisor
    nginx_pagespeed_module_enabled: no
    nginx_upload_module_enabled: no
    nginx_zip_module_enabled: yes
    nginx_zip_module_version: 01ce916943337b32d72cf0ab87f218caa8c598ab  # 17/10/2015
    nginx_version: release-1.9.4                                        # 17/10/2015

    postgresql_databases:
      template1:
        name: template1
        extensions:
          - postgis
          - hstore
      application:
        template: template1
        clients:
          - 127.0.0.1/32
        extensions:
          - postgis
          - hstore
        name: <my-django-application-name-here>
        user: admin
        password: ****
        with_test: yes
    postgresql_is_master: yes
    postgresql_master: 127.0.0.1
    postgresql_port: 5432

    rabbitmq_is_master: yes
    rabbitmq_master: 127.0.0.1
    rabbitmq_password: ****
    rabbitmq_port: 5672
    rabbitmq_user: <username-here>

    redis_master: 127.0.0.1
    redis_password: ****
    redis_port: 6379

    supervisor_password: ****
    supervisor_username: <username-here>

    uwsgi_apps:
      application:
        name: <my-django-application-name-here>
        config_file: app.xml.j2
        path: '{{ production_symlink }}'
        project: <my-django-project-name-here>
        python_version: python34
        chmod_socket: 666  # Fix access to socket by www-data
        user: '{{ user }}'
        group: '{{ group }}'
        limit_as: 2048

Mounting a S3 bucket with s3fs
==============================

PlayBook::

    - hosts:
        - all:!localhost
      roles:
        - s3fs
        - mounts

Variables::

    mounts:
      data:
        check: yes
        directory: /mnt/mybucket
        user: root
        group: root
        mode: 777
        fstype: fuse.s3fs
        options: _netdev,allow_other,noatime,endpoint=eu-west-1,iam_role=auto,max_stat_cache_size=60000,storage_class=standard_ia,use_sse
        source: mybucketname:/some/path

Installing AWS utilities
========================

PlayBook::

    - hosts:
        - all:!localhost
      roles:
        - cloudwatch-logs-agent
        - cloudwatch-mon-scripts

Variables::

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

2014-2017 - David Fischer
