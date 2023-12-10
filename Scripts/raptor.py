import pandas as pd
# from datetime import datetime, timedelta
import datetime

stop_times = pd.read_csv("stop_times.txt")
trips = pd.read_csv("trips.txt")
stop_times["arrival_time"] = pd.to_datetime(stop_times["arrival_time"], errors="coerce")
transfers = pd.read_csv("transfers.txt").sort_values(by="from_stop_id")
# stop_times["departure_time"] = pd.to_datetime(stop_times["departure_time"], errors="coerce")
origin_stop = 5002
destination_stop = 765

# type(transfers["from_stop_id"][10])

# Identify round trips
# round_trip_ids = []
# for trip_id, group in stop_times.groupby('trip_id'):
#     if group.iloc[0]['stop_id'] == group.iloc[-1]['stop_id']:
#         round_trip_ids.append(trip_id)

# Remove last stop from round trips
# stop_times = stop_times[~stop_times['trip_id'].isin(round_trip_ids)]
time_obj = datetime.datetime.strptime('16:15:32', '%H:%M:%S')
time_obj = time_obj.replace(year=2019, month=10, day=15)
stop_times = stop_times[stop_times["arrival_time"] >= time_obj].reset_index()
# l = stop_times[(stop_times['stop_id'] == int(origin_stop))]
est = stop_times[(stop_times['stop_id'] == int(origin_stop))].sort_values(by="arrival_time")
first_arrival_time = est['arrival_time'].iloc[0]
# stop_times = stop_times[stop_times["arrival_time"] >= first_arrival_time].reset_index()


def get_trips_at_stop(stop_id, time_str, trips_df, stop_times_df):
    # Get all trips that pass by the given stop at or after the given time
    time_obj = datetime.datetime.strptime(time_str, '%H:%M:%S')
    time_obj = time_obj.replace(year=2019, month=10, day=15)
    print(time_obj)
    trip_ids = stop_times_df[(stop_times_df['stop_id'] == int(stop_id))]['trip_id']
    # trip_ids = stop_times_df[(stop_times_df['stop_id'] == stop_id) & (stop_times_df['departure_time'] >= time_obj)]
    # trips = trips_df[trips_df['trip_id'].isin(trip_ids)]
    return trip_ids


def get_trips_at_dest_stop(stop_id, time_str, trips_df, stop_times_df):
    # Get all trips that pass by the given stop at or after the given time
    time_obj = datetime.datetime.strptime(time_str, '%H:%M:%S')
    time_obj = time_obj.replace(year=2019, month=10, day=15)
    trip_ids = stop_times_df[(stop_times_df['stop_id'] == int(stop_id))]['trip_id']
    # t = stop_times_df[(stop_times_df['stop_id'] == stop_id) & (stop_times_df['arrival_time'] >= time_str)]
    # trips = trips_df[trips_df['trip_id'].isin(trip_ids)]
    return trip_ids


trips_at_origin = get_trips_at_stop(origin_stop, '16:15:32', trips, stop_times)

# clean_stop_times_df_at_origin = stop_times[
#     stop_times['trip_id'].isin(trips_at_origin["trip_id"]) & stop_times['departure_time'] >= '16:15:32']
trips_at_destination = get_trips_at_dest_stop(destination_stop, '16:15:32', trips, stop_times)
# stop_times_df_at_dest = stop_times[stop_times['trip_id'].isin(trips_at_destination)]

""" for no transfers """

common_trips = list(set(trips_at_destination) & set(trips_at_origin))
x = stop_times[(stop_times['trip_id'].isin(common_trips)) & (
        (stop_times['stop_id'] == int(origin_stop)) | (stop_times['stop_id'] == int(destination_stop)))]
