state_point_file = shapefile.Reader("/Users/mac/Desktop/US_Road/AL_point.shp")
state_point = state_point.shapes()
state_road_file = shapefile.Reader("/Users/mac/Desktop/US_Road/AL_road.shp")
state_road = state_road.shapes()
state_road_record = state_road.records()

def in_point_set(x,y): #(point_set, point)
    for i in range(len(x)):
        if(geo_dist(x[i],y)<1e-3):
            return i
    return -1

point_set = []
dense_point = []
edge_table = []

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

for i in edge_table:
    sum_w = 0
    for j in i:
        sum_w += j[2]
    if(sum_w!=0):
        dense_point.append(1.0/log(sum_w))
    else:
        dense_point.append(0)

def get_n_point_line(st,en,n): #返回一个list，一条直线上的n等分点
    ret = []
    for i in range(n):
        lam = i*1.0/n
        ret.append([st[0]+lam*(en[0]-st[0]),st[1]+lam*(en[1]-st[1])])
    return ret

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

Kstate = 195.29585006693435 #AL
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
    road_point_num = int(Kstate * denseij)
    n_point = []
    n_point = get_n_point_line(st,en,road_point_num)
    for j in n_point:
        dense_point_set.append([j,road_point_num])

#画在shapefile上面：
state_dense_point_file = []
state_dense_point_file = shapefile.Writer(shapefile.POINTM) #3是直线，1是点
state_dense_point_file.field('State')
state_dense_point_file.field('Car_Number')

for i in dense_point_set:
    state_dense_point_file.record("AL",i[1])
    state_dense_point_file.point(i[0][0],i[0][1])

state_dense_point_file.save("/Users/mac/Desktop/US_Road/AL_dense_point")

#画在shapefile上面：
state_dense_point_file = []
state_dense_point_file = shapefile.Writer(shapefile.POINTM) #3是直线，1是点
state_dense_point_file.field('State')
state_dense_point_file.field('Car_Number')

for i in range(len(dense_point_set)):
    Kless = int(len(dense_point_set)/2805)
    if(i%Kless == 0):
        state_dense_point_file.record("AL",dense_point_set[i][1])
        state_dense_point_file.point(dense_point_set[i][0][0],dense_point_set[i][0][1])

state_dense_point_file.save("/Users/mac/Desktop/US_Road/AL_station_point")


    
