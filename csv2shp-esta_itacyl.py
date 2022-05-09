import pandas as pd
import os
from osgeo import gdal, ogr, osr

gdal.UseExceptions()

csv_path= 'UbicacionEstacionesITACyL 2009.csv'
outSHPfn = 'itacyl_estaciones.shp'
df = pd.read_csv(csv_path, sep=';')

shpDriver = ogr.GetDriverByName("ESRI Shapefile")
if os.path.exists(outSHPfn):
    shpDriver.DeleteDataSource(outSHPfn)
# El sistema de coordenadas de salida
srs_out = osr.SpatialReference()
srs_out.ImportFromEPSG(4258) # ETRS89
srs_out.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER) 
# Sistema de coordenadas de entrada
srs_in = osr.SpatialReference()
  
srs_in.ImportFromEPSG(23030) # ED50 UTM30N
transform = osr.CoordinateTransformation(srs_in, srs_out)

outDataSource = shpDriver.CreateDataSource(outSHPfn)
outLayer = outDataSource.CreateLayer(outSHPfn, srs_out, geom_type=ogr.wkbPoint)

# Añadimos los atributos que ha de tener el shp
field_sname = ogr.FieldDefn("Shorname", ogr.OFTString)
field_sname.SetWidth(5)
outLayer.CreateField(field_sname)
field_lname = ogr.FieldDefn("Name", ogr.OFTString)
field_lname.SetWidth(50)
outLayer.CreateField(field_lname)
outLayer.CreateField(ogr.FieldDefn("Altitud", ogr.OFTReal))
outLayer.CreateField(ogr.FieldDefn("IdProv", ogr.OFTInteger))
outLayer.CreateField(ogr.FieldDefn("IdEsta", ogr.OFTInteger))


for index, row in df.iterrows():
    print("IDESTACION: %s, %d, XUTM: %s YUTM: %s" % (row['SHORT NAME'],row['IDESTACION'], row['X  UTM30N ED50'], row['Y UTM30N ED50']))
    feature = ogr.Feature(outLayer.GetLayerDefn())
    # Set the attributes using the values from the delimited text file
    feature.SetField("Shorname", row['SHORT NAME'])
    feature.SetField("Name", row['NAME'])
    feature.SetField("Altitud", float(row['HEIGHT ASL (m)']))
    feature.SetField("IdProv", int(row['IDPROVINCIA']))
    feature.SetField("IdEsta", int(row['IDESTACION']))
    # create the WKT for the feature using Python string formatting
    wkt = "POINT(%f %f)" %  (float(row['Y UTM30N ED50']) , float(row['X  UTM30N ED50']))
    # Create the point from the Well Known Txt
    point = ogr.CreateGeometryFromWkt(wkt)
    # Transformamos las coordenadas de UTM ED50 a Geof ETRS89
    point.Transform(transform)
    # Set the feature geometry using the point
    feature.SetGeometry(point)
    # Create the feature in the layer (shapefile)
    outLayer.CreateFeature(feature)
    # Dereference the feature
    feature = None
    
outDataSource = None