import unittest
import json
from flask import Flask
from geobricks_common.core.log import logger
from geobricks_spatial_query.rest.spatial_query_rest import app

log = logger(__file__)

class GeobricksTest(unittest.TestCase):

    db = "spatial"
    layer_table = "ne_110m_admin_0_countries" # use 'country' for alias test (if mapped)
    column_geom = "geom"
    column_code = "iso_a2"
    column_label = ["iso_a2", "name"]
    codes = ['AF']

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(app, url_prefix='/spatialquery')
        self.tester = self.app.test_client(self)

    def test_bbox_rest_with_alias(self):
        response = self.tester.get('/spatialquery/db/spatial/bbox/layer/country/iso_a2/AF', content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result, [[38.4862816432164, 60.5284298033116], [29.3185724960443, 75.1580277851409]])

    def test_bbox_rest(self):
        response = self.tester.get('/spatialquery/db/spatial/bbox/layer/ne_110m_admin_0_countries/iso_a2/AF', content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result, [[38.4862816432164, 60.5284298033116], [29.3185724960443, 75.1580277851409]])

    def test_bbox_rest_to_3857(self):
        response = self.tester.get('/spatialquery/db/spatial/bbox/layer/ne_110m_admin_0_countries/iso_a2/AF/epsg/3857', content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result, [[4648350.70054128, 6737993.98422105], [3416255.99756658, 8366553.38206859]])

    def test_bbox_rest_to_3857_with_alias(self):
        response = self.tester.get('/spatialquery/db/spatial/bbox/layer/country/iso_a2/AF/epsg/3857', content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result, [[4648350.70054128, 6737993.98422105], [3416255.99756658, 8366553.38206859]])

    def test_query_rest(self):
        response = self.tester.get("/spatialquery/db/spatial/query/select name from spatial.ne_110m_admin_0_countries where iso_a2 = 'AF'", content_type='application/json')
        self.assertEqual(response.data, '[["Afghanistan"]]')

    # Centroids
    def test_centroid_rest(self):
        response = self.tester.get("/spatialquery/db/spatial/centroid/layer/ne_110m_admin_0_countries/iso_a2/AF", content_type='application/json')
        self.assertEqual(response.data, '{"type": "FeatureCollection", "features": [{"geometry": {"type": "Point", "coordinates": [66.0866902219283, 33.8563992816908]}, "type": "Feature", "properties": {"prop0": "AF"}}]}')

    def test_centroid_with_labels_rest(self):
        response = self.tester.get("/spatialquery/db/spatial/centroid/layer/ne_110m_admin_0_countries/iso_a2/AF/labels/iso_a2,name", content_type='application/json')
        self.assertEqual(response.data, '{"type": "FeatureCollection", "features": [{"geometry": {"type": "Point", "coordinates": [66.0866902219283, 33.8563992816908]}, "type": "Feature", "properties": {"prop0": "AF", "prop1": "Afghanistan"}}]}')


def run_test():
    suite = unittest.TestLoader().loadTestsFromTestCase(GeobricksTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    run_test()



