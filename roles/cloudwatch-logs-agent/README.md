# Role cloudwatch-logs-agent

## Status

Stable

## Example

### PlayBook

```
- hosts:
    - all:!localhost
  roles:
    - cloudwatch-logs-agent
    - cloudwatch-mon-scripts
```

### Variables

```
cloudwatch_logs_agent_default_buffer_duration: 10000
cloudwatch_logs_agent_default_group_name: production
cloudwatch_logs_agent_default_initial_position: start
cloudwatch_logs_agent_logs:

  dpkg:
    name: dpkg
    file: /var/log/dpkg.log
    datetime_format: '%Y-%m-%d %H:%M:%S'  # e.g. 2017-03-27 14:53:32
    stream_name: 'dpkg {instance_id}'

  fail2ban:
    name: fail2ban
    file: /var/log/fail2ban.log
    datetime_format: '%Y-%m-%d %H:%M:%S,%f'  # e.g. 2017-03-28 07:50:45
    stream_name: 'fail2ban {instance_id}'

  apache-default-access:
    name: apache-default-access
    file: /var/log/apache2/access.log
    datetime_format: '%d/%b/%Y:%H:%M:%S %z'  # e.g. 27/Mar/2017:15:26:29 +0000
    stream_name: 'apache default access {instance_id}'

  apache-default-error:
    name: apache-default-error
    file: /var/log/apache2/error.log
    datetime_format: '%b %d %H:%M:%S.%f %Y'  # e.g. May 19 06:25:01.551855 2017
    stream_name: 'apache default error {instance_id}'

  apache-other-vhosts-access:
    name: apache-other-vhosts-access
    file: /var/log/apache2/other_vhosts_access.log
    datetime_format: '%d/%b/%Y:%H:%M:%S %z'  # e.g. 27/Mar/2017:15:26:29 +0000
    stream_name: 'apache other vhosts access {instance_id}'

  apache-other-vhosts-error:
    name: apache-other-vhosts-error
    file: /var/log/apache2/other_vhosts_error.log
    datetime_format: '%b %d %H:%M:%S.%f %Y'  # e.g. May 19 06:25:01.551855 2017
    stream_name: 'apache other vhosts error {instance_id}'

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

  postgresql:
    name: postgresql
    file: '/var/log/postgresql/postgresql-{{ postgresql_version }}-main.log'
    datetime_format: '%Y-%m-%d %H:%M:%S %Z'  # e.g. 2017-05-08 12:50:06 UTC
    stream_name: 'postgresql {instance_id}'

  redis:
    name: redis
    file: /var/log/redis/redis-server.log
    datetime_format: '%d %b %H:%M:%S.%f'  # e.g. 21 Apr 14:21:46.727
    stream_name: 'redis {instance_id}'

  supervisor:
    name: supervisor
    file: /var/log/supervisor/supervisord.log
    datetime_format: '%Y-%m-%d %H:%M:%S,%f'  # e.g. 2017-03-28 07:50:45,644
    stream_name: 'supervisor {instance_id}'

  uwsgi-application:
    name: uwsgi-application
    file: /var/log/uwsgi/app/application.log
    datetime_format: '%c'  # e.g. May  8 12:50:17 2017
    stream_name: 'uwsgi application {instance_id}'
```
