| Calipso.io
| API Guide

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

Calipso.io API Guide 1

1 Pre Requisites 3

1.1 Calipso API container 3

2 Overview 3

2.1 Introduction 3

2.2 HTTP Standards 4

2.3 Calipso API module Code 4

3 Starting the Calipso API server 4

3.1 Authentication 4

3.2 Database 5

3.3 Running the API Server 5

4 Using the Calipso API server 6

4.1 Authentication 6

4.2 Messages 9

4.3 Inventory 14

4.4 Links 17

4.5 Cliques 20

4.6 Clique\_types 23

4.7 Clique\_constraints 26

4.8 Scans 29

4.9 Scheduled\_scans 32

4.10 Constants 35

4.11 Monitoring\_Config\_Templates 37

4.12 Aggregates 39

4.13 Environment\_configs 42

Pre Requisites 
===============

Calipso API container 
----------------------

    Calipso’s main application is written with Python3.5 for Linux
    Servers, tested successfully on Centos 7.3 and Ubuntu 16.04. When
    running using micro-services many of the required software packages
    and libraries are delivered per micro service, including the API
    module case. In a monolithic case dependencies are needed.

    Here is a list of the required software packages for the API, and
    the official supported steps required to install them:

1.  Python3.5.x for Linux :
    https://docs.python.org/3.5/using/unix.html#on-linux

2.  Pip for Python3 : https://docs.python.org/3/installing/index.html

3.  Python3 packages to install using pip3 :

4.  falcon (1.1.0)

5.  pymongo (3.4.0)

6.  gunicorn (19.6.0)

7.  ldap3 (2.1.1)

8.  setuptools (34.3.2)

9.  python3-dateutil (2.5.3-2)

10. bcrypt (3.1.1)

    You should use pip3 python package manager to install the specific
    version of the library. Calipso project uses Python 3, so
    package installation should look like this:

    pip3 install falcon==1.1.0

    The versions of the Python packages specified above are the ones
    that were used in the development of the API, other versions might
    also be compatible.

    This document describes how to setup Calipso API container for
    development against the API.

Overview 
=========

