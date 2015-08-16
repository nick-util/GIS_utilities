import transitfeed
import csv
import subprocess
import os
from  lib.transitfeed.kmlwriter import *



#description: explodes a multi route gtfs file into single gtfs files and kml files of its constituent routes.
#inputs: multi route gtfs file
#outputs: one gtfs file per route, and one kml file per route, all located in the specified out_directory
def explode_gtfs_file(in_gtfs_path, out_directory):
  schedule = get_schedule_object(in_gtfs_path)
  #checks if dir exists, if not makes it
  if not os.path.exists(out_directory): os.makedirs(out_directory)
  routes = get_routes(schedule)
  for route in routes:
    print routes

  for route in routes:
    out_path = out_directory + "/" + route 
    extract_single_route(route, in_gtfs_path, out_path + ".zip")
    single_gtfs_schedule = get_schedule_object(out_path + ".zip" , False)
    convert_gtfs_to_kml(single_gtfs_schedule, out_path + ".kml"  )


#description: takes a gtfs as input and outputs a single route as a gtfs file
#inputs: a gtfs file with at least one route
#outputs: a single route gtfs file 
def extract_single_route(route_number, in_gtfs_path, out_gtfs_path, string=False):
  transform = "{{\"op\":\"retain\", \"match\":{{\"file\":\"routes.txt\", \"route_short_name\":\"{0}\"}}}}".format(route_number)
  in_file = in_gtfs_path
  out_file =  out_gtfs_path
  command = "java -jar lib/onebus.jar --transform='{0}' {1} {2}".format(transform, in_file, out_file)
  print "Outputting route {0}".format(route_number)
  if string == True:
    print command
  else: 
    print subprocess.call(command , shell=True)


#takes a transitfeed schedule object from get_schedule_object 
#input: transitfeed get_schedule_object 
#output: A KML file
def convert_gtfs_to_kml(in_schedule_object, output_name="gtfs_to_kml_output.kml"):
  kml_writer = KMLWriter()
  kml_writer.Write(in_schedule_object, output_name)



#in memory representation of the full gtfs file
def get_schedule_object(in_gtfs_path, message=True):
    if message == True:
      print "Please Wait, loading GTFS file, this may take a hot minute."

    loader = transitfeed.Loader(in_gtfs_path)
    return loader.Load()



#simply returns an string list of all the routes in a gtfs file
def get_routes(in_schedule_object, to_string=False):
  routes = in_schedule_object.GetRouteList()
  out = []
  for item in routes:
    if to_string == True:
      print item.route_short_name
    else:
      out.append(item.route_short_name)
  return out
