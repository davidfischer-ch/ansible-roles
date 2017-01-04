================
Ansible Playbook
================

Set of Ansible roles for deploying various services.

This playbook is covering multiple use-cases:

* Deploying a full Django web stack
* Deploying an Ampache server
* Deploying the ELK stack (work in progress)
* Deploying a GitLab server using Omnibus
* Deploying an ownCloud server
* Installing a computer under Debian/Ubuntu
* Tweaking an Ubuntu Phone (never install nfs-client!)

Most are generic enough to be usable as-is.

--------
Examples
--------

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
        options: allow_other,endpoint=eu-west-1,iam_role=auto,storage_class=standard_ia
        source: mybucketname:/some/path

2014-2017 - David Fischer
