import transitfeed


#in memory representation of the gtfs file
def get_schedule_object(in_gtfs_path, message=True):
    if message == True:
      print "Please Wait, loading GTFS file into memory, this may take a hot minute."

    loader = transitfeed.Loader(in_gtfs_path)
    return loader.Load()


#provide a route short name and get a route_id in return
def get_route_id(in_schedule_object, route_short_name):
  route_list = in_schedule_object.GetRouteList()
  #to do: could enforce singularity by using any() or set() instead of [0] array
  return [ route['route_id'] for route in route_list if route['route_short_name'] == str(route_short_name) ][0]


#returns a trip_list of trip objects for a route
def get_trip_list(in_schedule_object, in_route_id):
  trip_list = in_schedule_object.GetTripList()
  return [trip for trip in trip_list if trip.route_id == str(in_route_id)]


#returns a list of stop ids, as strings, for a route, used for the method: get_stop_list
def get_stop_id_list(in_trip_list):
  stop_set = set()
  for trip in in_trip_list:
        stop_times = trip.GetStopTimes()
        for st in stop_times:
          stop_set.add(st.stop.stop_id)
  return stop_set

#returns a stop_list of stop dicts applicable to a list of trip objects
def get_stop_dict(in_schedule_object, in_trip_list):
  out = get_stop_list(in_schedule_object, in_trip_list)
  return stop_list_to_dict(out)


#returns a list of stop objects applicable to a list of trip objects
def get_stop_list(in_schedule_object, in_trip_list):
  stop_id_list = get_stop_id_list(in_trip_list)
  stop_list = in_schedule_object.GetStopList()
  out = [stop for stop in stop_list if stop.stop_id in stop_id_list]  
  return out


#this turns the stop list from objects into a simple dictionary limited to just the pertinant key,values
def stop_list_to_dict(in_stop_list):
  keys = list(in_stop_list[0].keys())
  out_list = []

  for stop in in_stop_list:
    out_dict = {}
    for key in keys:
      out_dict[key] = stop[key]
    out_list.append(out_dict)

  return out_list


#returns a list of shape objects corresponding to a list of trips
def get_shape_list(in_schedule_object, trip_list):
    #get an set of stings representing trip.shape_ids 
    trip_list = set(trip.shape_id for trip in trip_list)
    #get the shape list for the gtfs file
    shape_list = in_schedule_object.GetShapeList()
    #return shape objects corresponding to the shape id's from shape_list
    return [shape for shape in shape_list if shape.shape_id in trip_list]


#returns (unique) set of tuples of every coordinate contained in a list of shapes 
def get_coordinates(in_shape_list):
    out = set()
    for shape in in_shape_list:
      for point in shape.points:
        new_point = (point[0], point[1])
        out.add(new_point)
    return out

#just for testing, can be deleted
def test_seq():
   sched = get_schedule_object("../data/20150809V.zip")
   x = get_trip_list(sched, 9588)
   y = get_shape_list(sched,x)
   return y

















