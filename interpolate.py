from osgeo import gdal, ogr, osr

gdal.UseExceptions()

pixel_size = 0.0025
# Filename of input OGR file
vector_fn = 'itacyl_estaciones.shp'

# Filename of the raster Tiff that will be created
raster_fn = 'estaciones_interpolation.tif'

# Open the data source and read in the extent
source_ds = ogr.Open(vector_fn)
source_layer = source_ds.GetLayer()
x_min, x_max, y_min, y_max = source_layer.GetExtent()

# Create the destination data source
ancho = int((x_max - x_min) / pixel_size)
alto = int((y_max - y_min) / pixel_size)
    
# Rasterize
#rasterDs = gdal.Grid(raster_fn, vector_fn, format='GTiff', algorithm='invdist', zfield='Altitud', width= ancho, height= alto)
rasterDs = gdal.Grid(raster_fn, vector_fn, format='GTiff', algorithm='linear:radius=0.2:nodata=-9999', zfield='Altitud', width= ancho, height= alto)
rasterDs.FlushCache()