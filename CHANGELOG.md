# Changelog

## v1.0.3 (2023-05-25)

Diff : https://github.com/davidfischer-ch/ansible-roles/compare/v1.0.2...v1.0.3

### Features

- Add role `aws-xray`
- Add role `deconz`
- Add role `go`
- Add role `home-assistant`
- Add role `terraform`
- Add filter `set_vagrant_machines_ids`
- Add new scripts to work on roles

### Fix and enhancements

- Generate `ansible.cfg` using [generate-config.py](scripts/generate-config.py)
- Example [django-dev](examples/django-dev) : Make example compatible with latest version of the role `django-site`
- Playbook [ansible-bootstrap](playbooks/ansible-bootstrap.yml) : Ensure `ansible_python_interpreter` and `bootstrap_python_pacakge` are defined
- Module [vagrant_machine](library/vagrant_machine.py) : Fix it
- Modules : Remove shebang to prevent issues
- Clone roles using ssh protocol
- Fix deprecation warnings
- Cleanup imports
- Mode as string

## v1.0.2 (2020-03-26)

### Fix and enhancements

- Add script to generate ansible.cfg
- Register two more roles (buildah and fuse-overlayfs)
- library/virtualenv_relocate.py: Do not follow symbolic links

## v1.0.1 (2020-03-06)

### Fix and enhancements

- Fix an incredible bug related to no_log breaking dynamic_defaults

## v1.0.0 (2020-03-01)

- Initial release
