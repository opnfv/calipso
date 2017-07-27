###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
METADATA_EMPTY = {}

METADATA_SCANNERS_MISSING = {"scanners_package": "discover.fetchers"}

METADATA_NO_PACKAGE = {
  "scanners": {}
}

METADATA_NO_SCANNERS = {
  "scanners_package": "discover.fetchers"
}

METADATA_ZERO_SCANNERS = {
  "scanners_package": "discover.fetchers",
  "scanners": {}
}

METADATA_SIMPLE_SCANNER = {
  "scanners_package": "discover.fetchers",
  "scanners": {
    "ScanAggregate": [
      {
        "type": "host_ref",
        "fetcher": "DbFetchAggregateHosts"
      }
    ]
  }
}

METADATA_SCANNER_UNKNOWN_ATTRIBUTE = {
  "scanners_package": "discover.fetchers",
  "scanners": {
    "ScanAggregate": [
      {
        "xyz": "123",
        "type": "host_ref",
        "fetcher": "DbFetchAggregateHosts"
      }
    ]
  }
}

METADATA_SCANNER_NO_TYPE = {
  "scanners_package": "discover.fetchers",
  "scanners": {
    "ScanAggregate": [
      {
        "fetcher": "DbFetchAggregateHosts"
      }
    ]
  }
}

METADATA_SCANNER_NO_FETCHER = {
  "scanners_package": "discover.fetchers",
  "scanners": {
    "ScanAggregate": [
      {
        "type": "host_ref"
      }
    ]
  }
}

METADATA_SCANNER_INCORRECT_TYPE = {
  "scanners_package": "discover.fetchers",
  "scanners": {
    "ScanAggregate": [
      {
        "type": "t1",
        "fetcher": "DbFetchAggregateHosts"
      }
    ]
  }
}

METADATA_SCANNER_INCORRECT_FETCHER = {
  "scanners_package": "discover.fetchers",
  "scanners": {
    "ScanAggregate": [
      {
        "type": "host_ref",
        "fetcher": "f1"
      }
    ]
  }
}

METADATA_SCANNER_WITH_CHILD = {
  "scanners_package": "discover.fetchers",
  "scanners": {
    "ScanAggregatesRoot": [
      {
        "type": "aggregate",
        "fetcher": "DbFetchAggregates",
        "children_scanner": "ScanAggregate"
      }
    ],
    "ScanAggregate": [
      {
        "type": "host_ref",
        "fetcher": "DbFetchAggregateHosts"
      }
    ]
  }
}

METADATA_SCANNER_WITH_INCORRECT_CHILD = {
  "scanners_package": "discover.fetchers",
  "scanners": {
    "ScanAggregatesRoot": [
      {
        "type": "aggregate",
        "fetcher": "DbFetchAggregates",
        "children_scanner": 1
      }
    ]
  }
}

METADATA_SCANNER_WITH_MISSING_CHILD = {
  "scanners_package": "discover.fetchers",
  "scanners": {
    "ScanAggregatesRoot": [
      {
        "type": "aggregate",
        "fetcher": "DbFetchAggregates",
        "children_scanner": "ScanAggregate"
      }
    ]
  }
}

METADATA_SCANNER_FETCHER_INVALID_DICT = {
  "scanners_package": "discover.fetchers",
  "scanners": {
    "ScanEnvironment": [
      {
        "type": "regions_folder",
        "fetcher": {
          "types_name": "regions",
          "parent_type": "environment"
        }
      },
    ]

  }
}

METADATA_SCANNER_WITH_FOLDER = {
  "scanners_package": "discover.fetchers",
  "scanners": {
    "ScanEnvironment": [
      {
        "type": "regions_folder",
        "fetcher": {
          "folder": 1,
          "types_name": "regions",
          "parent_type": "environment"
        }
      },
      {
        "type": "projects_folder",
        "fetcher": {
          "folder": 1,
          "types_name": "projects",
          "parent_type": "environment"
        }
      }
    ]
  }
}

METADATA_SCANNER_WITH_INVALID_CONDITION = {
  "scanners_package": "discover.fetchers",
  "scanners": {
    "ScanHost": [
      {
        "type": "pnics_folder",
        "fetcher": "DbFetchAggregateHosts",
        "environment_condition": 1
      }
    ]
  }
}

METADATA_SCANNER_WITH_INVALID_MECHANISM_DRIVER_CONDITION = {
  "scanners_package": "discover.fetchers",
  "scanners": {
    "ScanHost": [
      {
        "type": "pnics_folder",
        "fetcher": {
          "folder": 1,
          "types_name": "pnics",
          "parent_type": "host",
          "text": "pNICs"
        },
        "environment_condition": {
          "mechanism_drivers": ""
        }
      }
    ]
  }
}

METADATA_SCANNER_WITH_INVALID_MECHANISM_DRIVER = {
  "scanners_package": "discover.fetchers",
  "scanners": {
    "ScanHost": [
      {
        "type": "pnics_folder",
        "fetcher": {
          "folder": 1,
          "types_name": "pnics",
          "parent_type": "host",
          "text": "pNICs"
        },
        "environment_condition": {
          "mechanism_drivers": [ 1, 2]
        }
      }
    ]
  }
}

METADATA_SCANNER_WITH_CONDITION = {
  "scanners_package": "discover.fetchers",
  "scanners": {
    "ScanHost": [
      {
        "type": "pnics_folder",
        "fetcher": {
          "folder": 1,
          "types_name": "pnics",
          "parent_type": "host",
          "text": "pNICs"
        },
        "environment_condition": {
          "mechanism_drivers": [
            "OVS",
            "LXB"
          ]
        }
      }
    ]
  }
}

CONSTANTS = {
  "scan_object_types": {
      "name": "scan_object_types", 
      "data": [
          {
              "value": "regions_folder", 
              "label": "regions_folder"
          },
          {
              "value": "pnics_folder", 
              "label": "pnics_folder"
          },
          {
              "value": "projects_folder",
              "label": "projects_folder"
          },
          {
              "value": "aggregate", 
              "label": "aggregate"
          },
          {
              "value": "host", 
              "label": "host"
          },
          {
              "value": "region", 
              "label": "region"
          }, 
          {
              "value": "host_ref", 
              "label": "host_ref"
          }
      ]
  },
  "mechanism_drivers": { 
      "data": [
          {
              "label": "OVS", 
              "value": "OVS"
          }, 
          {
              "label": "VPP", 
              "value": "VPP"
          }, 
          {
              "label": "LXB", 
              "value": "LXB"
          }, 
          {
              "label": "Arista", 
              "value": "Arista"
          }, 
          {
              "label": "Nexus", 
              "value": "Nexus"
          }
      ], 
      "name": "mechanism_drivers"
  }
}
