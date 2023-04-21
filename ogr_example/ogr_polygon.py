from osgeo import ogr
import os,math
driver = ogr.GetDriverByName("ESRI Shapefile")
extfile = 'rect_demo.shp'
if os.access( extfile, os.F_OK ):
 driver.DeleteDataSource( extfile )
extent = [400, 1100, 300, 600]
newds = driver.CreateDataSource(extfile)
layernew = newds.CreateLayer('rect',None,ogr.wkbPolygon)
width = math.fabs(extent[1]-extent[0])
height = math.fabs(extent[3]-extent[2])
tw = width/2
th = width/2
extnew = extent[0]+tw
wkt = 'POLYGON ((%f %f,%f %f,%f %f,%f %f,%f %f))' % (extent[0],extent[3],
    extent[1],extent[3], extent[1],extent[2],
    extent[0],extent[2], extent[0],extent[3])
geom = ogr.CreateGeometryFromWkt(wkt)
feat = ogr.Feature(layernew.GetLayerDefn())
feat.SetGeometry(geom)
layernew.CreateFeature(feat)
newds.Destroy()
