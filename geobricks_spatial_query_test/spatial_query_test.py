import unittest
import simplejson
import requests
from geobricks_common.core.log import logger
from geobricks_spatial_query.config.config import config
from geobricks_spatial_query.core.spatial_query_core import SpatialQuery

log = logger(__file__)

class GeobricksTest(unittest.TestCase):

    db = "spatial"
    layer_table = "gaul0_2015_4326" # use 'country' for alias test (if mapped)
    column_geom = "geom"
    column_code = "adm0_code"
    codes = ['1']

    def test_gaul0_2015_4326_in_4326(self):
        sq = SpatialQuery(config)
        result = sq.query_bbox(self.db, self.layer_table, self.column_code, self.codes, "4326")
        self.assertEqual(result, [[38.4906960000001, 60.475829], [29.3772500000001, 74.8898620000001]])

    def test_gaul0_2015_4326_in_3857(self):
        sq = SpatialQuery(config)
        result = sq.query_bbox(self.db, self.layer_table, self.column_code, self.codes, "3857")
        self.assertEqual(result, [[4648978.50570379, 6732138.48958109], [3423749.69036421, 8336701.30341853]])

    def test_gaul0_2015_4326_in_4326_geojson(self):
        sq = SpatialQuery(config)
        result = sq.query_bbox(self.db, self.layer_table, self.column_code, self.codes, "4326", "geojson")
        self.assertEqual(result, [('{"type":"Polygon","coordinates":[[[60.475829,29.3772500000001],[60.475829,38.4906960000001],[74.8898620000001,38.4906960000001],[74.8898620000001,29.3772500000001],[60.475829,29.3772500000001]]]}',)])

    def test_gaul0_2015_4326_in_3857_geojson(self):
        sq = SpatialQuery(config)
        result = sq.query_bbox(self.db, self.layer_table, self.column_code, self.codes, "3857", "geojson")
        self.assertEqual(result, [('{"type":"Polygon","coordinates":[[[6732138.48958109,3423749.69036421],[6732138.48958109,4648978.50570379],[8336701.30341853,4648978.50570379],[8336701.30341853,3423749.69036421],[6732138.48958109,3423749.69036421]]]}',)])

    def test_srid(self):
        sq = SpatialQuery(config)
        result = sq.query_srid(self.db, self.layer_table, self.column_geom)
        self.assertEqual(result, "4326")

    def test_bbox_rest_with_alias(self):
        try:
            requests.get("http://localhost:5925/spatialquery/discovery")
        except Exception, e:
            log.warn("Service is down. Please run rest/distribution_main.py to run the test")

        r = requests.get("http://localhost:5925/spatialquery/db/spatial/bbox/layer/country/adm0_code/1")
        result = simplejson.loads(r.text)
        self.assertEqual(result, [[38.4906960000001, 60.475829], [29.3772500000001, 74.8898620000001]])

    def test_bbox_rest(self):
        try:
            requests.get("http://localhost:5925/spatialquery/discovery")
        except Exception, e:
            log.warn("Service is down. Please run rest/distribution_main.py to run the test")

        r = requests.get("http://localhost:5925/spatialquery/db/spatial/bbox/layer/gaul0_2015_4326/adm0_code/1")
        result = simplejson.loads(r.text)
        self.assertEqual(result, [[38.4906960000001, 60.475829], [29.3772500000001, 74.8898620000001]])

    def test_bbox_rest_to_3857(self):
        try:
            requests.get("http://localhost:5925/spatialquery/discovery")
        except Exception, e:
            log.warn("Service is down. Please run rest/distribution_main.py to run the test")

        r = requests.get("http://localhost:5925/spatialquery/db/spatial/bbox/layer/gaul0_2015_4326/adm0_code/1/epsg/3857")
        result = simplejson.loads(r.text)
        self.assertEqual(result, [[4648978.50570379, 6732138.48958109], [3423749.69036421, 8336701.30341853]])

    def test_bbox_rest_to_3857_with_alias(self):
        try:
            requests.get("http://localhost:5925/spatialquery/discovery")
        except Exception, e:
            log.warn("Service is down. Please run rest/distribution_main.py to run the test")

        r = requests.get("http://localhost:5925/spatialquery/db/spatial/bbox/layer/country/adm0_code/1/epsg/3857")
        result = simplejson.loads(r.text)
        self.assertEqual(result, [[4648978.50570379, 6732138.48958109], [3423749.69036421, 8336701.30341853]])

    def test_query(self):
        sq = SpatialQuery(config)
        result = sq.query_db(self.db, "select adm0_code from spatial.gaul0_2015_4326 where adm0_code = '1'")
        result = simplejson.dumps(result)
        self.assertEqual(result, '[[1]]')

    def test_query_rest(self):
        try:
            requests.get("http://localhost:5925/spatialquery/discovery")
        except Exception, e:
            log.warn("Service is down. Please run rest/distribution_main.py to run the test")

        r = requests.get("http://localhost:5925/spatialquery/db/spatial/query/select adm0_code from spatial.gaul0_2015_4326 where adm0_code = '1'")
        result = simplejson.loads(r.text)
        self.assertEqual(result, [[1]])

def run_test():
    suite = unittest.TestLoader().loadTestsFromTestCase(GeobricksTest)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    run_test()



