import json
import os
from flask import Blueprint
from flask import Response
from flask import request
from flask.ext.cors import cross_origin
from geobricks_spatial_query.utils.log import logger
from geobricks_spatial_query.config.config import config
from flask import request, send_from_directory
from geobricks_dbms.core.dbms_postgresql import DBMSPostgreSQL

log = logger(__file__)

app = Blueprint("spatial_query", "spatial_query")

# TODO: How to map it to the download distribution URL? Get the one in the @app.route "/download/"
#distribution_url = request.host_url + "distribution/download/"

zip_filename = "layers"


@app.route('/discovery/')
@app.route('/discovery')
@cross_origin(origins='*')
def discovery():
    """
    Discovery service available for all Geobricks libraries that describes the plug-in.
    @return: Dictionary containing information about the service.
    """
    out = {
        'name': 'Spatial Query service',
        'description': 'Functionalities to handle spatial queries.',
        'type': 'SPATIAL_QUERY'
    }
    print "----"
    print request.script_root
    print request.path
    print request.base_url
    print request.url_root
    print request.url
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')


@app.route('/db/<datasource>/<query>/', methods=['GET'])
@app.route('/db/<datasource>/<query>', methods=['GET'])
@cross_origin(origins='*', headers=['Content-Type'])
def query_db(datasource, query):
    """
    Query the PostGIS with a custom query
    :param datasource: postgis/postgres datasource
    :param query: query to be passed to the db
    :return:
    """
    # TODO it's not used the schema in the query.
    # it should be replaced if the query contains {{SCHEMA}} or something like that
    try:
        spatial_db = DBMSPostgreSQL(config["settings"]["db"][datasource])
        result = spatial_db.query(query)
        return Response(json.dumps(result), content_type='application/json; charset=utf-8')
    except Exception, e:
        log.error(e)
        raise Exception(e)
