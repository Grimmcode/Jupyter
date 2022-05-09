from osgeo import ogr, osr
import os

spatialRef = osr.SpatialReference()
spatialRef.ImportFromEPSG(25830) #ETRS89 UTM30N 


# Create test polygon
ring = ogr.Geometry(ogr.wkbLinearRing)
ring.AddPoint(1179091.1646903288, 712782.8838459781)
ring.AddPoint(1161053.0218226474, 667456.2684348812)
ring.AddPoint(1214704.933941905, 641092.8288590391)
ring.AddPoint(1228580.428455506, 682719.3123998424)
ring.AddPoint(1218405.0658121984, 721108.1805541387)
ring.AddPoint(1179091.1646903288, 712782.8838459781)
poly = ogr.Geometry(ogr.wkbPolygon)
poly.AddGeometry(ring)

# Create the output Driver
outDriver = ogr.GetDriverByName('GeoJSON')

if os.path.exists('test.geojson'):
    outDriver.DeleteDataSource('test.geojson')
        
# Create the output GeoJSON
outDataSource = outDriver.CreateDataSource('test.geojson')
outLayer = outDataSource.CreateLayer('test.geojson', spatialRef, geom_type=ogr.wkbPolygon )


# Add Feature Attribute

idField = ogr.FieldDefn("Area", ogr.OFTReal)
outLayer.CreateField(idField)
idField = ogr.FieldDefn("Perimetro", ogr.OFTReal)
outLayer.CreateField(idField)

# Get the output Layer's Feature Definition
featureDefn = outLayer.GetLayerDefn()

# create a new feature
outFeature = ogr.Feature(featureDefn)

# Set new geometry
outFeature.SetGeometry(poly)

# Set Attributes Values
outFeature.SetField("Area", poly.GetArea())
outFeature.SetField("Perimetro", poly.Length())


# Add new feature to output Layer
outLayer.CreateFeature(outFeature)

# dereference the feature
outFeature = None

# Save and close DataSources
outDataSource = None