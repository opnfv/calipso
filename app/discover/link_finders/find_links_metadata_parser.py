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
            self.link_finders.append(instance)
        else:
            self.add_error('Failed to import link finder class "{}"'
                           .format(finder_class))

    def validate_metadata(self, metadata: dict):
        super().validate_metadata(metadata)
        self.finders_package = metadata[self.FINDERS_PACKAGE]
        self.base_finder = metadata[self.BASE_FINDER]
        base_finder_module = ClassResolver\
            .get_module_file_by_class_name(self.base_finder)

        base_finder_class = ClassResolver.get_class_name_by_module(
            ".".join((self.finders_package, base_finder_module)))

        if not base_finder_class:
            self.add_error("Couldn't find base link finder class")
            return

        for link_finder in metadata[self.LINK_FINDERS]:
            self.validate_link_finder(finder_class=link_finder)
        metadata[self.LINK_FINDERS] = self.link_finders

        return len(self.errors) == 0

    def get_required_fields(self) -> list:
        return [self.FINDERS_PACKAGE, self.BASE_FINDER, self.LINK_FINDERS]

