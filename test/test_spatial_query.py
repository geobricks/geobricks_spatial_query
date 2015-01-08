import unittest
import os
from geobricks_spatial_query.config.config import config
from geobricks_spatial_query.core.spatial_query_core import SpatialQuery

class GeobricksTest(unittest.TestCase):

    db = "spatial"
    layer_table = "gaul0_3857"
    column_geom = "geom"
    column_code = "adm0_code"
    codes = ['1']

    def test_gaul0_3857_in_4326(self):
        sq = SpatialQuery(config)
        result = sq.query_bbox(self.db, self.layer_table, self.column_code, self.codes)
        self.assertEqual(result, [('{"type":"Polygon","coordinates":[[[60.478443145752,29.3774768667367],[60.478443145752,38.4834261112114],[74.8794311871666,38.4834261112114],[74.8794311871666,29.3774768667367],[60.478443145752,29.3774768667367]]]}',)])

    def test_gaul0_3857_in_3857(self):
        sq = SpatialQuery(config)
        result = sq.query_bbox(self.db, self.layer_table, self.column_code, self.codes, "3857")
        self.assertEqual(result, [('{"type":"Polygon","coordinates":[[[6732429.49495505,3423778.67185],[6732429.49495505,4647944.61027722],[8335540.15064535,4647944.61027722],[8335540.15064535,3423778.67185],[6732429.49495505,3423778.67185]]]}',)])

    def test_srid(self):
        sq = SpatialQuery(config)
        result = sq.query_srid(self.db, self.layer_table, self.column_geom)
        self.assertEqual(result, "3857")



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(GeobricksTest)
    unittest.TextTestRunner(verbosity=2).run(suite)