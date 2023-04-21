#coding:utf-8
import cv2
from matplotlib import pyplot as plt
from osgeo import gdal_array  # 导入读取遥感影像的库

from tif_read_write import *

choose_band = [6,4,2]

def test():
    image = cv2.imread("data/test/Lena2.bmp")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    plt.subplot(131), plt.imshow(image, "gray")
    plt.title("source image"), plt.xticks([]), plt.yticks([])

    plt.subplot(132), plt.hist(image.ravel(), 256)
    plt.title("Histogram"), plt.xticks([]), plt.yticks([])

    ret1, th1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)  #方法选择为THRESH_OTSU
    plt.subplot(133), plt.imshow(th1, "gray")
    plt.title("OTSU,threshold is " + str(ret1)), plt.xticks([]), plt.yticks([])
    plt.show()

def multi_bands(tif_input,tif_output,shp_file,img_output):

    data = gdal_array.LoadFile(tif_input)
    proj, geotrans, im_data, row, column = read_img(tif_input)
    image = data[[2,1,0],:,:]

    image_rgb = image.transpose((1,2,0))
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)

    plt.subplot(131), plt.imshow(image_rgb, "gray")
    plt.title("source image"), plt.xticks([]), plt.yticks([])

    plt.subplot(132), plt.hist(image_rgb.ravel(),256)
    plt.title("Histogram"), plt.xticks([]), plt.yticks([])


    #
    ret1, th1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)  #方法选择为THRESH_OTSU
    plt.subplot(133), plt.imshow(th1, "gray")
    plt.title("OTSU,threshold is " + str(ret1)), plt.xticks([]), plt.yticks([])

    cv2.imwrite(img_output, th1)

    write_img(tif_output, proj, geotrans, th1)  # 写数据

    raster2shp(tif_output, shp_file)

    plt.show()

def array_convert():
    a = np.arange(30).reshape(2, 3, 5)
    print(a)
    b = a.transpose((1,2,0))
    print(b)



if __name__ == '__main__':
    # test()
    # array_convert()
    tif_input = 'D:/backup/penghu/jibei/20220316/S2_jibei.tif'
    tif_output = './data/otsu/S2_otsu_432.tif'
    shp_file = './data/otsu/S2_otsu_432.shp'
    img_output = './data/otsu/S2_otsu_432.jpg'

    multi_bands(tif_input,tif_output,shp_file,img_output)

