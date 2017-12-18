###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import re


from api.validation import regex


class DataValidate:
    LIST = "list"
    REGEX = "regex"

    def __init__(self):
        super().__init__()
        self.BOOL_CONVERSION = {
            "true": True,
            "1": True,
            1: True,
            "false": False,
            "0": False,
            0: False
        }
        self.TYPES_CUSTOMIZED_NAMES = {
            'str': 'string',
            'bool': 'boolean',
            'int': 'integer',
            'ObjectId': 'MongoDB ObjectId'
        }
        self.VALIDATE_SWITCHER = {
            self.LIST: self.validate_value_in_list,
            self.REGEX: regex.validate
        }

    def validate_type(self, obj, t, convert_to_type):
        if convert_to_type:
            # user may input different values for the
            # boolean True or False, convert the number or
            # the string to corresponding python bool values
            if t == bool:
                if isinstance(obj, str):
                    obj = obj.lower()
                if obj in self.BOOL_CONVERSION:
                    return self.BOOL_CONVERSION[obj]
                return None
            try:
                obj = t(obj)
            except Exception:
                return None
            return obj
        else:
            return obj if isinstance(obj, t) else None

    # get the requirement for validation
    # this requirement object will be used in validate_data method
    @staticmethod
    def require(types, convert_to_type=False, validate=None,
                requirement=None, mandatory=False, error_messages=None):
        if error_messages is None:
            error_messages = {}
        return {
            "types": types,
            "convert_to_type": convert_to_type,
            "validate": validate,
            "requirement": requirement,
            "mandatory": mandatory,
            "error_messages": error_messages
        }

    def validate_data(self, data, requirements,
                      additional_key_re=None,
                      can_be_empty_keys=None):
        if can_be_empty_keys is None:
            can_be_empty_keys = []

        illegal_keys = [key for key in data.keys()
                        if key not in requirements.keys()]

        if additional_key_re:
            illegal_keys = [key for key in illegal_keys
                            if not re.match(additional_key_re, key)]

        if illegal_keys:
            return 'Invalid key(s): {0}'.format(' and '.join(illegal_keys))

        for key, requirement in requirements.items():
            value = data.get(key)
            error_messages = requirement['error_messages']

            if not value and value is not False and value is not 0:
                if key in data and key not in can_be_empty_keys:
                    return "Invalid data: value of {0} key doesn't exist ".format(key)
                # check if the key is mandatory
                mandatory_error = error_messages.get('mandatory')
                error_message = self.mandatory_check(key,
                                                     requirement['mandatory'],
                                                     mandatory_error)
                if error_message:
                    return error_message
                continue

            # check the required types
            error_message = self.types_check(requirement["types"],
                                             requirement["convert_to_type"],
                                             key,
                                             value, data,
                                             error_messages.get('types'))
            if error_message:
                return error_message

            # after the types check, the value of the key may be changed
            # get the value again
            value = data[key]
            validate = requirement.get('validate')
            if not validate:
                continue
            requirement_value = requirement.get('requirement')
            # validate the data against the requirement
            req_error = error_messages.get("requirement")
            error_message = self.requirement_check(key, value, validate,
                                                   requirement_value,
                                                   req_error)
            if error_message:
                return error_message
        return None

    @staticmethod
    def mandatory_check(key, mandatory, error_message):
        if mandatory:
            return error_message if error_message \
                    else "{} must be specified".format(key)
        return None

    def types_check(self, requirement_types, convert_to_type, key,
                    value, data, error_message):
        if not isinstance(requirement_types, list):
            requirement_types = [requirement_types]
        for requirement_type in requirement_types:
            converted_val = self.validate_type(
                value, requirement_type, convert_to_type
            )
            if converted_val is not None:
                if convert_to_type:
                    # value has been converted, update the data
                    data[key] = converted_val
                return None
        required_types = self.get_type_names(requirement_types)
        return error_message if error_message else \
            "{0} must be {1}".format(key, " or ".join(required_types))

    def requirement_check(self, key, value, validate,
                          requirement, error_message):
        return self.VALIDATE_SWITCHER[validate](key, value, requirement,
                                                error_message)

    @staticmethod
    def validate_value_in_list(key, value,
                               required_list, error_message):
        if not isinstance(value, list):
            value = [value]

        if [v for v in value if v not in required_list]:
            return error_message if error_message else\
                "The possible value of {0} is {1}".\
                format(key, " or ".join(required_list))
        return None

    # get customized type names from type names array
    def get_type_names(self, types):
        return [self.get_type_name(t) for t in types]

    # get customized type name from string <class 'type'>
    def get_type_name(self, t):
        t = str(t)
        a = t.split(" ")[1]
        type_name = a.rstrip(">").strip("'")
        # strip the former module names
        type_name = type_name.split('.')[-1]
        if type_name in self.TYPES_CUSTOMIZED_NAMES.keys():
            type_name = self.TYPES_CUSTOMIZED_NAMES[type_name]
        return type_name
