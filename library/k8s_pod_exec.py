#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os

import kubernetes.client
from ansible.module_utils.basic import AnsibleModule
from kubernetes.stream import stream

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = """
---
module: k8s_pod_exec
author: "David Fischer (@davidfischer-ch)"
short_description: Execute a command inside a pod (container).
description:
  - This module uses the official kubernetes Python library.
options:
  host:
    required: false
    description:
      - Provide a URL for accessing the API.
      - Can also be specified via K8S_AUTH_HOST environment variable.
  api_key:
    required: false
    description:
      - Token used to authenticate with the API.
      - Can also be specified via K8S_AUTH_API_KEY environment variable.
  ca_cert:
    required: false
    default: None
    description:
      - Path to a CA certificate used to authenticate with the API.
      - The full certificate chain must be provided to avoid certificate validation errors.
      - Can also be specified via K8S_AUTH_SSL_CA_CERT environment variable.
  name:
    required: true
    description:
      - The name of the pod to execute the command.
  namespace:
    required: true
    description:
      - The namespace where the pod resides.
  command:
    required: true
    description:
      - Specify command by passing in an array.
  container:
    required: false
    default: None
    description:
      - Container in which to execute the command, not required if the pod has only one container.
"""

EXAMPLES = """
- k8s_pod_exec:
    host: https://your-k8s-cluster.some-domain.com:443
    api_key: 1234(.....)cafe
    name: my-pod
    namespace: my-namespace
    command:
      - echo
      - toto
  register: _exec

- debug: var=_exec.output
"""

RETURN = """
output:
    description: The output of the command.
    type: str
    returned: always
"""


def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(default=None),
            api_key=dict(default=None, no_log=True),
            ca_cert=dict(default=None, type='path'),
            name=dict(required=True),
            namespace=dict(required=True),
            command=dict(required=True, type='list'),
            container=dict(default=None)
        ),
        supports_check_mode=False
    )
    host, api_key, ca_cert, name, namespace, command, container = (
        module.params[k] for k in (
            'host',
            'api_key',
            'ca_cert',
            'name',
            'namespace',
            'command',
            'container'
        )
    )

    api_key = os.getenv('K8S_AUTH_API_KEY') if api_key is None else api_key

    config = kubernetes.client.Configuration()
    config.host = os.getenv('K8S_AUTH_HOST') if host is None else host
    config.ssl_ca_cert = os.getenv('K8S_AUTH_SSL_CA_CERT') if ca_cert is None else ca_cert
    config.api_key = {'authorization': 'Bearer {0}'.format(api_key)} if api_key else {}

    # https://github.com/kubernetes-client/python/issues/516#issuecomment-442580346
    api = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(config))
    output = stream(
        api.connect_get_namespaced_pod_exec,
        name,
        namespace,
        command=command,
        container=container or '',
        stderr=True,  # Redirect the standard error stream of the pod
        stdin=False,  # Do not redirect the standard input stream of the pod
        stdout=True,  # Redirect the standard output stream of the pod
        tty=False)    # Do not allocate a tty
    module.exit_json(changed=True, output=output)


if __name__ == '__main__':
    main()
