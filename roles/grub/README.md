# Role grub

## Status

Alpha

I only used it to fix Linux Mint not booting properly on an Asus ZenBook Pro!

## Example

Any variable prefixed by grub_ will be converted to upper case and used for
configuring /etc/default/grub. Value is written verbatim, meaning you need
to add quotes for string parameters.

### PlayBook

```
---

- hosts:
    - localhost
  roles:
    - grub
  vars:
    grub_cmdline_linux_default: '"nouveau.modeset=0 quiet splash"'
```
