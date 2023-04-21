from shapely.geometry import Polygon, Point,LineString
import matplotlib.pyplot as plt

from shapely.ops import nearest_points
import numpy as np
# 获取边线交点，并添加
step_length = 60
def get_line_seg_points(Sentinel,icesat):
    l_Sentinel = LineString(Sentinel)
    l_icesat = LineString(icesat)
    # l_si = l_Sentinel.intersection(l_icesat)
    l_si = l_Sentinel.intersection(l_icesat)

    # if l_si.is_empty:
    #     print('no intersection point')
    # elif l_si.geom_type == 'Point':
    #     print('')
    # elif l_si.geom_type == 'LineString':
    #
    # elif l_si.geom_type == 'GeometryCollection':
    if True:
        geoms = l_si.geoms
        for pol in geoms:
            if pol.geom_type == 'Point':
                point = Point(pol)
                # plt.plot(point.x, point.y,marker='.', color='coral')
                # Sentinel = add_point_point(Sentinel, point)
                icesat = add_point_2_point(icesat, point)

            elif pol.geom_type == 'LineString':

                l = LineString(pol)
                x, y = l.xy
                # plt.plot(x, y)
                # Sentinel = add_line_point(Sentinel, l)
                icesat =  add_line_2_line(icesat, l)
                # icesat = add_line(icesat, l)


    return Sentinel,icesat

def add_line_2_line(inter_line,Line_exp):
    x, y = Line_exp.xy
    point1 = Point([x[0], y[0]])
    point2 = Point([x[1], y[1]])
    inter_line = add_point_2_point(inter_line, point2)
    inter_line = add_point_2_point(inter_line, point1)
    return inter_line

def add_point_2_point(result, point):
    rowIndex = np.where((result == [point.x, point.y]).all(axis=1))
    if len(rowIndex[0]) > 0:
        return result
    else:
        find_x = np.where((result == point.x))
        find_y = np.where((result == point.y))
        flag = 0
        if len(find_x[0]) > 0 and  len(find_y[0]):
            min1, min1_index = find_min(result,point,find_x[0])
            min2, min2_index = find_min(result, point, find_y[0])
            if min1 <= min2 and min1 <=step_length:
                result = find_loc(result, point, min1_index)
            elif min2 < min1 and min2 <=step_length:
                result = find_loc(result, point, min2_index)

        elif len(find_x[0]) > 0 :
            min1, min1_index = find_min(result, point, find_x[0])
            if min1 <= step_length:
                result = find_loc(result,point, min1_index)
        elif len(find_y[0]) > 0 :
            min2, min2_index = find_min(result, point, find_y[0])
            if  min2 <=step_length:
                result = find_loc(result, point, min2_index)
        return result

def find_min(result,point,index_array):

    min = 10000
    min_index = 0
    for i in range(len(index_array)):
        index = index_array[i]
        node = result[index, :]
        pnode = Point(node)
        d = point.distance(pnode)
        if d < min:
            min = d
            min_index = index
    return min,min_index

def find_loc(result,point,min_index):

    index = min_index
    pre_node = result[index - 1, :]
    node = result[index, :]
    next_node = result[index + 1, :]

    pnode = Point(node)
    pp = Point(pre_node)
    nextp = Point(next_node)


    line_p_pp = LineString([pre_node, node])
    line_p_np = LineString([node, next_node])

    dl1 = point.distance(line_p_pp)
    dl2 = point.distance(line_p_np)

    if dl2 < 1e-8 and dl1 < 1e-8:
        # 共线
        # plt.plot(pnode.x, pnode.y, marker='.', color='r')
        # plt.plot(pp.x, pp.y, marker='.', color='lime')
        # plt.plot(nextp.x, nextp.y, marker='.', color='b')
        # plt.plot(point.x, point.y, marker='.', color='plum')
        # plt.show()

        d2 = point.distance(pp)
        d3 = point.distance(nextp)
        d1 = point.distance(pnode)
        if d2 < d3:
            first_p = result[:index, :]
            end_p = result[index:, :]
            first_p = np.row_stack((first_p, [point.x, point.y]))
            result = np.vstack((first_p, end_p))

        else:
            first_p = result[:index + 1, :]
            end_p = result[index + 1:, :]
            first_p = np.row_stack((first_p, [point.x, point.y]))
            result = np.vstack((first_p, end_p))
        pass
    elif dl1 < 1e-8:
        # plt.plot(pnode.x, pnode.y, marker='.', color='r')
        # plt.plot(pp.x, pp.y, marker='.', color='lime')
        # plt.plot(nextp.x, nextp.y, marker='.', color='b')
        # plt.plot(point.x, point.y, marker='.', color='plum')
        # plt.show()
        first_p = result[:index, :]
        end_p = result[index:, :]
        first_p = np.row_stack((first_p, [point.x, point.y]))
        result = np.vstack((first_p, end_p))
    else:
        # plt.plot(pnode.x, pnode.y, marker='.', color='r')
        # plt.plot(pp.x, pp.y, marker='.', color='lime')
        # plt.plot(nextp.x, nextp.y, marker='.', color='b')
        # plt.plot(point.x, point.y, marker='.', color='black')

        # plt.show()
        first_p = result[:index + 1, :]
        end_p = result[index + 1:, :]
        first_p = np.row_stack((first_p, [point.x, point.y]))
        result = np.vstack((first_p, end_p))

    return result





