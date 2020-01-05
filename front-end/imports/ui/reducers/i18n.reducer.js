///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
//import * as R from 'ramda';

const defaultState = { 
  apis: {

  },
  collections: {
    environments: {
      fields: {
        eventBasedScan: {
          header: 'Event based scan',
          desc: 'Update the inventory in real-time whenever a user makes a change to the OpenStack environment'
        }
      }
    }
  },
  components: {
    environment: {
      noGraphForLeafMsg: 'No clique for this focal_point',
      briefInfos: {
        lastScanning: {
          header: 'Last scanning'
        },
        vConnectorsNum: {
          header: 'Number of vConnectors'
        },
        hostsNum: {
          header: 'Number of hosts'
        },
        vServicesNum: {
          header: 'Number of vServices'
        },
        instancesNum: {
          header: 'Number of instances'
        },
        containersNum: {
            header: 'Number of containers'
        },
        podsNum: {
            header: 'Number of pods'
        },
      },
      newBriefInfos: {
        lastScanning: {
          header: 'Last scanning'
        },
        vConnectorsNum: {
          header: 'vConnectors'
        },
        hostsNum: {
          header: 'Hosts'
        },
        vServicesNum: {
          header: 'vServices'
        },
        instancesNum: {
          header: 'Instances'
        },
        containersNum: {
            header: 'Containers'
        },
        podsNum: {
            header: 'Pods'
        },
      },
      newListInfoBoxes: {
        regions: {
          header: 'Regions',
          baseType: 'region'
        },
        projects: {
          header: 'Projects',
          baseType: 'project'
        },
        networks: {
          header: 'Networks',
          baseType: 'network'
        },
        hosts: {
          header: 'Hosts',
          baseType: 'host'
        },
        namespaces: {
          header: 'Namespaces',
          baseType: 'namespace'
        }
      },
      listInfoBoxes: {
        regions: {
          header: 'Regions'
        },
        projects: {
          header: 'Projects'
        },
        networks: {
          header: 'Networks'
        },
        hosts: {
          header: 'Hosts'
        }
      }
    },
    projectDashboard: {
      infoBoxes: {
        networks: {
          header: 'Networks'
        },
        ports: {
          header: 'Ports'
        }
      }
    },

    regionDashboard: {
      infoBoxes: {
        instances: {
          header: 'Instances',
        },
        vServices: {
          header: 'vServices'
        },
        hosts: {
          header: 'Hosts'
        },
        vConnectors: {
          header: 'vConnectors'
        }
      },
      listInfoBoxes: {
        availabilityZones: {
          header: 'Availability zones',
          baseType: 'zone'
        },
        aggregates: {
          header: 'Aggregates',
          baseType: 'aggregate'
        }
      }
    },

    zoneDashboard: {
      infoBoxes: {
        instances: {
          header: 'Instances'
        },
        vServices: {
          header: 'vServices'
        },
        hosts: {
          header: 'Hosts'
        },
        vConnectors: {
          header: 'vConnectors'
        },
        vEdges: {
          header: 'vEdges'
        }
      },
      listInfoBoxes: {
        hosts: {
          header: 'Hosts',
          baseType: 'host'
        },
      }
    },

    aggregateDashboard: {
      infoBoxes: {
        instances: {
          header: 'Instances'
        },
        vServices: {
          header: 'vServices'
        },
        hosts: {
          header: 'Hosts'
        },
        vConnectors: {
          header: 'vConnectors'
        },
        vEdges: {
          header: 'vEdges'
        }
      },
      listInfoBoxes: {
        hosts: {
          header: 'Hosts',
          baseType: 'host'
        },
      }
    },

    hostDashboard: {
      infoBoxes: {
        instances: {
          header: 'Instances'
        },
        vServices: {
          header: 'vServices'
        },
        containers: {
            header: 'Containers'
        },
        pods: {
            header: 'Pods'
        },
        vConnectors: {
          header: 'vConnectors'
        },
        networkAgents: {
          header: 'Agents'
        },
        pnics: {
          header: 'pnics'
        },
        vEdges: {
          header: 'vEdges'
        },
        ports: {
          header: 'Ports'
        }
      },
    },

    generalFolderNodeDashboard: {
      mainCubic: {
        header: 'Number of children'
      }
    }
  }
};

export function reducer(state = defaultState, action) {
  switch (action.type) {

  default: 
    return state;
  }
}
