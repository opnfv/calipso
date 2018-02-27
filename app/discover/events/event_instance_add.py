###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.events.event_base import EventBase, EventResult
from discover.scanner import Scanner


class EventInstanceAdd(EventBase):

    def handle(self, env, values):
        # find the host, to serve as parent
        instance_id = values['payload']['instance_id']
        host_id = values['payload']['host']
        instances_root_id = host_id + '-instances'
        instances_root = self.inv.get_by_id(env, instances_root_id)
        if not instances_root:
            self.log.info('instances root not found, aborting instance add')
            return EventResult(result=False, retry=True)

        # scan instance
        scanner = Scanner()
        scanner.setup(env=env, origin=self.origin)
        scanner.scan("ScanInstancesRoot", instances_root,
                     limit_to_child_id=instance_id,
                     limit_to_child_type='instance')
        scanner.scan_from_queue()

        # scan host
        host = self.inv.get_by_id(env, host_id)
        scanner.scan('ScanHost', host,
                     limit_to_child_type=['vconnectors_folder',
                                          'vedges_folder'])
        scanner.scan_from_queue()
        scanner.scan_links()
        scanner.scan_cliques()

        return EventResult(result=True,
                           related_object=instance_id,
                           display_context=instance_id)
