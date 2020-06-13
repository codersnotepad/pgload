# should fail because of additional 'active' key in data row, not in type list
test01 = {
    "data": [
        {"id": 1, "name": "tim", "address": None},
        {"id": 2, "name": "kim", "address": "8 Bell Road", "alive": True},
        {"id": 3, "name": "caitlin", "address": "50 Nunmill", "active": False},
    ],
    "type": {
        "id": "bigint",
        "name": "character",
        "address": "character",
        "alive": "boolean",
    },
    "index": ["id"],
    "unique": ["id"],
    "schema": {
        "name": "testdata",
        "owner": "tim",
        "grant": {"usage": "group02", "all": "group01"},
    },
    "table": {"name": "table01", "owner": "tim", "grant": {"all": "group01"}},
}


# scd2_load
test01 = {
    "data": [
        {"id": 1, "name": "tim", "address": None},
        {"id": 2, "name": "kim", "address": "8 Bell Road", "alive": True},
        {"id": 3, "name": "caitlin", "address": "50 Nunmill"},
    ],
    "type": {
        "id": "bigint",
        "name": "character",
        "address": "character",
        "alive": "boolean",
    },
    "index": ["id"],
    "unique": ["id"],
    "schema": {
        "name": "testdata",
        "owner": "tim",
        "grant": {"usage": "group02", "all": "group01"},
    },
    "table": {"name": "table01", "owner": "tim", "grant": {"all": "group01"}},
}
test01 = {
    "data": [{"id": 4, "name": "timote wipiiti-benseman", "address": None},],
    "type": {
        "id": "bigint",
        "name": "character",
        "address": "character",
        "alive": "boolean",
    },
    "index": ["id"],
    "unique": ["id"],
    "schema": {
        "name": "testdata",
        "owner": "tim",
        "grant": {"usage": "group02", "all": "group01"},
    },
    "table": {"name": "table01", "owner": "tim", "grant": {"all": "group01"}},
}
