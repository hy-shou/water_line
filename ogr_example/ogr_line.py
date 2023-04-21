import os,math
from osgeo import ogr
from ospybook.vectorplotter import VectorPlotter

def m1():
    driver = ogr.GetDriverByName("ESRI Shapefile")
    extfile = 'line_demo.shp'
    point_coors = [300,450, 750, 700, 1200, 450, 750, 200]
    print(point_coors)
    driver = ogr.GetDriverByName("ESRI Shapefile")
    if os.access( extfile, os.F_OK ):
        driver.DeleteDataSource( extfile )
    newds  = driver.CreateDataSource(extfile)
    layernew = newds.CreateLayer('point',None,ogr.wkbLineString)
    wkt = 'LINESTRING (%f %f,%f %f,%f %f,%f %f,%f %f)' % (point_coors[0],point_coors[1],
        point_coors[2],point_coors[3], point_coors[4],point_coors[5],
        point_coors[6],point_coors[7], point_coors[0],point_coors[1])
    print(wkt)
    geom = ogr.CreateGeometryFromWkt(wkt)
    feat = ogr.Feature(layernew.GetLayerDefn())
    feat.SetGeometry(geom)
    layernew.CreateFeature(feat)
    newds.Destroy()
# 创建一个空的几何对象，并添加顶点
# 注意必须按顺序添加顶点

def create_line():

    # 创建2D线
    # 由西到东添加顶点 : 54-62-70.5-75
    sidewalk = ogr.Geometry(ogr.wkbLineString)
    sidewalk.AddPoint(54, 37)
    sidewalk.AddPoint(62, 35.5)
    sidewalk.AddPoint(70.5, 38)
    sidewalk.AddPoint(75, 41.5)

    # 绘制几何类型图像
    vp = VectorPlotter(True)
    vp.plot(sidewalk, 'b-')
    vp.draw()
    print(sidewalk)
    # 结果：LINESTRING (54 37 0,62.0 35.5 0,70.5 38.0 0,75.0 41.5 0)
    # 顶点坐标之间用空格分开，顶点之间用逗号隔开


    # 用SetPoint（）改变最后一个点的坐标
    # 索引为3的顶点
    sidewalk.SetPoint(3, 76, 41.5)
    vp.plot(sidewalk, 'k--', 'tmp')
    vp.draw()
    print(sidewalk)
    # 结果：LINESTRING (54 37 0,62.0 35.5 0,70.5 38.0 0,76.0 41.5 0)


    # 将线条向北微调
    # 遍历所有顶点，Y坐标加1
    for i in range(sidewalk.GetPointCount()):
        sidewalk.SetPoint(i, sidewalk.GetX(i), sidewalk.GetY(i) + 1)
    vp.plot(sidewalk, 'r--')
    vp.draw()
    print(sidewalk)
    # 结果：LINESTRING (54 38 0,62.0 36.5 0,70.5 39.0 0,76.0 42.5 0)

if __name__ == '__main__':
    create_line()