x = x.sort_values('arrival_time')
for trip_id, group in x.groupby('trip_id', sort=False):
    # group = group.sort_values('departure_time')
    if group.iloc[0]['arrival_time'] <= group.iloc[-1]['arrival_time']:
        print("journey starts at", group.iloc[0]['arrival_time'], " at bus stop ", group.iloc[0]['stop_id'], "and "
                                                                                                             "reach "
                                                                                                             "bus "
                                                                                                             "stop ",
              group.iloc[-1]['stop_id'], "at ", group.iloc[-1]['arrival_time'])
        # round_trip_ids.append(trip_id)

"""if there is no direct trip"""
# trips_origin = trips[trips["trip_id"].isin(trips_at_origin)]
# unique_routes_origin = trips_origin.drop_duplicates(subset=["route_id"])
# mask = unique_routes_origin["trip_id"].isin(common_trips)
# trips_origin = unique_routes_origin[~mask]
# # Merge the stop times with the filtered trips
# route_stop_times_origin = pd.merge(stop_times, trips_origin, on='trip_id')
# # Get the unique stop IDs for the route
# route_stop_ids_origin = route_stop_times_origin['stop_id'].unique().tolist()
#
# trips_dest = trips[trips["trip_id"].isin(trips_at_destination)]
# unique_routes_dest = trips_origin.drop_duplicates(subset=["route_id"])
# mask = unique_routes_dest["trip_id"].isin(common_trips)
# unique_routes_dest = unique_routes_dest[~mask]
# # unique_routes_destination = trips_origin.drop_duplicates(subset=["route_id"])
# # Optionally, get additional information about each stop
# # route_stops = stops[stops['stop_id'].isin(route_stop_ids)]
# route_stop_times_destination = pd.merge(stop_times, trips_dest, on='trip_id')
#
# # Get the unique stop IDs for the route
# route_stop_ids_dest = route_stop_times_destination['stop_id'].unique().tolist()
#
# common_stops = list(set(route_stop_ids_dest) & set(route_stop_ids_origin))
# common_stops.sort()
#
# # transfers at any point
# transfer_at_origin = transfers[transfers["from_stop_id"].isin(route_stop_ids_origin)]
# transfer_at_origin = transfer_at_origin[transfer_at_origin["to_stop_id"].isin(route_stop_ids_dest)]
# transfer_stops_origin = transfer_at_origin["from_stop_id"].unique().tolist()
# transfer_stops_dest = transfer_at_origin["to_stop_id"].unique().tolist()
# pairs = transfer_at_origin.groupby[transfer_at_origin["from_stop_id"]]
#
# transfer_dict = {}
# for _, row in transfer_at_origin.iterrows():
#     from_stop_id = row['from_stop_id']
#     to_stop_id = row['to_stop_id']
#     transfer_time = row['min_transfer_time']
#
#     # If the from_stop_id is not in the dictionary yet, add it as a key with an empty list as the value
#     if from_stop_id not in transfer_dict:
#         transfer_dict[from_stop_id] = []
#
#     # Append a tuple containing the to_stop_id and transfer_time to the list for the from_stop_id key
#     transfer_dict[from_stop_id].append((to_stop_id, transfer_time))



# time_since_midnight = dt_obj - dt_obj.replace(hour=0, minute=0, second=0, microsecond=0)
# total_seconds = time_since_midnight.total_seconds()

time_obj = datetime.datetime.strptime('23:59:59', '%H:%M:%S')
fastest_time = time_obj.replace(year=2019, month=10, day=15)


def find_fastest_trip(trip_ids, stop_id):
    fastest_trip = None
    fastest_time = time_obj.replace(year=2019, month=10, day=15)
    for trip_id in trip_ids:
        # print(trip_id)
        stop_time = stop_times[stop_times['stop_id'] == stop_id].iloc[0]
        # print(stop_time)
        arrival_time = stop_time['arrival_time']
        # print(arrival_time)
        # arrival_seconds = int(arrival_time[:2]) * 3600 + int(arrival_time[3:5]) * 60 + int(arrival_time[6:])
        if arrival_time < fastest_time:
            fastest_time = arrival_time
            fastest_trip = trip_id
            print(fastest_trip)
    return fastest_trip


