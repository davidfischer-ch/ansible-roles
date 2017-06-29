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


def ec2_group_rules(cidr_ips, **kwargs):
    for cidr_ip in cidr_ips:
        rules = {'cidr_ip': cidr_ip}
        rules.update(kwargs)
        yield rules


def oldest_ec2_snapshots(snapshots, keep):
    return sorted(snapshots, key=lambda s: s['start_time'])[keep:]


class FilterModule(object):
    """Ansible miscellaneous filters."""

    def filters(self):
        return {
            'chunk': chunk,
            'enumerate': enumerate_,
            'format_items': format_items,
            'ec2_group_rules': ec2_group_rules,
            'oldest_ec2_snapshots': oldest_ec2_snapshots
        }

if __name__ == '__main__':
    import doctest
    doctest.testmod()
