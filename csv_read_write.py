import pandas as pd
import numpy as np

file_name = './data/svm/train.csv'
def read():

    df = pd.read_csv(file_name,comment=';',header=None)
    # 4335 3300
    X = df.values[:,6:]

    y_w = list(np.ones([4335], dtype=int))
    y_l = list(np.zeros([3300], dtype=int))
    Y = np.array(y_w+y_l)
    return X,Y


    print(df)

if __name__ == '__main__':
    file_name = './data/svm/train.csv'
    read(file_name)