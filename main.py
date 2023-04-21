# coding=utf-8
# This is a sample Python script.

from remedy_by_line import *
from shapely_example.read_write_shp import *

def optimize():
    # 读取获取边线
    # label_x, label_y,Sentinel2_x, Sentinel2_y,icesat_x, icesat_y
    label_pts,Sentinel2_pts,icesat_pts = get_line_points()
    label = np.array(label_pts)
    Sentinel = np.array(Sentinel2_pts)

    # 参考边线
    icesat = np.array(icesat_pts)
    # icesat_line = LineString(icesat)
    # plt.plot(*icesat_line.xy)
    # 添加交点
    Sentinel,icesat = get_line_seg_points(Sentinel, icesat)

    # icesat_line = LineString(icesat)
    # plt.plot(*icesat_line.xy)
    # Sentinel_line = LineString(Sentinel)
    # plt.plot(*Sentinel_line.xy)

    # 方法1
    # 根据线修正边线，以参考线为基准，对参考线外线修正

    # #step1 获取待修正边线
    Sentinel_dif = get_diff(Sentinel, icesat)
    #
    # # step2 获取平均面积
    p_Sentinel = Polygon(Sentinel)
    p_icesat = Polygon(icesat)
    s_to_i_area = get_areas(p_Sentinel, p_icesat)
    i_to_s_area = get_areas(p_icesat, p_Sentinel)
    average_area = area_statistic(s_to_i_area, i_to_s_area)

    # step3 修正

    result = remedy_by_intersection(icesat, Sentinel_dif, average_area)
    icesat_line = LineString(result)
    plt.plot(*icesat_line.xy)
    data_address = './data/s2_icesat/v2.shp'
    write_shp(data_address, result)
    # 方法2
    # 根据pol修正边线，以参考线围成多边形为基准，对互补面进行修正
    # remedy_pol(Sentinel, icesat)


    # plt.show()






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    optimize()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
