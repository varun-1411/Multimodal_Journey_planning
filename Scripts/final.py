import pandas as pd
import datetime
import osmnx as ox
import networkx as nx

G = ox.graph_from_place("Bangalore India", network_type="drive")
stop_times = pd.read_csv("stop_times.txt")
trips = pd.read_csv("trips.txt")
transfers = pd.read_csv("transfers.txt").sort_values(by="from_stop_id")
stops = pd.read_csv("stops.txt")

stop_times["arrival_time"] = pd.to_datetime(stop_times["arrival_time"], errors="coerce")

origin_stop = 5002
destination_stop = 160
o = stops[(stops["stop_id"] == origin_stop)]
origin_lat = o["stop_lat"].iloc[0]
origin_long = o["stop_lon"].iloc[0]

o = stops[(stops["stop_id"] == destination_stop)]
destination_lat = o["stop_lat"].iloc[0]
destination_long = o["stop_lon"].iloc[0]

time_str = '16:15:32'
time_obj = datetime.datetime.strptime(time_str, '%H:%M:%S').replace(year=2019, month=10, day=15)

# Filter stop times
stop_times = stop_times[(stop_times["arrival_time"] >= time_obj)]
est = stop_times[(stop_times['stop_id'] == int(origin_stop))].sort_values(by="arrival_time")
first_arrival_time = est['arrival_time'].iloc[0]
stop_times = stop_times[stop_times["arrival_time"] >= first_arrival_time].reset_index()


# Get all trips that pass by the given stop at or after the given time
def get_trips_at_stop(stop_id, time_obj):
    trip_ids = stop_times[stop_times['stop_id'] == stop_id]['trip_id']
    return trip_ids


trips_at_origin = get_trips_at_stop(origin_stop, time_obj)
trips_at_destination = get_trips_at_stop(destination_stop, time_obj)

# Find common trips
common_trips = list(set(trips_at_destination) & set(trips_at_origin))

# Find direct trips
x = stop_times[(stop_times['trip_id'].isin(common_trips)) & (
        (stop_times['stop_id'] == origin_stop) | (stop_times['stop_id'] == destination_stop))]
x = x.sort_values('arrival_time')
for trip_id, group in x.groupby('trip_id', sort=False):
    if group.iloc[0]['arrival_time'] <= group.iloc[-1]['arrival_time']:
        print("Journey starts at", group.iloc[0]['arrival_time'], "at bus stop", group.iloc[0]['stop_id'],
              "and reaches bus stop", group.iloc[-1]['stop_id'], "at", group.iloc[-1]['arrival_time'])

# Find indirect trips (not implemented)

import datetime

time_obj = datetime.datetime.strptime('23:59:59', '%H:%M:%S')
fastest_time = time_obj.replace(year=2019, month=10, day=15)


def find_fastest_trip(trip_ids, stop_id):
    fastest_trip = None
    fastest_time = time_obj.replace(year=2019, month=10, day=15)
    for trip_id in trip_ids:
        stop_time = stop_times[stop_times['stop_id'] == stop_id].iloc[0]
        arrival_time = stop_time['arrival_time']
        if arrival_time < fastest_time:
            fastest_time = arrival_time
            fastest_trip = trip_id
    print(fastest_time)
    return fastest_trip


a = find_fastest_trip(trips_at_destination, destination_stop)

# Find transfer stops at destination
stop_times_for_trip = stop_times[stop_times['trip_id'] == a]
stops_dest = stop_times_for_trip['stop_id'].tolist()
transfer_at_dest = transfers[transfers["to_stop_id"].isin(stops_dest)]

# Find transfer stops at origin
stops_origin = set()
for trip_id in trips_at_origin:
    stop_times_for_trip = stop_times[stop_times['trip_id'] == trip_id]
    stops_origin.update(stop_times_for_trip['stop_id'].tolist())
