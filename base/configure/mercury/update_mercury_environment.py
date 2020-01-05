import argparse
import os

import json

from setup_initial_data import HOST, DB_USER, DEFAULT_DB, DEFAULT_PORT, MongoConnector, _exit

ENV_CONFIG_COLLECTION = "environments_config"
ENV_OPTIONS_COLLECTION = "environment_options"
SUPPORTED_ENVS_COLLECTION = "supported_environments"
CONSTANTS_COLLECTION = "constants"
REQUIRED_FIELDS = ('name', 'environment_type', 'distribution', 'distribution_version',
                   'mechanism_drivers', 'type_drivers')
DISTRIBUTION = 'Mercury'
ALLOWED_FEATURES = {
    'scanning': True,
    'monitoring': True,
    'listening': True
}

DEFAULT_SOURCE = "/data/mercury_environment_config.json"
DB_PWD = os.environ["CALIPSO_MONGO_SERVICE_PWD"]


def validate_env_config(env_dict):
    error_msg = ""
    missing_fields = [field for field in REQUIRED_FIELDS if field not in env_dict]
    if missing_fields:
        error_msg += "Missing fields: {}\n".format(
            ', '.join(field for field in REQUIRED_FIELDS if field not in env_dict)
        )
        return error_msg
    if env_dict.get('distribution') != DISTRIBUTION:
        error_msg += "Distribution must be '{}'\n".format(DISTRIBUTION)

    return error_msg


def update_constants(env_dict):
    distribution_versions = mongo_connector.find_one(CONSTANTS_COLLECTION,
                                                     {'name': 'distribution_versions'})
    dv = env_dict['distribution_version']
    for version in distribution_versions['data']:
        if version['label'] == dv:
            print("Distribution version '{}' already exists in constants".format(dv))
            return

    distribution_versions['data'].append({
        'label': dv,
        'value': dv
    })

    print("Inserting distribution version '{}' in constants".format(dv))
    mongo_connector.update(CONSTANTS_COLLECTION,
                           {'_id': distribution_versions['_id']},
                           distribution_versions)


def update_environment_options(env_dict):
    env_options = mongo_connector.find(ENV_OPTIONS_COLLECTION)

    distribution = env_dict['distribution']
    distribution_version = env_dict['distribution_version']
    type_driver = env_dict['type_drivers']

    # Find if distribution is already in env options
    doc = None
    for option in env_options:
        if distribution in option['distributions']:
            doc = option
            break

    if not doc:
        # No matching distribution found, create new doc
        print("Adding new environment option for '{}-{}'"
              .format(distribution, distribution_version))
        doc = {
            'distributions': [distribution],
            'distribution_versions': [distribution_version],
            'mechanism_drivers': env_dict['mechanism_drivers'],
            'type_drivers': [type_driver]
        }
        mongo_connector.insert(ENV_OPTIONS_COLLECTION, doc)
        return
    else:
        # Update existing doc with new options
        print("Updating existing environment option for '{}-{}'"
              .format(distribution, distribution_version))
        if distribution_version not in doc['distribution_versions']:
            doc['distribution_versions'].append(distribution_version)
        if type_driver not in doc['type_drivers']:
            doc['type_drivers'].append(type_driver)
        for mecha_driver in env_dict['mechanism_drivers']:
            if mecha_driver not in doc['mechanism_drivers']:
                doc['mechanism_drivers'].append(mecha_driver)
        mongo_connector.update(ENV_OPTIONS_COLLECTION, {'_id': doc['_id']}, doc)


def update_supported_environments(env_dict):
    env_options = mongo_connector.find(SUPPORTED_ENVS_COLLECTION,
                                       {'environment.distribution': env_dict['distribution']})

    for env_option in env_options:
        # Convert fields to lists for easier matching
        env_req = env_option['environment']
        dv, md, td = (
            env_req['distribution_version'], env_req['mechanism_drivers'], env_req['type_drivers']
        )
        requirements = {
            'distribution_version': dv if isinstance(dv, list) else [dv],
            'mechanism_drivers': md if isinstance(md, list) else [md],
            'type_drivers': td if isinstance(td, list) else [td]
        }

        # Find out whether this combination of mecha_drivers+type_drivers+features is already supported
        if (all(m in requirements['mechanism_drivers'] for m in env_dict['mechanism_drivers'])
                and env_dict['type_drivers'] in requirements['type_drivers']
                and ALLOWED_FEATURES == env_option['features']):
            # Add the distribution version if it's missing
            if env_dict['distribution_version'] not in requirements['distribution_version']:
                print("Updating supported environment configuration for '{}-{}'"
                      .format(env_dict['distribution'], env_dict['distribution_version']))
                env_option['environment']['distribution_version'] = (
                        requirements['distribution_version'] + [env_dict['distribution_version']]
                )
                mongo_connector.update(SUPPORTED_ENVS_COLLECTION,
                                       {'_id': env_option['_id']},
                                       env_option)
                return
            print("Environment configuration '{}-{}' with features '{}' already supported"
                  .format(env_dict['distribution'], env_dict['distribution_version'], ALLOWED_FEATURES))
            return

    # No matching entry found, need to add a new doc
    print("Adding a new supported environment configuration '{}-{}' with features '{}'"
          .format(env_dict['distribution'], env_dict['distribution_version'], ALLOWED_FEATURES))
    doc = {
        'features': ALLOWED_FEATURES,
        'environment': {
            'distribution': env_dict['distribution'],
            'distribution_version': env_dict['distribution_version'],
            'mechanism_drivers': env_dict['mechanism_drivers'][0],
            'type_drivers': env_dict['type_drivers']
        }
    }
    mongo_connector.insert(SUPPORTED_ENVS_COLLECTION, doc)


def enable_environment_config(env_dict):
    update_constants(env_dict)
    update_environment_options(env_dict)
    update_supported_environments(env_dict)


def update_environment_config(env_dict):
    env_name = env_dict['name']
    existing_env = mongo_connector.find_one(ENV_CONFIG_COLLECTION, {'name': env_name})
    if existing_env:
        print("Environment '{}' already exists. Updating document".format(env_name))
        env_id = existing_env['_id']
        mongo_connector.update(ENV_CONFIG_COLLECTION, {'_id': existing_env['_id']}, env_dict)
        print("Environment '{}' updated successfully".format(env_name))
    else:
        print("Inserting environment '{}'".format(env_name))
        env_id = mongo_connector.insert(ENV_CONFIG_COLLECTION, env_dict)
        print("Environment '{}' inserted successfully".format(env_name))
    return mongo_connector.find_one(ENV_CONFIG_COLLECTION, {'_id': env_id})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--db_name",
                        help="Database name (default={})".format(DEFAULT_DB),
                        type=str,
                        default=DEFAULT_DB,
                        required=False)
    parser.add_argument("-p", "--port",
                        help="Port for the MongoDB daemon (default={})".format(DEFAULT_PORT),
                        type=int,
                        default=DEFAULT_PORT,
                        required=False)
    parser.add_argument("-s", "--source",
                        help="Environment config file location (default={})".format(DEFAULT_SOURCE),
                        type=str,
                        default=DEFAULT_SOURCE,
                        required=False)
    args = parser.parse_args()

    mongo_connector = MongoConnector(HOST, args.port, DB_USER, DB_PWD, args.db_name)
    try:
        with open(args.source) as f:
            env_json = json.loads(f.read())
            validation_errors = validate_env_config(env_json)
            if validation_errors:
                raise ValueError(validation_errors)
            enable_environment_config(env_json)
            update_environment_config(env_json)
    finally:
        mongo_connector.disconnect()

    _exit(0)
