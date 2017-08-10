###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from bson.objectid import ObjectId

from discover.fetcher import Fetcher
from utils.inventory_mgr import InventoryMgr


class CliqueFinder(Fetcher):
    def __init__(self):
        super().__init__()
        self.inv = InventoryMgr()
        self.inventory = self.inv.inventory_collection
        self.links = self.inv.collections["links"]
        self.clique_types = self.inv.collections["clique_types"]
        self.clique_types_by_type = {}
        self.clique_constraints = self.inv.collections["clique_constraints"]
        self.cliques = self.inv.collections["cliques"]

    def find_cliques_by_link(self, links_list):
        return self.links.find({'links': {'$in': links_list}})

    def find_links_by_source(self, db_id):
        return self.links.find({'source': db_id})

    def find_links_by_target(self, db_id):
        return self.links.find({'target': db_id})

    def find_cliques(self):
        self.log.info("scanning for cliques")
        clique_types = self.get_clique_types().values()
        for clique_type in clique_types:
            self.find_cliques_for_type(clique_type)
        self.log.info("finished scanning for cliques")

    def get_clique_types(self):
        if not self.clique_types_by_type:
            clique_types = self.clique_types.find({"environment": self.get_env()})
            default_clique_types = \
                self.clique_types.find({'environment': 'ANY'})
            for clique_type in clique_types:
                focal_point_type = clique_type['focal_point_type']
                self.clique_types_by_type[focal_point_type] = clique_type
            # if some focal point type does not have an explicit definition in
            # clique_types for this specific environment, use the default
            # clique type definition with environment=ANY
            for clique_type in default_clique_types:
                focal_point_type = clique_type['focal_point_type']
                if focal_point_type not in clique_types:
                    self.clique_types_by_type[focal_point_type] = clique_type
            return self.clique_types_by_type

    def find_cliques_for_type(self, clique_type):
        type = clique_type["focal_point_type"]
        constraint = self.clique_constraints.find_one({"focal_point_type": type})
        constraints = [] if not constraint else constraint["constraints"]
        object_type = clique_type["focal_point_type"]
        objects_for_focal_point_type = self.inventory.find({
            "environment": self.get_env(),
            "type": object_type
        })
        for o in objects_for_focal_point_type:
            self.construct_clique_for_focal_point(o, clique_type, constraints)

    def rebuild_clique(self, clique):
        focal_point_db_id = clique['focal_point']
        constraint = self.clique_constraints.find_one({"focal_point_type": type})
        constraints = [] if not constraint else constraint["constraints"]
        clique_types = self.get_clique_types()
        o = self.inventory.find_one({'_id': focal_point_db_id})
        clique_type = clique_types[o['type']]
        new_clique = self.construct_clique_for_focal_point(o, clique_type, constraints)
        if not new_clique:
            self.cliques.delete({'_id': clique['_id']})

    def construct_clique_for_focal_point(self, o, clique_type, constraints):
        # keep a hash of nodes in clique that were visited for each type
        # start from the focal point
        nodes_of_type = {o["type"]: {str(o["_id"]): 1}}
        clique = {
            "environment": self.env,
            "focal_point": o["_id"],
            "focal_point_type": o["type"],
            "links": [],
            "links_detailed": [],
            "constraints": {}
        }
        for c in constraints:
            val = o[c] if c in o else None
            clique["constraints"][c] = val
        for link_type in clique_type["link_types"]:
            # check if it's backwards
            link_type_parts = link_type.split('-')
            link_type_parts.reverse()
            link_type_reversed = '-'.join(link_type_parts)
            self_linked = link_type == link_type_reversed
            if self_linked:
                reversed = False
            else:
                matches = self.links.find_one({
                    "environment": self.env,
                    "link_type": link_type_reversed
                })
                reversed = True if matches else False
            if reversed:
                link_type = link_type_reversed
            from_type = link_type[:link_type.index("-")]
            to_type = link_type[link_type.index("-") + 1:]
            side_to_match = 'target' if reversed else 'source'
            other_side = 'target' if not reversed else 'source'
            match_type = to_type if reversed else from_type
            if match_type not in nodes_of_type.keys():
                continue
            other_side_type = to_type if not reversed else from_type
            nodes_to_add = {}
            for match_point in nodes_of_type[match_type].keys():
                matches = self.links.find({
                    "environment": self.env,
                    "link_type": link_type,
                    side_to_match: ObjectId(match_point)
                })
                for link in matches:
                    id = link["_id"]
                    if id in clique["links"]:
                        continue
                    if not self.check_constraints(clique, link):
                        continue
                    clique["links"].append(id)
                    clique["links_detailed"].append(link)
                    other_side_point = str(link[other_side])
                    nodes_to_add[other_side_point] = 1
            if other_side_type not in nodes_of_type:
                nodes_of_type[other_side_type] = {}
            nodes_of_type[other_side_type].update(nodes_to_add)

        # after adding the links to the clique, create/update the clique
        if not clique["links"]:
            return None
        focal_point_obj = self.inventory.find({"_id": clique["focal_point"]})
        if not focal_point_obj:
            return None
        focal_point_obj = focal_point_obj[0]
        focal_point_obj["clique"] = True
        focal_point_obj.pop("_id", None)
        self.cliques.update_one(
            {
                "environment": self.get_env(),
                "focal_point": clique["focal_point"]
            },
            {'$set': clique},
            upsert=True)
        clique_document = self.inventory.update_one(
            {"_id": clique["focal_point"]},
            {'$set': focal_point_obj},
            upsert=True)
        return clique_document

    def check_constraints(self, clique, link):
        if "attributes" not in link:
            return True
        attributes = link["attributes"]
        constraints = clique["constraints"]
        for c in constraints:
            if c not in attributes:
                continue  # constraint not applicable to this link
            constr_values = constraints[c]
            link_val = attributes[c]
            if isinstance(constr_values, list):
                if link_val not in constr_values:
                    return False
            elif link_val != constraints[c]:
                return False
        return True
