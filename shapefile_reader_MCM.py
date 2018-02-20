import shapefile
from math import *
cross_file = shapefile.Reader("/Users/mac/Desktop/US_Road/cross_US.shp")
cross = cross_file.shapes()
road_file = shapefile.Reader("/Users/mac/Desktop/US_Road/road_US.shp")
road = road_file.shapes()


EPS=1e-12

def dist(x,y): #两点欧氏距离
	x=list(x)
	y=list(y)
	return sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)

line_road_file = []
line_road_file = shapefile.Writer(shapeType=3) #3是直线，1是点
line_road_file.autoBalance = 1
line_road_file.field('FIRST_FLD')
line_road_file.field('SECOND_FLD', 'C', '40')

for i in road:
	st=[]
	en=[]
	st=i.points[0]
	en=i.points[-1]
	line_road_file.record("row","one")
	line_road_file.line(parts=[[ st,en ]])

line_road_file.save("/Users/mac/Desktop/US_Road/line_road")

line_road = shapefile.Reader("/Users/mac/Desktop/US_Road/line_road.shp")
line_road = line_road.shapes()


inter_point_file = []
inter_point_file = shapefile.Writer(shapeType=3) #3是直线，1是点
linter_point_file.autoBalance = 1
inter_point_file.field('FIRST_FLD')
inter_point_file.field('SECOND_FLD', 'C', '40')

inter_point=[]

for i in line_road:
	inter_point.append(tuple(i.points[0]))
	inter_point.append(tuple(i.points[1]))

inter_point=list(set(all_point))


cross_unique_file = []
cross_unique_file = shapefile.Writer(shapefile.POINTM) #3是直线，1是点
cross_unique_file.autoBalance = 1
cross_unique_file.field('State')

cross_unique = []
cross_record = cross_file.records()

for i in range(len(cross)):
	cross_unique.append((tuple(cross[i].points[0]),cross_record[i][0]))

cross_unique = list(set(cross_unique))

for i in cross_unique:
	cross_unique_file.record(i[1])
	cross_unique_file.point(i[0][0],i[0][1])

cross_unique_file.save("/Users/mac/Desktop/US_Road/cross_unique_road")

def geo_dist(x,y):  
	latitude1 = float(x[0])
	longitude1 = float(x[1])
	latitude2 = float(y[0]) 
	longitude2 = float(y[1])
	#地理距离，单位公里
	latitude1 = (pi/180.0)*latitude1  
	latitude2 = (pi/180.0)*latitude2  
	longitude1 = (pi/180.0)*longitude1  
	longitude2= (pi/180.0)*longitude2  
	#因此AB两点的球面距离为:{arccos[sina*sinx+cosb*cosx*cos(b-y)]}*R  (a,b,x,y)  
	#地球半径  
	R = 6378.1  
	temp=sin(latitude1)*sin(latitude2)+\
			cos(latitude1)*cos(latitude2)*cos(longitude2-longitude1)  
	if temp>1.0:  
		temp = 1.0  
	d = acos(temp)*R  
	return d

line_road_dist_file = []
line_road_dist_file = shapefile.Writer(shapeType=3) #3是直线，1是点
#line_road_dist_file.autoBalance = 1
line_road_dist_file.field('Distance')
line_road_dist_file.field('State')

def get_point_state(x):
	x=list(x)
	for i in cross_unique:
		y=list(i[0])
		if(x==y):
			return i[1]
		#if(geo_dist(x,y)<=0.001):
		#	return i[1]

for i in line_road:
	st=[]
	en=[]
	st=i.points[0]
	en=i.points[-1]
	line_road_dist_file.record(geo_dist(st,en) , get_point_state(st) ) 
	#line_road_dist_file.record(get_point_state(st) ) 
	line_road_dist_file.line(parts=[[ st,en ]])

line_road_dist_file.save("/Users/mac/Desktop/US_Road/line_dist_road")

