from osgeo import ogr

wkt = "POINT (1120351.5712494177 741921.4223245403 545)"
point = ogr.CreateGeometryFromWkt(wkt)
print ("%d,%d,%d" % (point.GetX(), point.GetY(), point.GetZ()))