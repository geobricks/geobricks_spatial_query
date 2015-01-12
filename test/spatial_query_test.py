import unittest
from geobricks_spatial_query.config.config import config
from geobricks_spatial_query.core.spatial_query_core import SpatialQuery


class GeobricksTest(unittest.TestCase):

    db = "spatial"
    layer_table = "gaul0_2015_4326"
    column_geom = "geom"
    column_code = "adm0_code"
    codes = ['1']


    def test_gaul0_2015_4326_in_4326(self):
        sq = SpatialQuery(config)
        result = sq.query_bbox(self.db, self.layer_table, self.column_code, self.codes, "4326")
        self.assertEqual(result, [[60.475829, 38.4906960000001], [74.8898620000001, 29.3772500000001]])

    def test_gaul0_2015_4326_in_3857(self):
        sq = SpatialQuery(config)
        result = sq.query_bbox(self.db, self.layer_table, self.column_code, self.codes, "3857")
        self.assertEqual(result, [[6732138.48958109, 4648978.50570379], [8336701.30341853, 3423749.69036421]])

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


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(GeobricksTest)
    unittest.TextTestRunner(verbosity=2).run(suite)



