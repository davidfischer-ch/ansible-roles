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
  application:
    template: template1
    extensions: []
    name: my-database
    users:
      - name: my-user
        password: some-password-here
        role_flags: [SUPERUSER, CREATEDB]
        clients:
          - all  # see https://stackoverflow.com/questions/3278379/how-to-configure-postgresql-to-accept-all-incoming-connections
```
