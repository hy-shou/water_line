# coding=utf-8
# This is a sample Python script.

import numpy as np
from shapely.geometry import Polygon, Point,LineString
from shapely_example.read_write_shp import get_line_points
from collections import Counter
import copy

PIX_LENGTH = 10
def get_distance():

    label_x, label_y,Sentinel2_x, Sentinel2_y,icesat_x, icesat_y = get_line_points()
    label_x = list(label_x)
    label_y = list(label_y)
    label = np.array(list(zip(label_x, label_y)))

    Sentinel2_x = list(Sentinel2_x)
    Sentinel2_y = list(Sentinel2_y)
    Sentinel = np.array(list(zip(Sentinel2_x, Sentinel2_y)))


    icesat_x = list(icesat_x)
    icesat_y = list(icesat_y)
    icesat = np.array(list(zip(icesat_x, icesat_y)))

    p_Sentinel = Polygon(Sentinel)
    p_icesat = Polygon(icesat)

    # plt.plot(*p_Sentinel.exterior.xy)
    # plt.plot(*p_icesat.exterior.xy)
    # plt.show()

    s_to_i_area = get_areas(p_Sentinel,p_icesat)
    i_to_s_area = get_areas(p_icesat, p_Sentinel)
    area_statistic(s_to_i_area, i_to_s_area)

    #

def get_areas(p_Sentinel,p_icesat):
    dif21 = p_Sentinel.difference(p_icesat)
    multi_21 = dif21.geoms
    print(len(multi_21))
    s_to_i_area = []
    for polygon in multi_21:
        #
        # plt.plot(*polygon.exterior.xy)
        s_to_i_area.append(polygon.area)
    all_area = dif21.area
    # plt.show()
    return s_to_i_area


def area_statistic(s_to_i_area, i_to_s_area):
    data = s_to_i_area + i_to_s_area
    # plt.hist(data, bins=[x for x in range(1, 20000, 100)])
    # plt.title("histogram")
    count = int(len(data)*0.8)
    print('根据帕累托法则，统计面积分布占比阈值:',count)
    c = Counter(data)


    sorted_x = sorted(c.items(), key=lambda x: x[1], reverse=True)
    print(sorted_x)
    tmp = 0
    tmp_area = 0
    for p in sorted_x:
        tmp = tmp + p[1]
        tmp_area = tmp_area + p[0]*p[1]

        if len(c) < count and tmp >= count:
            print('面积阈值:',p[0])
            break
    average_area = tmp_area/tmp
    print('面积均值:', average_area)
    # plt.show()
    return average_area


def find_point(inter_line,p_line,refer_line):
    index_array = []
    inter_sub_bound = []
    else_sub_bound = []
    sub_bound = []
    first_p = []
    end_p = []
    find_point = []

    inter_line_shp = LineString(inter_line)
    for i in range(p_line.shape[0]-1):
        pa = p_line[i]
        point = Point(pa)
        rowIndex = np.where((inter_line == pa).all(axis=1))
        if len(rowIndex[0]) >0:
            index_array.append(rowIndex[0][0])
            inter_sub_bound.append(list(pa))
        else:
            if inter_line_shp.distance(point) < 1e-8:
                inter_sub_bound.append(list(pa))
                find_point.append(list(pa))
            else:
                else_sub_bound.append(list(pa))

    # 交集截断
    if len(index_array) <= 1:
        # sub_bound = find_point
        # print('.')
        pass

    else:
        index_array.sort()
        end = len(index_array) - 1

        first_p = inter_line[:index_array[0], :]
        end_p = inter_line[index_array[end]:, :]

        if len(index_array) ==1 and len(find_point) >0:
           first_p = np.row_stack((first_p, pa))

        # 近边
        if refer_line == 's_i':
            sub_bound = inter_sub_bound
            sub_bound = np.flip(sub_bound, axis=0)
        if refer_line == 'i_s':
            sub_bound = else_sub_bound
    # sub_bound.append(sub_bound[0])
    return first_p, end_p, sub_bound

