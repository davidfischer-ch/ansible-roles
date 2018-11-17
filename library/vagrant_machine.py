#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import itertools, re, subprocess, time

from ansible.module_utils.basic import AnsibleModule

# FIXME report changed only if content changed when operation is 'none'.

DOCUMENTATION = r"""
---
module: vagrant_machine
author: "David Fischer (@davidfischer-ch)"
short_description: Manage a Vagrant Machine.
description:
  - TODO
options:
  chdir:
    required: true
    description:
      - The directory with the Vagrantfile.
  name:
    required: true
    description:
      - The machine name.
  provider:
    required: false
    description:
      - A valid Vagrant provider when provisioning is required, see https://www.vagrantup.com/docs/providers/index.html.
  state:
    required: true
    choices: [absent, poweroff, running, saved]
  timeout:
    required: false
    description:
      - The timeout in seconds for the transition from poweroff or saved to running.
    default: 120
"""

EXAMPLES = r"""
- vagrant_machine: chdir=/some/path name=my-vm provider=virtualbox state=running
- vagrant_machine: chdir=/some/path name=my-vm provider=virtualbox state=saved
- vagrant_machine: chdir=/some/path name=my-vm state=running timeout=60
- vagrant_machine: chdir=/some/path name=my-vm state=absent
"""

ACTION_FOR_TRANSITION = {
    'absent': {'running': ['up', '--provider']},
    'aborted': {'absent': ['destroy', '--force'], 'running': ['up', '--no-provision']},
    'poweroff': {'absent': ['destroy', '--force'], 'running': ['up', '--no-provision']},
    'running': {'absent': ['destroy', '--force'], 'poweroff': ['halt'], 'saved': ['suspend']},
    'saved': {'absent': ['destroy', '--force'], 'running': ['resume']}
}
STOP_TO_START_STATES = {'aborted', 'poweroff', 'saved'}
VBOX_LIST_REGEX = re.compile(r'^(?P<name>[^\s]+)\s+(?P<status>[a-z\s]+)\s+\(', re.MULTILINE)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            chdir=dict(required=True, type='path'),
            name=dict(required=True),
            provider=dict(required=False),
            state=dict(required=True, choice=['absent', 'poweroff', 'running', 'saved']),
            timeout=dict(required=False, type='int', default=120)
        ),
        supports_check_mode=True
    )
    chdir, name, provider, state, timeout = (
        module.params[k] for k in ('chdir', 'name', 'provider', 'state', 'timeout')
    )

    if timeout < 1:
        module.fail_json(msg='Timeout must be greater than 0.')

    current_state = get_state(chdir, name)
    if current_state == 'absent' and state != 'absent' and not provider:
        module.fail_json(msg='A provider is required because machine "%s" is absent.' % name)

    if not module.check_mode:
        if current_state != state:
            try:
                set_state(chdir, name, state, provider=provider, timeout=timeout)
            except Exception as e:
                module.fail_json(msg=str(e))
    module.exit_json(changed=current_state != state, diff={'after': state, 'before': current_state})


def set_state(directory, name, state, provider=None, timeout=120):
    current_state = get_state(directory, name, wait=True)
    if current_state != state:
        try:
            action = ACTION_FOR_TRANSITION[current_state][state]
        except KeyError:
            raise NotImplementedError(
                'Unable to find a suitable action for the transition from %s to %s.' %
                (current_state, state))

        if action[-1] == '--provider':
            action.append(provider)

        process = subprocess.Popen(
            itertools.chain(['vagrant'], action, [name]),
            cwd=directory,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        if current_state in STOP_TO_START_STATES:
            start_time = time.time()
            while True:
                time.sleep(1)
                new_state = get_state(
                    directory,
                    name,
                    wait=True,
                    timeout=timeout + start_time - time.time())
                if new_state == state:
                    process.kill()
                    break
                if new_state != current_state:
                    raise NotImplementedError(
                        'Unexpected transition from %s to %s.' % (current_state, new_state))
                if time.time() - start_time > timeout:
                    raise RuntimeError(
                        'Transition to %s timed-out, current state: %s.' % (state, new_state))
        else:
            stdout, stderr = process.communicate()
            if process.returncode:
                raise RuntimeError('Error message: ' + str(stderr))


def get_state(directory, name, wait=False, timeout=120):
    start_time = time.time()
    while True:
        match = VBOX_LIST_REGEX.search(
            subprocess.check_output(
                ['vagrant', 'status', name],
                cwd=directory))
        state = match.groupdict()['status'] if match else 'not created'
        if state == 'not created':
            state = 'absent'
        if state in ACTION_FOR_TRANSITION.keys() or not wait:
            return state
        if time.time() - start_time > timeout:
            raise RuntimeError('Timed-out during a transition, current state: %s.' % state)
        time.sleep(1)


if __name__ == '__main__':
    main()
