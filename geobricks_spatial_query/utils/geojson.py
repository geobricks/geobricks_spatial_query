import simplejson
from geobricks_spatial_query.utils.encode_postgis import _encode_geometry

# TODO: rename to GeoJSON
def encode_geojson(rows, encode_geometry=True):
    # print rows
    output = {}
    output["type"] = "FeatureCollection"
    output["features"] = []
    for v in rows:
        j = simplejson.loads(v[0])
        f = {}
        f["type"] = "Feature"
        f["geometry"] = {}
        f["geometry"]["type"] = j["type"]
        if encode_geometry:
            f["geometry"]["coordinates"] = _encode_geometry(j)
        f["properties"] = {}
        for p in range(1, len(v)):
            f["properties"]["prop" + str(p-1)] = v[p]
        output["features"].append(f)
    return output
