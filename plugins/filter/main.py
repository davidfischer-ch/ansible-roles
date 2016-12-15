# -*- encoding: utf-8 -*-


def oldest_ec2_snapshots(snapshots, keep):
    return sorted(snapshots, key=lambda s: s['start_time'])[keep:]


class FilterModule(object):
    """Ansible miscellaneous filters."""

    def filters(self):
        return {
            'oldest_ec2_snapshots': oldest_ec2_snapshots
        }
