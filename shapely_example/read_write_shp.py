# -*- coding: utf-8 -*-

import shapefile# 使用pyshp
import matplotlib.pyplot as plt
import numpy as np
from osgeo import osr
# 标注数据 13
label_line = r'D:/backup/penghu/jibei/label/20220316_label.shp'
# icesat2等深线0m附近 15
icesat_dep = r'D:/backup/penghu/jibei/20220316/stumpf/S2_2020316_stumpf__1.shp'
# 哨兵2号ndwi水体边线 56
Sentinel2_ndwi = r'D:/backup/penghu/jibei/20220316/ndwi/20220316_m_001.shp'
# 高光谱250m潮汐时近海岸水体边线 4
ENMap_line = r'D:/backup/penghu/jibei/enmap/water_by_spectral_sub.shp'

# file = shapefile.Reader(label_line)#读取
#读取元数据
# print(str(file.shapeType))  # 输出shp类型
# print(file.encoding)# 输出shp文件编码
# print(file.bbox)  # 输出shp的文件范围（外包矩形）
# print(file.numRecords)  # 输出shp文件的要素数据
# print(file.fields)# 输出所有字段信息
# # print(file.records())  # 输出所有属性表

def compare_as_img():
    label = shapefile.Reader(label_line)  # 读取
    Sentinel2 = shapefile.Reader(Sentinel2_ndwi)  # 读取

    label_shapes = label.shapes()
    label_pts = label_shapes[13].points
    label_x,label_y = zip(*label_pts)#把经纬度分别给到x,y
    plt.plot(label_x, label_y, '-', lw=1, color='k')

    Sentinel2_shapes = Sentinel2.shapes()
    Sentinel2_pts = Sentinel2_shapes[56].points
    Sentinel2_x,Sentinel2_y = zip(*Sentinel2_pts)#把经纬度分别给到x,y
    plt.plot(Sentinel2_x, Sentinel2_y, '-', lw=1, color='r')

    # plt.show()

def find_ind():
    file = shapefile.Reader(icesat_dep)  # 读取
    shapes = file.shapes()
    i = 0
    for i in range(shapes.__len__()):
        data = shapes[i].points
        len = data.__len__()
        print(i,len)


def get_line_points():
    label = shapefile.Reader(label_line)  # 读取
    Sentinel2 = shapefile.Reader(Sentinel2_ndwi)  # 读取
    icesat = shapefile.Reader(icesat_dep)  # 读取

    label_shapes = label.shapes()
    label_pts = label_shapes[13].points
    # print(label_pts.__len__())
    label_x, label_y = zip(*label_pts)  # 把经纬度分别给到x,y


    Sentinel2_shapes = Sentinel2.shapes()
    Sentinel2_pts = Sentinel2_shapes[56].points
    Sentinel2_x, Sentinel2_y = zip(*Sentinel2_pts)  # 把经纬度分别给到x,y
    # print(Sentinel2_pts.__len__())

    icesat_shapes = icesat.shapes()
    icesat_pts = icesat_shapes[15].points
    icesat_x, icesat_y = zip(*icesat_pts)  # 把经纬度分别给到x,y
    # plt.plot(icesat_x, icesat_y, '-', lw=1, color='r')
    # print(icesat_pts.__len__())

    # plt.show()
    return label_pts,Sentinel2_pts,icesat_pts

# def get_points(shp_file):
#     shp = shapefile.Reader(shp_file)  # 读取

def writer_shp(data_array):

    file = shapefile.Writer("./data/remedy_line.shp")  # 新建数据存放位置
    # 创建两个字段
    file.field('FIRST_FLD')
    file.field('SECOND_FLD', 'C', '2000')  # 'SECOND_FLD'为字段名称，C代表数据类型为字符串，长度为40

    file.line(list(data_array))
    file.record('First', 'polyline')

    # 写入数据
    file.close()

def read_shp(shp_file):
    file = shapefile.Reader(shp_file)  # 读取
    print(file.fields)# 输出所有字段信息
    print(file.record(0)[0])#第一个对象的第一个属性值
    icesat_shapes = file.shapes()
    icesat_pts = icesat_shapes[15].points
    data = np.array(icesat_pts)
    icesat_x, icesat_y = zip(*icesat_pts)  # 把经纬度分别给到x,y
    data_address = "./data/point2.shp"
    write_shp(data_address,data)

def write_shp(data_address,polygn):

    file = shapefile.Writer(data_address)
    # 创建两个字段
    file.field('FIRST_FLD') # file.field('FIRST_FLD', 'N',0 '31') # 数值类型 file.field('type', 'C', '40') # 'SECOND_FLD'为字段名称，C代表数据类型为字符串，长度为4
    # 要素1
    file.line([polygn])
    file.record('First', 'Line')

    file.close()
    # 定义投影
    proj = osr.SpatialReference()
    proj.ImportFromEPSG(32650) # 4326-GCS_WGS_1984; 32650	WGS_1984_UTM_Zone_50N
    wkt = proj.ExportToWkt()
    # 写入投影
    f = open(data_address.replace(".shp", ".prj"), 'w')
    f.write(wkt)#写入投影信息
    f.close()#关闭操作流

if __name__ == '__main__':
    # find_ind()
    shp_file = '../data/icesat_shp/S2_2020316_stumpf__1.shp'
    read_shp(shp_file)
