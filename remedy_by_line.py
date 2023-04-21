from shapely.geometry import Polygon, Point,LineString
import matplotlib.pyplot as plt
from shapely.ops import snap, split, nearest_points
import numpy as np
from add_intersection_point import compare_2_num
from optimize_line import *
from add_intersection_point import *
def remedy_by_intersection(icesat,diff_lines,average_area):
    # 获取两线相交部分，保持不变，获取参考线中不相交部分。
    result = icesat
    icesat_line = LineString(icesat)
    geoms_lines = diff_lines.geoms
    for dif_line in geoms_lines:
            x, y = dif_line.xy
            # plt.plot(x, y)

            inter_points = dif_line.intersection(icesat_line)
            if inter_points.is_empty:
                # print('no')
                pass
                # plt.plot(x, y)
            elif dif_line.geom_type == 'LineString':
                # 顶点在线段里面有重复
                # print(inter_points.geoms[0])
                # print(inter_points.geoms[1])
                if inter_points.geom_type == 'Point':
                    print('one point')
                else:
                    icesat_first, icesat_sub, icesat_end = clipLine(result, inter_points)
                    if len(icesat_sub) >0:
                        # remedy(icesat_sub, list(zip(x,y)),average_area)
                        # 多边形

                        polygon_array = np.vstack((icesat_sub, np.flip(list(zip(x,y)), axis=0)))
                        polygon = Polygon(polygon_array)
                        # plt.plot(*polygon.exterior.xy)
                        if polygon.area > average_area:
                            rps = split_line_to_points(icesat_sub, polygon, average_area)

                            if len(rps) == 0:
                                result = np.vstack((icesat_first, icesat_end))
                            else:
                                first_pa = np.row_stack((icesat_first, rps))

                                result = np.vstack((first_pa, icesat_end))
                        else:
                            result = np.vstack((icesat_first, icesat_end))

            else:
                print(dif_line.geom_type)
    return result

def clipLine(icesat, inter_points):
    icesat_first = []
    icesat_sub = []
    icesat_end = []
    point1 = inter_points.geoms[0]
    point2 = inter_points.geoms[1]
    rowIndex = np.where((icesat == [point1.x, point1.y]).all(axis=1))
    rowIndex2 = np.where((icesat == [point2.x, point2.y]).all(axis=1))

    # plt.show()
    if len(rowIndex[0]) > 0 and len(rowIndex2[0]) > 0:
        if abs(rowIndex[0][0]-rowIndex2[0][0]) < 500:
            # 分三段
            idx1 = rowIndex[0][0]
            idx2 = rowIndex2[0][0]
            idx1,idx2 = compare_2_num(idx1,idx2)
            # 交点部分重复
            icesat_first = icesat[:idx1 + 1,:]
            icesat_sub = icesat[idx1:idx2+1,:]
            icesat_end = icesat[idx2:,:]
        else:
            print('first,end')
    # elif len(rowIndex[0]) > 0:
    #     # [point2.x, point2.y]
    #
    #     plt.plot(point2.x, point2.y, marker='*', color='lime')
    #     plt.plot(point1.x, point1.y, marker='*', color='black')
    #     # plt.show()
    #
    #     idx = rowIndex[0][0]
    #     node = icesat[idx,:]
    #
    #     get_index(icesat, point2)
    #     # node1 = icesat[idx + 1, :]
    #     # tesst_line = LineString([node,node1])
    #


    # elif len(rowIndex2[0]) > 0:
    #     plt.plot(point2.x, point2.y, marker='*', color='r')
    #     pass
    else:
        # plt.plot(point1.x, point1.y, marker='*', color='lime')
        # plt.plot(point2.x, point2.y, marker='*', color='lime')
        print('no')

    return icesat_first,icesat_sub,icesat_end

def get_index(result, point):
    find_x = np.where((result == point.x))
    find_y = np.where((result == point.y))
    flag = 0
    if len(find_x[0]) > 0 and len(find_y[0]):
        min1, min1_index = find_min(result, point, find_x[0])
        min2, min2_index = find_min(result, point, find_y[0])
        if min1 < min2 and min1 < 50:
            result = find_loc(result, point, min1_index)
        elif min2 < min1 and min2 < 50:
            # result = find_loc(result, point, min2_index)
            pass
        else:
            print(min1,min2)
            print('max')

    elif len(find_x[0]) > 0:
        min1, min1_index = find_min(result, point, find_x[0])
        if min1 < 50:
            # result = find_loc(result, point, min1_index)
            pass
        else:
            print(min1)
            print('max')
    elif len(find_y[0]) > 0:
        min2, min2_index = find_min(result, point, find_y[0])
        if min2 < 50:

            # result = find_loc(result, point, min2_index)
            pass
        else:
            print(min2)
            print('max')
    return result


def remedy(icesat_sub,dif_line,average_area):

    result = np.vstack((icesat_sub, np.flip(dif_line,axis=0)))

    # 多边形
    polygon = Polygon(result)
    # plt.plot(*polygon.exterior.xy)
    if polygon.area > average_area:
        rps = split_line_to_points(icesat_sub, polygon, average_area)
    else:
        result = np.vstack((first_p, end_p))
    # split_line_to_points(icesat_sub,average_area)
    pass
