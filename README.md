Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)
and others

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Calipso = OpenStack/VIM Network Discovery and Assurance
==================================================
### About
We are going to enhance the way Cloud Network Administrators(CNA) and Tenant Network Administrators(TNA) 
Understands, Monitors and Troubleshoot highly distributed OpenStack and other virtual Environments.

We are following Domain-Driven-Design process and procedures:
ref: http://www.methodsandtools.com/archive/archive.php?id=97

### Prototype Intent:

Provide CNA and TNA with support for:
<br>
1. Building virtual Network inventory and visualizing all inter-connections in real-time
<br>
2. Monitor virtual network objects state and health
<br>
3. Troubleshoot failures in virtual networks
<br>
4. Assess impact of failure in virtual networks
<br>
5. baseline plugin framework for analytics of this type of data/details

### Proto (mockups, updated Jul 15th)
calipso.io 

### Contacts
* Koren Lev (korlev@cisco.com)
* Yaron Yogev (yayogev@cisco.com)

Calipso uses API, DataBase and Command-Line adapters for interfacing with the Cloud infrastructure to logically discover every networking component and it's relationships with others, building a smart topology and inventory.
Calipso uses Sensu framework for Monitoring. It automatically deploys and configures the necessary config files on all hosts, writes customized checks and handlers to setup monitoring per inventory object.
After collecting the data, from processes and workers provisioned by the cloud management systems, calipso dynamically checks for health and availability, as a baseline for SLA monitoring.
Calipso allows networking administrators to operate, plan for maintenance or troubleshooting and provides an easy to use hierarchical representation of all the virtual networking components.
Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)
and others.