state_code = [
	'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 
	'DE', 'FL', 'GA', 'IA', 'ID', 'IL', 'IN', 
	'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 
	'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 
	'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 
	'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 
	'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

state_point = []

for i in state_code:
	state_point.append([])

for i in cross_unique:
	state_point[state_code.index(i[1])].append((i[0][0],i[0][1]))

for i in range(len(state_code)):
	print(state_code[i],len(state_point[i]))

for i in state_code:
	#state_point_shp:
	state_point_file = []
	state_point_file = shapefile.Writer(shapefile.POINTM) #3是直线，1是点
	state_point_file.autoBalance = 1
	state_point_file.field('State')
	for j in cross_unique:
		if(j[1]==i):
			state_point_file.record(j[1])
			state_point_file.point(j[0][0],j[0][1])
	state_point_file.save("/Users/mac/Desktop/US_Road/%s_point"%i)
	#state_road_shp:


line_dist_road_file = shapefile.Reader("/Users/mac/Desktop/US_Road/line_dist_road.shp")
line_dist_road_record = line_dist_road_file.records()
line_dist_road = line_dist_road_file.shapes()

for i in state_code:
	state_road_file = []
	state_road_file = shapefile.Writer(shapeType=3) #3是直线，1是点
	state_road_file.autoBalance = 1
	state_road_file.field('Distance')
	state_road_file.field('State')
	for j in range(len(line_dist_road)):
		if(line_dist_road_record[j][1] == i):
			st=[]
			en=[]
			st=line_dist_road[j].points[0]
			en=line_dist_road[j].points[1]
			state_road_file.record( line_dist_road_record[j][0], line_dist_road_record[j][1]) 
			#line_road_dist_file.record(get_point_state(st) ) 
			state_road_file.line(parts=[[ st,en ]])
	state_road_file.save("/Users/mac/Desktop/US_Road/%s_road"%i)


state_station_num=[
	2753, 2235, 2865, 17799, 2178, 1629, 249, 538, 9467, 4264, 1570, 
	732, 5453, 2808, 1181, 2065, 1717, 2778, 2381, 493, 3914, 2508, 2709, 
	1013, 531, 4274, 293, 843, 638, 3432, 796, 1262, 5894, 5657, 1662, 
	1788, 5592, 525, 2218, 439, 2829, 9987, 1133, 3907, 276, 3538, 2603, 
	704, 255]

state_car_num=[71584, 58124, 74514, 462775, 56647, 42377, 6481, 14007, 246148, 
110870, 40834, 19048, 141784, 73017, 30720, 53696, 44664, 72243, 
61919, 12823, 101789, 65231, 70439, 26344, 13825, 111127, 7625, 
21943, 16591, 89239, 20718, 32819, 153259, 147087, 43218, 46488, 
145411, 13670, 57668, 11424, 73569, 259685, 29474, 101606, 7193, 
91990, 67682, 18318, 6630]

#对于每个州的每个点，计算充电站分布
def in_point_set(x,y): #(point_set, point)
	for i in range(len(x)):
		if(geo_dist(x[i],y)<1e-3):
			return i
	return -1

def get_n_point_line(st,en,n): #返回一个list，一条直线上的n等分点
	ret = []
	for i in range(n):
		lam = i*1.0/n
		ret.append([st[0]+lam*(en[0]-st[0]),st[1]+lam*(en[1]-st[1])])
	return ret

country_urban_station = 0
country_suburban_station = 0
country_rural_station = 0

country_urban_station_point = []
country_suburban_station_point = []
country_rural_station_point = []

for state_code_i in range(int(len(state_code)) ):
	state_name_i = state_code[state_code_i]
	print("********")
	print("state_name:",state_name_i)
	print("state_car_num:",state_car_num[state_code_i])
	print("state_station_num:",state_station_num[state_code_i])
	state_point_file = shapefile.Reader("/Users/mac/Desktop/US_Road/%s_point.shp"%state_name_i)
	state_point = state_point_file.shapes()
	state_road_file = shapefile.Reader("/Users/mac/Desktop/US_Road/%s_road.shp"%state_name_i)
	state_road = state_road_file.shapes()
	state_road_record = state_road_file.records()
	point_set = []
	dense_point = []
	edge_table = []
	print("point_data:",len(state_point))
	print("road_data:",len(state_road))
	for i in state_point:
	    point_set.append(i.points[0])
	for i in point_set:
	    edge_table.append([])
	for i in range(len(state_road)):
	    st=[]
	    en=[]
	    st=state_road[i].points[0]
	    en=state_road[i].points[1]
	    st=list(st)
	    en=list(en)
	    if(in_point_set(point_set,st) != -1):
	        edge_table[in_point_set(point_set,st)].append([st,en,float(state_road_record[i][0])])
	    if(in_point_set(point_set,en) != -1):
	        edge_table[in_point_set(point_set,en)].append([st,en,float(state_road_record[i][0])])
	print("Edge_table:",len(edge_table))
	#
	for i in edge_table:
	    sum_w = 0
	    for j in i:
	        sum_w += j[2]
	    if(sum_w!=0):
	        dense_point.append(1.0/sum_w )
	    else:
	        dense_point.append(0)
	Kstate = 0
	sum_dense_w = 0
	for i in range(len(state_road)):
	    st=[]
	    en=[]
	    st=state_road[i].points[0]
	    en=state_road[i].points[1]
	    st=list(st)
	    en=list(en)
	    equal_dense = 0    
	    if(in_point_set(point_set,st) != -1):
	        equal_dense += dense_point[in_point_set(point_set,st)]
	    if(in_point_set(point_set,en) != -1):
	        equal_dense += dense_point[in_point_set(point_set,en)]
	    equal_dense /= 2
	    wij = float(state_road_record[i][0])
	    denseij = equal_dense
	    sum_dense_w += wij * denseij
	Kstate = state_car_num[state_code_i]/sum_dense_w #AL
	print("sum_dense_w:",sum_dense_w)
	print("Kstate:",Kstate)
	#Kstate = state_car_num[state_code.index(i)]
	dense_point_set = []
	for i in range(len(state_road)):
	    st=[]
	    en=[]
	    st=state_road[i].points[0]
	    en=state_road[i].points[1]
	    st=list(st)
	    en=list(en)
	    equal_dense = 0    
	    if(in_point_set(point_set,st) != -1):
	        equal_dense += dense_point[in_point_set(point_set,st)]
	    if(in_point_set(point_set,en) != -1):
	        equal_dense += dense_point[in_point_set(point_set,en)]
	    equal_dense /= 2
	    wij = float(state_road_record[i][0])
	    denseij = equal_dense
	    road_point_num = int(Kstate * denseij * wij)
	    n_point = []
	    n_point = get_n_point_line(st,en,road_point_num)
	    for j in n_point:
	        dense_point_set.append([j,road_point_num])
	print("dense_point_set:",len(dense_point_set))
	#画在shapefile上面：
	state_dense_point_file = []
	state_dense_point_file = shapefile.Writer(shapefile.POINTM) #3是直线，1是点
	state_dense_point_file.field('State')
	state_dense_point_file.field('Car_Number')
	#
	for i in dense_point_set:
		#print(i[1])
		state_dense_point_file.record(state_name_i, i[1] )
		state_dense_point_file.point(i[0][0],i[0][1])
	state_dense_point_file.save("/Users/mac/Desktop/US_Road/%s_dense_point"%state_name_i)
	#
	#画在shapefile上面：
	state_station_point_file = []
	state_station_point_file = shapefile.Writer(shapefile.POINTM) #3是直线，1是点
	state_station_point_file.field('State')
	state_station_point_file.field('Station_Number')
	#
	Kless = int(len(dense_point_set)/state_station_num[state_code_i])
	for i in range(len(dense_point_set)):
	    if(i%Kless == 0):
	        state_station_point_file.record(state_name_i,dense_point_set[i][1]/
	        									state_station_num[state_code_i])
	        state_station_point_file.point(dense_point_set[i][0][0],dense_point_set[i][0][1])
	#
	state_station_point_file.save("/Users/mac/Desktop/US_Road/%s_station_point"%state_name_i)
	#统计城乡分布
	state_urban_station = 0
	state_suburban_station = 0
	state_rural_station = 0
	Avg_road_dense = 0
	for i in range(len(state_road)):
	    st=[]
	    en=[]
	    st=state_road[i].points[0]
	    en=state_road[i].points[1]
	    st=list(st)
	    en=list(en)
	    equal_dense = 0    
	    if(in_point_set(point_set,st) != -1):
	        equal_dense += dense_point[in_point_set(point_set,st)]
	    if(in_point_set(point_set,en) != -1):
	        equal_dense += dense_point[in_point_set(point_set,en)]
	    equal_dense /= 2
	    wij = float(state_road_record[i][0])
	    denseij = equal_dense
	    road_point_num = int(Kstate * denseij * wij)
	    if(road_point_num==0):
	    	continue
	    dense_now_road = road_point_num/ Kless / float(state_road_record[i][0])
	    Avg_road_dense += dense_now_road 
	    #print(dense_now_road)
	Avg_road_dense /= len(state_road)
	print("Avg road dense:",Avg_road_dense)
	for i in range(len(state_road)):
	    st=[]
	    en=[]
	    st=state_road[i].points[0]
	    en=state_road[i].points[1]
	    st=list(st)
	    en=list(en)
	    equal_dense = 0    
	    if(in_point_set(point_set,st) != -1):
	        equal_dense += dense_point[in_point_set(point_set,st)]
	    if(in_point_set(point_set,en) != -1):
	        equal_dense += dense_point[in_point_set(point_set,en)]
	    equal_dense /= 2
	    wij = float(state_road_record[i][0])
	    denseij = equal_dense
	    road_point_num = int(Kstate * denseij * wij)
	    if(road_point_num==0):
	    	continue
	    dense_now_road = road_point_num/ Kless / float(state_road_record[i][0])
	    #print(dense_now_road)
	    relative_dense = dense_now_road/Avg_road_dense
	    n_point = []
	    n_point = get_n_point_line(st,en,int(road_point_num/Kless))
	    if( relative_dense> 0.478 ) :
	    	state_urban_station += road_point_num / Kless  #urban
	    	country_urban_station_point.append(n_point)
	    if( relative_dense >= 0.250 and relative_dense <= 0.478):
	    	state_suburban_station += road_point_num / Kless #suburban
	    	country_suburban_station_point.append(n_point)
	    if( relative_dense < 0.250):
	    	state_rural_station += road_point_num / Kless #rural
	    	country_rural_station_point.append(n_point)
	print("state_urban_station Number:",state_urban_station)
	print("state_suburban_station Number:",state_suburban_station)
	print("state_rural_station Number:",state_rural_station)
	country_urban_station += state_urban_station
	country_suburban_station += state_suburban_station
	country_rural_station += state_rural_station
	#ration
	print("state_urban_station Ration:",state_urban_station/state_station_num[state_code_i])
	print("state_suburban_station Ration:",state_suburban_station/state_station_num[state_code_i])
	print("state_rural_station Ration:",state_rural_station/state_station_num[state_code_i])

def show_country_result():
	print("Country_urban_station Number:",country_urban_station)
	print("Country_suburban_station Number:",country_suburban_station)
	print("Country_rural_station Number:",country_rural_station)
	print("Country_urban_station Ration:",country_urban_station/sum(state_station_num))
	print("Country_suburban_station Ration:",country_suburban_station/sum(state_station_num))
	print("Country_rural_station Ration:",country_rural_station/sum(state_station_num))


#城乡数据可视化：

urban_set=[]
suburban_set=[]
rural_set=[]

for i in country_urban_station_point:
	if(i!=[]):
		urban_set.append(i)

for i in country_suburban_station_point:
	if(i!=[]):
		suburban_set.append(i)

for i in country_rural_station_point:
	if(i!=[]):
		rural_set.append(i)		

urban_point=[]
suburban_point=[]
rural_point=[]

for i in urban_set:
	for j in i:
		urban_point.append(j)

for i in suburban_set:
	for j in i:
		suburban_point.append(j)

for i in rural_set:
	for j in i:
		rural_point.append(j)

#画在shapefile上面：
urban_file = []
urban_file = shapefile.Writer(shapefile.POINTM) #3是直线，1是点
urban_file.field('Area')
#
for i in urban_point:
	urban_file.record("Urban")
	urban_file.point(i[0],i[1])

urban_file.save("/Users/mac/Desktop/US_Road/Urban_station_point")


#画在shapefile上面：
suburban_file = []
suburban_file = shapefile.Writer(shapefile.POINTM) #3是直线，1是点
suburban_file.field('Area')
#
for i in suburban_point:
	suburban_file.record("Suburban")
	suburban_file.point(i[0],i[1])

suburban_file.save("/Users/mac/Desktop/US_Road/Suburban_station_point")


#画在shapefile上面：
rural_file = []
rural_file = shapefile.Writer(shapefile.POINTM) #3是直线，1是点
rural_file.field('Area')
#
for i in rural_point:
	rural_file.record("Rural")
	rural_file.point(i[0],i[1])

rural_file.save("/Users/mac/Desktop/US_Road/Rural_station_point")
