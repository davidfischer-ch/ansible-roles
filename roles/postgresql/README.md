# Role postgresql

## Status

Stable

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
postgresql_version: 9.6
```
