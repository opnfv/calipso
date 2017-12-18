###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from discover.link_finders.find_links import FindLinks


class FindImplicitLinks(FindLinks):

    def __init__(self):
        super().__init__()
        self.links = []
        self.constraint_attributes = self.get_constraint_attributes()

    def add_links(self):
        self.log.info('adding implicit links')
        self.get_existing_links()
        self.get_transitive_closure()

    def get_constraint_attributes(self) -> list:
        attributes = set()
        for c in self.inv.find({'environment': self.get_env()},
                               collection='clique_constraints'):
            for a in c['constraints']:
                attributes.add(a)
        return list(attributes)

    def get_existing_links(self):
        self.log.info('fetching existing links')
        existing_links = self.inv.find({'environment': self.get_env()},
                                       collection='links')
        for l in existing_links:
            self.links.append({'pass': 0, 'link': l})

    def constraints_match(self, link1, link2):
        if 'attributes' not in link1 or 'attributes' not in link2:
            return True
        attr1 = link1['attributes']
        attr2 = link2['attributes']
        for a in self.constraint_attributes:
            if a in attr1 and a in attr2 and attr1[a] != attr2[a]:
                return False
        return True

    def links_match(self, start, dest):
        if start['link_type'] == dest['link_type']:
            return False  # obviously we cannot make an implicit link of this
        if start['source_id'] == dest['target_id']:
            return False  # avoid cyclic links
        if not self.constraints_match(start, dest):
            return False
        return start['target_id'] == dest['source_id']

    def add_matching_links(self, link, pass_no):
        self.log.debug('looking for matches for link: {};{}'
                       .format(link['source_id'], link['target_id']))
        matches = [l for l in self.links
                   if l['pass'] == 0  # take only original links
                   and self.links_match(link, l['link'])]
        for l in matches:
            implicit = self.add_implicit_link(link, l['link'])
            self.links.append({'pass': pass_no, 'link': implicit})
        return len(matches)

    def get_link_constraint_attributes(self, link1, link2) -> dict:
        attributes = {}
        for a in self.constraint_attributes:
            # constraints_match() verified the attribute values don't conflict
            if a in link1.get('attributes', {}):
                attributes[a] = link1['attributes'][a]
            elif a in link2.get('attributes', {}):
                attributes[a] = link2['attributes'][a]
        return attributes

    @staticmethod
    def get_attr(attr, link1, link2):
        if attr not in link1 and attr not in link2:
            return None
        if attr not in link1:
            return link2[attr]
        if attr not in link2 or link1[attr] == link2[attr]:
            return link1[attr]
        return None

    def add_implicit_link(self, link1, link2):
        link_type_from = link1['link_type'].split('-')[0]
        link_type_to = link2['link_type'].split('-')[1]
        link_type = '{}-{}'.format(link_type_from, link_type_to)
        link_name = ''
        state = 'down' \
            if link1['state'] == 'down' or link2['state'] == 'down' \
            else 'up'
        link_weight = 0  # TBD
        host = self.get_attr('host', link1, link2)
        switch = self.get_attr('switch', link1, link2)
        extra_attributes = self.get_link_constraint_attributes(link1, link2)
        self.log.debug('adding implicit link: link type: {}, from: {}, to: {}'
                       .format(link_type,
                               link1['source_id'],
                               link2['target_id']))
        implicit = self.create_link(self.get_env(),
                                    link1['source'], link1['source_id'],
                                    link2['target'], link2['target_id'],
                                    link_type, link_name, state, link_weight,
                                    host=host, switch=switch,
                                    implicit=True,
                                    extra_attributes=extra_attributes)
        return implicit

    def get_transitive_closure(self):
        pass_no = 1
        while True:
            match_count = 0
            last_pass_links = [l for l in self.links if l['pass'] == pass_no-1]
            for l in last_pass_links:
                match_count += self.add_matching_links(l['link'], pass_no)
            self.log.info('Transitive closure pass #{}: '
                          'found {} implicit links'
                          .format(pass_no, match_count))
            if match_count == 0:
                break
            pass_no += 1
        self.log.info('done adding implicit links')
