# Role seafile

## Status

Beta

Not (yet) implemented:

* Handling of multi-tier architecture (database external host, ...)

* Role actions such as configure, ...
* Mounting the data directory. I think this roles should not take this responsibility. When deploying more than one web host, make sure your PlayBook mount the data directory prior to calling this role.

## Example

### Variables

```
java_apt_repository: ''
java_version: 8

mariadb_interface: lo
mariadb_root_password: cFazXrbhJyfpu5B7
mariadb_version: 10.2

memcache_interface: lo

nginx_zip_module_enabled: no
nginx_version: release-1.13.6  # 19/11/2017
nginx_daemon_mode: supervisor
nginx_build_flags:
  - --with-http_addition_module
  - --with-http_auth_request_module
  - --with-http_dav_module
  - --with-http_geoip_module
  - --with-http_gzip_static_module
  - --with-http_image_filter_module
  - --with-http_realip_module
  - --with-http_ssl_module
  - --with-http_stub_status_module
  - --with-http_sub_module
  - --with-http_v2_module
  - --with-http_xslt_module
  - --with-ipv6
  - --with-pcre-jit

nginx_sites:
  seafile:
    name: '{{ seafile_instance_name }}'
    config_file: '{{ playbook_dir }}/../roles/seafile/templates/example.nginx.site.conf.j2'
    domains: '{{ seafile_domains }}'
    with_dhparam: yes

postfix_hostname: '{{ ansible_hostname }}'

ssl_cert_country: CH
ssl_cert_locality: Geneva
ssl_cert_organization: antiNSA
ssl_cert_organization_unit: ''
ssl_cert_state: Geneva
ssl_cert_crt_filename: '/etc/nginx/sites-ssl/{{ seafile_instance_name }}.crt'
ssl_cert_key_filename: '/etc/nginx/sites-ssl/{{ seafile_instance_name }}.key'

supervisor_daemon_mode: '{{ ansible_service_mgr }}'
supervisor_username: supercool
supervisor_password: h3mQ2FbrGUzNE85m

seafile_admin_email: admin@seafile.example
seafile_admin_password: xTv6w7f5r2KaTKJS
seafile_daemon_mode: systemd
seafile_database_password: K89YeTgZmqRFYJGC
seafile_domains:
  - '{{ ansible_host }}'
  - 127.0.0.1
seafile_instance_name: seafile
seafile_interface: lo
seafile_version: 6.1.9
```

### PlayBook

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
    - bash
    - miscellaneous
    - openssl
    - kernel
    - python
    - mounts
    - rsync
    - ufw
    - fail2ban

# Application Services

# TODO: Mount shared storage

- hosts:
    - seafile
  roles:
    - memcache
    - mariadb
    - seafile
    - nginx
```
