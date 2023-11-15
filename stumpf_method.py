import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
from sklearn.metrics import mean_squared_error , r2_score
from sklearn.model_selection import train_test_split
import matplotlib
import matplotlib.pyplot as plt
import math


def ChooseBands_Prisma_Hawaii(file_location1):
    # file_location1 = r'D:/backup/penghu/jibei/icesat/icesat_sample_for_dep_20230306.csv'
    bands_data = pd.read_csv(file_location1, dtype=float)
    count = len(open(file_location1).readlines())
    n = 0.01
    R2_max = 0
    for i in range(4): #波段数
        Band1 = np.array(bands_data.iloc[:,4+i])  #csv文件按序号、X、Y、Z、波段顺序，所以从4+i
        for j in range(4):
            if i is not j:
                Band2=np.array(bands_data.iloc[:,4+j])
                Ratio = np.array(np.log(n * Band1) / np.log(n * Band2))
                Ratio = Ratio.reshape(count - 1, 1)
                X = Ratio
                y = np.array(bands_data[['Z']])
                X_train, X_test, y_train, y_test = train_test_split(X,y , test_size=0.2, random_state=100)
                LR = LinearRegression()
                LR.fit(X_train, y_train)
                R2 = r2_score(y_test, LR.predict(X_test))
                if R2 > R2_max:
                    R2_max = R2
                    band1 = i
                    band2 = j
                    k = LR.coef_
                    b = LR.intercept_
                    reg=LR
                    print('RMSE: %.10f' % math.sqrt(mean_squared_error(y_test, reg.predict(X_test))))
                    print(Band1)
                    print(Band2)
    print(band1 + 3, band2 + 3, R2_max, k, b, n)  #所有+4同上，其他影像修改数字
    Band_1 = pd.Series(bands_data.iloc[:,band1+3])
    Band_2 = pd.Series(bands_data.iloc[:,band2+3])
    Ratio2 = np.array(np.log(n * Band_1) / np.log(n * Band_2))
    X = Ratio2.reshape(count-1,1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)

    plt.scatter(X_train, y_train, color='orange',label='train')
    plt.scatter(X_test, y_test, color='blue',label='test')
    plt.plot(X, reg.predict(X), 'r-',label='Predict')
    plt.legend()
    plt.xlabel('Ration')
    plt.ylabel('Z')

    f, ax = plt.subplots(1, 1, sharex=True, figsize=(6, 5))
    ax.set_xlim([-30, 5])
    ax.set_ylim([-30, 5])
    Axis_line = np.linspace(*ax.get_xlim(), 2)
    ax.plot(Axis_line, Axis_line, transform=ax.transAxes, linestyle='--', linewidth=2, color='black')  # 1:1标准线
    ax.scatter(y_train, reg.predict(X_train), color="orange", label="Train")
    ax.scatter(y_test, reg.predict(X_test), color="blue", label="Test")
    ypre = reg.predict(X_test)
    print(' ')

    # plt.legend(loc='upper right')
    # plt.xticks(fontsize=8, fontweight='normal')
    # plt.yticks(fontsize=8, fontweight='normal')
    # plt.title('Predictions for Stumpf')
    # plt.xlabel('True depth', fontsize=10)
    # plt.ylabel('Predicted depth', fontsize=10)
    # plt.show()
    # filename = '../data/' + '20220910_train.txt'
    # np.savetxt(filename, np.column_stack([reg.predict(X_train), y_train]))
    # filename = '../data/' + '20220910_test.txt'
    # np.savetxt(filename, np.column_stack([reg.predict(X_test), y_test]))
    return band1+4, band2+4, k, b, n


