import unittest
import simplejson
from geobricks_common.core.log import logger
from geobricks_spatial_query.config.config import config
from geobricks_spatial_query.core.spatial_query_core import SpatialQuery

log = logger(__file__)


class GeobricksTest(unittest.TestCase):

    db = "spatial"
    layer_table = "ne_110m_admin_0_countries" # use 'country' for alias test (if mapped)
    column_geom = "geom"
    column_code = "iso_a2"
    column_label = ["iso_a2", "name"]
    codes = ['AF']

    def test_countries_4326_in_4326(self):
        sq = SpatialQuery(config)
        result = sq.query_bbox(self.db, self.layer_table, self.column_code, self.codes, "4326")
        self.assertEqual(result, [[38.4862816432164, 60.5284298033116], [29.3185724960443, 75.1580277851409]])

    def test_countries_4326_in_3857(self):
        sq = SpatialQuery(config)
        result = sq.query_bbox(self.db, self.layer_table, self.column_code, self.codes, "3857")
        self.assertEqual(result, [[4648350.70054128, 6737993.98422105], [3416255.99756658, 8366553.38206859]])

    def test_countries_4326_in_4326_geojson(self):
        sq = SpatialQuery(config)
        result = sq.query_bbox(self.db, self.layer_table, self.column_code, self.codes, "4326", "geojson")
        self.assertEqual(result, [('{"type":"Polygon","coordinates":[[[60.5284298033116,29.3185724960443],[60.5284298033116,38.4862816432164],[75.1580277851409,38.4862816432164],[75.1580277851409,29.3185724960443],[60.5284298033116,29.3185724960443]]]}',)]                         )

    def test_countries_4326_in_3857_geojson(self):
        sq = SpatialQuery(config)
        result = sq.query_bbox(self.db, self.layer_table, self.column_code, self.codes, "3857", "geojson")
        self.assertEqual(result, [('{"type":"Polygon","coordinates":[[[6737993.98422105,3416255.99756658],[6737993.98422105,4648350.70054128],[8366553.38206859,4648350.70054128],[8366553.38206859,3416255.99756658],[6737993.98422105,3416255.99756658]]]}',)]                         )

    def test_srid(self):
        sq = SpatialQuery(config)
        result = sq.query_srid(self.db, self.layer_table, self.column_geom)
        self.assertEqual(result, "4326")

    # Query
    def test_query(self):
        sq = SpatialQuery(config)
        result = sq.query_db(self.db, "select name from spatial.ne_110m_admin_0_countries where iso_a2 = 'AF'")
        result = simplejson.dumps(result)
        self.assertEqual(result, '[["Afghanistan"]]')

    # Centroids
    def test_centroid(self):
        sq = SpatialQuery(config)
        result = sq.query_centroid(self.db, self.layer_table, self.column_code, self.codes, "4326", self.column_label, "geojson")
        self.assertEqual(result, {'type': 'FeatureCollection', 'features': [{'geometry': {'type': 'Point', 'coordinates': [66.0866902219283, 33.8563992816908]}, 'type': 'Feature', 'properties': {'prop0': 'AF', 'prop1': 'Afghanistan'}}]})


def run_test():
    suite = unittest.TestLoader().loadTestsFromTestCase(GeobricksTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    run_test()



