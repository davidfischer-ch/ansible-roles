# Role postgresql

## Status

Stable

Not (yet) implemented:

* Role actions such as flush, ...

## Example

### PlayBook

```
- hosts:
    - database
  roles:
    - postgresql
```

### Variables

```
postgresql_is_master: yes
postgresql_port: 5432
postgresql_version: 9.4
postgresql_databases:
  template1:
    name: template1
    extensions: []
    with_test: no
  application:
    template: template1
    clients:
      - all  # see https://stackoverflow.com/questions/3278379/how-to-configure-postgresql-to-accept-all-incoming-connections
    extensions: []
    name: my-database
    user: my-user
    password: some-password-here
    with_test: no
```
