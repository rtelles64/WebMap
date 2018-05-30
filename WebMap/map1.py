import folium # an external python library to do this project
import pandas

data = pandas.read_csv("Volcanoes_USA.txt") # loads volcanoes data
lat = list(data["LAT"]) # creates a list with latitudes from LON column
lon = list(data["LON"]) # creates a list with longitudes from LAT column
elev = list(data["ELEV"])

def color_producer(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "red"

# Note: Map.location takes in parameter (Northing, Easting) hence the (-) val
# Here we pass coordinates to SF

map = folium.Map(location = [37.7749, -122.4194], zoom_start = 6, \
                 tiles = "Mapbox Bright") # the last one changes the background


# it is suggested to create a feature group to keep code more organized
fgv = folium.FeatureGroup(name = "Volcanoes")
# add a marker to the Map (i.e. popups)
# one way to add multiple markers is to make multiple folium.Marker statements
# or, as we know, we can use a for loop!
# for coordinates in [[37.8, -122.5],[38.8, -120.5]]:
# given lat and lon above, the above for loop is not useful
# instead we use the one below
for lt, ln, el in zip(lat, lon, elev): # double iteration for loop!
    '''
    This format no longer legible either:
    fg.add_child(folium.Marker(location = coordinates, \
                                popup = "Hi I am a Marker",\
                                icon = folium.Icon(color = "green")))
    '''
    fgv.add_child(folium.CircleMarker(location = [lt, ln], radius = 6, \
                              popup = str(el) + " m", \
                              fill_color = color_producer(el), color = "grey", \
                              fill_opacity = 0.7, fill = True))

fgp = folium.FeatureGroup(name = "Population")
# adding polygons and change colors of the polygons
fgp.add_child(folium.GeoJson(data = open("world.json", 'r', \
                            encoding = "utf-8-sig").read(), \
                            style_function = lambda x: {"fillColor":"green" \
                            if x["properties"]["POP2005"] < 10000000 else "orange" \
                            if 10000000 <= x["properties"]["POP2005"] < 20000000 \
                            else "red"}))

map.add_child(fgv)
map.add_child(fgp)
# this order is important!
map.add_child(folium.LayerControl())

map.save("Map1.html")
