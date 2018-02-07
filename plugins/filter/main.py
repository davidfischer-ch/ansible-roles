# -*- encoding: utf-8 -*-

import itertools


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


class FilterModule(object):
    """Ansible miscellaneous filters."""

    def filters(self):
        return {
            'chunk': chunk,
            'enumerate': enumerate_,
            'format_items': format_items,
            'map_items': map_items,
            'ec2_group_rules': ec2_group_rules,
            'ec2_vpc_routes': ec2_vpc_routes,
            'oldest_ec2_snapshots': oldest_ec2_snapshots
        }

if __name__ == '__main__':
    import doctest
    doctest.testmod()