unique_stops_origin = list(stops_origin)
transfer_at_origin = transfer_at_dest[transfer_at_dest["from_stop_id"].isin(unique_stops_origin)]

# Add stops of the trips that originate at origin
from_stop_ids = transfer_at_origin["from_stop_id"].tolist()

trips_with_from_stop = set()
for trip_id in trips_at_origin:
    stop_times_for_trip = stop_times[stop_times['trip_id'] == trip_id]
    for from_stop_id in from_stop_ids:
        if from_stop_id in stop_times_for_trip['stop_id'].tolist():
            trips_with_from_stop.add(trip_id)


def get_stops_for_trip(trip_id):
    # Load stop_times.txt into a Pandas DataFrame
    # Filter the rows that have the given trip_id
    stops_for_trip = stop_times.loc[stop_times['trip_id'] == trip_id, 'stop_id']

    # Convert the resulting Series to a list and return it
    return list(stops_for_trip)


# For each trip originating at the origin stop, find any transfers needed and print out the route information
for trip_id in trips_at_origin:
    trip_stops = get_stops_for_trip(trip_id)
    start_time = stop_times.loc[
        (stop_times['trip_id'] == trip_id) & (stop_times['stop_id'] == int(origin_stop)), 'arrival_time'].iloc[0]
    # reach_time = stop_times.loc[
    #     (stop_times['trip_id'] == a) & (stop_times['stop_id'] == int(destination_stop)), 'arrival_time'].iloc[0]
    for stop in trip_stops:
        if stop in transfer_at_origin["from_stop_id"].tolist():
            from_stop = stop
            to_stop = transfer_at_origin[transfer_at_origin["from_stop_id"] == int(stop)]["to_stop_id"].iloc[0]
            time = transfer_at_origin[transfer_at_origin["from_stop_id"] == int(stop)]["min_transfer_time"].iloc[0]
            arrival_subset = stop_times.loc[
                (stop_times['trip_id'] == trip_id) & (stop_times['stop_id'] == from_stop) & (
                        stop_times['arrival_time'] >= start_time), 'arrival_time']
            arrival = 0
            if len(arrival_subset) > 0:
                arrival = arrival_subset.iloc[0]
            departure = \
                stop_times.loc[(stop_times['trip_id'] == a) & (stop_times['stop_id'] == to_stop), 'arrival_time'].iloc[
                    0]

            if arrival != 0 and (arrival + datetime.timedelta(seconds=int(time)) <= departure):
                if int(to_stop) == int(destination_stop):
                    print("start at", origin_stop, "at", start_time, "reach at", from_stop, "at", arrival,
                          "transfer from",
                          from_stop, "to", to_stop, "by walking for", time, "seconds and reach at",
                          arrival + datetime.timedelta(seconds=int(time)))
                else:
                    subset = stop_times.loc[
                        (stop_times['trip_id'] == a) & (stop_times['stop_id'] == int(destination_stop)) & (
                                stop_times['arrival_time'] >= departure), 'arrival_time']
                    if len(subset) > 0:
                        reach_time = subset.iloc[0]
                        # print("re",reach_time)
                        print("start at", origin_stop, "at", start_time, "reach at", arrival, "transfer from",
                              from_stop,
                              "to", to_stop, "by walking for", time, "seconds and reach at", destination_stop, "at",
                              reach_time)

# ----------------------------------------
df = stops.drop_duplicates(subset=['stop_id'])
li1 = []
for idd, row in df.iterrows():
    li1.append((row.stop_id, row.stop_lon, row.stop_lat))

stop_node = {}
for i in range(len(li1)):
    stop_node[li1[i][0]] = ox.nearest_nodes(G, li1[i][1], li1[i][2])

distance = {}

for i in stop_node:
    distance[i] = {}
    for j in stop_node:
        distance[i][j] = (
            nx.shortest_path_length(G, source=stop_node[i], target=stop_node[j], weight='length', method='dijkstra'))


