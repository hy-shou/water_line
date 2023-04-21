from shapely.geometry import Point,LineString,Polygon
import geopandas as gpd
import matplotlib.pyplot as plt

def read_shp():

    shapefile = gpd.read_file("path/to/shapes.shp")
    shapefile.plot()
    plt.show()


def point_test():
    p = Point(0, 0)
    print(p.geom_type)  # Point
    print(p.distance(Point(1, 1)))  # 1.4142135623730951

    line = LineString([(2, 0), (2, 4), (3, 4)])
    print(p.hausdorff_distance(line))  # 5.0 点p到直线line上的最远距离
    print(p.distance(line))  # 2.0 最近距离


    plt.plot(p.x, p.y)

    plt.show()

def line_test():
    line = LineString([(0, 0), (1, 1)])
    x,y = line.xy
    plt.plot(x,y)

    plt.show()

def polygon_test():
    p= Polygon([
        [-122.5, 45.46],
        [-122.801742, 45.49],
        [-122.82, 45.55],
        [-122.584762, 45.691],
        [-122.4, 45.5]

    ])
    p
    plt.plot(*p.exterior.xy)

    # 获取多边形点的顺序
    # print(sgp.orient(b, sign=1))  # 顺时针
    # print(sgp.orient(b, sign=-1))  # 逆时针

    plt.show()

if __name__ == '__main__':
    polygon_test()