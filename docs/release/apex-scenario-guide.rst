| Calipso.io
| Installation Guide

|image0|

Project “Calipso” tries to illuminate complex virtual networking with
real time operational state visibility for large and highly distributed
Virtual Infrastructure Management (VIM).

We believe that Stability is driven by accurate Visibility.

Calipso provides visible insights using smart discovery and virtual
topological representation in graphs, with monitoring per object in the
graph inventory to reduce error vectors and troubleshooting, maintenance
cycles for VIM operators and administrators.

Table of Contents

Calipso.io Installation Guide 1

1 Pre Requisites 3

1.1 Pre Requisites for Calipso “all in one” application 3

1.2 Pre Requisites for Calipso UI application 3

2 Installation Option used with Apex 4

2.1 Micro Services App, single line install 4

3 OPNFV Scenario 5

3.1 APEX automatic configurator and setup 5

3.2 Apex scenario 5

3.3 Calipso functest 6

TBD 6

Pre Requisites 
===============

Pre Requisites for Calipso “all in one” application 
----------------------------------------------------

    Calipso’s main application is written with Python3.5 for Linux
    Servers, tested successfully on Centos 7.3 and Ubuntu 16.04. When
    running using micro-services many of the required software packages
    and libraries are delivered per micro service, but for an “all in
    one” application case there are several dependencies.

    Here is a list of the required software packages, and the official
    supported steps required to install them:

1. Python3.5.x for Linux :
   https://docs.python.org/3.5/using/unix.html#on-linux

2. Pip for Python3 : https://docs.python.org/3/installing/index.html

3. Python3 packages to install using pip3 :

    **sudo pip3 install falcon (>1.1.0)**

    **sudo pip3 install pymongo (>3.4.0)**

    **sudo pip3 install gunicorn (>19.6.0)**

    **sudo pip3 install ldap3 (>2.1.1)**

    **sudo pip3 install setuptools (>34.3.2)**

    **sudo pip3 install python3-dateutil (>2.5.3-2)**

    **sudo pip3 install bcrypt (>3.1.1)**

    **sudo pip3 install bson**

    **sudo pip3 install websocket**

    **sudo pip3 install datetime**

    **sudo pip3 install typing**

    **sudo pip3 install kombu**

    **sudo pip3 install boltons**

    **sudo pip3 install paramiko**

    **sudo pip3 install requests **

    **sudo pip3 install httplib2**

    **sudo pip3 install mysql.connector**

    **sudo pip3 install xmltodict**

    **sudo pip3 install cryptography**

    **sudo pip3 install docker**

1. Git : https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

2. Docker : https://docs.docker.com/engine/installation/

