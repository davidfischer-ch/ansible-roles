# Role seafile

## Status

Beta

Not (yet) implemented:

* Handling of multi-tier architecture (database external host, ...)

* Role actions such as configure, ...
* Mounting the data directory. I think this roles should not take this responsibility. When deploying more than one web host, make sure your PlayBook mount the data directory prior to calling this role.
