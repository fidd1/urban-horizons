import numpy as np
from sklearn.cluster import KMeans
import folium

# Function to separate passed attractions (but potentially also other categories that have location coordinates) in clusters
def loc_clustering(attractions, days_trip, intensity_trip):

    # Create a list of tuples with name and location of the places 
    places = []
    for name, info in attractions.items():
        location = info['loc']
        place = (name, location)
        places.append(place)
    
    # Limit places to the total number of attractions for the user (see Limitations in Documentation)
    max_places = days_trip * intensity_trip
    places = places[:max_places]

    # Use locations to create np array
    location_list = []
    for name, loc in places:
        location_list.append(loc)

    locations = np.array(location_list)

    # Clustering in n groups according to the number of days inputed
    kmeans = KMeans(n_clusters = days_trip)
    kmeans.fit(locations)
    clusters = kmeans.predict(locations) # create array with cluster indices and corresponding location

    # Create empty dictionary to store indices and related clustered places
    clustered_places = {} 
    for i in range(days_trip):
        clustered_places[i] = [] 
    
    for place, cluster in zip(places, clusters): 
        clustered_places[cluster].append(place) # appends to the cluster index the corresponding places information 

    return clustered_places

# Function to create maps to be later displayed
def create_maps(attractions, days_trip, intensity_trip):

    # Running clustering function with passed arguments
    clustered_places = loc_clustering(attractions, days_trip, intensity_trip)

    # Creating maps per each day
    maps = []
    day = 1  # initializing day counter
    for place in clustered_places.values(): # place will be a list of tuples having name of the attraction and its coordinates
        names, locs = zip(*place) # unpacking list to separate names and coordinates
        map_center = locs[0]
        map = folium.Map(location = map_center, zoom_start = 14) # center in first location and arbitrary zoom

        index = 1  # initializing index (number) counter
        numbered_names = []
        for name, loc in zip(names, locs):  # adding numbered folium Marker and appending numbered name of location
            folium.Marker(
                location = loc,
                popup = f'{index}. {name}',
                icon = folium.DivIcon(
                    html=f"""<div style="font-family: sans-serif; color: white; font-size: 15pt; background-color: red; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center;">{index}</div>"""
                    )
                    ).add_to(map)
    
            numbered_names.append(f"{index}. {name}")
            index += 1

        maps.append((map, numbered_names))
        day += 1

    return maps