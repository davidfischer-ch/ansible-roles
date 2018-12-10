# Role s3fs

## Status

Stable

## Example

### PlayBook

```
---

- hosts:
    - all:!localhost
  roles:
    - s3fs
    - mounts
```

### Variables

```
mounts:
  data:
    check: yes
    directory: /mnt/mybucket
    user: root
    group: root
    mode: 777
    fstype: fuse.s3fs
    options: _netdev,allow_other,noatime,endpoint=eu-west-1,iam_role=auto,max_stat_cache_size=60000,storage_class=standard_ia,use_sse
    source: mybucketname:/some/path

s3fs_version: v1.82  # 20/09/2018
```