Pre Requisites for Calipso UI application 
------------------------------------------

    Calipso UI is developed and maintained using Meteor Framework
    (https://www.meteor.com/tutorials). For stability and manageability
    reasons we decided to always build the latest Calipso UI as a Docker
    container pre-parameterized for stable and supported behavior. The
    required steps for installing the Calipso UI with several options
    are listed below.

Installation Option used with Apex
==================================

Micro Services App, single line install
---------------------------------------

    For most users, this will be the fastest and more reliable install
    option. We currently have Calipso divided into 7 major containers,
    those are installed using a single installer. The Calipso containers
    are pre-packaged and fully customized per our design needs. Here are
    the required steps for installation using this option:

1. Follow steps 1- 5 per section 2.1 above.

2. Install Docker : https://docs.docker.com/engine/installation/

3. Install the following python3 libraries using pip3 : docker, pymongo

4. Although Calipso installer can download all needed containers, if
   they doesn’t exist locally already, we recommend doing a manual
   download of all 7 containers, providing better control and logging:

    **sudo docker login** # use your DockerHub username and password to
    login.

    **sudo docker pull korenlev/calipso:scan** # scan container used to
    scan VIM

    **sudo docker pull korenlev/calipso:listen** # listen container to
    attach to VIM’s BUS.

    **sudo docker pull korenlev/calipso:api** # api container for
    application integration

    **sudo docker pull korenlev/calipso:sensu** # sensu server container
    for monitoring

    **sudo docker pull korenlev/calipso:mongo** # calipso mongo DB
    container

    **sudo docker pull korenlev/calipso:ui** # calipso ui container

    **sudo docker pull korenlev/calipso:ldap** # calipso ldap container

1. Check that all containers were downloaded and registered
   successfully:

    **sudo docker images**

    Expected results (As of Aug 2017):

    **REPOSITORY TAG IMAGE ID CREATED SIZE**

    **korenlev/calipso listen 12086aaedbc3 6 hours ago 1.05GB**

    **korenlev/calipso api 34c4c6c1b03e 6 hours ago 992MB**

    **korenlev/calipso scan 1ee60c4e61d5 6 hours ago 1.1GB**

    **korenlev/calipso sensu a8a17168197a 6 hours ago 1.65GB**

    **korenlev/calipso mongo 17f2d62f4445 22 hours ago 1.31GB**

    **korenlev/calipso ui ab37b366e812 11 days ago 270MB**

    **korenlev/calipso ldap 316bc94b25ad 2 months ago 269MB**

1. Run the calipso installer using single line arguments:

    **python3 calipso/app/install/calipso-installer.py--command
    start-all --copy q**

    This should launch all calipso modules in sequence along with all
    needed configuration files placed in /home/calipso.

OPNFV Scenario 
===============

Although calipso is designed for any VIM and for enterprise use-cases
too, service providers can use additional capability to install calipso
with Apex for OPNFV.

APEX automatic configurator and setup
-------------------------------------

    When using apex to install OPNFV, the Triple-O based OpenStack is
    installed automatically and calipso installation can be initiated
    automatically after apex completes the VIM installation process for
    a certain scenario.

    In this case setup\_apex\_environment.py can be used for creating a
    new environment automatically into mongoDB and UI of Calipso
    (instead of using the calipso UI to do that as typical user would
    do), then detailed scanning can start immediately, the following
    options are available for setup\_apex\_environment.py:

    **-m [MONGO\_CONFIG], --mongo\_config [MONGO\_CONFIG]**

    **name of config file with MongoDB server access details**

    **(Default: /local\_dir/calipso\_mongo\_access.conf)**

    **-d [CONFIG\_DIR], --config\_dir [CONFIG\_DIR]**

    **path to directory with config data (Default:**

    **/home/calipso/apex\_setup\_files)**

    **-i [INSTALL\_DB\_DIR], --install\_db\_dir [INSTALL\_DB\_DIR]**

    **path to directory with DB data (Default:**

    **/home/calipso/Calipso/app/install/db)**

    **-a [APEX], --apex [APEX]**

    **name of environment to Apex host**

    **-e [ENV], --env [ENV]**

    **name of environment to create(Default: Apex-Euphrates)**

    **-l [LOGLEVEL], --loglevel [LOGLEVEL]**

    **logging level (default: "INFO")**

    **-f [LOGFILE], --logfile [LOGFILE]**

    **log file (default:**

    **"/home/calipso/log/apex\_environment\_fetch.log")**

    **-g [GIT], --git [GIT]**

    **URL to clone Git repository (default:**

    **https://git.opnfv.org/calipso)**

Apex scenario
-------------

    Starting Euphrates 1.0 the following scenario added with Apex
    installer:

    **os-nosdn-calipso-noha**

    Following CI jobs defined:

    https://build.opnfv.org/ci/job/calipso-verify-euphrates/

    https://build.opnfv.org/ci/job/apex-testsuite-os-nosdn-calipso-noha-baremetal-euphrates/

    https://build.opnfv.org/ci/job/apex-os-nosdn-calipso-noha-baremetal-euphrates/

    Note: destination deploy server needs to have pre-requisites
    detailed above.

Calipso functest
----------------

TBD 
----

.. |image0| image:: media/image1.png
   :width: 6.50000in
   :height: 4.27153in
