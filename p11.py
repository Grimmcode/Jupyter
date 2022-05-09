from osgeo import gdal
gtif = gdal.Open( "wellington_west.tif" )
print (gtif.GetMetadata())