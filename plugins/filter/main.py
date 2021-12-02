# -*- encoding: utf-8 -*-

import itertools, re, subprocess

from ansible import errors


def chunk(objects, length, of_type=list):
    """
    Yield successive chunks of defined `length` from `objects`. Last chunk may be smaller.
    Copied from https://github.com/davidfischer-ch/pytoolbox/blob/master/pytoolbox/itertools.py#L34.

    **Example usage**

    >>> iterable = iter(range(7))
    >>> assert list(chunk(iterable, 3)) == [[0, 1, 2], [3, 4, 5], [6]]
    >>> assert list(chunk(iterable, 3)) == []
    >>> assert list(chunk((0, 1, (2, 3)), 1, of_type=set)) == [{0}, {1}, {(2, 3)}]
    """
    iterable = iter(objects)
    while True:
        chunk = of_type(itertools.islice(iterable, 0, length))
        if not chunk:
            break
        yield chunk


def enumerate_(objects, *args, **kwargs):
    return ({'index': i, 'objects': o} for i, o in enumerate(objects, *args, **kwargs))


def format_items(items, pattern):
    return [pattern.format(i) for i in items]


def map_items(items, key, **defaults):
    for item in items:
        item_dict = defaults.copy()
        item_dict[key] = item
        yield item_dict


def really_mandatory(item):
    from jinja2.runtime import Undefined
    if isinstance(item, Undefined) or not item:
        raise errors.AnsibleFilterError('Mandatory variable is empty or not defined.')
    return item


def ec2_group_rules(cidr_ips, **defaults):
    for cidr_ip in cidr_ips:
        rule = defaults.copy()
        rule['cidr_ip'] = cidr_ip
        yield rule


def ec2_vpc_routes(dests, **defaults):
    for dest in dests:
        route = defaults.copy()
        route['dest'] = dest
        yield route


def oldest_ec2_snapshots(snapshots, keep):
    return sorted(snapshots, key=lambda s: s['start_time'])[keep:]


def regex_findall(value, expression):
    """
    >>> regex_findall('something\\nspecial\\nis\\nhidden', 'spec.Al')
    []
    >>> regex_findall('something\\nspecial\\nis\\nhidden', 'spec.al')
    ['special']
    >>> regex_findall(
    ...     '<td> x-forwarded-for  </td>  <td> 10.137.69.68  </td>',
    ...     '<td>\\s*x-forwarded-for\\s*</td>[^<]+<td>\\s*([0-9\\.]+)')
    ['10.137.69.68']
    """
    return re.findall(expression, value, re.MULTILINE)


# VirtualBox ---------------------------------------------------------------------------------------

VBOX_LIST_REGEX = re.compile(r'"(?P<name>[^"]+)"\s+{(?P<uuid>[0-9a-f\-]+)}')


def get_virtualbox_machines_list():
    result = subprocess.check_output(['vboxmanage', 'list', 'vms']).decode('utf-8')
    return {n: u for n, u in VBOX_LIST_REGEX.findall(result)}


def get_vagrant_machine_id(name, provider):
    if provider == 'virtualbox':
        return get_virtualbox_machines_list().get(name)
    else:
        raise NotImplementedError(
            'Handling machine {0} provider {1} not yet implemented.'.format(name, provider))


def set_vagrant_machines_ids(machines):

    def with_id(machine):
        value = {'uuid': get_vagrant_machine_id(machine['name'], machine['provider'])}
        value.update(machine)
        return value

    return [with_id(machine) for machine in machines]


# Filters ------------------------------------------------------------------------------------------

class FilterModule(object):
    """Ansible miscellaneous filters."""

    def filters(self):
        return {
            'chunk': chunk,
            'enumerate': enumerate_,
            'format_items': format_items,
            'map_items': map_items,
            'really_mandatory': really_mandatory,
            'ec2_group_rules': ec2_group_rules,
            'ec2_vpc_routes': ec2_vpc_routes,
            'oldest_ec2_snapshots': oldest_ec2_snapshots,
            'regex_findall': regex_findall,
            'set_vagrant_machines_ids': set_vagrant_machines_ids
        }


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    print('All tests passed')
