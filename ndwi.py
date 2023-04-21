#coding:utf-8
import cv2
from matplotlib import pyplot as plt
from osgeo import gdal_array  # 导入读取遥感影像的库
from tif_read_write import *


def NDWI(img, threshold=0.01):
    """
    该函数采用最简单的NDWI进行水体的提取。
    需要输入的参数为加载好的影像img和阈值threshold
    返回为提取好的水体掩模
    """
    # NDWI用到了Landsat 8 OLI的第3和第6波段，先找到这两个波段
    green = img[2].astype(float)
    nir = img[5].astype(float)

    # 计算NDWI并创建掩模
    ndwi = (green - nir) / (green + nir)

    # 根据阈值来确定掩模的值
    for row in range(ndwi.shape[0]):
        for col in range(ndwi.shape[1]):
            if ndwi[row, col] >= threshold:
                # ndwi_mask[row, col] = 1
                ndwi[row, col] = 255
            else:
                ndwi[row, col] = 0

    # 最后对图像进行开运算进行去噪，即先腐蚀后膨胀
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(ndwi, cv2.MORPH_OPEN, kernel)
    return ndwi

def get_result(tif_input,tif_output,shp_file,img_output):
    data = gdal_array.LoadFile(tif_input)
    proj, geotrans, im_data, row, column = read_img(tif_input)
    image = data[[6, 4, 2], :, :]
    image2 = im_data[[6, 4, 2], :, :].astype(int)
    image_rgb = image.transpose((1, 2, 0))
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)
    extracted_img = NDWI(data)
    plt.imshow(extracted_img, "gray")
    plt.show()
    cv2.imwrite(img_output, extracted_img)

    write_img(tif_output, proj, geotrans, extracted_img)  # 写数据

    raster2shp(tif_output, shp_file)


if __name__ == '__main__':
    tif_input = 'D:/backup/penghu/jibei/20220316/S2_jibei.tif'
    tif_output = './mndwi/20220316_raw_36.tif'
    shp_file = 'data/mndwi/20220316_raw_36.shp'
    img_output = './mndwi/20220316_raw_36.jpg'
    get_result(tif_input,tif_output,shp_file,img_output)