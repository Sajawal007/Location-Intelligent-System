import gmplot
import geopy.distance

# We subclass this just to change the map type
class CustomGoogleMapPlotter(gmplot.GoogleMapPlotter):
    def __init__(self, center_lat, center_lng, zoom, apikey='',
                 map_type='satellite'):
        super().__init__(center_lat, center_lng, zoom, apikey)

        self.map_type = map_type
        assert(self.map_type in ['roadmap', 'satellite', 'hybrid', 'terrain'])

    def write_map(self,  f):
        f.write('\t\tvar centerlatlng = new google.maps.LatLng(%f, %f);\n' %
                (self.center[0], self.center[1]))
        f.write('\t\tvar myOptions = {\n')
        f.write('\t\t\tzoom: %d,\n' % (self.zoom))
        f.write('\t\t\tcenter: centerlatlng,\n')

        # This is the only line we change
        f.write('\t\t\tmapTypeId: \'{}\'\n'.format(self.map_type))


        f.write('\t\t};\n')
        f.write(
            '\t\tvar map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);\n')
        f.write('\n')


class PlotGraph:
    @staticmethod
    def plotGraph(lat,long):
        gmap = CustomGoogleMapPlotter(lat,long,13)

        gmap.marker(lat,long, color='cornflowerblue')

        gmap.circle(lat,long, 5000, face_alpha = 0,edge_color='#ffffff', fc='#EAF6F6')

        return gmap


    @staticmethod 
    def mentionDistance(gmap,proposed_lat,proposed_long,lats,longs,filename,competitors_df):
        df = competitors_df
        location_coordinates_ = (proposed_lat, proposed_long)
        min_distant_location = geopy.distance.geodesic(location_coordinates_,(lats[0],longs[0])).km
        min_place = [((min_distant_location,str(df.iloc[0]['place_id'])))]
        for i in range(len(lats)):
            pump_loc = (lats[i],longs[i])
            distance_ = geopy.distance.geodesic(location_coordinates_, pump_loc).km
            min_place.append(((distance_,str(df.iloc[i]['place_id']))))
            gmap.marker(lats[i],longs[i],color='yellow',label='P', info_window="<a href="+df.iloc[i]['url']+">"+df.iloc[i]['name']+"</a>"+"<br>Dist: "+str(round(distance_,2))+" km")
        gmap.draw(filename)
        return min_place



