from  pyproj  import  CRS,Transformer

# https://blog.csdn.net/tap880507/article/details/111608529
crs=CRS.from_epsg(4326)
crs = CRS.from_string("epsg:4326")
crs = CRS.from_proj4("+proj=latlon")
crs = CRS.from_user_input(4326)
crs_cs = CRS.from_string("epsg:32651")
#  "epsg:32650"
transformer = Transformer.from_crs(crs,crs_cs)

lat = 40.0691643333333

lon = 116.242161333333
x3, y3 = transformer.transform(lat, lon)
transformer.transform(lat, lon)
# (435376.10572293965, 4435708.949468517)


