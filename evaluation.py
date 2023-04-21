import numpy as np
from pyproj import CRS,Transformer
import shapefile# 使用pyshp
from shapely.geometry import Polygon, Point,LineString
import matplotlib.pyplot as plt
import pandas as pd
# 标注数据 13
label_line = r'D:/backup/penghu/jibei/label/20220316_label.shp'
# icesat2等深线0m附近 15
icesat_dep = r'D:/backup/penghu/jibei/20220316/stumpf/S2_2020316_stumpf__1.shp'
# 哨兵2号ndwi水体边线 56
Sentinel2_ndwi = r'D:/backup/penghu/jibei/20220316/ndwi/20220316_m_001.shp'
# 高光谱250m潮汐时近海岸水体边线 4
ENMap_line = r'D:/backup/penghu/jibei/enmap/water_by_spectral_sub.shp'

re_correct_file = './data/s2_icesat/v1.shp'

def unit_find():
    import haversine
    print(tuple(haversine.Unit))  # 查看所有可用的单位

from haversine import haversine, Unit

def eva_example(a):
    a = [5, 6, 16, 9]

    # 一般的均值可以用 numpy 中的 mean
    np.mean(a)

    # numpy 中的 average 方法不仅能求得简单平均数，也可以求出加权平均数。average 里面可以跟一个 weights 参数，里面是一个权数的数组
    np.average(a)
    np.average(a, weights=[1, 2, 1, 1])

    np.std(a)  # 计算总体标准差
    4.301162633521313

    np.std(a, ddof=1)  # 计算样本标准差
    4.96655480858378


def distance(point1,point2):

    # 两点的经纬度
    # point1 = (39.995304, 116.308264)
    # point2 = (40.003304, 116.326759)
    result_km = haversine(point1, point2, unit=Unit.KILOMETERS)    # km
    result_m = haversine(point1, point2, unit=Unit.METERS)        # m

    # 打印计算结果
    # print("距离：{:.3f}km".format(result_km))
    # print("距离：{:.3f}m".format(result_m))

    return result_m

def convert_prj(lat,lon):
    crs = CRS.from_epsg(4326)
    crs = CRS.from_string("epsg:4326")
    crs = CRS.from_proj4("+proj=latlon")
    crs = CRS.from_user_input(4326)
    crs_cs = CRS.from_string("epsg:32650")
    #  "epsg:32650"
    transformer = Transformer.from_crs(crs_cs,crs)

    # lat = 40.0691643333333
    # lon = 116.242161333333
    lat_utm, lon_utm = transformer.transform(lat, lon)
    transformer.transform(lat, lon)
    return lat_utm, lon_utm

# 获取x，范围，随机取样本点，计算样本点到参考线距离，根据距离求平均和标准差
# 获取样本点，求距离
def get_all_points(re_correct_file,idx):
    re_distance = []
    cankao_file = shapefile.Reader(label_line)  # 读取
    cankao_shapes = cankao_file.shapes()
    cankao_pts = cankao_shapes[13].points
    cankao_line = LineString(cankao_pts)
    cankao_x, cankao_y = zip(*cankao_pts)  # 把经纬度分别给到x,y
    plt.plot(cankao_x, cankao_y)

    shp = shapefile.Reader(re_correct_file)  # 读取
    file_shapes = shp.shapes()

    label_pts = file_shapes[idx].points

    label_x, label_y = zip(*label_pts)  # 把经纬度分别给到x,y

    # plt.plot(label_x, label_y)
    line_shp = LineString(label_pts)

    # print(len(label_pts))
    x, y = zip(*label_pts)  # 把经纬度分别给到x,y
    max_x = np.array(x).max()
    min_x = np.array(x).min()

    max_y = np.array(y).max()
    min_y = np.array(y).min()

    line_points = []
    x = np.arange(min_x, max_x, 1)
    for px in x:
        new_line = LineString([[px,min_y-100],[px,max_y + 100]])
        mp = new_line.intersection(line_shp)
        if mp.is_empty:
            pass
        elif mp.geom_type == 'Point':
            d = get_p2p_distance(cankao_line, mp)
            re_distance.append(d)
            pass
        elif mp.geom_type == 'MultiPoint':
            multi_p = mp.geoms
            for point in multi_p:
                d = get_p2p_distance(cankao_line, point)
                re_distance.append(d)
                # line_points.append([point.x, point.y])
                # plt.plot(point.x, point.y, marker='.', color='coral')
        elif mp.geom_type == 'LineString':
            px, py = mp.xy

            for i in range(len(px)):
                d = get_p2p_distance(cankao_line, Point([px[i], py[i]]))
                re_distance.append(d)
                # line_points.append([px[i], py[i]])
        else:
            multi_p = mp.geoms
            for point in multi_p:
                if point.geom_type == 'Point':
                    d = get_p2p_distance(cankao_line, point)
                    re_distance.append(d)
                    # line_points.append([point.x, point.y])
                    # plt.plot(point.x, point.y, marker='.', color='coral')
                elif point.geom_type == 'LineString':
                    px,py = point.xy

                    for i in range(len(px)):
                        d = get_p2p_distance(cankao_line, Point([px[i], py[i]]))
                        re_distance.append(d)
                        # line_points.append([px[i],py[i]])

                        # plt.plot(px[i],py[i], marker='.', color='coral')

                    # plt.plot(point.x, point.y, marker='.', color='coral')
                else:
                    print('line')

    # x_sample = np.random.choice(x, 100, replace=False)
    print(len(line_points))

    # plt.show()
    return re_distance


def get_p2p_distance(cankao_line,point):

    d = cankao_line.project(point)
    p = cankao_line.interpolate(d)
    closest_point_coords = list(p.coords)[0]
    prj_lat, prj_lon = convert_prj(closest_point_coords[0], closest_point_coords[1])
    lat, lon = convert_prj(point.x, point.y)
    d = distance(tuple([lat, lon]),tuple([prj_lat, prj_lon]))
    return d

def calculate_distance_by_sample():
    re_correct_file = './data/s2_icesat/v1.shp'
    re_points = get_all_points(re_correct_file, 0)
    icesat_points = get_all_points(icesat_dep, 15)
    sentinel2_points = get_all_points(Sentinel2_ndwi, 56)
    mean_re = np.array(re_points).mean()
    mean_icesat = np.array(icesat_points).mean()
    mean_sentinel2 = np.array(sentinel2_points).mean()

    df_re = pd.DataFrame(re_points)
    df_re.to_csv('./data/recorrect_distance.csv')

    # df_icesat = pd.DataFrame(icesat_points)
    # df_icesat.to_csv('./data/icesat_distance.csv')

    # df_sentinel = pd.DataFrame(sentinel2_points)
    # df_sentinel.to_csv('./data/sentinel_distance.csv')

    # data = np.random.choice(50, 10, replace=False)
    print(mean_re, mean_icesat, mean_sentinel2)

def load_distance():
    data = pd.read_csv('./data/recorrect_distance.csv',index_col=0, header=0)
    re_points = data.values
    mean_re = np.array(re_points).mean()

    data = pd.read_csv('./data/icesat_distance.csv', index_col=0, header=0)
    icesat_points = data.values
    mean_icesat = np.array(icesat_points).mean()

    data = pd.read_csv('./data/sentinel_distance.csv', index_col=0, header=0)
    sentinel2_points = data.values
    mean_sentinel2 = np.array(sentinel2_points).mean()

    print(mean_re,mean_icesat,mean_sentinel2)

if __name__ == '__main__':
    # calculate_distance_by_sample()
    load_distance()
#     5.723330654868764 6.48423253938779 12.335843370808915