a = find_fastest_trip(trips_at_destination, destination_stop)
"""destination fastest route"""
stops_dest = []
stop_times_for_trip = stop_times[stop_times['trip_id'] == a]
stops_dest = stop_times_for_trip['stop_id'].tolist()
transfer_at_dest = transfers[transfers["to_stop_id"].isin(stops_dest)]

"""origin route"""
stops_origin = set()  # create a set to hold unique stop ids
for trip_id in trips_at_origin:
    stop_times_for_trip = stop_times[stop_times['trip_id'] == trip_id]
    stops_origin.update(stop_times_for_trip['stop_id'].tolist())
unique_stops_origin = list(stops_origin)

transfer_at_origin = transfer_at_dest[transfer_at_dest["from_stop_id"].isin(unique_stops_origin)]


""" to add trips that are originating at origin"""
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

for trip_id in trips_at_origin:
    trip_stops = get_stops_for_trip(trip_id) # implement this function to get the stops for a given trip ID
    start_time = stop_times.loc[(stop_times['trip_id'] == trip_id) & (stop_times['stop_id'] == int(origin_stop)), 'arrival_time'].iloc[0]
    reach_time = stop_times.loc[(stop_times['trip_id'] == a) & (stop_times['stop_id'] == int(destination_stop)), 'arrival_time'].iloc[0]
    for stop in trip_stops:
        # print(stop)
        if stop in transfer_at_origin["from_stop_id"].tolist():
            from_stop = stop
            # print(from_stop)
            to_stop = transfer_at_origin[transfer_at_origin["from_stop_id"]==int(stop)]["to_stop_id"].iloc[0]
            time = transfer_at_origin[transfer_at_origin["from_stop_id"]==int(stop)]["min_transfer_time"].iloc[0]
            # print("stop",to_stop)
            # time = datetime.timedelta(seconds=int(time))
            # print("time",time)
            departure = stop_times.loc[(stop_times['trip_id'] == trip_id) & (stop_times['stop_id'] == from_stop), 'arrival_time'].iloc[0]
            # print("d",departure)
            arrival = stop_times.loc[(stop_times['trip_id'] == a) & (stop_times['stop_id'] == to_stop), 'arrival_time'].iloc[0]
            # print("a",arrival)

            if departure + datetime.timedelta(seconds=int(time))<= arrival:
                if int(to_stop) == int(destination_stop):
                    print("start at ", origin_stop, "at", start_time, "reach at",from_stop,"at", departure, "transfer from ",
                          from_stop, "to", to_stop, "by walking for", time, "seconds and reach at",arrival)
                else:
                    print("start at ",origin_stop,"at",start_time,"reach at",departure,"transfer from ",from_stop, "to",to_stop,"by walking for",time,"seconds and reach at",destination_stop,"at",reach_time )







# compatible_trips = set()
#
# for trip_id in trips_at_origin:
#     trip_stops = get_stops_for_trip(trip_id) # implement this function to get the stops for a given trip ID
#     for stop in trip_stops:
#         if stop in transfer_dict:
#             transfer_tuples = transfer_dict[stop]
#             print(transfer_tuples)
#             for transfer_tuple in transfer_tuples:
#                 transfer_to_stop_id = transfer_tuple[0]
#                 transfer_time = transfer_tuple[1]
#                 trips_to = a
#                 print(trips_to)
#                 stop_times_to = get_stop_times_for_trip(
#                     trips_to[0][0])  # implement this function to get the stop times for a given trip ID
#                 stop_index_to = stop_times_to.index[stop_times_to['stop_id'] == transfer_to_stop_id][0]
#                 stop_time_to = stop_times_to.iloc[stop_index_to]
#                 arrival_time_to = stop_time_to['arrival_time']
#                 trips_from = get_trips_for_stop(stop, [trip_id])
