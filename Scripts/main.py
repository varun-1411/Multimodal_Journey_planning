import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Load GeoJSON file as a GeoDataFrame
gdf = gpd.read_file('bangalore_wards.json')
# uber_data = pd.read_csv("bangalore-wards-2020-1-All-DatesByHourBucketsAggregate.csv")
uber_data = pd.read_csv("bangalore-wards-2018-1-All-HourlyAggregate.csv")
# Plot the GeoDataFrame
gdf.plot()

# Show the plot
plt.show()

import json
from shapely.geometry import shape, Point

# Load GeoJSON data
with open('bangalore_wards.json') as f:
    data = json.load(f)

# Sample point
point = Point(77.505573, 12.969722)  # longitude, latitude
import final


def find_ward(point):
    for feature in data['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            ward_no = feature['properties']['WARD_NO']
            ward_name = feature['properties']['WARD_NAME']
            print(f"The point lies in Ward Number {ward_no}")
            print(f"The point lies in Ward Number {ward_name}")
            return int(ward_no), ward_name
            break
        elif polygon.touches(point):
            ward_no = feature['properties']['WARD_NO']
            ward_name = feature['properties']['WARD_NAME']
            print(f"The point lies in Ward Number {ward_no}")
            print(f"The point lies in Ward Number {ward_name}")
            return int(ward_no), ward_name
            break
    else:
        print("Point does not lie inside any polygon")


# This is an implementation of the "point in polygon" algorithm using ray casting. The algorithm works by casting a
# horizontal ray from the point to the right and counting how many times the ray intersects with the edges of the
# polygon. If the number of intersections is odd, then the point is inside the polygon. If it is even, the point is
# outside the polygon.

origin = Point( origin_long, origin_lat)
destination = Point( destination_long,destination_lat)
time = int(input("Enter time of depature in terms of hour of the day"))
month = int(input("enter month of travel"))
day = int(input("enter day of travel"))
time = 16
month = 1
day = 18
# origin = Point(77.64719738, 12.976004656)
# destination = Point(77.59719395, 12.91684059)
origin_zone, o = find_ward(origin)
destination_zone, d = find_ward(destination)

journey_time = (uber_data["sourceid"] == origin_zone) & (uber_data["dstid"] == destination_zone) & (uber_data[
                                                                                                        "month"] == month) & (
                           uber_data["start_hour"] <= time) & (uber_data["end_hour"] >= time) & (
                           uber_data["day"] == day)
# journey_time = (uber_data["sourceid"] == origin_zone) & (uber_data["dstid"] == destination_zone)  & (
                           # uber_data["start_hour"] <= time) & (uber_data["end_hour"] >= time)
journey_time = uber_data[journey_time].reset_index()
value = journey_time.at[0, 'mean_travel_time'] / 60
# journey_time = journey_time["mean_travel_time"] / 60
# pd.to_numeric(journey_time["mean_travel_time"])

print("waiting time is 6 minutes and Approximate time to reach by uber is", value , "minutes")

# --------------------------------------------------------------------------------------------

routes = pd.read_csv("BMTC/route_point.csv")
unique_values = routes["route_id"].unique()
stop_times = pd.read_csv("stop_times.txt")
stop_times["arrival_time"] = pd.to_datetime(stop_times["arrival_time"],errors = "coerce")
stop_times["departure_time"] = pd.to_datetime(stop_times["departure_time"],errors = "coerce")

# Create transfers dataframe
transfers = pd.merge(stop_times, stop_times, on='trip_id')
transfers = transfers[transfers['stop_sequence_x'] < transfers['stop_sequence_y']]
transfers = transfers.rename(columns={'stop_id_x': 'from_stop_id', 'stop_id_y': 'to_stop_id'})
transfers['transfer_time'] = transfers['departure_time_y'] - transfers['arrival_time_x']

def generate_transfer_patterns(from_stop_id, to_stop_id):
    transfer_options = transfers[(transfers['from_stop_id'] == from_stop_id) & (transfers['to_stop_id'] == to_stop_id)]
    transfer_options = transfer_options[['trip_id', 'arrival_time_x', 'departure_time_y', 'transfer_time']]
    transfer_patterns = transfer_options.groupby(['arrival_time_x', 'departure_time_y']).agg({'trip_id': 'count', 'transfer_time': 'mean'})
    transfer_patterns = transfer_patterns.reset_index()
    return transfer_patterns

origin_stop_id = '3004'
destination_stop_id = '6012'
transfer_patterns = generate_transfer_patterns(origin_stop_id, destination_stop_id)