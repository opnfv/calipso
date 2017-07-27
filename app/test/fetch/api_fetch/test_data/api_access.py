from datetime import datetime, timedelta


TIME_WITH_DOT = "2016-10-19T23:21:09.418406Z"
TIME_WITHOUT_DOT = "2016-10-19T23:21:09Z"
ILLEGAL_TIME = "23243423"
TEST_PROJECT = "test"
PROJECT = "admin"
TEST_URL = "test_url"
TEST_HEADER = "test_headers"
TEST_BODY = "test_body"

RESPONSE = {
    'server': 'Apache',
    'vary': 'X-Auth-Token',
    'content-type': 'application/json',
    'date': 'Wed, 19 Oct 2016 23:15:36 GMT',
    'content-length': '4876',
    'x-openstack-request-id': 'req-01cda259-7f60-4440-99a0-508fed90f815',
    'connection': 'close',
    'status': '200'
}
ERROR_RESPONSE = {
    'connection': 'close',
    'status': '400'
}
GET_CONTENT = b'{"text":"test"}'
CORRECT_AUTH_CONTENT = b'{"access": {"token": {"issued_at": "2016-10-21T23:49:50.000000Z", "expires": "2016-10-22T00:49:50.445603Z", "id": "gAAAAABYCqme1l0qCm6mi3jON4ElweTkhZjGXZ_bYuxLHZGGXgO3T_JLnxKJ7KbK4xA8KjQ-DQe2trDncKQA0M-yeX167wT0xO_rjqqcCA19JV-EeXFfx7QOukkt8eC4pfK1r8Dc_kvBc-bwAemjZ1IvPGu5Nd2f0ktGWre0Qqzbg9QGtCEJUe8", "tenant": {"is_domain": false, "description": "admin tenant", "enabled": true, "id": "8c1751e0ce714736a63fee3c776164da", "parent_id": null, "name": "admin"}, "audit_ids": ["8BvzDPpyRBmeJho-FzKuGA"]}, "serviceCatalog": [{"endpoints": [{"adminURL": "http://192.168.0.2:8774/v2/8c1751e0ce714736a63fee3c776164da", "region": "RegionOne", "internalURL": "http://192.168.0.2:8774/v2/8c1751e0ce714736a63fee3c776164da", "id": "274cbbd9fd6d4311b78e78dd3a1df51f", "publicURL": "http://172.16.0.3:8774/v2/8c1751e0ce714736a63fee3c776164da"}], "endpoints_links": [], "type": "compute", "name": "nova"}, {"endpoints": [{"adminURL": "http://192.168.0.2:9696", "region": "RegionOne", "internalURL": "http://192.168.0.2:9696", "id": "8dc28584da224c4b9671171ead3c982a", "publicURL": "http://172.16.0.3:9696"}], "endpoints_links": [], "type": "network", "name": "neutron"}, {"endpoints": [{"adminURL": "http://192.168.0.2:8776/v2/8c1751e0ce714736a63fee3c776164da", "region": "RegionOne", "internalURL": "http://192.168.0.2:8776/v2/8c1751e0ce714736a63fee3c776164da", "id": "2c30937688e944889db4a64fab6816e6", "publicURL": "http://172.16.0.3:8776/v2/8c1751e0ce714736a63fee3c776164da"}], "endpoints_links": [], "type": "volumev2", "name": "cinderv2"}, {"endpoints": [{"adminURL": "http://192.168.0.2:8774/v3", "region": "RegionOne", "internalURL": "http://192.168.0.2:8774/v3", "id": "1df917160dfb4ce5b469764fde22b3ab", "publicURL": "http://172.16.0.3:8774/v3"}], "endpoints_links": [], "type": "computev3", "name": "novav3"}, {"endpoints": [{"adminURL": "http://192.168.0.2:8080", "region": "RegionOne", "internalURL": "http://192.168.0.2:8080", "id": "4f655c8f2bef46a0a7ba4a20bba53666", "publicURL": "http://172.16.0.3:8080"}], "endpoints_links": [], "type": "s3", "name": "swift_s3"}, {"endpoints": [{"adminURL": "http://192.168.0.2:9292", "region": "RegionOne", "internalURL": "http://192.168.0.2:9292", "id": "475c6c77a94e4e63a5a0f0e767f697a8", "publicURL": "http://172.16.0.3:9292"}], "endpoints_links": [], "type": "image", "name": "glance"}, {"endpoints": [{"adminURL": "http://192.168.0.2:8777", "region": "RegionOne", "internalURL": "http://192.168.0.2:8777", "id": "617177a3dcb64560a5a79ab0a91a7225", "publicURL": "http://172.16.0.3:8777"}], "endpoints_links": [], "type": "metering", "name": "ceilometer"}, {"endpoints": [{"adminURL": "http://192.168.0.2:8000/v1", "region": "RegionOne", "internalURL": "http://192.168.0.2:8000/v1", "id": "0f04ec6ed49f4940822161bf677bdfb2", "publicURL": "http://172.16.0.3:8000/v1"}], "endpoints_links": [], "type": "cloudformation", "name": "heat-cfn"}, {"endpoints": [{"adminURL": "http://192.168.0.2:8776/v1/8c1751e0ce714736a63fee3c776164da", "region": "RegionOne", "internalURL": "http://192.168.0.2:8776/v1/8c1751e0ce714736a63fee3c776164da", "id": "05643f2cf9094265b432376571851841", "publicURL": "http://172.16.0.3:8776/v1/8c1751e0ce714736a63fee3c776164da"}], "endpoints_links": [], "type": "volume", "name": "cinder"}, {"endpoints": [{"adminURL": "http://192.168.0.2:8773/services/Admin", "region": "RegionOne", "internalURL": "http://192.168.0.2:8773/services/Cloud", "id": "390dddc753cc4d378b489129d06c4b7d", "publicURL": "http://172.16.0.3:8773/services/Cloud"}], "endpoints_links": [], "type": "ec2", "name": "nova_ec2"}, {"endpoints": [{"adminURL": "http://192.168.0.2:8004/v1/8c1751e0ce714736a63fee3c776164da", "region": "RegionOne", "internalURL": "http://192.168.0.2:8004/v1/8c1751e0ce714736a63fee3c776164da", "id": "9e60268a5aaf422d9e42f0caab0a19b4", "publicURL": "http://172.16.0.3:8004/v1/8c1751e0ce714736a63fee3c776164da"}], "endpoints_links": [], "type": "orchestration", "name": "heat"}, {"endpoints": [{"adminURL": "http://192.168.0.2:8080/v1/AUTH_8c1751e0ce714736a63fee3c776164da", "region": "RegionOne", "internalURL": "http://192.168.0.2:8080/v1/AUTH_8c1751e0ce714736a63fee3c776164da", "id": "12e78e06595f48339baebdb5d4309c70", "publicURL": "http://172.16.0.3:8080/v1/AUTH_8c1751e0ce714736a63fee3c776164da"}], "endpoints_links": [], "type": "object-store", "name": "swift"}, {"endpoints": [{"adminURL": "http://192.168.0.2:35357/v2.0", "region": "RegionOne", "internalURL": "http://192.168.0.2:5000/v2.0", "id": "404cceb349614eb39857742970408301", "publicURL": "http://172.16.0.3:5000/v2.0"}], "endpoints_links": [], "type": "identity", "name": "keystone"}], "user": {"username": "admin", "roles_links": [], "name": "admin", "roles": [{"id": "888bdf92213a477ba9f10554bc382e57", "name": "admin"}], "enabled": true, "email": "admin@localhost", "id": "13baa553aae44adca6615e711fd2f6d9"}, "metadata": {"is_admin": 0, "roles": []}}}'
ERROR_AUTH_CONTENT = b'{"access": {}}'
ERROR_TOKEN_CONTENT = b'{"error":{"code":"code","title":"title","message":"message",", URL":"URL"},"access": {}}'

VALID_TOKENS = {
    PROJECT: {
        # make sure the expired time of the token is later than now
        "expires": (datetime.now() + timedelta(1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    }
}

EMPTY_TOKENS = {}

REGION_NAME = "RegionOne"
ERROR_REGION_NAME = "ERROR"
SERVICE_NAME = "nova"
ERROR_SERVICE_NAME = "ERROR"

REGION_URL = "http://10.56.20.239:8774/v2/329e0576da594c62a911d0dccb1238a7"
