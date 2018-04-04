# Role certbot

## Status

Preview

This role is not intended to be fully automated, but to streamline some of the
steps required to work with certbot. I am not using nginx plugin as its trying
to install nginx using apt-get ...

Not (yet) implemented:

* Role actions such as list, ...
* "Automating" creation of certificate (and make idempotent)
* Integration with apache and nginx role (chicken and egg problem when setting-up sites)
