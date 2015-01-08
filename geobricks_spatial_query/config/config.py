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
                "username": "user",
                "password": "pwd",
                "schema": "public",
            },

            },
    }
}
