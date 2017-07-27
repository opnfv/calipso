from bson.objectid import ObjectId


AGGREGATE = {
    "id": "1",
}

HOSTS = [
    {
        "id": "aggregate-osdna-agg-node-5.cisco.com",
        "name": "node-5.cisco.com"
    }
]

HOST_IN_INVENTORY = {
    "_id": "595ac4b6d7c037efdb8918a7"
}

HOSTS_RESULT = [
    {
        "id": "aggregate-osdna-agg-node-5.cisco.com",
        "name": "node-5.cisco.com",
        "ref_id": ObjectId(HOST_IN_INVENTORY["_id"])
    }
]
