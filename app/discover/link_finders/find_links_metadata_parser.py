###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from utils.metadata_parser import MetadataParser
from utils.util import ClassResolver


class FindLinksMetadataParser(MetadataParser):

    FINDERS_FILE = "link_finders.json"

    FINDERS_PACKAGE = "finders_package"
    BASE_FINDER = "base_finder"
    LINK_FINDERS = "link_finders"

    def __init__(self):
        super().__init__()
        self.finders_package = None
        self.base_finder_class = None
        self.base_finder = None
        self.link_finders = []

    def validate_link_finder(self, finder_class):
        try:
            module_name = ClassResolver.get_module_file_by_class_name(finder_class)
            instance = ClassResolver\
                .get_instance_of_class(package_name=self.finders_package,
                                       module_name=module_name,
                                       class_name=finder_class)

        except ValueError:
            instance = None

        if instance:
            if isinstance(instance, self.base_finder.__class__):
                self.link_finders.append(instance)
            else:
                self.add_error('Link finder "{}" should subclass '
                               'base link finder "{}"'
                               .format(finder_class, self.base_finder_class))
        else:
            self.add_error('Failed to import link finder class "{}"'
                           .format(finder_class))

    def validate_metadata(self, metadata: dict):
        super().validate_metadata(metadata)
        self.finders_package = metadata[self.FINDERS_PACKAGE]
        self.base_finder_class = metadata[self.BASE_FINDER]
        base_finder_module = ClassResolver\
            .get_module_file_by_class_name(self.base_finder_class)

        try:
            self.base_finder = ClassResolver\
                .get_instance_of_class(package_name=self.finders_package,
                                       module_name=base_finder_module,
                                       class_name=self.base_finder_class)
        except ValueError:
            self.base_finder = None

        if not self.base_finder:
            self.add_error("Couldn't create base link finder instance"
                           "for class name '{}'".format(self.base_finder_class))
            return False

        for link_finder in metadata[self.LINK_FINDERS]:
            self.validate_link_finder(finder_class=link_finder)
        metadata[self.LINK_FINDERS] = self.link_finders

        return len(self.errors) == 0

    def get_required_fields(self) -> list:
        return [self.FINDERS_PACKAGE, self.BASE_FINDER, self.LINK_FINDERS]

