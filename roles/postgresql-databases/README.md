# Role postgresql-databases

## Status

Stable

## Example

### PlayBook

```
- hosts:
    - database
  roles:
    - postgresql-databases
```

### Variables

```
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
