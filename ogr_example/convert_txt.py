#!/usr/bin/env python3
#-*- coding:utf-8 -*-

try:
    from osgeo import ogr
except ImportError:
    import ogr
import os,sys
#切换路径
icesat_dep = r'D:/backup/penghu/jibei/20220316/stumpf/S2_2020316_stumpf__1.shp'
os.chdir(r'D:\backup\pythonProject\jibei_waterline\data')
#注册驱动，打开文件和图层
driver = ogr.GetDriverByName("ESRI Shapefile")
ds = ogr.Open('S2_2020316_stumpf__1.shp',0)#以只读方式打开矢量文件
if ds ==None:
    print("打开文件失败！")
    sys.exit(1)
layer = ds.GetLayer()
#为避免不能提前知道shp属性字段，这里读取属性表所有字段
featuredefn = layer.GetLayerDefn()#获取图层属性表定义
fieldcount = featuredefn.GetFieldCount()#获取属性表中字段数
for attr in range(fieldcount):
    fielddefn = featuredefn.GetFieldDefn(attr)
    print("%s:  %s"%(fielddefn.GetNameRef(), fielddefn.GetFieldTypeName(fielddefn.GetType())))
#layer = ds.GetLayerByIndex(0)
#打开TXT文件
outtxtfile = open('sites.txt','w')#以可写方式打开
#遍历所有要素，开始读取和写入
feature = layer.GetNextFeature()
while feature:
    #读取ID、cover字段值
    id = feature.GetFieldAsString('id')
    cover = feature.GetFieldAsString('cover')
    #获取要素几何
    geom = feature.GetGeometryRef()
    X = str(geom.GetX())#读取xy坐标,转为字符串，方便TXT写入
    Y = str(geom.GetY())
    #写入TXT文件
    outtxtfile.write(id +' ' + cover+' '+ X +' '+ Y +'\n')#这种写入方式如果第二次运行，会覆盖原TXT文件
    #清除缓存并获取下一个要素
    feature.Destroy()
    feature = layer.GetNextFeature()
#清除DataSource缓存并关闭TXT文件
ds.Destroy()
outtxtfile.close()
