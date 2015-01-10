from geobricks_common.config.config_COMMON_IMPORT import merge_config_from_file

import logging

config = {
    "settings": {
        # To be used by Flask: DEVELOPMENT ONLY
        "debug": True,

        # Flask host: DEVELOPMENT ONLY
        "host": "localhost",

        # Flask port: DEVELOPMENT ONLY
        "port": 5904,

        "db": {
            # Spatial Database
            "spatial": {
                # default_db will search in the dbs["database"] as default option
                "dbname": "fenix",
                "host": "localhost",
                "port": "5432",
                "username": "fenix",
                "password": "Qwaszx",
                "schema": "public",
                },

            },
        }
}

# config merge with possible
config = merge_config_from_file(config)