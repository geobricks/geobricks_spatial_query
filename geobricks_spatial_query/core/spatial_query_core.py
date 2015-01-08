import simplejson
from geobricks_common.core.log import logger
from geobricks_dbms.core.dbms_postgresql import DBMSPostgreSQL


log = logger(__file__)


class SpatialQuery():

    # default settings
    config = None

    def __init__(self, config):
        self.config = config["settings"]

    def query_db(self, datasource, query, output_json=False):
        db_datasource = get_db_datasource(self.config, datasource)
        db = get_db(db_datasource)
        log.info(query)
        return db.query(query, output_json)

    def query_srid(self, datasource, table, geom_column):
        srid = self.query_db(datasource, "SELECT ST_SRID(" + geom_column + ") FROM " + table + " LIMIT 1")
        return str(srid[0][0])

    def query_bbox(self, datasource, layer_code, column_code, codes, epsg="4326", output_geojson=True):
        db_datasource = get_db_datasource(self.config, datasource)
        layer = get_layer(db_datasource, layer_code)
        table = get_table(layer)
        geom_column = get_layer_column_geom(layer)
        column_code = get_layer_column(layer, column_code)
        srid = self.query_srid(datasource, table, geom_column)
        codes = parse_codes(codes)

        # query
        query = "SELECT  "
        # add geojson
        if output_geojson: query += " ST_AsGeoJSON( "

        # TODO: the transform is not always needed
        # add ST_Transform (in theory add if needed) and extent
        query += "ST_Transform(ST_SetSRID(ST_Extent(" + geom_column + "), " + srid + "), " + epsg + " ) "

        if output_geojson: query += ") "

        # From
        query += "FROM " + table + " "

        # where
        query += "WHERE " + column_code + " IN(" + codes + ")"

        db = DBMSPostgreSQL(db_datasource)
        log.info(query)
        result = db.query(query)
        log.info(result)

        return result


# [["BOX(60.475829 29.3772500000001,74.8898620000001 38.4906960000001)"]]
# [["{\"type\":\"Polygon\",\"coordinates\":[[[60.475829,29.3772500000001],[60.475829,38.4906960000001],[74.8898620000001,38.4906960000001],[74.8898620000001,29.3772500000001],[60.475829,29.3772500000001]]]}"]]

def get_db_datasource(config, datasource):
    return config["db"][datasource]


def get_db(db_datasource):
    return DBMSPostgreSQL(db_datasource)

def get_layer(db_datasource, layer_code):
    if "tables" in db_datasource:
        if layer_code in db_datasource["tables"]:
            return db_datasource["tables"][layer_code]
    log.warn("layer code no mapped, returning the passed layer_code:" + layer_code)
    return layer_code


def get_table(layer):
    if "table" in layer:
        return layer["table"]
    log.warn('No "table" in layer definition, passing as table' + layer)
    return layer


def get_layer_column(layer, column_code):
    if "column" in layer:
        if column_code in layer["column"]:
            return layer["column"][column_code]
        else:
            log.warn('No "' + column_code + '" in layer definition' + layer)
    else:
        log.error('"column" it\'s not set in' + layer)
    log.warn("Returning default '" + column_code + "' value for the column")
    return column_code


#TODO: how to query the layer to get the geometry column?
def get_layer_column_geom(layer):
    return get_layer_column(layer, 'geom')


# TODO: how to get the geometry srid dinamically?
def get_layer_srid(layer):
    if "srid" in layer:
        return layer["srid"]
    log.warn("Returning default SRID: 4326")
    return None


def parse_codes(codes, is_string=True):
    codes_string = ""
    for c in codes:
        codes_string += "'"+c+"'," if is_string else c+","
    return codes_string[:-1]



