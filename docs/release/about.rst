| Calipso.io
| Product Description and Value

Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others                                                                
All rights reserved. This program and the accompanying materials           
are made available under the terms of the Apache License, Version 2.0       
which accompanies this distribution, and is available at                    
http://www.apache.org/licenses/LICENSE-2.0

|image0|

Virtual and Physical networking low level details and inter-connections,
dependencies in OpenStack, Docker or Kubernetes environments are
currently invisible and abstracted, by design, so data is not exposed
through any API or UI.

During virtual networking failures, troubleshooting takes substantial
amount of time due to manual discovery and analysis.

Maintenance work needs to happen in the data center, virtual and
physical networking (controlled or not) are impacted.

Most of the times, the impact of any of the above scenarios is
catastrophic.

Project “Calipso” tries to illuminate complex virtual networking with
real time operational state visibility for large and highly distributed
Virtual Infrastructure Management (VIM).

*Customer needs during maintenance:*

Visualize the networking topology, easily pinpointing the location
needed for maintenance and show the impact of maintenance work needed in
that location.

Administrator can plan ahead easily and report up his command chain the
detailed impact – Calipso substantially lower the admin time and
overhead needed for that reporting.

*Customer need during troubleshooting:*

Visualize and pinpointing the exact location of the failure in the
networking chain, using a suspected ‘focal point’ (ex: a VM that cannot
communicate).

Monitor the networking location and alerting till the problem is
resolved. Calipso also covers pinpointing the root cause.

*Calipso is for multiple distributions/plugins and many virtual
environment variances:*

We built a fully tested unified model to deal with many variances.

Supporting in initial release: VPP, OVS, LXB with all type drivers
possible, onto 5 different OS distributions, totaling to more than 60
variances (see Calipso-model guide).

New classes per object, link and topology can be programmed (see
development guide).

*Detailed Monitoring:*

Calipso provides visible insights using smart discovery and virtual
topological representation in graphs, with monitoring per object in the
graph inventory to reduce error vectors and troubleshooting, maintenance
cycles for VIM operators and administrators.

*We believe that Stability is driven by accurate Visibility*.

Table of Contents

Calipso.io Product Description and Value 1

1 About 4

1.1 Project Description 4

2 Main modules 5

2.1 High level module descriptions 5

2.2 High level functionality 5

3 Customer Requirements 6

3.1 Releases and Distributions 7

About
=====

Project Description
-------------------

Calipso interfaces with the virtual infrastructure (like OpenStack)
through API, DB and CLI adapters, discovers the specific
distribution/plugins in-use, their versions and based on that collects
detailed data regarding running objects in the underlying workers and
processes running on the different hosts. Calipso analyzes the inventory
for inter-relationships and keeps them in a common and highly adaptive
data model.

Calipso then represents the inter-connections as real-time topologies
using automatic updates per changes in VIM, monitors the related objects
and analyzes the data for impact and root-cause analysis.

This is done with the objective to lower and potentially eliminate
complexity and lack of visibility from the VIM layers as well as to
offer a common and coherent representation of all physical and virtual
network components used under the VIM, all exposed through an API.

Calipso is developed to work with different OpenStack flavors, plugins
and installers.

Calipso is developed to save network admins discovery and
troubleshooting cycles of the networking aspects. Calipso helps estimate
the impact of several micro failure in the infrastructure to allow
appropriate resolutions.

Calipso focuses on scenarios, which requires VIM/OpenStack maintenance
and troubleshooting enhancements using operations dashboards i.e.
connectivity, topology and related stats – as well as their correlation.

|image1|

 Main modules
=============

High level module descriptions
------------------------------

Calipso modules included with initial release:

-  *Scanning*: detailed inventory discovery and inter-connection
   analysis, smart/logical and automated learning from the VIM, based on
   specific environment version/type etc.

-  *Listening*: Attach to VIM message BUS and update changes in real
   time.

-  *Visualization*: represent the result of the discovery in browsable
   graph topology and tree.

-  *Monitoring*: Health and status for all discovered objects and
   inter-connections: use the discovered data to configure monitoring
   agents and gather monitoring results.

-  *Analysis*: some traffic analysis, impact and root-cause analysis for
   troubleshooting.

-  *API:* allow integration with Calipso application’s inventory and
   monitoring results.

-  *Database*: Mongo based

-  *LDAP*: pre-built integration for smooth attachment to corporate
   directories.

For Monitoring we are planning to utilize the work done by ‘Sensu’ and
‘Barometer’.

The project also develops required enhancements to individual components
in OpenStack like Neutron, Telemetry API and the different OpenStack
monitoring agents in order to provide a baseline for “Operations APIs”.

High level functionality 
-------------------------

*Scanning*:

Calipso uses API, Database and Command-Line adapters for interfacing
with the Cloud infrastructure to logically discover every networking
component and it's relationships with others, building a smart topology
and inventory.

*Automated setup*:

Calipso uses Sensu framework for Monitoring. It automatically deploys
and configures the necessary configuration files on all hosts, writes
customized checks and handlers to setup monitoring per inventory object.

*Modeled analysis*:

Calipso uses a unique logical model to help facilitate the topology
discovery, analysis of inter-connections and dependencies. Impact
Analysis is embedded, other types of analysis is possible through a
plugin framework.

*Visualization:*

Using its unique dependency model calipso visualize topological
inventory and monitoring results, in a highly customizable and modeled
UI framework

*Monitoring*:

After collecting the data, from processes and workers provisioned by the
cloud management systems, calipso dynamically checks for health and
availability, as a baseline for SLA monitoring.

*Reporting:*

Calipso allows networking administrators to operate, plan for
maintenance or troubleshooting and provides an easy to use hierarchical
representation of all the virtual networking components.

Customer Requirements
=====================

We identified an operational challenge: lack of visibility that leads to
limited stability.

The lack of operational tooling coupled with the reality of deployment
tools really needs to get solved to decrease the complexity as well as
assist not only deploying but also supporting OpenStack and other cloud
stacks.

Calispo integrates well with installers like Apex to offer enhanced day
2 operations.

Releases and Distributions
--------------------------

Calipso is distributed for enterprises - ‘S’ release, through
calipso.io, and for service providers - ‘P’ release, through OPNFV.

.. |image0| image:: media/image1.png
   :width: 6.50000in
   :height: 4.27153in
.. |image1| image:: media/image2.png
   :width: 6.50000in
   :height: 3.52153in
