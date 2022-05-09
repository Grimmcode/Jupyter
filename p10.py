from osgeo import ogr, osr
import os
shapefile = "states.shp"
driver = ogr.GetDriverByName("ESRI Shapefile")
dataSource = driver.Open(shapefile, 0)
dataDestination = driver.CreateDataSource("states-centroid.shp")
# create the spatial reference, WGS84
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)
# create the layer
layerOut = dataDestination.CreateLayer("centroides", srs, ogr.wkbPoint)
# Add the fields we're interested in
field_name = ogr.FieldDefn("STATE_NAME", ogr.OFTString)
field_name.SetWidth(24)
layerOut.CreateField(field_name)
# open layer input to iterate
layerIn = dataSource.GetLayer()

for featureIn in layerIn:
    featureOut = ogr.Feature(layerOut.GetLayerDefn())
    featureOut.SetField("STATE_NAME", featureIn.GetField("STATE_NAME"))
    featureOut.SetGeometry(featureIn.GetGeometryRef().Centroid())
    layerOut.CreateFeature(featureOut)
    # Dereference the feature
    featureOut = None
    print (featureIn.GetField("STATE_NAME"))
    
layerIn.ResetReading()
# Save and close the data source
dataDestination = None