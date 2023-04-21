import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from csv_read_write import *
from sklearn.model_selection import train_test_split
import sklearn.svm as svm
from tif_read_write import *
from osgeo import gdal_array  # 导入读取遥感影像的库

def get_para():
    X,y = read()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    svc = SVC()
    parameters = {
        'C': np.linspace(0.1, 20, 50),
        'gamma': np.linspace(0.1, 20, 20),
        'kernel': ['linear', 'rbf', 'sigmoid', 'poly']
    }
    grid = GridSearchCV(svc, parameters, cv=5, n_jobs=8)

    grid.fit(X_train, y_train)
    print("The best parameters are %s with a score of %0.2f"
          % (grid.best_params_, grid.best_score_))

# The best parameters are {'C': 0.1, 'gamma': 0.1, 'kernel': 'linear'} with a score of 1.00
def method(tif_input,tif_output,shp_file,img_output):
    # 建立模型
    model = svm.SVC(C=10, gamma=0.1, kernel='linear')
    X, y = read()
    # 训练模型,x为训练集， y为标签
    model.fit(X, y)

    # 预测,test为测试集

    data = gdal_array.LoadFile(tif_input)
    proj, geotrans, im_data, row, column = read_img(tif_input)
    image = data[:, :, :]
    # image2 = im_data[[6, 4, 2], :, :].astype(int)
    result = np.zeros([image.shape[1],image.shape[2]])
    imag_hv = image.transpose((1, 2, 0))
    for i in range(imag_hv.shape[0]):
        for j in range(imag_hv.shape[1]):
            v  = imag_hv[i,j,:]
            y = model.predict([v])
            result[i,j] = y[0]

    write_img(tif_output, proj, geotrans, result)  # 写数据

    raster2shp(tif_output, shp_file)



def get_img_data(tif_input):
    data = gdal_array.LoadFile(tif_input)
    proj, geotrans, im_data, row, column = read_img(tif_input)
    image = data[:, :, :]
    # image2 = im_data[[6, 4, 2], :, :].astype(int)
    image_rgb = image.transpose((1, 2, 0))

if __name__ == '__main__':
    # get_para()
    tif_input = 'D:/backup/penghu/jibei/20220316/S2_jibei.tif'
    # get_img_data(tif_input)
    tif_output = './data/svm/S2_svm_v4.tif'
    shp_file = './data/svm/S2_svm_v4.shp'
    img_output = './data/svm/S2_svm_v4.jpg'
    # method(tif_input,tif_output,shp_file,img_output)
    raster2shp(tif_output, shp_file)