from optimize_line import *

def remedy_sub_line_by_pol(p1,p2,average_area,intersect_coor,refer_line):
    # p1在交集外围，s在外参考i,s_i 参考边在交集部分s为内边，获取s边内部的面积，获取公共边时，可能无交点;i在外参考i,i_s,参考边在外边
    dif = p1.difference(p2)
    multi_12 = dif.geoms
    result = intersect_coor
    for polygon in multi_12:
        # plt.plot(*polygon.exterior.xy)
        # 找断点
        px, py = polygon.exterior.xy

        p_coor = np.vstack((px, py)).T
        first_p, end_p, sub_bound = find_point(intersect_coor, p_coor, refer_line)
        if len(sub_bound) == 0:
            continue
        # 大于平均面积
        # 二维矩阵按行反转

        if polygon.area > average_area:
            # print(polygon.area)
            # plt.plot(*p2.exterior.xy)
            # plt.plot(px, py)
            # plt.show()
            rps = split_line_to_points(sub_bound, polygon, average_area)

            # 是否需要转置
            # reverse = np.flip(rps, axis=0)
            if len(rps) ==0:
                result = np.vstack((first_p, end_p))
            else:
                first_pa = np.row_stack((first_p, rps))

                result = np.vstack((first_pa, end_p))

        else:
            # 小于等于平均面积
            result = np.vstack((first_p, end_p))

        intersect_coor = result
    # pol = Polygon(result)
    # plt.plot(*pol.exterior.xy)

    return result


def remedy_pol(Sentinel,icesat):
    p_Sentinel = Polygon(Sentinel)
    p_icesat = Polygon(icesat)
    # plt.plot(*p_Sentinel.exterior.xy)
    plt.plot(*p_icesat.exterior.xy)

    x, y = p_icesat.exterior.xy
    intersect_coor = np.vstack((x, y)).T

    # 根据平面修正边线
    s_to_i_area = get_areas(p_Sentinel, p_icesat)
    i_to_s_area = get_areas(p_icesat, p_Sentinel)

    #
    # # 获取平均面积
    average_area = area_statistic(s_to_i_area, i_to_s_area)
    #
    result_si = remedy_sub_line_by_pol(p_Sentinel,p_icesat,average_area,intersect_coor,'s_i')

    result_is = remedy_sub_line_by_pol(p_icesat,p_Sentinel, average_area, result_si, 'i_s')

    return result_is