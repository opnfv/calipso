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
        self.log.info("Scanning for cliques")
        clique_types = self.get_clique_types().values()
        for clique_type in clique_types:
            self.find_cliques_for_type(clique_type)
        self.log.info("Finished scanning for cliques")

    # Calculate priority score for clique type per environment and configuration
    def get_priority_score(self, clique_type):
        # environment-specific clique type takes precedence
        env = clique_type.get('environment')
        config = self.env_config
        # ECT - Clique Type with Environment name
        if env:
            if self.env == env:
                return 2**6
            if env == 'ANY':
                # environment=ANY serves as fallback option
                return 2**0
            return 0
        # NECT - Clique Type without Environment name
        else:
            env_type = clique_type.get('environment_type')
            # TODO: remove backward compatibility ('if not env_type' check)
            if env_type and env_type != config.get('environment_type'):
                return 0

            score = 0

            distribution = clique_type.get('distribution')
            if distribution:
                if config['distribution'] != distribution:
                    return 0

                score += 2**5

                dv = clique_type.get('distribution_version')
                if dv:
                    if dv != config['distribution_version']:
                        return 0
                    score += 2**4

            mechanism_drivers = clique_type.get('mechanism_drivers')
            if mechanism_drivers:
                if mechanism_drivers not in config['mechanism_drivers']:
                    return 0
                score += 2**3

            type_drivers = clique_type.get('type_drivers')
            if type_drivers:
                if type_drivers != config['type_drivers']:
                    return 0
                score += 2**2

            # If no configuration is specified, this clique type
            # is a fallback for its environment type
            return max(score, 2**1)

    # Get clique type with max priority
    # for given focal point type
    def _get_clique_type(self, clique_types):
        scored_clique_types = [{'score': self.get_priority_score(clique_type),
                                'clique_type': clique_type}
                               for clique_type in clique_types]
        max_score = max(scored_clique_types, key=lambda t: t['score'])
        if max_score['score'] == 0:
            self.log.warn('No matching clique types '
                          'for focal point type: {fp_type}'
                          .format(fp_type=clique_types[0].get('focal_point_type')))
            return None
        return max_score.get('clique_type')

    def get_clique_types(self):
        if not self.clique_types_by_type:
            clique_types_candidates = {}
            for clique in self.clique_types.find({}):
                fp_type = clique.get('focal_point_type', '')
                if not clique_types_candidates.get(fp_type):
                    clique_types_candidates[fp_type] = []
                clique_types_candidates[fp_type].append(clique)
            for t in clique_types_candidates.keys():
                selected = self._get_clique_type(clique_types_candidates[t])
                if not selected:
                    continue
                self.clique_types_by_type[t] = selected
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
        clique_type = clique_types.get(o['type'])
        if not clique_type:
            self.cliques.delete({'_id': clique['_id']})
        else:
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
        allow_implicit = clique_type.get('use_implicit_links', False)
        for link_type in clique_type["link_types"]:
            if not self.check_link_type(clique, link_type, nodes_of_type,
                                        allow_implicit=allow_implicit):
                break

        # after adding the links to the clique, create/update the clique
        if not clique["links"]:
            return None
        clique["clique_type"] = clique_type["_id"]
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

    def check_link_type(self, clique, link_type, nodes_of_type,
                        allow_implicit=False) -> bool:
        # check if it's backwards
        link_type_reversed = self.get_link_type_reversed(link_type)
        # handle case of links like T<-->T
        self_linked = link_type == link_type_reversed
        use_reversed = False
        if not self_linked:
            link_search_condition = {
                "environment": self.env,
                "link_type": link_type_reversed
            }
            if not allow_implicit:
                link_search_condition['implicit'] = False
            matches = self.links.find_one(link_search_condition)
            use_reversed = True if matches else False
        if self_linked or not use_reversed:
            return self.check_link_type_forward(clique, link_type,
                                                nodes_of_type,
                                                allow_implicit=allow_implicit)
        if self_linked or use_reversed:
            return self.check_link_type_back(clique, link_type, nodes_of_type,
                                             allow_implicit=allow_implicit)

    def check_link_type_for_direction(self, clique, link_type, nodes_of_type,
                                      is_reversed=False,
                                      allow_implicit=False) -> bool:
        if is_reversed:
            link_type = self.get_link_type_reversed(link_type)
        from_type = link_type[:link_type.index("-")]
        to_type = link_type[link_type.index("-") + 1:]
        side_to_match = 'target' if is_reversed else 'source'
        other_side = 'target' if not is_reversed else 'source'
        match_type = to_type if is_reversed else from_type
        if match_type not in nodes_of_type.keys():
            return False
        other_side_type = to_type if not is_reversed else from_type
        nodes_to_add = set()
        for match_point in nodes_of_type[match_type]:
            matches = self.find_matches_for_point(match_point,
                                                  clique,
                                                  link_type,
                                                  side_to_match,
                                                  other_side,
                                                  allow_implicit=allow_implicit)
            nodes_to_add = nodes_to_add | matches
        if other_side_type not in nodes_of_type:
            nodes_of_type[other_side_type] = set()
        nodes_of_type[other_side_type] = \
            nodes_of_type[other_side_type] | nodes_to_add
        return len(nodes_to_add) > 0

    def find_matches_for_point(self, match_point, clique, link_type,
                               side_to_match, other_side,
                               allow_implicit=False) -> set:
        nodes_to_add = set()
        link_search_condition = {
            "environment": self.env,
            "link_type": link_type,
            side_to_match: ObjectId(match_point)
        }
        if not allow_implicit:
            link_search_condition['implicit'] = False
        matches = self.links.find(link_search_condition)
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

    def check_link_type_forward(self, clique, link_type, nodes_of_type,
                                allow_implicit=False) -> bool:
        return self.check_link_type_for_direction(clique, link_type,
                                                  nodes_of_type,
                                                  is_reversed=False,
                                                  allow_implicit=allow_implicit)

    def check_link_type_back(self, clique, link_type, nodes_of_type,
                             allow_implicit=False) -> bool:
        return self.check_link_type_for_direction(clique, link_type,
                                                  nodes_of_type,
                                                  is_reversed=True,
                                                  allow_implicit=allow_implicit)
