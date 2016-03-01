================
Ansible Playbook
================

Set of Ansible roles for deploying various services.

This playbook is covering multiple use-cases:

* Deploying a full Django web stack
* Deploying an Ampache server
* Deploying an ownCloud server
* Installing a computer under Debian/Ubuntu
* Tweaking an Ubuntu Phone (never install nfs-client!)

Most are generic enough to be usable as-is.

Some roles requires `pytoolbox <https://github.com/davidfischer-ch/pytoolbox>`_.
So install requirements with pip{2,3}, defined in ``requirements.pip{2,3}``.

2014-2016 - David Fischer
