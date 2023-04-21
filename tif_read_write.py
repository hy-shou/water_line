from osgeo import gdal
import numpy as np
from osgeo import ogr, osr  # 导入处理shp文件的库
# 读图像文件
def read_img(filename):
    dataset = gdal.Open(filename)  # 打开文件
    im_width = dataset.RasterXSize  # 栅格矩阵的列数
    im_height = dataset.RasterYSize  # 栅格矩阵的行数
    im_geotrans = dataset.GetGeoTransform()  # 仿射矩阵
    im_proj = dataset.GetProjection()  # 地图投影信息
    im_data = dataset.ReadAsArray(0, 0, im_width, im_height).astype(np.float)  # 将数据写成数组，对应栅格矩阵
    del dataset  # 关闭对象，文件dataset
    return im_proj, im_geotrans, im_data, im_height, im_width

def write_img(filename, im_proj, im_geotrans, im_data):
    # gdal数据类型包括
    # gdal.GDT_Byte,
    # gdal .GDT_UInt16, gdal.GDT_Int16, gdal.GDT_UInt32, gdal.GDT_Int32,
    # gdal.GDT_Float32, gdal.GDT_Float64

    # 判断栅格数据的数据类型
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32

    # 判读数组维数
    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    else:
        im_bands, (im_height, im_width) = 1, im_data.shape

    # 创建文件
    driver = gdal.GetDriverByName("GTiff")  # 数据类型必须有，因为要计算需要多大内存空间
    dataset = driver.Create(filename, im_width, im_height, im_bands, datatype)

    dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
    dataset.SetProjection(im_proj)  # 写入投影

    if im_bands == 1:
        dataset.GetRasterBand(1).WriteArray(im_data)  # 写入数组数据
    else:
        for i in range(im_bands):
            dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
    del dataset

def raster2shp(tif_img,shp_file):
    """
    函数输入的是一个二值影像，利用这个二值影像，创建shp文件
    """
    # src = "extracted_img.tif"
    # 输出的shapefile文件名称
    tgt = shp_file
    # 图层名称
    tgtLayer = "extract"
    # 打开输入的栅格文件
    srcDS = gdal.Open(tif_img)
    # 获取第一个波段
    band = srcDS.GetRasterBand(1)
    # 让gdal库使用该波段作为遮罩层
    mask = band
    # 创建输出的shapefile文件
    driver = ogr.GetDriverByName("ESRI Shapefile")
    shp = driver.CreateDataSource(tgt)
    # 拷贝空间索引
    srs = osr.SpatialReference()
    srs.ImportFromWkt(srcDS.GetProjectionRef())
    layer = shp.CreateLayer(tgtLayer, srs=srs)
    # 创建dbf文件
    fd = ogr.FieldDefn("DN", ogr.OFTInteger)
    layer.CreateField(fd)
    dst_field = 0
    # 从图片中自动提取特征
    extract = gdal.Polygonize(band, mask, layer, dst_field, [], None)


if __name__=='__main__':
    proj, geotrans, im_data, row, column = read_img('输入数据')  # 读数据
    write_img(r'输出地址', proj, geotrans, '输出影像名称')#写数据
