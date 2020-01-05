from base.utils.util import ClassResolver

from base.utils.metadata_parser import MetadataParser


class ProcessorsMetadataParser(MetadataParser):

    PROCESSORS_FILE = "processors.json"

    PROCESSORS_PACKAGE = "processors_package"
    BASE_PROCESSOR = "base_processor"
    PROCESSORS = "processors"

    def __init__(self):
        super().__init__()
        self.processors_package = None
        self.base_processor_class = None
        self.base_processor = None
        self.processors = []

    def validate_processor(self, processor_class):
        try:
            module_name = ClassResolver.get_module_file_by_class_name(processor_class)
            instance = ClassResolver.get_instance_of_class(package_name=self.processors_package,
                                                           module_name=module_name,
                                                           class_name=processor_class)

        except ValueError:
            instance = None

        if instance:
            if isinstance(instance, self.base_processor.__class__):
                self.processors.append(instance)
            else:
                self.add_error('Processor "{}" should subclass base processor "{}"'
                               .format(processor_class, self.base_processor_class))
        else:
            self.add_error('Failed to import link finder class "{}"'
                           .format(processor_class))

    def validate_metadata(self, metadata: dict):
        super().validate_metadata(metadata)
        self.processors_package = metadata[self.PROCESSORS_PACKAGE]
        self.base_processor_class = metadata[self.BASE_PROCESSOR]
        base_processor_module = ClassResolver.get_module_file_by_class_name(self.base_processor_class)

        try:
            self.base_processor = ClassResolver.get_instance_of_class(package_name=self.processors_package,
                                                                      module_name=base_processor_module,
                                                                      class_name=self.base_processor_class)
        except ValueError:
            self.base_processor = None

        if not self.base_processor:
            self.add_error("Couldn't create base processor instance"
                           "for class name '{}'".format(self.base_processor_class))
            return False

        for processor in metadata[self.PROCESSORS]:
            self.validate_processor(processor_class=processor)
        metadata[self.PROCESSORS] = self.processors

        return len(self.errors) == 0

    def get_required_fields(self) -> list:
        return [self.PROCESSORS_PACKAGE, self.BASE_PROCESSOR, self.PROCESSORS]
