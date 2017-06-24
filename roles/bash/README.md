# Role bash

## Status

Preview

## Example

### PlayBook

```
- hosts:
    - localhost
  roles:
    - bash
```

### Variables

```
bash_aliases:

  # SysOps
  rr: 'rsync -ah -lH --delete --progress'
  pp: 'netstat -ntlp | grep LISTEN'

  # Git Shortcuts
  add: 'git add -p'
  dif: 'git difftool -y'
  st: 'git status'

bash_extra_user_configuration: |
  # Yeah, still using my old-school project :)
  export LU_PATH='{{ ansible_user_dir }}/david-develop/logicielsUbuntu'
  . '{{ ansible_user_dir }}/david-develop/logicielsUbuntu/logicielsUbuntuExports'
```
