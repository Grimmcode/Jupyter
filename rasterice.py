from osgeo import gdal, ogr, osr

gdal.UseExceptions()

# Define pixel_size and NoData value of new raster
pixel_size = 0.0025
NoData_value = -9999

# Filename of input OGR file
vector_fn = 'itacyl_estaciones.shp'

# Filename of the raster Tiff that will be created
raster_fn = 'itacyl_estaciones.tif'

# Open the data source and read in the extent
source_ds = ogr.Open(vector_fn)
source_layer = source_ds.GetLayer()
x_min, x_max, y_min, y_max = source_layer.GetExtent()

# Create the destination data source
x_res = int((x_max - x_min) / pixel_size)
y_res = int((y_max - y_min) / pixel_size)
target_ds = gdal.GetDriverByName('GTiff').Create(raster_fn, x_res, y_res, 1, gdal.GDT_Byte)
target_ds.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))
band = target_ds.GetRasterBand(1)
band.SetNoDataValue(NoData_value)

outRasterSRS = osr.SpatialReference()
outRasterSRS.ImportFromEPSG(4258)
target_ds.SetProjection(outRasterSRS.ExportToWkt())
    
# Rasterize
gdal.RasterizeLayer(target_ds, [1], source_layer, burn_values=[1])