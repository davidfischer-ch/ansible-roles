#!/usr/bin/env bash
ansible-galaxy install -r roles/requirements.yml --roles-path roles "$@"
