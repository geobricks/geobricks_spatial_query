import simplejson
from geobricks_common.core.log import logger
from geobricks_dbms.core.dbms_postgresql import DBMSPostgreSQL
from geobricks_spatial_query.utils.geojson import encode_geojson


log = logger(__file__)


class SpatialQuery():

    # default settings
    config = None
    default_db = "spatial"

    def __init__(self, config):
        self.config = config["settings"] if "settings" in config else config

    def query_db(self, datasource, query, output_json=False, geojson_encoding=None):
        db_datasource = get_db_datasource(self.config, datasource)
        db = get_db(db_datasource)
        result = db.query(query, output_json)
        if geojson_encoding:
            result = encode_geojson(result)
        return result

    def query_srid(self, datasource, layer_code, geom_column=None):
        # TODO: implement a function that returns all the info in sequence (it's the same as query_bbox)
        db_datasource = get_db_datasource(self.config, datasource)
        schema = db_datasource["schema"] if "schema" in db_datasource else None
        layer = get_layer(db_datasource, layer_code)
        table = get_table(layer, schema)
        if geom_column is None:
            geom_column = get_layer_column_geom(layer)
        # TODO: untill here

        srid = self.query_db(datasource, "SELECT ST_SRID(" + geom_column + ") FROM " + table + " LIMIT 1")
        return str(srid[0][0])

    def query_bbox(self, datasource, layer_code, column_code, codes, epsg="4326", output_type="bbox"):
        # Standard query PostGIS by function
        query = self._get_query_postgis_function(datasource, layer_code, column_code, codes, epsg, output_type, 'ST_Extent')

        log.info(query)
        result = self.query_db(datasource, query, False, False)
        # log.info(result)

        # different kind of result based on the request
        if output_type == "geojson":
            return result
        else:
            # TODO: fix the process to json
            result = simplejson.dumps(result)
            result = simplejson.loads(result)
            result = simplejson.loads(result[0][0])
            minlat = result["coordinates"][0][0][0]
            minlon = result["coordinates"][0][1][1]
            maxlat = result["coordinates"][0][2][0]
            maxlon = result["coordinates"][0][0][1]
            # result = [[minlat, minlon], [maxlat, maxlon]]
            result = [[minlon, minlat], [maxlon, maxlat]]
        return result

    def _get_query_postgis_function(self, datasource, layer_code, column_code, codes, epsg="4326", output_type="geojson", postgis_function='ST_Extent', additional_select_fields=None):
        '''
        :param datasource:
        :param layer_code:
        :param column_code:
        :param codes:
        :param epsg:
        :param output_type:
        :param postgis_function: i.e ST_Extent (bbox), ST_Centroid (centroids)
        :return:
        '''
        db_datasource = get_db_datasource(self.config, datasource)
        schema = db_datasource["schema"] if "schema" in db_datasource else None
        layer = get_layer(db_datasource, layer_code)
        table = get_table(layer, schema)
        geom_column = get_layer_column_geom(layer)
        column_code = get_layer_column(layer, column_code)
        srid = self.query_srid(datasource, table, geom_column)
        codes = parse_codes(codes)

        # query
        query = "SELECT "
        # add geojson
        if output_type == "geojson" or output_type == "bbox": query += "ST_AsGeoJSON("

        # TODO: the transform is not always needed
        # add ST_Transform (in theory add if needed) and extent
        query += "ST_Transform(ST_SetSRID(" + postgis_function + "(" + geom_column + "), " + srid + "), " + epsg + ") "

        if output_type == "geojson" or output_type == "bbox": query += ") "

        # additional select fields (if needed in the returned query. It's useful in the geojson encoding)
        if additional_select_fields:
            for field in additional_select_fields:
                query += ", " + field + " "


        # From
        query += "FROM " + table + " "

        # where
        if column_code:
            if codes:
                query += "WHERE " + column_code + " IN (" + codes + ")"
        return query

    def query_centroid(self, datasource, layer_code, column_code, codes, epsg="4326", additional_select_fields=None, output_type="geojson"):

        # adding column_code to additional_select_fields in case it is None
        additional_select_fields = additional_select_fields if additional_select_fields is not None else [column_code] if column_code is not None else None

        # Standard query PostGIS by function
        query = self._get_query_postgis_function(datasource, layer_code, column_code, codes, epsg, output_type, 'ST_Centroid', additional_select_fields)

        log.info(query)
        result = self.query_db(datasource, query, False, True)

        # different kind of result based on the request
        if output_type == "geojson":
            return result
        else:
            # TODO: fix the process to json
            return result

    def get_query_string_select_all(self, datasource, layer_code, column_code, codes, select="*", groupby=None):
        db_datasource = get_db_datasource(self.config, datasource)
        schema = db_datasource["schema"] if "schema" in db_datasource else None
        layer = get_layer(db_datasource, layer_code)
        table = get_table(layer, schema)
        column_code = get_layer_column(layer, column_code)
        codes = parse_codes(codes)

        # query
        query = "SELECT " + select + " "
        # From
        query += "FROM " + table + " "

        # where
        if column_code:
            if codes:
                query += "WHERE " + column_code + " IN (" + codes + ") "

        if groupby is not None:
            query += "GROUP BY " + groupby + " "

        return query

    def get_db_instance(self, datasource=None):
        if datasource:
            return get_db(get_db_datasource(self.config, datasource))
        log.warn("Returing the default db instance: " + self.default_db)
        return get_db(get_db_datasource(self.config, self.default_db))



def get_db_datasource(config, datasource):
    return config["db"][datasource]


def get_db(db_datasource):
    return DBMSPostgreSQL(db_datasource)


def get_layer(db_datasource, layer_code):
    if "tables" in db_datasource:
        if layer_code in db_datasource["tables"]:
            return db_datasource["tables"][layer_code]
    log.warn("layer code not mapped, returning the passed layer_code: %s" % layer_code)
    return layer_code


def get_table(layer, schema=None):
    table = layer if isinstance(layer, basestring) else ""
    if "table" in layer:
        table = layer["table"]
    else:
        log.warn('No "table" in layer definition, passing as table %s' % layer)
    if isinstance(layer, basestring):
        if schema is not None and not table.startswith(schema):
            table = schema + "." + table
    log.info('The table to search : ' + table)
    return table
    # if "table" in layer:
    #     return layer["table"]
    # log.warn('No "table" in layer definition, passing as table' + layer)
    # return layer


def get_layer_column(layer, column_code):
    if column_code:
        if "column" in layer:
            if column_code in layer["column"]:
                return layer["column"][column_code]
            else:
                log.warn('No "' + column_code + '" in layer definition %s' % layer)
        else:
            log.warn('"column" it\'s not set in %s' % layer)
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
    codes_string = None
    if codes:
        codes_string = ""
        for c in codes:
            codes_string += "'"+str(c)+"'," if is_string else str(c)+","
    return codes_string[:-1] if codes_string else None



