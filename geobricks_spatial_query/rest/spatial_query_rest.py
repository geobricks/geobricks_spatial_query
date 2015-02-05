import simplejson
import os
from flask import Blueprint
from flask import Response
from flask.ext.cors import cross_origin
from geobricks_spatial_query.config.config import config
from geobricks_common.core.log import logger
from geobricks_spatial_query.core.spatial_query_core import SpatialQuery
from flask import request

log = logger(__file__)

app = Blueprint("spatialquery", "spatialquery")


@app.route('/')
@cross_origin(origins='*')
def root():
    """
    Root REST service.
    @return: Welcome message.
    """
    return 'Welcome to Geobricks SpatialQuery!'


@app.route('/discovery/')
@app.route('/discovery')
@cross_origin(origins='*')
def rest_discovery():
    """
    Discovery service available for all Geobricks libraries that describes the plug-in.
    @return: Dictionary containing information about the service.
    """
    out = {
        'name': 'spatialquery',
        'title': 'Spatial Query service',
        'description': 'Functionalities to handle spatial queries.',
        'type': 'SERVICE',
    }
    return Response(simplejson.dumps(out), content_type='application/json; charset=utf-8')


@app.route('/db/<datasource>/query/<query>/', methods=['GET'])
@app.route('/db/<datasource>/query/<query>', methods=['GET'])
@cross_origin(origins='*', headers=['Content-Type'])
def rest_query_db(datasource, query):
    """
    Query the PostGIS with a custom query
    :param datasource: postgis/postgres datasource
    :param query: query to be passed to the db
    :return:
    """
    # TODO it's not used the schema in the query.
    # it should be replaced if the query contains {{SCHEMA}} or something like that
    try:
        sq = SpatialQuery(config)
        geojson_encoding = request.args.get('geojsonEncoding')
        result = sq.query_db(datasource, query, False, geojson_encoding)
        return Response(simplejson.dumps(result), content_type='application/json; charset=utf-8')
    except Exception, e:
        log.error(e)
        raise Exception(e)


@app.route('/db/<datasource>/bbox/layer/<layer_code>/<column_code>/<codes>/', methods=['GET'])
@app.route('/db/<datasource>/bbox/layer/<layer_code>/<column_code>/<codes>', methods=['GET'])
@cross_origin(origins='*', headers=['Content-Type'])
def rest_query_bbox(datasource, layer_code, column_code, codes):
    try:
        sq = SpatialQuery(config)
        codes = codes.split(",")
        result = sq.query_bbox(datasource, layer_code, column_code, codes)
        return Response(simplejson.dumps(result), content_type='application/json; charset=utf-8')
    except Exception, e:
        log.error(e)
        raise Exception(e)


@app.route('/db/<datasource>/bbox/layer/<layer_code>/<column_code>/<codes>/epsg/<epsg>/', methods=['GET'])
@app.route('/db/<datasource>/bbox/layer/<layer_code>/<column_code>/<codes>/epsg/<epsg>', methods=['GET'])
@cross_origin(origins='*', headers=['Content-Type'])
def rest_query_bbox_epsg(datasource, layer_code, column_code, codes, epsg):
    try:
        sq = SpatialQuery(config)
        codes = codes.split(",")
        result = sq.query_bbox(datasource, layer_code, column_code, codes, epsg)
        return Response(simplejson.dumps(result), content_type='application/json; charset=utf-8')
    except Exception, e:
        log.error(e)
        raise Exception(e)


# @app.route('/db/<datasource>/query/layer/<layer_code>/select/<select_codes>/', methods=['GET'])
# @app.route('/db/<datasource>/query/layer/<layer_code>/select/<select_codes>', methods=['GET'])
# @cross_origin(origins='*', headers=['Content-Type'])
# def rest_query_bbox_epsg(datasource, layer_code, column_code, codes, epsg):
#     try:
#         sq = SpatialQuery(config)
#         codes = codes.split(",")
#         result = sq.query_bbox(datasource, layer_code, column_code, codes, epsg)
#         return Response(simplejson.dumps(result), content_type='application/json; charset=utf-8')
#     except Exception, e:
#         log.error(e)
#         raise Exception(e)