def ChooseBands_S2(file_location1):
    n = 10
    bands_data = pd.read_csv(file_location1,header=0, dtype=float)
    count = len(open(file_location1).readlines())
    Band1 = np.array(bands_data.iloc[:, 6])
    Band2 = np.array(bands_data.iloc[:, 5])
    Ratio = np.array(np.log(n * Band1) / np.log(n * Band2))
    Ratio = Ratio.reshape(count - 1, 1)
    X = Ratio
    y = np.array(bands_data[['dep']])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)
    LR = LinearRegression()
    LR.fit(X_train, y_train)
    k = LR.coef_
    b = LR.intercept_
    reg = LR
    pre = LR.predict(X_test)
    R2 = r2_score(y_test, LR.predict(X_test))
    print('RMSE: %.10f' % math.sqrt(mean_squared_error(y_test, reg.predict(X_test))))
    print(R2)
    plt.scatter(X_train, y_train, color='orange',label='train')
    plt.scatter(X_test, y_test, color='blue',label='test')
    plt.plot(X, reg.predict(X), 'r-',label='Predict')
    plt.legend()
    plt.xlabel('Ration')
    plt.ylabel('Z')

    f, ax = plt.subplots(1, 1, sharex=True, figsize=(6, 5))
    ax.set_xlim([-30, 5])
    ax.set_ylim([-30, 5])
    Axis_line = np.linspace(*ax.get_xlim(), 2)
    ax.plot(Axis_line, Axis_line, transform=ax.transAxes, linestyle='--', linewidth=2, color='black')  # 1:1标准线
    ax.scatter(y_train, reg.predict(X_train), color="orange", label="Train")
    ax.scatter(y_test, reg.predict(X_test), color="blue", label="Test")
    plt.legend(loc='upper right')
    plt.xticks(fontsize=8, fontweight='normal')
    plt.yticks(fontsize=8, fontweight='normal')
    plt.title('Predictions for Stumpf')
    plt.xlabel('True depth', fontsize=10)
    plt.ylabel('Predicted depth', fontsize=10)
    plt.show()
    # filename = 'D:/Desktop/Stumpf/results/Hawaii_PRI_2m1000_train.txt'
    # np.savetxt(filename, np.column_stack([reg.predict(X_train), y_train]))
    # filename = 'D:/Desktop/Stumpf/results/Hawaii_PRI_2m1000_test.txt'
    # np.savetxt(filename, np.column_stack([reg.predict(X_test), y_test]))
    return  k, b, n


def Predict(file_location,k,b,n,dep_file):

    bands_data = pd.read_csv(file_location,header=0, dtype=float)
    count = len(open(file_location).readlines())
    R1 = np.array(bands_data.iloc[:,6])
    R2 = np.array(bands_data.iloc[:,5])
    Z_predict = np.array(k*((np.log(n*R1))/(np.log(n*R2)))+b)
    Z_predict = Z_predict.reshape(count - 1, 1)
    Local_X = bands_data.values[:,1]
    Local_Y = bands_data.values[:,2]
    name = ['X', 'Y', 'Z_predict']
    output = pd.DataFrame()
    output.loc[:, 'X'] = Local_X
    output.loc[:, 'Y'] = Local_Y
    output.loc[:, 'Z_predict'] = Z_predict
    output.to_csv(dep_file)

if __name__ == '__main__':
    # 3
    file_location1 = r'D:/backup/cm/20230128_sample.csv'
    # file_location1 = r'D:/backup/penghu/jibei/icesat/icesat_sample_for_dep_20211111.csv'
    # file_location1 = r'D:/backup/penghu/jibei/sentinel2/20220316/stumpf/S2_2020316_sample.csv'
    # m1, m0, n = ChooseBands_S2(file_location1)
    file_s2_points = r'D:/backup/cm/20230128_points.csv'
    def_file = r'D:/backup/cm/20230128_Stumpf.csv'
    Predict(file_s2_points, 28.96322057, -31.54552856, 0.01,def_file)
    # ChooseBands_Prisma_Hawaii(file_location1)


# 3 4 0.48239212721311986 [[188.68141948]] [-185.27759039] 10 RMSE: 0.9090736136