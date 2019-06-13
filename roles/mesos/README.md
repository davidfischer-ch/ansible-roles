# Role mesos

## Status

Alpha

This role is not complete, old and (probably) outdated.
Apache MesOS 1.4.1 was released the 16th November 2017.

## Example

### PlayBook

```
- hosts:
    - mesos
  roles:
    - mesos
```

### Variables

```
java_apt_repository: ''
java_version: 8

mesos_version: 1.4.1
```
