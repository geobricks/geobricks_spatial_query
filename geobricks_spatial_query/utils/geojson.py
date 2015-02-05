import simplejson
from geobricks_spatial_query.utils.encode_postgis import _encode_geometry


def encode_geojson(rows):
    output = {}
    output["type"] = "FeatureCollection"
    output["features"] = []
    for v in rows:
        j = simplejson.loads(v[0])
        f = {}
        f["type"] = "Feature"
        f["geometry"] = {}
        f["geometry"]["type"] = j["type"]
        f["geometry"]["coordinates"] = _encode_geometry(j)
        f["properties"] = {}
        for p in range(1, len(v)):
            f["properties"]["prop" + str(p)] = v[p]
        output["features"].append(f)
    return output
