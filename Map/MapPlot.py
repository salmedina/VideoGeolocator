import matplotlib.pyplot as plt
import csv
import utm
from progressbar import ProgressBar

class Pos:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        
    def set_utm(easting, northing, zone_number=17): #Zone17: Pittsburgh
        self.latitude, self.longitude = utm.to_latlon(easting, northing, zone_number)

class Marker:
    def __init__(self, latitude, longitude, color='red', size = '30'):
        self.pos = None
        self.latitude = latitude
        self.longitude = longitude
        self.color = color
        self.size = size
    
    def set_pos(latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        
    def set_color(color):
        self.color = color
    
    def set_size(size):
            self.size = size
        
class ScatterMap:
    def __init__(self, coords_path):
        self.coords_path = coords_path
        self.markers = []
    
    def add_marker(self, latitude, longitude, color='orange'):
        self.markers.append(Marker(latitude, longitude, color))
    
    def plot(self):
        data_file = open(self.coords_path)
        data_reader = csv.reader(data_file, delimiter=' ')
        
        total_locs = len(open(self.coords_path).readlines(  ))
            
        loc_pts = []
        latitude_list = []
        longitude_list = []
        
        for data_input in data_reader:
            latitude_list.append(float(data_input[0]))
            longitude_list.append(float(data_input[1]))
        
        left_border = min(longitude_list)
        right_border = max(longitude_list)
        top_border = max(latitude_list)
        bottom_border = min(latitude_list)
        
        area_width = right_border - left_border
        area_height = top_border - bottom_border
        
        MAP_SIZE = 10
        MAP_COLOR = 'gray'

        #Plot all the map dots
        plt.scatter(longitude_list, latitude_list, s=MAP_SIZE, c=MAP_COLOR, edgecolors='none')
        #Plot the marker dots
        for marker in self.markers:
            plt.scatter(marker.longitude, marker.latitude, s=marker.size, c=marker.color, edgecolors='none')
        
        #Format the plot
        plt.xlim([left_border, right_border])
        plt.ylim([bottom_border, top_border])
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.grid(b='on')
        
        plt.show()        

def convert_utm_to_latlong(data_path, save_path):
    total_locs = len(open(data_path).readlines(  )) -1
    data_reader = csv.reader(open(data_path), delimiter=' ')
    save_file = open(save_path, 'w')

    for data_input in data_reader:
        long_lat = utm.to_latlon(float(data_input[0]), float(data_input[1]), 17, northern=True)
        write_str = '%f %f\n'%(long_lat[0], long_lat[1])
        save_file.write(write_str)
    
    save_file.close()

def plot_whole_map():
    data_path = '/Users/zal/CMU/Spring2016/11775/Project/netvlad/analysis/Pittsburgh250k/latlong_export.txt'
    data_file = open(data_path)
    data_reader = csv.reader(data_file, delimiter=' ')
    
    total_locs = len(open(data_path).readlines(  ))
        
    loc_pts = []
    latitude_list = []
    longitude_list = []
    
    for data_input in data_reader:
        latitude_list.append(float(data_input[0]))
        longitude_list.append(float(data_input[1]))
    
    left_border = min(latitude_list)
    right_border = max(latitude_list)
    top_border = max(longitude_list)
    bottom_border = min(longitude_list)
    
    area_width = right_border - left_border
    area_height = top_border - bottom_border
    
    MAP_SIZE = 10
    MAP_COLOR = 'gray'
    MARKER_SIZE = 30
    MARKER_COLOR = 'red'
    MARKER_POS = 1234
    plt.scatter(longitude_list, latitude_list, s=MAP_SIZE, c=MAP_COLOR, edgecolors='none')
    plt.scatter(longitude_list[MARKER_POS], latitude_list[MARKER_POS], s=MARKER_SIZE, c=MARKER_COLOR, edgecolors='none')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    
    plt.show()
    
def convert_map_locs_to_latlong():
    data_path = '/Users/zal/CMU/Spring2016/11775/Project/netvlad/analysis/Pittsburgh250k/utm_export.txt'
    export_path = '/Users/zal/CMU/Spring2016/11775/Project/netvlad/analysis/Pittsburgh250k/latlong_export.txt'
    convert_utm_to_latlong(data_path, export_path)
    
if __name__=='__main__':
    #convert_map_locs_to_latlong()
    #plot_whole_map()
    pittMap = ScatterMap('/Users/zal/CMU/Spring2016/11775/Project/netvlad/analysis/Pittsburgh250k/latlong_export.txt')
    pittMap.plot()