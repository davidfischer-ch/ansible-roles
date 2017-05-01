# -*- encoding: utf-8 -*-


def format_items(items, pattern):
    return [pattern.format(i) for i in items]


def oldest_ec2_snapshots(snapshots, keep):
    return sorted(snapshots, key=lambda s: s['start_time'])[keep:]


class FilterModule(object):
    """Ansible miscellaneous filters."""

    def filters(self):
        return {
            'format_items': format_items,
            'oldest_ec2_snapshots': oldest_ec2_snapshots
        }