# v1.根据分段个数切分面积 spaa = average_area / (line_point_count - 1)
# v2.根据分段长度切分面积
def split_line_to_points(sub_bound,polygon, average_area):
    rect_points = []
    line_point_count = len(sub_bound)
    if line_point_count == 1:
        return sub_bound
    else:
        spaa = average_area / (line_point_count - 1)
        all_len = line_lenght(sub_bound)
        for i in range(line_point_count - 1):
            first_p = sub_bound[i]
            # rect_points.append(first_p)

            end_p = sub_bound[i+1]

            pf = Point(first_p)
            pe = Point(end_p)
            d = pf.distance(pe)

            if d <= 10:
                continue
            line_points = [first_p, end_p]

            spaa = average_area*(d/all_len)
            points = find_rect_points(line_points,polygon,spaa)
            rect_points.append(points)
            # p = re_calculate_area(line_points, points)
            rect_points.append(points)
        # rect_points.append(sub_bound[-1])
    return rect_points


    # 获取交点
    line = [inter_line[index_array[0]], inter_line[index_array[end]]]

# 线段长度
def line_lenght(sub_bound):
    l_len = 0
    line_point_count = len(sub_bound)
    for i in range(line_point_count - 1):
        first_p = sub_bound[i]
        # rect_points.append(first_p)

        end_p = sub_bound[i + 1]

        pf = Point(first_p)
        pe = Point(end_p)
        d = pf.distance(pe)
        l_len = l_len + d
    return l_len
#求俩点之间中垂线
def find_rect_points(line_points,polygon,split_average_area):
    # 中垂线(x1 + x2) / 2, (y1 + y2) / 2)
    # Ax + By + C = 0
    x1 = line_points[0][0]
    y1 = line_points[0][1]
    x2  = line_points[1][0]
    y2 = line_points[1][1]


    points = []
    if x1 == x2:
        y = (y1 + y2) / 2
        px = x1 - 1
        tmp_point = Point([px, y])
        if polygon.contains(tmp_point):
            while True:
                    px = px - 1
                    p = calculat_area(line_points, [px, y], split_average_area)
                    if len(p) > 0:
                        points = p
                        break
                    else:
                        px = px - 1
        else:
            while True:
                    px = px + 1
                    p = calculat_area(line_points, [px, y], split_average_area)
                    if len(p) > 0:
                        points = p
                        break
                    else:
                        px = px + 1

    elif y1 == y2:
        px = (x1 + x2) / 2

        py = y1 - 1
        tmp_point = Point([px, py])
        if polygon.contains(tmp_point):
            while True:
                py = py - 1
                p = calculat_area(line_points, [px, py], split_average_area)
                if len(p) > 0:
                    points=p
                    break
                else:
                    py = py - 1
        else:
            while True:
                py = py + 1
                p = calculat_area(line_points, [px, py], split_average_area)
                if len(p) > 0:
                    points=p
                    break
                else:
                    py = py + 1
    #     y小于y1，y2
    else:
        k = (y2 - y1) / (x2 - x1);
        c = (x1 + x2) / (2 * k) + (y1 + y2) / 2
        tmp = copy.deepcopy(x1)
        if x1 > x2:
            x1 = copy.deepcopy(x2)
            x2 = copy.deepcopy(tmp)

        for i in np.arange(x1, x2, 0.001):
            py = -(1 / k) * i + c

            tmp_point = Point([i,py])

            if not polygon.contains(tmp_point):
                continue

            p = calculat_area(line_points, [i,py], split_average_area)
            if len(p)>0:
                points=p
                break

    # line = LineString(line_points)
    # x, y = line.xy
    # plt.plot(x, y)

    # points = np.array(points)
    # line_points.append(points)
    # pol = Polygon(line_points)
    #
    # plt.plot(*pol.exterior.xy)
    # plt.show()

    return points

def calculat_area(line_points,point,split_average_area):
    tmp_points = copy.deepcopy(line_points)
    tmp_points.append(point)
    pol = Polygon(tmp_points)

    if pol.area >= split_average_area:
        return point
    else:
        return []



# def re_calculate_area(sub_bound,points):
#     count = points.shape[0]
#     p = []
#     for i in range(count):
#         tmp_bound = copy.deepcopy(sub_bound)
#         p = points[i]
#         tmp_bound.append(p)
#         pol = Polygon(tmp_bound)
#         if pol.area <= 0.004427:
#             print(p)
#             break
#
#     return p
#     # sub_bound.append(points[100])
#
#     # plt.plot(*pol.exterior.xy)
#
#     # sub = Polygon(sub_bound)
#     # plt.plot(*sub.exterior.xy)
#     # plt.show()
#

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_distance()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
