###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import re
from bson.objectid import ObjectId

from listen.events.event_base import EventBase, EventResult
from scan.clique_finder import CliqueFinder


class EventDeleteBase(EventBase):

    def delete_handler(self, env, object_id, object_type) -> EventResult:
        item = self.inv.get_by_id(env, object_id)
        if not item:
            self.log.info('{0} document is not found, aborting {0} delete'.format(object_type))
            return EventResult(result=False, retry=False)

        db_id = ObjectId(item['_id'])
        id_path = item['id_path'] + '/'

        # remove related clique
        clique_finder = CliqueFinder()
        self.inv.delete('cliques', {'focal_point': db_id})

        # keep related links to do rebuild of cliques using them
        matched_links_source = clique_finder.find_links_by_source(db_id)
        matched_links_target = clique_finder.find_links_by_target(db_id)

        links_using_object = []
        links_using_object.extend([l['_id'] for l in matched_links_source])
        links_using_object.extend([l['_id'] for l in matched_links_target])

        # find cliques using these links
        if links_using_object:
            matched_cliques = clique_finder.find_cliques_by_link(links_using_object)
            # find cliques using these links and rebuild them
            for clique in matched_cliques:
                clique_finder.rebuild_clique(clique)

        # remove all related links
        self.inv.delete('links', {'source': db_id})
        self.inv.delete('links', {'target': db_id})

        # remove object itself
        self.inv.delete('inventory', {'_id': db_id})

        # remove children
        regexp = re.compile('^' + id_path)
        self.inv.delete('inventory', {'id_path': {'$regex': regexp}})
        return EventResult(result=True,
                           related_object=object_id,
                           display_context=object_id)
