from geobricks_spatial_query.config.config import config
from geobricks_dbms.core.dbms_postgresql import DBMSPostgreSQL


def query_db(datasource, query):
    spatial_db = DBMSPostgreSQL(config["settings"]["db"][datasource])
    return spatial_db.query(query)