config = {
    "settings": {
        # To be used by Flask: DEVELOPMENT ONLY
        "debug": True,

        # Flask host: DEVELOPMENT ONLY
        "host": "localhost",

        # Flask port: DEVELOPMENT ONLY
        "port": 5925,

        "db": {
            # Spatial Database
            "spatial": {
                # default_db will search in the dbs["database"] as default option
                "dbname": "spatialdbtest",
                "host": "localhost",
                "port": "5432",
                "username": "spatialuser",
                "password": "spatial",
                "schema": "spatial",
                "tables": {
                    "country": {
                        "table": "ne_110m_admin_0_countries"
                    }
                }
            }
        }
    }
}