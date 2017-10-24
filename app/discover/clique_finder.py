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

    link_type_reversed = {}

    def __init__(self):
        super().__init__()
        self.env_config = None
        self.inv = InventoryMgr()
        self.inventory = self.inv.inventory_collection
        self.links = self.inv.collections["links"]
        self.clique_types = self.inv.collections["clique_types"]
        self.clique_types_by_type = {}
        self.clique_constraints = self.inv.collections["clique_constraints"]
        self.cliques = self.inv.collections["cliques"]

    def set_env(self, env):
        super().set_env(env)
        self.env_config = self.configuration.environment

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

    # Calculate priority score
    def _get_priority_score(self, clique_type):
        if self.env == clique_type['environment']:
            return 4
        if (self.env_config['distribution'] == clique_type.get('distribution') and
            self.env_config['distribution_version'] == clique_type.get('distribution_version')):
            return 3
        if clique_type.get('mechanism_drivers') in self.env_config['mechanism_drivers']:
            return 2
        if self.env_config['type_drivers'] == clique_type.get('type_drivers'):
            return 1
        else:
            return 0

    # Get clique type with max priority
    # for given environment configuration and focal point type
    def _get_clique_type(self, focal_point, clique_types):
        # If there's no configuration match for the specified environment,
        # we use the default clique type definition with environment='ANY'
        fallback_type = next(
            filter(lambda t: t['environment'] == 'ANY', clique_types),
            None
        )
        if not fallback_type:
            raise ValueError("No fallback clique type (ANY) "
                             "defined for focal point type '{}'"
                             .format(focal_point))

        clique_types.remove(fallback_type)

        priority_scores = [self._get_priority_score(clique_type)
                           for clique_type
                           in clique_types]
        max_score = max(priority_scores) if priority_scores else 0

        return (fallback_type
                if max_score == 0
                else clique_types[priority_scores.index(max_score)])

    def get_clique_types(self):
        if not self.clique_types_by_type:
            clique_types_by_focal_point = self.clique_types.aggregate([{
                "$group": {
                    "_id": "$focal_point_type",
                    "types": {"$push": "$$ROOT"}
                }
            }])

            self.clique_types_by_type = {
                cliques['_id']: self._get_clique_type(cliques['_id'],
                                                      cliques['types'])
                for cliques in
                clique_types_by_focal_point
            }

        return self.clique_types_by_type

    def find_cliques_for_type(self, clique_type):
        focal_point_type = clique_type["focal_point_type"]
        constraint = self.clique_constraints \
            .find_one({"focal_point_type": focal_point_type})
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
        o = self.inventory.find_one({'_id': focal_point_db_id})
        constraint = self.clique_constraints \
            .find_one({"focal_point_type": o['type']})
        constraints = [] if not constraint else constraint["constraints"]
        clique_types = self.get_clique_types()
        clique_type = clique_types[o['type']]
        new_clique = self.construct_clique_for_focal_point(o, clique_type,
                                                           constraints)
        if not new_clique:
            self.cliques.delete({'_id': clique['_id']})

    def construct_clique_for_focal_point(self, o, clique_type, constraints):
        # keep a hash of nodes in clique that were visited for each type
        # start from the focal point
        nodes_of_type = {o["type"]: {str(o["_id"])}}
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
            self.check_link_type(clique, link_type, nodes_of_type)

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

    @staticmethod
    def check_constraints(clique, link):
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

    @staticmethod
    def get_link_type_reversed(link_type: str) -> str:
        if not CliqueFinder.link_type_reversed.get(link_type):
            link_type_parts = link_type.split('-')
            link_type_parts.reverse()
            CliqueFinder.link_type_reversed[link_type] = \
                '-'.join(link_type_parts)
        return CliqueFinder.link_type_reversed.get(link_type)

    def check_link_type(self, clique, link_type, nodes_of_type):
        # check if it's backwards
        link_type_reversed = self.get_link_type_reversed(link_type)
        # handle case of links like T<-->T
        self_linked = link_type == link_type_reversed
        use_reversed = False
        if not self_linked:
            matches = self.links.find_one({
                "environment": self.env,
                "link_type": link_type_reversed
            })
            use_reversed = True if matches else False
        if self_linked or not use_reversed:
            self.check_link_type_forward(clique, link_type, nodes_of_type)
        if self_linked or use_reversed:
            self.check_link_type_back(clique, link_type, nodes_of_type)

    def check_link_type_for_direction(self, clique, link_type, nodes_of_type,
                                      is_reversed=False):
        if is_reversed:
            link_type = self.get_link_type_reversed(link_type)
        from_type = link_type[:link_type.index("-")]
        to_type = link_type[link_type.index("-") + 1:]
        side_to_match = 'target' if is_reversed else 'source'
        other_side = 'target' if not is_reversed else 'source'
        match_type = to_type if is_reversed else from_type
        if match_type not in nodes_of_type.keys():
            return
        other_side_type = to_type if not is_reversed else from_type
        nodes_to_add = set()
        for match_point in nodes_of_type[match_type]:
            matches = self.find_matches_for_point(match_point,
                                                  clique,
                                                  link_type,
                                                  side_to_match,
                                                  other_side)
            nodes_to_add = nodes_to_add | matches
        if other_side_type not in nodes_of_type:
            nodes_of_type[other_side_type] = set()
        nodes_of_type[other_side_type] = \
            nodes_of_type[other_side_type] | nodes_to_add

    def find_matches_for_point(self, match_point, clique, link_type,
                               side_to_match, other_side) -> set:
        nodes_to_add = set()
        matches = self.links.find({
            "environment": self.env,
            "link_type": link_type,
            side_to_match: ObjectId(match_point)
        })
        for link in matches:
            link_id = link["_id"]
            if link_id in clique["links"]:
                continue
            if not self.check_constraints(clique, link):
                continue
            clique["links"].append(link_id)
            clique["links_detailed"].append(link)
            other_side_point = str(link[other_side])
            nodes_to_add.add(other_side_point)
        return nodes_to_add

    def check_link_type_forward(self, clique, link_type, nodes_of_type):
        self.check_link_type_for_direction(clique, link_type, nodes_of_type,
                                           is_reversed=False)

    def check_link_type_back(self, clique, link_type, nodes_of_type):
        self.check_link_type_for_direction(clique, link_type, nodes_of_type,
                                           is_reversed=True)