# 添加线段点
def add_line_point(inter_line,Line_exp):
    index_array = []
    result = inter_line
    inter_line_shp = LineString(inter_line)
    x,y = Line_exp.xy
    point1 = Point([x[0],y[0]])
    point2 = Point([x[1],y[1]])
    rowIndex = np.where((inter_line == [x[0],y[0]]).all(axis=1))
    rowIndex2 = np.where((inter_line == [x[1], y[1]]).all(axis=1))
    if len(rowIndex[0]) > 0 and len(rowIndex2[0]) > 0:
        pass
    elif len(rowIndex[0]) > 0 :
        # p2不在边
        index = rowIndex[0][0]
        if index!=0:
            result = add_lpoint_to_line(result, index,point2)

    elif len(rowIndex2[0]) > 0:
        # p1不在边
        index = rowIndex2[0][0]
        if index!=0:
            result = add_lpoint_to_line(result, index,point1)
    else:
        # plt.plot(point1.x, point1.y, marker='.', color='lime')
        # plt.plot(point2.x, point2.y, marker='.', color='r')
        # result = add_point_to_point(result, point1)
        # result = add_point_to_point(result, point2)

        print('都不在交点')
    return result


def add_lpoint_to_line(inter_line,index,point):
    result = inter_line
    find_x = np.where((inter_line == point.x))
    find_y = np.where((inter_line == point.y))

    if len(find_x[0]) > 0 and (index in find_x[0]):
        result = add_point_to_array(result, find_x, 1, point)
    elif len(find_y[0]) > 0 and (index in find_y[0]):
        result = add_point_to_array(result, find_y, 0, point)
    else:
        print('斜边')
    return result


# 添加交点点
def add_point_point(inter_line,point):

    result = inter_line
    inter_line_shp = LineString(inter_line)

    rowIndex = np.where((inter_line == [point.x,point.y]).all(axis=1))
    if len(rowIndex[0]) >0:
        return result
    else:
        find_x = np.where((inter_line == point.x))
        find_y = np.where((inter_line == point.y))
        if len(find_x[0]) > 0:
            result = add_point_to_array(result, find_x, 1, point)
        elif len(find_y[0]) > 0:
            result = add_point_to_array(result, find_y, 0, point)
        else:
            print('斜边')

    return result



# 截断并添加点
def add_point_to_array(inter_line,id_array,colum,point):
    index_array = id_array[0]
    result = inter_line
    for i in range(0,len(index_array), 2):
        index = index_array[i]
        line_node = inter_line[index]
        line_node_next = inter_line[index + 1]
        # 根据colum 0，1，比较选择x,还是y
        y1, y2 = compare_2_num(line_node[colum], line_node_next[colum])
        if point.xy[colum] > y1 and point.xy[colum] < y2:
            #     截断，添加点
            first_p = inter_line[:index + 1, :]
            end_p = inter_line[index + 1:, :]
            first_p = np.row_stack((first_p, [point.x, point.y]))
            result = np.vstack((first_p, end_p))

    return result



def get_diff(Sentinel,icesat):
    l_Sentinel = LineString(Sentinel)
    l_icesat = LineString(icesat)
    l_si = l_Sentinel.intersection(l_icesat)
    l_dif = l_Sentinel.difference(l_icesat)
    if l_si.is_empty:
        print('no intersection point')
    elif l_si.geom_type == 'Point':
        # print('')
        pass
    elif l_si.geom_type == 'LineString':
        pass
    elif l_si.geom_type == 'GeometryCollection':
        geoms = l_si.geoms
        for pol in geoms:
            x, y = pol.xy
            # plt.plot(x, y)

    geoms = l_dif.geoms
    for pol in geoms:
        x, y = pol.xy
        # plt.plot(x, y)

    return l_dif




def compare_2_num(a,b):
    if a > b:
        return b,a
    else:
        return a,b

if __name__ == '__main__':
    pass