Introduction
------------

    The Calipso API provides access to the Calipso data stored in the
    MongoDB.

    Calispo API uses
    `falcon <https://falconframework.org/>`__ (https://falconframework.org)
    web framework and `gunicorn <http://gunicorn.org/>`__
    (http://gunicorn.org) WSGI server.

    The authentication of the Calipso API is based on LDAP (Lightweight
    Directory Access Protocol). It can therefore interface with any
    directory servers which implements the LDAP protocol, e.g. OpenLDAP,
    Active Directory etc. Calipso app offers and uses the LDAP built-in
    container by default to make sure this integration is fully tested,
    but it is possible to interface to other existing directories.

HTTP Standards
--------------

    | The Calipso API supports standard \ `HTTP
      methods <https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html>`__
      described here:
      https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html.
    | At present two types of operations are supported: GET (retrieve
      data) and POST (create a new data object).

Calipso API module Code
-----------------------

    Clipso API code is currently located in opnfv repository.

    Run the following command to get the source code:

    git
    clone \ `**https://git.opnfv.org/calipso/** <https://git.opnfv.org/calipso/>`__

    The source code of the API is located in the app/api directory
    sub-tree.

Starting the Calipso API server 
================================

Authentication 
---------------

    Calipso API uses LDAP as the protocol to implement the
    authentication, so you can use any LDAP directory server as the
    authentication backend,
    like \ `OpenLDAP <https://help.ubuntu.com/lts/serverguide/openldap-server.html>`__
    and `Microsoft
    AD <https://msdn.microsoft.com/en-us/library/bb742424.aspx>`__. You
    can edit the ldap.conf file which is located in app/config directory
    to configure LDAP server options (see details in quickstart-guide):

    | # url for connecting to the LDAP server (customize to your own as
      needed):
    | url ldap\_url
    | # LDAP attribute mapped to user id, must not be a multivalued
      attributes:
    | user\_id\_attribute CN
    | # LDAP attribute mapped to user password:
    | user\_pass\_attribute userPassword
    | # LDAP objectclass for user
    | user\_objectclass inetOrgPerson
    | # Search base for users
    | user\_tree\_dn OU=Employees,OU=Example Users,DC=exmaple,DC=com
    | query\_scope one
    | # Valid options for tls\_req\_cert are demand, never, and allow
    | tls\_req\_cert demand
    | # CA certificate file path for communicating with LDAP servers.
    | tls\_cacertfile ca\_cert\_file\_path
    | group\_member\_attribute member

    Calipso currently implements the basic authentication, the client
    send the query request with its username and password in the auth
    header, if the user can be bound to the LDAP server, authentication
    succeeds otherwise fails. Other methods will be supported in future
    releases.

Database
--------

    Calipso API query for and retrieves data from MongoDB container, the
    data in the MongoDB comes from the results of Calipso scanning,
    monitoring or the user inputs from the API. All modules of a single
    Calipso instance of the application must point to the same MongoDB
    used by the scanning and monitoring modules. Installation and
    testing of mongoDB is covered in install-guide and quickstart-guide.

Running the API Server
----------------------

    The entry point (initial command) running the Calipso API
    application is the server.py script in the app/api directory.
    Options for running the API server can be listed using: python3
    server.py –help. Here is the current options available:

    | -m [MONGO\_CONFIG], --mongo\_config [MONGO\_CONFIG]
    |                    name of config file with mongo access details
    | --ldap\_config [LDAP\_CONFIG]
    |                    name of the config file with ldap server config
    |                    details
    | -l [LOGLEVEL], --loglevel [LOGLEVEL] logging level (default:
      'INFO')
    | -b [BIND], --bind [BIND]
    |                    binding address of the API server (default:
      127.0.0.1:8000)
    | -y [INVENTORY], --inventory [INVENTORY]
    |                    name of inventory collection (default:
      'inventory')

    For testing, you can simply run the API server by:

    python3 app/api/server.py

    This will start a HTTP server listening on \ http://localhost:8000,
    if you want to change the binding address of the server, you can run
    it using this command:

    python3 server.py --bind ip\_address/server\_name:port\_number

    You can also use your own configuration files for LDAP server and
    MongoDB, just add --mongo\_config and --ldap\_config options in your
    command:

    python3 server.py --mongo\_config your\_mongo\_config\_file\_path
    --ldap\_config your\_ldap\_config\_file\_path

    --inventory option is used to set the collection names the server
    uses for the API, as per the quickstart-guide this will default to
    **/local\_dir/calipso\_mongo\_access.conf** and
    **/local\_dir/ldap.conf** mounted inside the API container.

    Notes: the --inventory argument can only change the collection names
    of the inventory, links, link\_types, clique\_types,
    clique\_constraints, cliques, constants and scans collections, names
    of the monitoring\_config\_templates, environments\_config and
    messages collections will remain at the root level across releases.

Using the Calipso API server 
=============================

The following covers the currently available requests and responses on
the Calipso API

Authentication
--------------

**POST**        /auth/tokens

Description: get token with password and username or a valid token.

Normal response code: 201

Error response code: badRequest(400), unauthorized(401)

**Request**

+-------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------+
| **Name**                | **In**   | **Type**   | **Description**                                                                                                                  |
+=========================+==========+============+==================================================================================================================================+
| auth(Mandatory)         | body     | object     | An auth object that contains the authentication information                                                                      |
+-------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------+
| methods(Mandatory)      | body     | array      | The authentication methods. For password authentication, specify password, for token authentication, specify token.              |
+-------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------+
| credentials(Optional)   | body     | object     | Credentials object which contains the username and password, it must be provided when getting the token with user credentials.   |
+-------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------+
| token(Optional)         | body     | string     | The token of the user, it must be provided when getting the user with an existing valid token.                                   |
+-------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------+

**Response**

+---------------+----------+------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| **Name**      | **In**   | **Type**   | **Description**                                                                                                                            |
+===============+==========+============+============================================================================================================================================+
| token         | body     | string     | Token for the user.                                                                                                                        |
+---------------+----------+------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| issued-at     | body     | string     | The date and time when the token was issued. the date and time format follows \ `*ISO 8610* <https://en.wikipedia.org/wiki/ISO_8601>`__:   |
|               |          |            |                                                                                                                                            |
|               |          |            | YYYY-MM-DDThh:mm:ss.sss+hhmm                                                                                                               |
+---------------+----------+------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| expires\_at   | body     | string     | The date and time when the token expires. the date and time format follows \ `*ISO 8610* <https://en.wikipedia.org/wiki/ISO_8601>`__:      |
|               |          |            |                                                                                                                                            |
|               |          |            | YYYY-MM-DDThh:mm:ss.sss+hhmm                                                                                                               |
+---------------+----------+------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| method        | body     | string     | The method which achieves the token.                                                                                                       |
+---------------+----------+------------+--------------------------------------------------------------------------------------------------------------------------------------------+

**
Examples**

**Get token with credentials:**

Post\ ** **\ `*http://korlev-osdna-staging1.cisco.com:8000/auth/tokens* <http://korlev-osdna-staging1.cisco.com:8000/auth/tokens>`__

| {
|      "auth": {
|          "methods": ["credentials"],
|          "credentials": {
|                "username": "username",
|                "password": "password"
|           }
|        }
| }

**Get token with token**

post\ ** **\ http://korlev-calipso-staging1.cisco.com:8000/auth/tokens

| {
|     "auth": {
|           "methods": ["token"],
|           "token": "17dfa88789aa47f6bb8501865d905f13"
|     }
| }

**
**

**DELETE**       /auth/tokens

Description: delete token with a valid token.

Normal response code: 200

Error response code: badRequest(400), unauthorized(401)

**Request**

+----------------+----------+------------+-------------------------------------------------------------+
| **Name**       | **In**   | **Type**   | **Description**                                             |
+================+==========+============+=============================================================+
| X-Auth-Token   | header   | string     | A valid authentication token that is doing to be deleted.   |
+----------------+----------+------------+-------------------------------------------------------------+

**Response**

200 OK will be returned when the delete succeed

Messages 
---------

**GET         **/messages

Description: get message details with environment name and message id,
or get a list of messages with filters except id.

Normal response code: 200

Error response code: badRequest(400), unauthorized(401), notFound(404)

**Request**

+------------------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Name**                           | **In**   | **Type**   | **Description**                                                                                                                                                                                                                  |
+====================================+==========+============+==================================================================================================================================================================================================================================+
| env\_name(Mandatory)               | query    | string     | Environment name of the messages. e.g. "Mirantis-Liberty-API".                                                                                                                                                                   |
+------------------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id (Optional)                      | query    | string     | ID of the message.                                                                                                                                                                                                               |
+------------------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| source\_system (Optional)          | query    | string     | Source system of the message, e.g. "OpenStack".                                                                                                                                                                                  |
+------------------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| start\_time (Optional)             | query    | string     | Start time of the messages, when this parameter is specified, the messages after that time will be returned, the date and time format follows `*ISO 8610: * <https://en.wikipedia.org/wiki/ISO_8601>`__                          |
|                                    |          |            |                                                                                                                                                                                                                                  |
|                                    |          |            | YYYY-MM-DDThh:mm:ss.sss\ *+*\ hhmm                                                                                                                                                                                               |
|                                    |          |            |                                                                                                                                                                                                                                  |
|                                    |          |            | The *+*\ hhmm value, if included, returns the time zone as an offset from UTC, For example, 2017-01-25T09:45:33.000-0500. If you omit the time zone, the UTC time is assumed.                                                    |
+------------------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| end\_time (Optional)               | query    | string     | End time of the message, when this parameter is specified, the messages before that time will be returned, the date and time format follows \ `*ISO 8610* <https://en.wikipedia.org/wiki/ISO_8601>`__:                           |
|                                    |          |            |                                                                                                                                                                                                                                  |
|                                    |          |            | YYYY-MM-DDThh:mm:ss.sss\ *+*\ hhmm                                                                                                                                                                                               |
|                                    |          |            |                                                                                                                                                                                                                                  |
|                                    |          |            | The *+*\ hhmm value, if included, returns the time zone as an offset from UTC, For example, 2017-01-25T09:45:33.000-0500. If you omit the time zone, the UTC time is assumed.                                                    |
+------------------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| level (Optional)                   | query    | string     | The severity of the messages, we accept the severities strings described in `*RFC 5424* <https://tools.ietf.org/html/rfc5424>`__, possible values are "panic", "alert", "crit", "error", "warn", "notice", "info" and "debug".   |
+------------------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| related\_object (Optional)         | query    | string     | ID of the object related to the message.                                                                                                                                                                                         |
+------------------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| related\_object\_type (Optional)   | query    | string     | Type of the object related to the message, possible values are "vnic", "vconnector", "vedge", "instance", "vservice", "host\_pnic", "network", "port", "otep" and "agent".                                                       |
+------------------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| page (Optional)                    | query    | int        | Which page will to be returned, the default is first page, if the page is larger than the maximum page of the query, and it will return an empty result set (Page start from 0).                                                 |
+------------------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| page\_size (Optional)              | query    | int        | Size of each page, the default is 1000.                                                                                                                                                                                          |
+------------------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**Response **

+-------------------------+----------+------------+---------------------------------------------------+
| **Name**                | **In**   | **Type**   | **Description**                                   |
+=========================+==========+============+===================================================+
| environment             | body     | string     | Environment name of the message.                  |
+-------------------------+----------+------------+---------------------------------------------------+
| id                      | body     | string     | ID of the message.                                |
+-------------------------+----------+------------+---------------------------------------------------+
| \_id                    | body     | string     | MongoDB ObjectId of the message.                  |
+-------------------------+----------+------------+---------------------------------------------------+
| timestamp               | body     | string     | Timestamp of message.                             |
+-------------------------+----------+------------+---------------------------------------------------+
| viewed                  | body     | boolean    | Indicates whether the message has been viewed.    |
+-------------------------+----------+------------+---------------------------------------------------+
| display\_context        | body     | string     | The content which will be displayed.              |
+-------------------------+----------+------------+---------------------------------------------------+
| message                 | body     | object     | Message object.                                   |
+-------------------------+----------+------------+---------------------------------------------------+
| source\_system          | body     | string     | Source system of the message, e.g. "OpenStack".   |
+-------------------------+----------+------------+---------------------------------------------------+
| level                   | body     | string     | The severity of the message.                      |
+-------------------------+----------+------------+---------------------------------------------------+
| related\_object         | body     | string     | Related object of the message.                    |
+-------------------------+----------+------------+---------------------------------------------------+
| related\_object\_type   | body     | string     | Type of the related object.                       |
+-------------------------+----------+------------+---------------------------------------------------+
| messages                | body     | array      | List of message ids which match the filters.      |
+-------------------------+----------+------------+---------------------------------------------------+

**Examples**

**Example Get Messages **

**Request:**

http://korlev-calipso-testing.cisco.com:8000/messages?env_name=Mirantis-Liberty-API&start_time=2017-01-25T14:28:32.400Z&end_time=2017-01-25T14:28:42.400Z

**Response:**

| {
|      messages: [                   

    | {
    |      "level": "info",
    |      "environment": "Mirantis-Liberty",
    |      "id": "3c64fe31-ca3b-49a3-b5d3-c485d7a452e7",
    |      "source\_system": "OpenStack"
    | },
    | {
    |      "level": "info",
    |      "environment": "Mirantis-Liberty",
    |      "id": "c7071ec0-04db-4820-92ff-3ed2b916738f",
    |      "source\_system": "OpenStack"
    | },

|       ]
| }

**Example Get Message Details**

**Request**

http://korlev-calipso-testing.cisco.com:8000/messages?env_name=Mirantis-Liberty-API&id=80b5e074-0f1a-4b67-810c-fa9c92d41a98

**Response**

| {
| "related\_object\_type": "instance",
| "source\_system": "OpenStack",
| "level": "info",
| "timestamp": "2017-01-25T14:28:33.057000",
| "\_id": "588926916a283a8bee15cfc6",
| "viewed": true,
| "display\_context": "\*",
| "related\_object": "97a1e179-6a42-4c7b-bced-4f64bd9e4b6b",
| "environment": "Mirantis-Liberty-API",
| "message": {
| "\_context\_show\_deleted": false,
| "\_context\_user\_name": "admin",
| "\_context\_project\_id": "a3efb05cd0484bf0b600e45dab09276d",
| "\_context\_service\_catalog": [
| {
| "type": "volume",
| "endpoints": [
| {
| "internalURL":
  "`*http://192.168.0.2:8776/v1/a3efb05cd0484bf0b600e45dab09276d* <http://192.168.0.2:8776/v1/a3efb05cd0484bf0b600e45dab09276d>`__",
| "publicURL":
  "`*http://172.16.0.3:8776/v1/a3efb05cd0484bf0b600e45dab09276d* <http://172.16.0.3:8776/v1/a3efb05cd0484bf0b600e45dab09276d>`__",
| "adminURL":
  "`*http://192.168.0.2:8776/v1/a3efb05cd0484bf0b600e45dab09276d* <http://192.168.0.2:8776/v1/a3efb05cd0484bf0b600e45dab09276d>`__",
| "region": "RegionOne"
| }
| ],
| "name": "cinder"
| },
| {
| "type": "volumev2",
| "endpoints": [
| {
| "internalURL":
  "`*http://192.168.0.2:8776/v2/a3efb05cd0484bf0b600e45dab09276d* <http://192.168.0.2:8776/v2/a3efb05cd0484bf0b600e45dab09276d>`__",
| "publicURL":
  "`*http://172.16.0.3:8776/v2/a3efb05cd0484bf0b600e45dab09276d* <http://172.16.0.3:8776/v2/a3efb05cd0484bf0b600e45dab09276d>`__",
| "adminURL":
  "`*http://192.168.0.2:8776/v2/a3efb05cd0484bf0b600e45dab09276d* <http://192.168.0.2:8776/v2/a3efb05cd0484bf0b600e45dab09276d>`__",
| "region": "RegionOne"
| }
| ],
| "name": "cinderv2"
| }
| ],
| "\_context\_user\_identity": "a864d9560b3048e9864118555bb9614c
  a3efb05cd0484bf0b600e45dab09276d - - -",
| "\_context\_project\_domain": null,
| "\_context\_is\_admin": true,
| "\_context\_instance\_lock\_checked": false,
| "\_context\_timestamp": "2017-01-25T22:27:08.773313",
| "priority": "INFO",
| "\_context\_project\_name": "project-osdna",
| "publisher\_id":
  "`*compute.node-1.cisco.com* <http://compute.node-1.cisco.com>`__",
| "\_context\_read\_only": false,
| "message\_id": "80b5e074-0f1a-4b67-810c-fa9c92d41a98",
| "\_context\_user\_id": "a864d9560b3048e9864118555bb9614c",
| "\_context\_quota\_class": null,
| "\_context\_tenant": "a3efb05cd0484bf0b600e45dab09276d",
| "\_context\_remote\_address": "192.168.0.2",
| "\_context\_request\_id": "req-2955726b-f227-4eac-9826-b675f5345ceb",
| "\_context\_auth\_token":
  "gAAAAABYiSVcHmaq1TWwNc1\_QLlKhdUeC1-M6zBebXyoXN4D0vMlxisny9Q61crBzqwSyY\_Eqd\_yjrL8GvxatWI1WI1uG4VeWU6axbLe\_k5FaXS4RVOP83yR6eh5g\_qXQtsNapQufZB1paypZm8YGERRvR-vV5Ee76aTSkytVjwOBeipr9D0dXd-wHcRnSNkTD76nFbGKTu\_",
| "\_context\_user\_domain": null,
| "payload": {
| "image\_meta": {
| "container\_format": "bare",
| "disk\_format": "qcow2",
| "min\_ram": "64",
| "base\_image\_ref": "5f048984-37d1-4952-8b8a-9acb0237bad7",
| "min\_disk": "0"
| },
| "display\_name": "test",
| "terminated\_at": "",
| "access\_ip\_v6": null,
| "architecture": null,
| "image\_ref\_url":
  "`*http://192.168.0.3:9292/images/5f048984-37d1-4952-8b8a-9acb0237bad7* <http://192.168.0.3:9292/images/5f048984-37d1-4952-8b8a-9acb0237bad7>`__",
| "audit\_period\_beginning": "2017-01-01T00:00:00.000000",
| "metadata": {},
| "node": "`*node-2.cisco.com* <http://node-2.cisco.com>`__",
| "audit\_period\_ending": "2017-01-25T22:27:12.888042",
| "instance\_type": "m1.micro",
| "ramdisk\_id": "",
| "availability\_zone": "nova",
| "kernel\_id": "",
| "hostname": "test",
| "vcpus": 1,
| "bandwidth": {},
| "user\_id": "a864d9560b3048e9864118555bb9614c",
| "state\_description": "block\_device\_mapping",
| "old\_state": "building",
| "root\_gb": 0,
| "instance\_flavor\_id": "8784e0b5-7d17-4281-a509-f49d6fd102f9",
| "cell\_name": "",
| "reservation\_id": "r-zt7sh7vy",
| "access\_ip\_v4": null,
| "deleted\_at": "",
| "tenant\_id": "a3efb05cd0484bf0b600e45dab09276d",
| "disk\_gb": 0,
| "instance\_id": "97a1e179-6a42-4c7b-bced-4f64bd9e4b6b",
| "host": "`*node-2.cisco.com* <http://node-2.cisco.com>`__",
| "memory\_mb": 64,
| "os\_type": null,
| "old\_task\_state": "block\_device\_mapping",
| "state": "building",
| "instance\_type\_id": 6,
| "launched\_at": "",
| "ephemeral\_gb": 0,
| "created\_at": "2017-01-25 22:27:09+00:00",
| "progress": "",
| "new\_task\_state": "block\_device\_mapping"
| },
| "\_context\_read\_deleted": "no",
| "event\_type": "compute.instance.update",
| "\_context\_roles": [
| "admin",
| "\_member\_"
| ],
| "\_context\_user": "a864d9560b3048e9864118555bb9614c",
| "timestamp": "2017-01-25 22:27:12.912744",
| "\_unique\_id": "d6dff97e6f71401bb8890057f872644f",
| "\_context\_resource\_uuid": null,
| "\_context\_domain": null
| },
| "id": "80b5e074-0f1a-4b67-810c-fa9c92d41a98"
| }

Inventory
---------

**GET            **/inventory**            **

Description: get object details with environment name and id of the
object, or get a list of objects with filters except id.

Normal response code: 200

Error response code:  badRequest(400), unauthorized(401), notFound(404)

**Request**

+---------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Name**                  | **In**   | **Type**   | **Description**                                                                                                                                                                                                                                                                                                                  |
+===========================+==========+============+==================================================================================================================================================================================================================================================================================================================================+
| env\_name (Mandatory)     | query    | string     | Environment of the objects. e.g. "Mirantis-Liberty-API".                                                                                                                                                                                                                                                                         |
+---------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id (Optional)             | query    | string     | ID of the object. e.g. "`*node-2.cisco.com* <http://node-2.cisco.com>`__".                                                                                                                                                                                                                                                       |
+---------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| parent\_id (Optional)     | query    | string     | ID of the parent object. e.g. "nova".                                                                                                                                                                                                                                                                                            |
+---------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id\_path (Optional)       | query    | string     | ID path of the object. e.g. "/Mirantis-Liberty-API/Mirantis-Liberty-API-regions/RegionOne/RegionOne-availability\_zones/nova/`*node-2.cisco.com* <http://node-2.cisco.com>`__".                                                                                                                                                  |
+---------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| parent\_path (Optional)   | query    | string     | ID path of the parent object. "/Mirantis-Liberty-API/Mirantis-Liberty-API-regions/RegionOne/RegionOne-availability\_zones/nova".                                                                                                                                                                                                 |
+---------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| sub\_tree (Optional)      | query    | boolean    | If it is true and the parent\_path is specified, it will return the whole sub-tree of that parent object which includes the parent itself, If it is false and the parent\_path is specified, it will only return the siblings of that parent (just the children of that parent node), the default value of sub\_tree is false.   |
+---------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| page (Optional)           | query    | int        | Which page is to be returned, the default is the first page, if the page is larger than the maximum page of the query, it will return an empty set, (page starts from 0).                                                                                                                                                        |
+---------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| page\_size (Optional)     | query    | int        | Size of each page, the default is 1000.                                                                                                                                                                                                                                                                                          |
+---------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**Response **

+-----------------+----------+------------+--------------------------------------------------+
| **Name**        | **In**   | **Type**   | **Description**                                  |
+=================+==========+============+==================================================+
| environment     | body     | string     | Environment name of the object.                  |
+-----------------+----------+------------+--------------------------------------------------+
| id              | body     | string     | ID of the object.                                |
+-----------------+----------+------------+--------------------------------------------------+
| \_id            | body     | string     | MongoDB ObjectId of the object.                  |
+-----------------+----------+------------+--------------------------------------------------+
| type            | body     | string     | Type of the object.                              |
+-----------------+----------+------------+--------------------------------------------------+
| parent\_type    | body     | string     | Type of the parent object.                       |
+-----------------+----------+------------+--------------------------------------------------+
| parent\_id      | body     | string     | ID of the parent object.                         |
+-----------------+----------+------------+--------------------------------------------------+
| name\_path      | body     | string     | Name path of the object.                         |
+-----------------+----------+------------+--------------------------------------------------+
| last\_scanned   | body     | string     | Time of last scanning.                           |
+-----------------+----------+------------+--------------------------------------------------+
| name            | body     | string     | Name of the object.                              |
+-----------------+----------+------------+--------------------------------------------------+
| id\_path        | body     | string     | ID path of the object.                           |
+-----------------+----------+------------+--------------------------------------------------+
| objects         | body     | array      | The list of object IDs that match the filters.   |
+-----------------+----------+------------+--------------------------------------------------+

**Examples**

**Example Get Objects **

**Request**

http://korlev-calipso-testing.cisco.com:8000/inventory?env_name=Mirantis-Liberty-API&parent_path=/Mirantis-Liberty-API/Mirantis-Liberty-API-regions/RegionOne&sub_tree=false

**Response**

{

    "objects": [    

    | {
    |      "id": "Mirantis-Liberty-regions",
    |      "name": "Regions",
    |      "name\_path": "/Mirantis-Liberty/Regions"
    | },
    | {
    |      "id": "Mirantis-Liberty-projects",
    |      "name": "Projects",
    |      "name\_path": "/Mirantis-Liberty/Projects"
    | }

    ]

}

**Examples Get Object Details**

**Request**

http://korlev-calipso-testing.cisco.com:8000/inventory?env_name=Mirantis-Liberty-API&id=node-2.cisco.com

**Response**

| {
|    'ip\_address': '192.168.0.5',
|    'services': {
|       'nova-compute': {
|          'active': True,
|          'updated\_at': '2017-01-20T23:03:57.000000',
|          'available': True
|        }
|     },
| 'name': '`*node-2.cisco.com* <http://node-2.cisco.com>`__',
| 'id\_path':
  '/Mirantis-Liberty-API/Mirantis-Liberty-API-regions/RegionOne/RegionOne-availability\_zones/nova/`*node-2.cisco.com* <http://node-2.cisco.com>`__',
| 'show\_in\_tree': True,
| 'os\_id': '1',
| 'object\_name': '`*node-2.cisco.com* <http://node-2.cisco.com>`__',
| '\_id': '588297ae6a283a8bee15cc0d',
| 'host\_type': [
|    'Compute'
| ],
| 'name\_path': '/Mirantis-Liberty-API/Regions/RegionOne/Availability
  Zones/nova/\ `*node-2.cisco.com* <http://node-2.cisco.com>`__',
| 'parent\_type': 'availability\_zone',
| 'zone': 'nova',
| 'parent\_id': 'nova',
| 'host': '`*node-2.cisco.com* <http://node-2.cisco.com>`__',
| 'last\_scanned': '2017-01-20T15:05:18.501000',
| 'id': '`*node-2.cisco.com* <http://node-2.cisco.com>`__',
| 'environment': 'Mirantis-Liberty-API',
| 'type': 'host'
| }

Links
-----

**GET            **/links

Description: get link details with environment name and id of the link,
or get a list of links with filters except id

Normal response code: 200

Error response code: badRequest(400), unauthorized(401), notFound(404)

**Request**

+-------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Name**                | **In**   | **Type**   | **Description**                                                                                                                                                                                                                                     |
+=========================+==========+============+=====================================================================================================================================================================================================================================================+
| env\_name (Mandatory)   | query    | string     | Environment of the links. e.g. "Mirantis-Liberty-API".                                                                                                                                                                                              |
+-------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id (Optional)           | query    | string     | ID of the link, it must be a string which can be converted to MongoDB ObjectId.                                                                                                                                                                     |
+-------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| host (Optional)         | query    | string     | Host of the link. e.g. "`*node-1.cisco.com* <http://node-1.cisco.com>`__".                                                                                                                                                                          |
+-------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| link\_type (Optional)   | query    | string     | Type of the link, some possible values for that are "instance-vnic", "otep-vconnector", "otep-host\_pnic", "host\_pnic-network", "vedge-otep", "vnic-vconnector", "vconnector-host\_pnic", "vnic-vedge", "vedge-host\_pnic" and "vservice-vnic" .   |
+-------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| link\_name (Optional)   | query    | string     | Name of the link. e.g. "Segment-2".                                                                                                                                                                                                                 |
+-------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| source\_id (Optional)   | query    | string     | ID of the source object of the link. e.g. "qdhcp-4f4bf8b5-ca42-411a-9f64-5b214d1f1c71".                                                                                                                                                             |
+-------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| target\_id (Optional)   | query    | string     | ID of the target object of the link. "tap708d399a-20".                                                                                                                                                                                              |
+-------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| state (Optional)        | query    | string     | State of the link, "up" or "down".                                                                                                                                                                                                                  |
+-------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| attributes              | query    | object     | The attributes of the link, e.g. the network attribute of the link is attributes:network="4f4bf8b5-ca42-411a-9f64-5b214d1f1c71".                                                                                                                    |
+-------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| page (Optional)         | query    | int        | Which page is to be returned, the default is first page, when the page is larger than the maximum page of the query,                                                                                                                                |
|                         |          |            |                                                                                                                                                                                                                                                     |
|                         |          |            | it will return an empty set. (Page starts from 0).                                                                                                                                                                                                  |
+-------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| page\_size (Optional)   | query    | int        | Size of each page, the default is 1000.                                                                                                                                                                                                             |
+-------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**Response **

+-----------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Name**        | **In**   | **Type**   | **Description**                                                                                                                                                                                                                                    |
+=================+==========+============+====================================================================================================================================================================================================================================================+
| id              | body     | string     | ID of the link.                                                                                                                                                                                                                                    |
+-----------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| \_id            | body     | string     | MongoDB ObjectId of the link.                                                                                                                                                                                                                      |
+-----------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| environment     | body     | string     | Environment of the link.                                                                                                                                                                                                                           |
+-----------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| source\_id      | body     | string     | ID of the source object of the link.                                                                                                                                                                                                               |
+-----------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| target\_id      | body     | string     | ID of the target object of the link.                                                                                                                                                                                                               |
+-----------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| source          | body     | string     | MongoDB ObjectId of the source object.                                                                                                                                                                                                             |
+-----------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| target          | body     | string     | MongoDB ObjectId of the target object.                                                                                                                                                                                                             |
+-----------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| source\_label   | body     | string     | Descriptive text for the source object.                                                                                                                                                                                                            |
+-----------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| target\_label   | body     | string     | Descriptive text for the target object.                                                                                                                                                                                                            |
+-----------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| link\_weight    | body     | string     | Weight of the link.                                                                                                                                                                                                                                |
+-----------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| link\_type      | body     | string     | Type of the link, some possible values for that are "instance-vnic", "otep-vconnector", "otep-host\_pnic", "host\_pnic-network", "vedge-otep", "vnic-vconnector", "vconnector-host\_pnic", "vnic-vedge", "vedge-host\_pnic" and "vservice-vnic".   |
+-----------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| state           | body     | string     | State of the link, "up" or "down".                                                                                                                                                                                                                 |
+-----------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| attributes      | body     | object     | The attributes of the link.                                                                                                                                                                                                                        |
+-----------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| links           | body     | array      | List of link IDs which match the filters.                                                                                                                                                                                                          |
+-----------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**Examples**

**Example Get Link Ids**

**Request**

`*http://korlev-calipso-testing.cisco.com:8000/links?env\_name=Mirantis-Liberty-API&host=node-2.cisco.com* <http://korlev-osdna-testing.cisco.com:8000/links?env_name=Mirantis-Liberty-API&host=node-2.cisco.com>`__

**Response**

{

    "links": [        

    | {
    |       "id": "58ca73ae3a8a836d10ff3b45",
    |       "host": "`*node-1.cisco.com* <http://node-1.cisco.com>`__",
    |       "link\_type": "host\_pnic-network",
    |       "link\_name": "Segment-103",
    |       "environment": "Mirantis-Liberty"
    | }

     ]

}

**Example Get Link Details**

**Request**

http://korlev-calipso-testing.cisco.com:8000/links?env_name=Mirantis-Liberty-API&id=5882982c6a283a8bee15cc62

**Response**

| {
|      "target\_id": "6d0250ae-e7df-4b30-aa89-d9fcc22e6371",
|      "target": "58a23ff16a283a8bee15d3e6",
|      "link\_type": "vnic-vedge",
|      "link\_name":
  "`*qr-24364cd7-ab-node-1.cisco.com* <http://qr-24364cd7-ab-node-1.cisco.com>`__-OVS-3",
|      "environment": "Mirantis-Liberty-API",
|      "\_id": "58a240646a283a8bee15d438",
|      "source\_label": "fa:16:3e:38:11:c9",
|      "state": "up",
|      "link\_weight": 0,
|      "id": "58a240646a283a8bee15d438",
|      "host": "`*node-1.cisco.com* <http://node-1.cisco.com>`__",
|      "source": "58a23fd46a283a8bee15d3c6",
|      "target\_label": "10",
|      "attributes": {},
|      "source\_id": "qr-24364cd7-ab"
| }

Cliques
-------

**GET            **/cliques

Description: get clique details with environment name and clique id, or
get a list of cliques with filters except id

Normal response code: 200

Error response code: badRequest(400), unauthorized(401), notFound(404)

**Request**

+---------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Name**                        | **In**   | **Type**   | **Description**                                                                                                                                                                                                                                                                                                                                                     |
+=================================+==========+============+=====================================================================================================================================================================================================================================================================================================================================================================+
| env\_name (Mandatory)           | query    | string     | Environment of the cliques. e.g. "Mirantis-Liberty-API".                                                                                                                                                                                                                                                                                                            |
+---------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id (Optional)                   | query    | string     | ID of the clique, it must be a string that can be converted to Mongo ObjectID.                                                                                                                                                                                                                                                                                      |
+---------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| focal\_point (Optional)         | query    | string     | MongoDB ObjectId of the focal point object, it must be a string that can be converted to Mongo ObjectID.                                                                                                                                                                                                                                                            |
+---------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| focal\_point\_type (Optional)   | query    | string     | Type of the focal point object, some possible values are  "vnic", "vconnector", "vedge", "instance", "vservice", "host\_pnic", "network", "port", "otep" and "agent".                                                                                                                                                                                               |
+---------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| link\_type(Optional)            | query    | string     | Type of the link, when this filter is specified, it will return all the cliques which contain the specific type of the link, some possible values for link\_type are "instance-vnic", "otep-vconnector", "otep-host\_pnic", "host\_pnic-network", "vedge-otep", "vnic-vconnector", "vconnector-host\_pnic", "vnic-vedge", "vedge-host\_pnic" and "vservice-vnic".   |
+---------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| link\_id (Optional)             | query    | string     | MongoDB ObjectId of the link, it must be a string that can be converted to MongoDB ID, when this filter is specified, it will return all the cliques which contain that specific link.                                                                                                                                                                              |
+---------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| page (Optional)                 | query    | int        | The page is to be returned, the default is the first page, if the page is larger than the maximum page of the query, it will return an empty set. (Page starts from 0).                                                                                                                                                                                             |
+---------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| page\_size (Optional)           | query    | int        | The size of each page, the default is 1000.                                                                                                                                                                                                                                                                                                                         |
+---------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**Response**

+----------------------+----------+------------+---------------------------------------------------------+
| **Name**             | **In**   | **Type**   | **Description**                                         |
+======================+==========+============+=========================================================+
| id                   | body     | string     | ID of the clique.                                       |
+----------------------+----------+------------+---------------------------------------------------------+
| \_id                 | body     | string     | MongoDB ObjectId of the clique.                         |
+----------------------+----------+------------+---------------------------------------------------------+
| environment          | body     | string     | Environment of the clique.                              |
+----------------------+----------+------------+---------------------------------------------------------+
| focal\_point         | body     | string     | Object ID of the focal point.                           |
+----------------------+----------+------------+---------------------------------------------------------+
| focal\_point\_type   | body     | string     | Type of the focal point object, e.g. "vservice".        |
+----------------------+----------+------------+---------------------------------------------------------+
| links                | body     | array      | List of MongoDB ObjectIds of the links in the clique.   |
+----------------------+----------+------------+---------------------------------------------------------+
| links\_detailed      | body     | array      | Details of the links in the clique.                     |
+----------------------+----------+------------+---------------------------------------------------------+
| constraints          | body     | object     | Constraints of the clique.                              |
+----------------------+----------+------------+---------------------------------------------------------+
| cliques              | body     | array      | The list of clique ids that match the filters.          |
+----------------------+----------+------------+---------------------------------------------------------+

**Examples**

**Example Get Cliques**

**Request**

`*http://10.56.20.32:8000/cliques?env\_name=Mirantis-Liberty-API&link\_id=58a2405a6a283a8bee15d42f* <http://10.56.20.32:8000/cliques?env_name=Mirantis-Liberty-API&link_id=58a2405a6a283a8bee15d42f>`__

**Response**

{

    "cliques": [               

    | {
    |       "link\_types": [
    |           "instance-vnic",
    |           "vservice-vnic",
    |           "vnic-vconnector"
    |       ],
    |      "environment": "Mirantis-Liberty",
    |      "focal\_point\_type": "vnic",
    |      "id": "576c119a3f4173144c7a75c5"
    | },

    | {
    |      "link\_types": [
    |          "vnic-vconnector",
    |          "vconnector-vedge"
    |      ],
    |      "environment": "Mirantis-Liberty",
    |      "focal\_point\_type": "vconnector",
    |      "id": "576c119a3f4173144c7a75c6"
    | }

       ]

}

**Example Get Clique Details**

**Request**

http://korlev-calipso-testing.cisco.com:8000/cliques?env_name=Mirantis-Liberty-API&id=58a2406e6a283a8bee15d43f

**Response**

| {
|    'id': '58867db16a283a8bee15cd2b',
|    'focal\_point\_type': 'host\_pnic',
|    'environment': 'Mirantis-Liberty',
|    '\_id': '58867db16a283a8bee15cd2b',
|    'links\_detailed': [
|       {
|          'state': 'up',
|          'attributes': {
|             'network': 'e180ce1c-eebc-4034-9e50-b3bab1c13979'
|          },
|          'target': '58867cc86a283a8bee15cc92',
|          'source': '58867d166a283a8bee15ccd0',
|          'host': '`*node-1.cisco.com* <http://node-1.cisco.com>`__',
|          'link\_type': 'host\_pnic-network',
|          'target\_id': 'e180ce1c-eebc-4034-9e50-b3bab1c13979',
|          'source\_id':
  'eno16777728.103@eno16777728-00:50:56:ac:e8:97',
|          'link\_weight': 0,
|          'environment': 'Mirantis-Liberty',
|          '\_id': '58867d646a283a8bee15ccf3',
|          'target\_label': '',
|          'link\_name': 'Segment-None',
|          'source\_label': ''
|       }
|    ],

| 'links': [
|    '58867d646a283a8bee15ccf3'
|  ],
| 'focal\_point': '58867d166a283a8bee15ccd0',
| 'constraints': {
|    }

}

Clique\_types
-------------

**GET        **/clique\_types

Description: get clique\_type details with environment name and
clique\_type id, or get a list of clique\_types with filters except id

Normal response code: 200

Error response code:  badRequest(400), unauthorized(401), notFound(404)

**Request**

+---------------------------------+----------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Name**                        | **In**   | **Type**   | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
+=================================+==========+============+==============================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================+
| env\_name                       | query    | string     | Environment of the clique\_types. e.g. "Mirantis-Liberty-API"                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
+---------------------------------+----------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                              | query    | string     | ID of the clique\_type, it must be a string that can be converted to the MongoDB ObjectID.                                                                                                                                                                                                                                                                                                                                                                                                                                   |
+---------------------------------+----------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| focal\_point\_type (Optional)   | query    | string     | Type of the focal point object, some possible values for it are "vnic", "vconnector", "vedge", "instance", "vservice", "host\_pnic", "network", "port", "otep" and "agent".                                                                                                                                                                                                                                                                                                                                                  |
+---------------------------------+----------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| link\_type(Optional)            | query    | string     | Type of the link, when this filter is specified, it will return all the clique\_types which contain the specific link\_type in its link\_types array. Some possible values of the link\_type are "instance-vnic", "otep-vconnector", "otep-host\_pnic", "host\_pnic-network", "vedge-otep", "vnic-vconnector", "vconnector-host\_pnic", "vnic-vedge", "vedge-host\_pnic" and "vservice-vnic". Repeat link\_type several times to specify multiple link\_types, e.g link\_type=instance-vnic&link\_type=host\_pnic-network.   |
+---------------------------------+----------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| page\_size(Optional)            | query    | int        | Size of each page, the default is 1000.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
+---------------------------------+----------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| page (Optional)                 | query    | int        | Which page is to be returned, the default is first page, if the page is larger than the maximum page of the query, it will return an empty result set. (Page starts from 0).                                                                                                                                                                                                                                                                                                                                                 |
+---------------------------------+----------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**Response**

+----------------------+----------+------------+--------------------------------------------------------------------+
| **Name**             | **In**   | **Type**   | **Description**                                                    |
+======================+==========+============+====================================================================+
| id                   | body     | string     | ID of the clique\_type.                                            |
+----------------------+----------+------------+--------------------------------------------------------------------+
| \_id                 | body     | string     | MongoDB ObjectId of the clique\_type                               |
+----------------------+----------+------------+--------------------------------------------------------------------+
| environment          | body     | string     | Environment of the clique\_type.                                   |
+----------------------+----------+------------+--------------------------------------------------------------------+
| focal\_point\_type   | body     | string     | Type of the focal point, e.g. "vnic".                              |
+----------------------+----------+------------+--------------------------------------------------------------------+
| link\_types          | body     | array      | List of link\_types of the clique\_type.                           |
+----------------------+----------+------------+--------------------------------------------------------------------+
| name                 | body     | string     | Name of the clique\_type.                                          |
+----------------------+----------+------------+--------------------------------------------------------------------+
| clique\_types        | body     | array      | List of clique\_type ids of clique types that match the filters.   |
+----------------------+----------+------------+--------------------------------------------------------------------+

**Examples**

**Example Get Clique\_types**

**Request**

`*** *** <http://korlev-osdna-testing.cisco.com:8000/clique_types?env_name=Mirantis-Liberty-API&id=&focal_point_type=&link_type=instance-vnic&page=&page_size=3&link_type=&link_type=pnic-network>`__\ http://korlev-calipso-testing.cisco.com:8000/clique_types?env_name=Mirantis-Liberty-API&link_type=instance-vnic&page_size=3&link_type=host_pnic-network

`**Response** <http://korlev-osdna-testing.cisco.com:8000/clique_types?env_name=Mirantis-Liberty-API&link_type=instance-vnic&page_size=3&link_type=pnic-network>`__

{

    "clique\_types": [        

    | {
    |        "environment": "Mirantis-Liberty",
    |        "focal\_point\_type": "host\_pnic",
    |        "id": "58ca73ae3a8a836d10ff3b80"
    | }

    ]

}

**Example Get Clique\_type Details**

**Request**

http://korlev-calipso-testing.cisco.com:8000/clique_types?env_name=Mirantis-Liberty-API&id=585b183c761b05789ee3c659

**Response**

| {
|    'id': '585b183c761b05789ee3c659',
|    'focal\_point\_type': 'vnic',
|    'environment': 'Mirantis-Liberty-API',
|    '\_id': '585b183c761b05789ee3c659',
|    'link\_types': [
|       'instance-vnic',
|       'vservice-vnic',
|       'vnic-vconnector'
|    ],
|    'name': 'vnic\_clique'
| }

**POST           **/clique\_types

Description: Create a new clique\_type

Normal response code: 201(Created)

Error response code: badRequest(400), unauthorized(401),  conflict(409)

**Request**

+---------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Name**                        | **In**   | **Type**   | **Description**                                                                                                                                                                                                                                                           |
+=================================+==========+============+===========================================================================================================================================================================================================================================================================+
| environment(Mandatory)          | body     | string     | Environment of the system, the environment must be the existing environment in the system.                                                                                                                                                                                |
+---------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| focal\_point\_type(Mandatory)   | body     | string     | Type of the focal point, some possible values are "vnic", "vconnector", "vedge", "instance", "vservice", "host\_pnic", "network", "port", "otep" and "agent".                                                                                                             |
+---------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| link\_types(Mandatory)          | body     | array      | Link\_types of the clique\_type, some possible values of the link\_type are "instance-vnic", "otep-vconnector", "otep-host\_pnic", "host\_pnic-network", "vedge-otep", "vnic-vconnector", "vconnector-host\_pnic", "vnic-vedge", "vedge-host\_pnic" and "vservice-vnic"   |
+---------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| name(Mandatory)                 | body     | string     | Name of the clique type, e.g. "instance\_vconnector\_clique"                                                                                                                                                                                                              |
+---------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**Request Example**

**post  **\ http://korlev-calipso-testing.cisco.com:8000/clique_types

| {
|    "environment" : "RDO-packstack-Mitaka",   
|     "focal\_point\_type" : "instance",       
|     "link\_types" : [
|         "instance-vnic",
|         "vnic-vconnector",
|         "vconnector-vedge",
|         "vedge-otep",
|         "otep-host\_pnic",
|         "host\_pnic-network"
|     ],
|     "name" : "instance\_vconnector\_clique"
| }

**Response**

**Successful Example**

| {
|         "message": "created a new clique\_type for environment
  Mirantis-Liberty"
| }

Clique\_constraints
-------------------

**GET            **/clique\_constraints

Description: get clique\_constraint details with clique\_constraint id,
or get a list of clique\_constraints with filters except id.

Normal response code: 200

Error response code: badRequest(400), unauthorized(401), notFound(404)

Note: this is not environment specific so query starts with parameter,
not env\_name (as with all others), example:

http://korlev-calipso-testing.cisco.com:8000/clique_constraints?focal_point_type=instance

**Request**

+---------------------------------+----------+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Name**                        | **In**   | **Type**   | **Description**                                                                                                                                                                |
+=================================+==========+============+================================================================================================================================================================================+
| id (Optional)                   | query    | string     | ID of the clique\_constraint, it must be a string that can be converted to MongoDB ObjectId.                                                                                   |
+---------------------------------+----------+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| focal\_point\_type (Optional)   | query    | string     | Type of the focal\_point, some possible values for that are "vnic", "vconnector", "vedge", "instance", "vservice", "host\_pnic", "network", "port", "otep" and "agent".        |
+---------------------------------+----------+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| constraint(Optional)            | query    | string     | Constraint of the cliques, repeat this filter several times to specify multiple constraints. e.g                                                                               |
|                                 |          |            |                                                                                                                                                                                |
|                                 |          |            | constraint=network&constraint=host\_pnic.                                                                                                                                      |
+---------------------------------+----------+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| page (Optional)                 | query    | int        | Which page is to be returned, the default is the first page, if the page is larger than the maximum page of the query, the last page will be returned. (Page starts from 0.)   |
+---------------------------------+----------+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| page\_size (Optional)           | query    | int        | Size of each page, the default is 1000                                                                                                                                         |
+---------------------------------+----------+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**Response **

+-----------------------+----------+------------+----------------------------------------------------------+
| **Name**              | **In**   | **Type**   | **Description**                                          |
+=======================+==========+============+==========================================================+
| id                    | body     | string     | Object id of the clique constraint.                      |
+-----------------------+----------+------------+----------------------------------------------------------+
| \_id                  | body     | string     | MongoDB ObjectId of the clique\_constraint.              |
+-----------------------+----------+------------+----------------------------------------------------------+
| focal\_point\_type    | body     | string     | Type of the focal point object.                          |
+-----------------------+----------+------------+----------------------------------------------------------+
| constraints           | body     | array      | Constraints of the clique.                               |
+-----------------------+----------+------------+----------------------------------------------------------+
| clique\_constraints   | body     | array      | List of clique constraints ids that match the filters.   |
+-----------------------+----------+------------+----------------------------------------------------------+

**Examples**

**Example Get Clique\_constraints**

**Request**

http://korlev-calipso-testing.cisco.com:8000/clique_constraints?constraint=host_pnic&constraint=network

**Response**

{

     "clique\_constraints": [ 

    | {
    |        "id": "576a4176a83d5313f21971f5"
    | },
    | {
    |         "id": "576ac7069f6ba3074882b2eb"
    | }

    ]

}

**Example Get Clique\_constraint Details**

**Request**

http://korlev-calipso-testing.cisco.com:8000/clique_constraints?id=576a4176a83d5313f21971f5

`**Response** <http://korlev-osdna-testing.cisco.com:8000/clique_constraints?focal_point_type=&constraint=&id=576a4176a83d5313f21971f5&constraint=&page=&page_size=>`__

| {
|       "\_id": "576a4176a83d5313f21971f5",
|       "constraints": [
|            "network",
|           "host\_pnic"
|       ],
|      "id": "576a4176a83d5313f21971f5",
|     "focal\_point\_type": "instance"
| }

Scans
-----

**GET            **/scans

Description: get scan details with environment name and scan id, or get
a list of scans with filters except id

Normal response code: 200

Error response code: badRequest (400), unauthorized (401), notFound(404)

**Request**

+--------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Name**                 | **In**   | **Type**   | **Description**                                                                                                                                                             |
+==========================+==========+============+=============================================================================================================================================================================+
| env\_name (Mandatory)    | query    | string     | Environment of the scans. e.g. "Mirantis-Liberty".                                                                                                                          |
+--------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id (Optional)            | query    | string     | ID of the scan, it must be a string that can be converted MongoDB ObjectId.                                                                                                 |
+--------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| base\_object(Optional)   | query    | string     | ID of the scanned base object. e.g. "`*node-2.cisco.com* <http://node-2.cisco.com>`__".                                                                                     |
+--------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| status (Optional)        | query    | string     | Status of the scans, the possible values for the status are "draft", "pending", "running", "completed", "failed" and "aborted".                                             |
+--------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| page (Optional)          | query    | int        | Which page is to be returned, the default is the first page, if the page is larger than the maximum page of the query, it will return an empty set. (Page starts from 0.)   |
+--------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| page\_size (Optional)    | query    | int        | Size of each page, the default is 1000.                                                                                                                                     |
+--------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**Response**

+-------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------+
| **Name**                | **In**   | **Type**   | **Description**                                                                                                           |
+=========================+==========+============+===========================================================================================================================+
| status                  | body     | string     | The current status of the scan, possible values are "draft", "pending", "running", "completed", "failed" and "aborted".   |
+-------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------+
| log\_level              | body     | string     | Logging level of the scanning, the possible values are "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG" and "NOTSET".      |
+-------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------+
| clear                   | body     | boolean    | Indicates whether it needs to clear all the data before scanning.                                                         |
+-------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------+
| scan\_only\_inventory   | body     | boolean    | Only scan and store data in the inventory.                                                                                |
+-------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------+
| scan\_only\_links       | body     | boolean    | Limit the scan to find only missing links.                                                                                |
+-------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------+
| scan\_only\_cliques     | body     | boolean    | Limit the scan to find only missing cliques.                                                                              |
+-------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------+
| scan\_completed         | body     | boolean    | Indicates if the scan completed                                                                                           |
+-------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------+
| submit\_timestamp       | body     | string     | Submit timestamp of the scan                                                                                              |
+-------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------+
| environment             | body     | string     | Environment name of the scan                                                                                              |
+-------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------+
| inventory               | body     | string     | Name of the inventory collection.                                                                                         |
+-------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------+
| object\_id              | body     | string     | Base object of the scan                                                                                                   |
+-------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------+

**Examples**

**Example Get Scans**

**Request**

http://korlev-calipso-testing.cisco.com:8000/scans?status=completed&env_name=Mirantis-Liberty&base_object=ff

**Response**

| {
|       "scans": [

|            {
|               "status": "pending",
|               "environment": "Mirantis-Liberty",
|              "id": "58c96a075eb66a121cc4e75f",
|              "scan\_completed": true
|           }

       ]

}

**Example Get Scan Details**

**Request**

http://korlev-calipso-testing.cisco.com:8000/scans?env_name=Mirantis-Liberty&id=589a49cf2e8f4d154386c725

**Response**

| {
|       "scan\_only\_cliques": true,
|       "object\_id": "ff",
|       "start\_timestamp": "2017-01-28T01:02:47.352000",
|       "submit\_timestamp": null,
|       "clear": true,
|       "\_id": "589a49cf2e8f4d154386c725",
|       "environment": "Mirantis-Liberty",
|       "scan\_only\_links": true,
|       "id": "589a49cf2e8f4d154386c725",
|       "inventory": "update-test",
|       "scan\_only\_inventory": true,
|       "log\_level": "warning",
|       "status": "completed",
|       "end\_timestamp": "2017-01-28T01:07:54.011000"
| }

**POST            **/scans

Description: create a new scan (ask calipso to scan an environment for
detailed data gathering).

Normal response code: 201(Created)

Error response code: badRequest (400), unauthorized (401)

**Request **

+------------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------+
| **Name**                           | **In**   | **Type**   | **Description**                                                                                                           |
+====================================+==========+============+===========================================================================================================================+
| status (mandatory)                 | body     | string     | The current status of the scan, possible values are "draft", "pending", "running", "completed", "failed" and "aborted".   |
+------------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------+
| log\_level (optional)              | body     | string     | Logging level of the scanning, the possible values are "critical", "error", "warning", "info", "debug" and "notset".      |
+------------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------+
| clear (optional)                   | body     | boolean    | Indicates whether it needs to clear all the data before scanning.                                                         |
+------------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------+
| scan\_only\_inventory (optional)   | body     | boolean    | Only scan and store data in the inventory.                                                                                |
+------------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------+
| scan\_only\_links (optional)       | body     | boolean    | Limit the scan to find only missing links.                                                                                |
+------------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------+
| scan\_only\_cliques (optional)     | body     | boolean    | Limit the scan to find only missing cliques.                                                                              |
+------------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------+
| environment (mandatory)            | body     | string     | Environment name of the scan                                                                                              |
+------------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------+
| inventory (optional)               | body     | string     | Name of the inventory collection.                                                                                         |
+------------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------+
| object\_id (optional)              | body     | string     | Base object of the scan                                                                                                   |
+------------------------------------+----------+------------+---------------------------------------------------------------------------------------------------------------------------+

**Request Example**

**post
 **\ http://korlev-calipso-testing.cisco.com:8000/\ `*scans* <http://korlev-osdna-testing.cisco.com:8000/scans>`__

| {
|        "status" : "pending",
|        "log\_level" : "warning",
|        "clear" : true,
|        "scan\_only\_inventory" : true,
|        "env\_name" : "Mirantis-Liberty",
|        "inventory" : "koren",
|        "object\_id" : "ff"
| }

**Response**

**Successful Example**

| {
|        "message": "created a new scan for environment
  Mirantis-Liberty"
| }

Scheduled\_scans
----------------

**GET            **/scheduled\_scans

Description: get scheduled\_scan details with environment name and
scheduled\_scan id, or get a list of scheduled\_scans with filters
except id

Normal response code: 200

Error response code: badRequest (400), unauthorized (401), notFound(404)

**Request**

+-------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Name**                | **In**   | **Type**   | **Description**                                                                                                                                                             |
+=========================+==========+============+=============================================================================================================================================================================+
| env\_name(Mandatory)    | query    | string     | Environment of the scheduled\_scans. e.g. "Mirantis-Liberty".                                                                                                               |
+-------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id (Optional)           | query    | string     | ID of the scheduled\_scan, it must be a string that can be converted to MongoDB ObjectId.                                                                                   |
+-------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| freq (Optional)         | query    | string     | Frequency of the scheduled\_scans, the possible values for the freq are "HOURLY", "DAILY", "WEEKLY", "MONTHLY", and "YEARLY".                                               |
+-------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| page (Optional)         | query    | int        | Which page is to be returned, the default is the first page, if the page is larger than the maximum page of the query, it will return an empty set. (Page starts from 0.)   |
+-------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| page\_size (Optional)   | query    | int        | Size of each page, the default is 1000.                                                                                                                                     |
+-------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**Response**

+-------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------+
| **Name**                | **In**   | **Type**   | **Description**                                                                                                                              |
+=========================+==========+============+==============================================================================================================================================+
| freq                    | body     | string     | The frequency of the scheduled\_scan, possible values are "HOURLY", "DAILY", "WEEKLY", "MONTHLY", and "YEARLY".                              |
+-------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------+
| log\_level              | body     | string     | Logging level of the scheduled\_scan, the possible values are "critical", "error", "warning", "info", "debug" and "notset".                  |
+-------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------+
| clear                   | body     | boolean    | Indicates whether it needs to clear all the data before scanning.                                                                            |
+-------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------+
| scan\_only\_inventory   | body     | boolean    | Only scan and store data in the inventory.                                                                                                   |
+-------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------+
| scan\_only\_links       | body     | boolean    | Limit the scan to find only missing links.                                                                                                   |
+-------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------+
| scan\_only\_cliques     | body     | boolean    | Limit the scan to find only missing cliques.                                                                                                 |
+-------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------+
| submit\_timestamp       | body     | string     | Submitted timestamp of the scheduled\_scan                                                                                                   |
+-------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------+
| environment             | body     | string     | Environment name of the scheduled\_scan                                                                                                      |
+-------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------+
| scheduled\_timestamp    | body     | string     | Scheduled time for the scanning, it should follows `*ISO 8610: * <https://en.wikipedia.org/wiki/ISO_8601>`__\ YYYY-MM-DDThh:mm:ss.sss+hhmm   |
+-------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------------------------------+

**Examples**

**Example Get Scheduled\_scans**

**Request**

http://korlev-calipso-testing.cisco.com:8000/scheduled_scans?env_name=Mirantis-Liberty

**Response**

| {
|       "scheduled\_scans": [

           {

|               "freq":"WEEKLY",
|               "environment": "Mirantis-Liberty",
|               "id": "58c96a075eb66a121cc4e75f",
|               "scheduled\_timestamp": "2017-01-28T01:07:54.011000"
|           }

       ]

}

**Example Get Scheduled\_Scan Details**

**Request**

http://korlev-calipso-testing.cisco.com:8000/scheduled\_scans?env\_name=Mirantis-Liberty&id=589a49cf2e8f4d154386c725

**Response**

| {
|       "scan\_only\_cliques": true,
|       "scheduled\_timestamp": "2017-01-28T01:02:47.352000",
|       "submit\_timestamp": 2017-01-27T01:07:54.011000"",
|       "clear": true,
|       "\_id": "589a49cf2e8f4d154386c725",
|       "environment": "Mirantis-Liberty",
|       "scan\_only\_links":false,
|       "id": "589a49cf2e8f4d154386c725",
|       "scan\_only\_inventory":false,
|       "log\_level": "warning",
|       "freq": "WEEKLY"
| }

**POST            **/scheduled\_scans

Description: create a new scheduled\_scan (request calipso to scan in a
future date).

Normal response code: 201(Created)

Error response code: badRequest (400), unauthorized (401)

**Request **

+------------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| **Name**                           | **In**   | **Type**   | **Description**                                                                                                                                     |
+====================================+==========+============+=====================================================================================================================================================+
| log\_level (optional)              | body     | string     | Logging level of the scheduled\_scan, the possible values are "critical", "error", "warning", "info", "debug" and "notset".                         |
+------------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| clear (optional)                   | body     | boolean    | Indicates whether it needs to clear all the data before scanning.                                                                                   |
+------------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| scan\_only\_inventory (optional)   | body     | boolean    | Only scan and store data in the inventory.                                                                                                          |
+------------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| scan\_only\_links (optional)       | body     | boolean    | Limit the scan to find only missing links.                                                                                                          |
+------------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| scan\_only\_cliques (optional)     | body     | boolean    | Limit the scan to find only missing cliques.                                                                                                        |
+------------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| environment (mandatory)            | body     | string     | Environment name of the scan                                                                                                                        |
+------------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| freq(mandatory)                    | body     | string     | The frequency of the scheduled\_scan, possible values are "HOURLY", "DAILY", "WEEKLY", "MONTHLY", and "YEARLY".                                     |
+------------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| submit\_timestamp(mandatory)       | body     | string     | Submitted time for the scheduled\_scan, it should follows `*ISO 8610: * <https://en.wikipedia.org/wiki/ISO_8601>`__\ YYYY-MM-DDThh:mm:ss.sss+hhmm   |
+------------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+

**
Post** http://korlev-calipso-testing.cisco.com:8000/scheduled_scans

| {
|        "freq" : "WEEKLY",
|        "log\_level" : "warning",
|        "clear" : true,
|        "scan\_only\_inventory" : true,
|        "env\_name" : "Mirantis-Liberty",
|        "submit\_timestamp" : "2017-01-28T01:07:54.011000"
| }

**Response**

**Successful Example**

| {
|        "message": "created a new scheduled\_scan for environment
  Mirantis-Liberty"
| }

Constants
---------

**GET            **/constants

Description: get constant details with name (constants are used by ui
and event/scan managers)

Normal response code: 200

Error response code: badRequest(400), unauthorized(401), notFound(404)

**Request**

+--------------------+----------+------------+-----------------------------------------------+
| **Name**           | **In**   | **Type**   | **Description**                               |
+====================+==========+============+===============================================+
| name (Mandatory)   | query    | string     | Name of the constant. e.g. "distributions".   |
+--------------------+----------+------------+-----------------------------------------------+

**Response**

+------------+----------+------------+-------------------------------------+
| **Name**   | **In**   | **Type**   | **Description**                     |
+============+==========+============+=====================================+
| id         | body     | string     | ID of the constant.                 |
+------------+----------+------------+-------------------------------------+
| \_id       | body     | string     | MongoDB ObjectId of the constant.   |
+------------+----------+------------+-------------------------------------+
| name       | body     | string     | Name of the constant.               |
+------------+----------+------------+-------------------------------------+
| data       | body     | array      | Data of the constant.               |
+------------+----------+------------+-------------------------------------+

**Examples**

**Example Get Constant Details **

**Request**

`*http://korlev-osdna-testing.cisco.com:8000/constants?name=link\_states* <http://korlev-osdna-testing.cisco.com:8000/constants?name=link_states>`__

**Response**

| {
|      "\_id": "588796ac2e8f4d02b8e7aa2a",
|      "data": [
|           {
|                "value": "up",
|                "label": "up"
|           },
|          {
|              "value": "down",
|              "label": "down"
|          }
|       ],
|       "id": "588796ac2e8f4d02b8e7aa2a",
|       "name": "link\_states"
| }

list of constants available in current release:

    "name" : "constraints"

    "name" : "env_types"

    "name" : "log_levels"

    "name" : "environment_types"

    "name" : "mechanism_drivers"

    "name" : "type_drivers"

    "name" : "environment_monitoring_types"

    "name" : "monitoring_check_statuses"

    "name" : "link_states"

    "name" : "environment_provision_types"

    "name" : "environment_operational_status"

    "name" : "link_types"

    "name" : "monitoring_sides"

    "name" : "messages_severity"

    "name" : "object_types"

    "name" : "scans_statuses"

    "name" : "distributions"

    "name" : "distribution_versions"

    "name" : "message_source_systems"

    "name" : "object_types_for_links"

    "name" : "scan_object_types"

    "name" : "configuration_targets"




Monitoring\_Config\_Templates
-----------------------------

**GET            **/monitoring\_config\_templates 

Description: get monitoring\_config\_template details with template id,
or get a list of templates with filters except id (see
monitoring-guide).

Normal response code: 200

Error response code: badRequest(400), unauthorized(401), notFound(404) 
               

**Request**

+------------------------+----------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Name**               | **In**   | **Type**   | **Description**                                                                                                                                                                                                        |
+========================+==========+============+========================================================================================================================================================================================================================+
| id (Optional)          | query    | string     | ID of the monitoring config template, it must be a string that can be converted MongoDB ObjectId                                                                                                                       |
+------------------------+----------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| order (Optional)       | query    | int        | Order by which templates are applied, 1 is the OSDNA default template. Templates that the user added later we use higher order and will override matching attributes in the default templates or add new attributes.   |
+------------------------+----------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| side (Optional)        | query    | string     | The side which runs the monitoring, the possible values are "client" and "server".                                                                                                                                     |
+------------------------+----------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| type (Optional)        | query    | string     | The name of the config file, e.g. "client.json".                                                                                                                                                                       |
+------------------------+----------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| page (Optional)        | query    | int        | Which page is to be returned, the default is the first page, if the page is larger than the maximum page of the query, it will return an empty result set. (Page starts from 0).                                       |
+------------------------+----------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| page\_size(Optional)   | query    | int        | Size of each page, the default is 1000.                                                                                                                                                                                |
+------------------------+----------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**Response **

+----------------------+----------+------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Name**             | **In**   | **Type**   | **Description**                                                                                                                                                                                                         |
+======================+==========+============+=========================================================================================================================================================================================================================+
| id                   | body     | string     | ID of the monitoring\_config\_template.                                                                                                                                                                                 |
+----------------------+----------+------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| \_id                 | body     | srting     | MongoDB ObjectId of the monitoring\_config\_template.                                                                                                                                                                   |
+----------------------+----------+------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| monitoring\_system   | body     | string     | System that we use to do the monitoring, e.g, "Sensu".                                                                                                                                                                  |
+----------------------+----------+------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| order                | body     | string     | Order by which templates are applied, 1 is the OSDNA default templates. Templates that the user added later we use higher order and will override matching attributes in the default templates or add new attributes.   |
+----------------------+----------+------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| config               | body     | object     | Configuration of the monitoring.                                                                                                                                                                                        |
+----------------------+----------+------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| side                 | body     | string     | The side which runs the monitoring.                                                                                                                                                                                     |
+----------------------+----------+------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| type                 | body     | string     | The name of the config file, e.g. "client.json".                                                                                                                                                                        |
+----------------------+----------+------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**Examples**

**Example Get Monitoring\_config\_templates**

**Request**

http://korlev-calipso-testing.cisco.com:8000/monitoring_config_templates?side=client&order=1&type=rabbitmq.json&page=0&page_size=1

**Response**

| {
|      "monitoring\_config\_templates": [            

    | {
    |       "type": "rabbitmq.json",
    |       "side": "client",
    |       "id": "583711893e149c14785d6daa"
    | }

|      ]
| }

**Example Get Monitoring\_config\_template Details**

**Request**

http://korlev-calipso-testing.cisco.com:8000/monitoring_config_templates?id=583711893e149c14785d6daa

**Response**

| {
|      "order": "1",
|      "monitoring\_system": "sensu",
|      "\_id": "583711893e149c14785d6daa",
|      "side": "client",
|      "type": "rabbitmq.json",
|      "config": {
|      "rabbitmq": {
|      "host": "{server\_ip}",
|      "vhost": "/sensu",
|      "password": "{rabbitmq\_pass}",
|      "user": "{rabbitmq\_user}",
|      "port": 5672
|        }
|      },
|     "id": "583711893e149c14785d6daa"
| }

Aggregates
----------

**GET            **/aggregates

Description: List some aggregated information about environment, message
or constant.

Normal response code: 200

Error response code: badRequest(400), unauthorized(401), notFound(404)

**Request**

+------------------------+----------+------------+--------------------------------------------------------------------------------------------------------------+
| **Name**               | **In**   | **Type**   | **Description**                                                                                              |
+========================+==========+============+==============================================================================================================+
| env\_name (Optional)   | query    | string     | Environment name, if the aggregate type is "environment", this value must be specified.                      |
+------------------------+----------+------------+--------------------------------------------------------------------------------------------------------------+
| type (Optional)        | query    | string     | Type of aggregate, currently we support three types of aggregate, "environment", "message" and "constant".   |
+------------------------+----------+------------+--------------------------------------------------------------------------------------------------------------+

**Response **

+------------------------+----------+------------+------------------------------------------------------------------------------------------------------------+
| **Name**               | **In**   | **Type**   | **Description**                                                                                            |
+========================+==========+============+============================================================================================================+
| type                   | body     | string     | Type of aggregate, we support three types of aggregates now, "environment", "message" and "constant".      |
+------------------------+----------+------------+------------------------------------------------------------------------------------------------------------+
| env\_name (Optional)   | body     | string     | Environment name of the aggregate, when the aggregate type is "environment", this attribute will appear.   |
+------------------------+----------+------------+------------------------------------------------------------------------------------------------------------+
| aggregates             | body     | object     | The aggregates information.                                                                                |
+------------------------+----------+------------+------------------------------------------------------------------------------------------------------------+

**Examples**

**Example Get Environment Aggregate **

**Request**

http://korlev-calipso-testing.cisco.com:8000/aggregates?env_name=Mirantis-Liberty-API&type=environment

**Response**

| {
|       "env\_name": "Mirantis-Liberty-API",
|       "type": "environment",
|       "aggregates": {
|           "object\_types": {
|              "projects\_folder": 1,
|              "instances\_folder": 3,
|              "otep": 3,
|              "region": 1,
|              "vedge": 3,
|              "networks\_folder": 2,
|              "project": 2,
|              "vconnectors\_folder": 3,
|              "availability\_zone": 2,
|              "vedges\_folder": 3,
|              "regions\_folder": 1,
|              "network": 3,
|              "vnics\_folder": 6,
|              "instance": 2,
|             "vservice": 4,
|             "availability\_zones\_folder": 1,
|             "vnic": 8,
|             "vservices\_folder": 3,
|             "port": 9,
|             "pnics\_folder": 3,
|             "network\_services\_folder": 3,
|             "ports\_folder": 3,
|             "host": 3,
|             "vconnector": 6,
|             "network\_agent": 6,
|             "aggregates\_folder": 1,
|             "pnic": 15,
|             "network\_agents\_folder": 3,
|             "vservice\_miscellenaous\_folder": 1
|             }
|       }
| }

**Example Get Messages Aggregate**

**Request**

http://korlev-calipso-testing.cisco.com:8000/aggregates?type=message

**Response**

{

    "type": "message",

    "aggregates": {

         "levels": {

              "warn": 5,

              "info": 10,

              "error": 10

         },

        "environments": {

              "Mirantis-Liberty-API": 5,

              "Mirantis-Liberty": 10

         }

    }

}

**Example Get Constants Aggregate**

**Request**

http://korlev-calipso-testing.cisco.com:8000/aggregates?type=constant

**Response**

| {
|        "type": "constant",
|        "aggregates": {
|        "names": {
|           "link\_states": 2,
|           "scan\_statuses": 6,
|           "type\_drivers": 5,
|           "log\_levels": 6,
|           "monitoring\_sides": 2,
|           "mechanism\_drivers": 5,
|           "messages\_severity": 8,
|           "distributions": 16,
|           "link\_types": 11,
|           "object\_types": 10
|          }
|        }
| }

Environment\_configs
--------------------

**GET            **/environment\_configs

Description: get environment\_config details with name, or get a list of
environments\_config with filters except name

Normal response code: 200

Error response code: badRequest(400), unauthorized(401), notFound(404)

**Request**

+-------------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Name**                            | **In**   | **Type**   | **Description**                                                                                                                                                                                           |
+=====================================+==========+============+===========================================================================================================================================================================================================+
| name(Optional)                      | query    | string     | Name of the environment.                                                                                                                                                                                  |
+-------------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| distribution(Optional)              | query    | string     | The distribution of the OpenStack environment, it must be one of the distributions we support, e.g "Mirantis-8.0".(you can get all the supported distributions by querying the distributions constants)   |
+-------------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| mechanism\_drivers(Optional)        | query    | string     | The mechanism drivers of the environment, it should be one of the drivers in mechanism\_drivers constants, e.g "ovs".                                                                                     |
+-------------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| type\_drivers(Optional)             | query    | string     | 'flat', 'gre', 'vlan', 'vxlan'.                                                                                                                                                                           |
+-------------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| user(Optional)                      | query    | string     | name of the environment user                                                                                                                                                                              |
+-------------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| listen(Optional)                    | query    | boolean    | Indicates whether the environment is being listened.                                                                                                                                                      |
+-------------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| scanned(Optional)                   | query    | boolean    | Indicates whether the environment has been scanned.                                                                                                                                                       |
+-------------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| monitoring\_setup\_done(Optional)   | query    | boolean    | Indicates whether the monitoring setup has been done.                                                                                                                                                     |
+-------------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| operational(Optional)               | query    | string     | operational status of the environment, the possible statuses are "stopped", "running" and "error".                                                                                                        |
+-------------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| page(Optional)                      | query    | int        | Which page is to be returned, the default is the first page, if the page is larger than the maximum page of the query, it will return an empty result set. (Page starts from 0).                          |
+-------------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| page\_size(Optional)                | query    | int        | Size of each page, the default is 1000.                                                                                                                                                                   |
+-------------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**Response**

+---------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------+
| **Name**                  | **In**   | **Type**   | **Description**                                                                                                      |
+===========================+==========+============+======================================================================================================================+
| configuration             | body     | array      | List of configurations of the environment, including configurations of mysql, OpenStack, CLI, AMQP and Monitoring.   |
+---------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------+
| distribution              | body     | string     | The distribution of the OpenStack environment, it must be one of the distributions we support, e.g "Mirantis-8.0".   |
+---------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------+
| last\_scanned             | body     | string     | The date of last time scanning the environment, the format of the date is MM/DD/YY.                                  |
+---------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------+
| mechanism\_dirvers        | body     | array      | The mechanism drivers of the environment, it should be one of the drivers in mechanism\_drivers constants.           |
+---------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------+
| monitoring\_setup\_done   | body     | boolean    | Indicates whether the monitoring setup has been done.                                                                |
+---------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------+
| name                      | body     | string     | Name of the environment.                                                                                             |
+---------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------+
| operational               | body     | boolean    | Indicates if the environment is operational.                                                                         |
+---------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------+
| scanned                   | body     | boolean    | Indicates whether the environment has been scanned.                                                                  |
+---------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------+
| type                      | body     | string     | Production, testing, development, etc.                                                                               |
+---------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------+
| type\_drivers             | body     | string     | 'flat', 'gre', 'vlan', 'vxlan'.                                                                                      |
+---------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------+
| user                      | body     | string     | The user of the environment.                                                                                         |
+---------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------+
| listen                    | body     | boolean    | Indicates whether the environment is being listened.                                                                 |
+---------------------------+----------+------------+----------------------------------------------------------------------------------------------------------------------+

**Examples**

**Example Get Environments config**

**Request**

http://korlev-calipso-testing.cisco.com:8000/environment_configs?mechanism_drivers=ovs

`**Response** <http://korlev-osdna-testing.cisco.com:8000/environment_configs?mechanism_drivers=ovs&name=>`__

| {
|         environment\_configs: [         

    | {
    |       "distribution": "Canonical-icehouse",
    |       "name": "thundercloud"
    | }

|         ]
| }

**Example Environment config Details**

**Request**

http://korlev-calipso-testing.cisco.com:8000/environment_configs?name=Mirantis-Mitaka-2

**Response**

| {
|        "type\_drivers": "vxlan",
|        "name": "Mirantis-Mitaka-2",
|        "app\_path": "/home/yarony/osdna\_prod/app",
|        "scanned": true,
|        "type": "environment",
|        "user": "test",
|        "distribution": "Mirantis-9.1",
|        "monitoring\_setup\_done": true,
|        "listen": true,
|        "mechanism\_drivers": [
|              "ovs"
|        ],
|        "configuration": [
|        {
|               "name": "mysql",
|               "user": "root",
|               "host": "10.56.31.244",
|               "port": "3307",
|               "password": "TsbQPwP2VPIUlcFShkCFwBjX"
|         },
|         {
|               "name": "CLI",
|               "user": "root",
|               "host": "10.56.31.244",
|               "key": "/home/ilia/Mirantis\_Mitaka\_id\_rsa"
|          },
|         {
|               "password": "G1VfxeJmtK5vIyNNMP4qZmXB",
|               "user": "nova",
|               "name": "AMQP",
|               "port": "5673",
|               "host": "10.56.31.244"
|          },
|         {
|              "server\_ip":
  "`*korlev-nsxe1.cisco.com* <http://korlev-nsxe1.cisco.com>`__",
|              "name": "Monitoring",
|              "port": "4567",
|              "env\_type": "development",
|              "rabbitmq\_pass": "sensuaccess",
|              "rabbitmq\_user": "sensu",
|              "provision": "DB",
|              "server\_name": "devtest-sensu",
|              "type": "Sensu",
|              "config\_folder": "/tmp/sensu\_test"
|         },
|        {
|             "user": "admin",
|             "name": "OpenStack",
|             "port": "5000",
|             "admin\_token": "qoeROniLLwFmoGixgun5AXaV",
|             "host": "10.56.31.244",
|            "pwd": "admin"
|          }
|         ],
|        "\_id": "582d77ee3e149c1318b3aa54",
|        "operational": "yes"
| }

**POST            **/environment\_configs

Description: create a new environment configuration.

Normal response code: 201(Created)

Error response code:
badRequest(400), unauthorized(401), notFound(404), conflict(409)

**Request**

+---------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Name**                        | **In**   | **Type**   | **Description**                                                                                                                                                                                           |
+=================================+==========+============+===========================================================================================================================================================================================================+
| configuration(Mandatory)        | body     | array      | List of configurations of the environment, including configurations of mysql(mandatory), OpenStack(mandatory), CLI(mandatory), AMQP(mandatory) and Monitoring(Optional).                                  |
+---------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| distribution(Mandatory)         | body     | string     | The distribution of the OpenStack environment, it must be one of the distributions we support, e.g "Mirantis-8.0".(you can get all the supported distributions by querying the distributions constants)   |
+---------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| last\_scanned(Optional)         | body     | string     | The date and time of last scanning, it should follows `*ISO 8610: * <https://en.wikipedia.org/wiki/ISO_8601>`__                                                                                           |
|                                 |          |            |                                                                                                                                                                                                           |
|                                 |          |            | YYYY-MM-DDThh:mm:ss.sss\ *+*\ hhmm                                                                                                                                                                        |
+---------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| mechanism\_dirvers(Mandatory)   | body     | array      | The mechanism drivers of the environment, it should be one of the drivers in mechanism\_drivers constants, e.g "OVS".                                                                                     |
+---------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| name(Mandatory)                 | body     | string     | Name of the environment.                                                                                                                                                                                  |
+---------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| operational(Mandatory)          | body     | boolean    | Indicates if the environment is operational. e.g. true.                                                                                                                                                   |
+---------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| scanned(Optional)               | body     | boolean    | Indicates whether the environment has been scanned.                                                                                                                                                       |
+---------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| listen(Mandatory)               | body     | boolean    | Indicates if the environment need to been listened.                                                                                                                                                       |
+---------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| user(Optional)                  | body     | string     | The user of the environment.                                                                                                                                                                              |
+---------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| app\_path(Mandatory)            | body     | string     | The path that the app is located in.                                                                                                                                                                      |
+---------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| type(Mandatory)                 | body     | string     | Production, testing, development, etc.                                                                                                                                                                    |
+---------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| type\_drivers(Mandatory)        | body     | string     | 'flat', 'gre', 'vlan', 'vxlan'.                                                                                                                                                                           |
+---------------------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**Request Example**

**Post** http://korlev-calipso-testing:8000/environment_configs

| {
|        "app\_path" : "/home/korenlev/OSDNA/app/",
|        "configuration" : [
|             {
|                   "host" : "172.23.165.21",
|                   "name" : "mysql",
|                   "password" : "password",
|                   "port" : NumberInt(3306),
|                   "user" : "root",
|                   "schema" : "nova"
|             },
|             {
|                   "name" : "OpenStack",
|                   "host" : "172.23.165.21",
|                   "admin\_token" : "TL4T0I7qYNiUifH",
|                   "admin\_project" : "admin",
|                   "port" : "5000",
|                   "user" : "admin",
|                   "pwd" : "admin"
|            },
|           {
|                   "host" : "172.23.165.21",
|                   "key" : "/home/yarony/.ssh/juju\_id\_rsa",
|                   "name" : "CLI",
|                   "user" : "ubuntu"
|           },
|          {
|                   "name" : "AMQP",
|                   "host" : "10.0.0.1",
|                   "port" : "5673",
|                   "user" : "User",
|                   "password" : "abcd1234"
|            },
|           {
|                   "config\_folder" : "/tmp/sensu\_test\_liberty",
|                   "provision" : "None",
|                   "env\_type" : "development",
|                   "name" : "Monitoring",
|                   "port" : "4567",
|                   "rabbitmq\_pass" : "sensuaccess",
|                   "rabbitmq\_user" : "sensu",
|                   "server\_ip" :
  "`*korlev.cisco.com* <http://korlev.cisco.com>`__",
|                   "server\_name" : "devtest-sensu",
|                   "type" : "Sensu"
|             }
|          ],
|         "distribution" : "Canonical-icehouse",
|         "last\_scanned" : "2017-02-13T16:07:15Z",
|         "listen" : true,
|         "mechanism\_drivers" : [
|                  "OVS"
|           ],
|          "name" : "thundercloud",
|          "operational" : "yes",
|          "scanned" : false,
|          "type" : "environment",
|           "type\_drivers" : "gre",
|           "user" : "WS7j8oTbWPf3LbNne"
| }

**Response **

**Successful Example**

| {
|         "message": "created environment\_config for Mirantis-Liberty"
| }

.. |image0| image:: media/image1.png
   :width: 6.50000in
   :height: 4.27153in
