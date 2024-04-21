from pyquadtree import QuadTree
import json
import shutil



quadtree = QuadTree(bbox=(0, 0, 1000, 500), max_elements=10, max_depth=5)



def convert_crs(geojson_data):    # Заменяем CRS
    geojson_data["crs"] = {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}    
    arr = []
    # Пересчитываем координаты в новую систему
    for feature in geojson_data["features"]:        
        geometry = feature["geometry"]
        if geometry["type"] == "MultiLineString":            
            coordinates = geometry["coordinates"]
            for line in coordinates:                
                for i, point in enumerate(line):
                    x, y = point[:2]                    
                    arr.append([x, y])
    return arr

with open('blue_3.geojson', 'r') as file:
    geojson_data = json.load(file)
coor_b = convert_crs(geojson_data)

with open('red_3.geojson', 'r') as file:
    geojson_data = json.load(file)
coor_r = convert_crs(geojson_data)


coor_g = []

print(coor_b)
print("sasdasd",coor_r , "asdasdad")

for i in range(len(coor_b)):
    quadtree.add(i, (coor_b[i][0], coor_b[i][1]))





for i in range(len(coor_r)):
    nearest_neighbor = quadtree.nearest_neighbors((coor_r[i][0], coor_r[i][1]))[0]
    coor_g.append(nearest_neighbor.point)













#FILE GREEN
print("green", *coor_g)

shutil.copyfile("red_3.geojson", "green_3.geojson")
with open('green_3.geojson', 'r') as file:
    geojson_data["crs"] = {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}    
    arr = []
    # Пересчитываем координаты в новую систему
    for feature in geojson_data["features"]:        
        geometry = feature["geometry"]
        if geometry["type"] == "MultiLineString":            
            coordinates = geometry["coordinates"][0]
            for i in range(len(coordinates)):                
                coordinates[i] = [coor_g[i][0], coor_g[i][1]]
                print(coordinates[i])
                print(coor_g[i])
    data = geojson_data
with open("green_3.geojson", 'w') as file:
    json.dump(data, file, ensure_ascii=False)


coor_g_final = []
#print(coor_b)
#print(coor_b[coor_b.index(list(coor_g[0])):coor_b.index(list(coor_g[1]))+1])
#print(coor_g[0], coor_g[1])
#print(coor_b.index(list(coor_g[1])))
for i in range(len(coor_g) - 1):
    srez = coor_b[coor_b.index(list(coor_g[i])):coor_b.index(list(coor_g[i+1]))+1]
    coor_g_final+=srez

print(coor_g_final)

#FINAL GREEN FILE
shutil.copyfile("red_3.geojson", "green_3.geojson")
with open('green_3.geojson', 'r') as file:
    geojson_data["crs"] = {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}    
    arr = []
    # Пересчитываем координаты в новую систему
    for feature in geojson_data["features"]:        
        geometry = feature["geometry"]
        if geometry["type"] == "MultiLineString":            
            coordinates = geometry["coordinates"][0]
            geometry["coordinates"][0] = coor_g_final
    data = geojson_data
with open("green_3.geojson", 'w') as file:
    json.dump(data, file, ensure_ascii=False)