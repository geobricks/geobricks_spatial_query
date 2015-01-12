from flask import Flask
from flask.ext.cors import CORS
from geobricks_spatial_query.config.config import config
from geobricks_spatial_query.rest import spatial_query_rest
import logging

# Initialize the Flask app
app = Flask(__name__)

# Initialize CORS filters
cors = CORS(app, resources={r'/*': {'origins': '*'}})

# Url blueprint prefix
url_prefix = "/spatialquery"

# Core services.
app.register_blueprint(spatial_query_rest.app, url_prefix=url_prefix)

# Logging level.
log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)

# Start Flask server
if __name__ == '__main__':
    app.run(host=config['settings']['host'], port=config['settings']['port'], debug=config['settings']['debug'], threaded=True)