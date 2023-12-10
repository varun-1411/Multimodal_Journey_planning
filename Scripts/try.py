import pandas as pd

# Load stop_times.txt, transfers.txt and trips.txt into Pandas DataFrames
stop_times = pd.read_csv('stop_times.txt')
transfers = pd.read_csv('transfers.txt')
trips = pd.read_csv('trips.txt')

# Define the origin and destination stops
origin_stop_id = 5002
dest_stop_id = 160

# Step 1: Get all the trips that start from the origin stop and end at any stop
origin_trips = trips[trips['trip_id'].isin(stop_times[stop_times['stop_id'] == origin_stop_id]['trip_id'])]

# Step 2: Get all the trips that start from any stop and end at the destination stop
dest_trips = trips[trips['trip_id'].isin(stop_times[stop_times['stop_id'] == dest_stop_id]['trip_id'])]

# Step 3: Find all stops that are transferable from the origin stop
transfer_stops = set(transfers[transfers['from_stop_id'] == origin_stop_id]['to_stop_id'])

# Initialize a list to store all journeys with one transfer
journeys = []

# Step 4: For each origin trip, find all stops that are transferable from the origin stop and also served by the trip
for _, origin_trip in origin_trips.iterrows():
    origin_stop_times = stop_times[stop_times['trip_id'] == origin_trip['trip_id']]
    origin_transfer_stops = set(origin_stop_times[origin_stop_times['stop_id'].isin(transfer_stops)]['stop_id'])

    # Step 5: For each destination trip, find all stops that are transferable to the destination stop and also served by the trip
    for _, dest_trip in dest_trips.iterrows():
        dest_stop_times = stop_times[stop_times['trip_id'] == dest_trip['trip_id']]
        dest_transfer_stops = set(dest_stop_times[dest_stop_times['stop_id'].isin(
            transfers[transfers['to_stop_id'] == dest_stop_id]['from_stop_id'])]['stop_id'])

        # Step 6: Check if there is a potential transfer point that is common to both sets of stops and is reachable within the transfer time specified in the transfer file
        common_transfer_stops = origin_transfer_stops.intersection(dest_transfer_stops)
        for transfer_stop in common_transfer_stops:
            transfer_time = \
            transfers[(transfers['from_stop_id'] == origin_stop_id) & (transfers['to_stop_id'] == transfer_stop)][
                'min_transfer_time'].values[0]
            dest_arrival_time = dest_stop_times[dest_stop_times['stop_id'] == dest_stop_id]['arrival_time'].values[0]
            origin_departure_time = \
            origin_stop_times[origin_stop_times['stop_id'] == origin_stop_id]['arrival_time'].values[0]
            if (dest_arrival_time - origin_departure_time <= transfer_time):
                journeys.append((origin_trip['trip_id'], transfer_stop, dest_trip['trip_id']))

# Print the list of journeys with one transfer
print(journeys)



# Function to get the trips that visit a given stop from a list of trips
def get_trips_for_stop(stop_id, trips):
    matching_trips = []
    for trip_id in trips:
        stop_times_for_trip = stop_times[stop_times['trip_id'] == trip_id]
        if stop_id in stop_times_for_trip['stop_id'].tolist():
            matching_trips.append(trip_id)
    return matching_trips
a = get_trips_for_stop(8308, trips_at_destination)

def get_stop_times_for_trip(trip_id):
    stop_times_for_trip = stop_times[stop_times['trip_id'] == trip_id]
    return stop_times_for_trip



compatible_trips = set()

for trip_id in trips_at_origin:
    trip_stops = get_stops_for_trip(trip_id) # implement this function to get the stops for a given trip ID
    for stop in trip_stops:
        if stop in transfer_dict:
            transfer_tuples = transfer_dict[stop]
            print(transfer_tuples)
            for transfer_tuple in transfer_tuples:
                transfer_to_stop_id = transfer_tuple[0]
                transfer_time = transfer_tuple[1]
                trips_to = get_trips_for_stop(transfer_to_stop_id, trips_at_destination) # implement this function to get the trips that visit a given stop from a list of trips
                print(trips_to)
                stop_times_to = get_stop_times_for_trip(trips_to[0][0]) # implement this function to get the stop times for a given trip ID
                stop_index_to = stop_times_to.index[stop_times_to['stop_id'] == transfer_to_stop_id][0]
                stop_time_to = stop_times_to.iloc[stop_index_to]
                arrival_time_to = stop_time_to['arrival_time']
                trips_from = get_trips_for_stop(stop, [trip_id]) # implement this function to get the trips that visit a given stop from a list of trips
                for trip_from in trips_from:
                        stop_times_from = get_stop_times_for_trip(trip_from) # implement this function to get the stop times for a given trip ID
                        stop_index_from = stop_times_from.index[stop_times_from['stop_id'] == stop][0]
                        stop_time_from = stop_times_from.iloc[stop_index_from]
                        departure_time_from = stop_time_from['arrival_time']
                        arrival_seconds_to = int(arrival_time_to[:2]) * 3600 + int(arrival_time_to[3:5]) * 60 + int(
                            arrival_time_to[6:])
                        departure_seconds_from = int(departure_time_from[:2]) * 3600 + int(departure_time_from[3:5]) * 60 + int(
                            departure_time_from[6:])

                        if (arrival_seconds_to - departure_seconds_from >= transfer_time):
                            compatible_trips.add((trip_from, trips_to[0]))


# compatible_trips now contains a set of tuples where each tuple contains the IDs of two compatible trips for a one-transfer journey



