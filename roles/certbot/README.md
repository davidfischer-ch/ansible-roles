# Role certbot

## Status

Preview

This role is not intended to be fully automated, but to streamline some of the
steps required to work with certbot. I am not using nginx plugin as its trying
to install nginx using apt-get ...

Not (yet) implemented:

* Role actions such as list, ...
* "Automating" creation of certificate (and make idempotent)
* Integration with apache and nginx role (chicken and egg problem when setting-up sites)

## Guide

### Generate or Renew a Certificate

TODO Complete it

#### Action

```
ssh <your-server>
$ sudo su
# certbot certonly --manual -d *.your-app.com -m your@email.com --agree-tos
```

Create file required for validating ownership and restart nginx:

```
ssh <your-server>
$ sudo su
# mkdir /etc/certbot/challenges/your-site -p
# echo '<challenge-file-content>' > /etc/certbot/challenges/your-site/<challenge-file-name>
# supervisorctl restart nginx
```

#### Configuration

Example host variables:

```
application_name: your-app
application_domains:
  - your-app.com
  - www.your-app.com

nginx_zip_module_enabled: no
nginx_version: release-1.15.2  # 16/08/2018
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
nginx_log_rotations_frequency: weekly
nginx_log_rotations_max_count: 52
nginx_port: 80
nginx_port_ssl: 443
nginx_server_header_engine: your-application
nginx_sites:
  application:
    name: '{{ application_name }}'
    config_file: '{{ playbook_dir }}/../roles/your-application/templates/nginx.config.conf.j2'
    ssl_crt_file: /etc/letsencrypt/live/{{ application_name }}/fullchain.pem
    ssl_key_file: /etc/letsencrypt/live/{{ application_name }}/privkey.pem
    ssl_use_directive: no
    domains: '{{ application_domains }}'
    # A bunch of variable used by your template nginx.config.conf.j2
    redirect_ssl: yes
    with_dhparam: yes
    with_hsts: yes
    with_http2: yes
    with_ssl: yes
    x_frame_options: SAMEORIGIN
```
