from bs4 import BeautifulSoup
import utility_ops
import json



#returns a string with the basic framework of a new KML file
def new_kml():
	xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>'
	kml_declaration = '<kml xmlns="http://earth.google.com/kml/2.1">'
	doc_declarataion = '<Document></Document>'
	kml_close_tag =	   '</kml>'
	return xml_declaration + kml_declaration + doc_declarataion + kml_close_tag

#returns the string for a new folder inside of a kml file. 
def new_folder_string(name="new_folder"):
	return "<Folder><name>{0}</name></Folder>".format(name)

def new_folder(name="new_folder"):
	return BeautifulSoup(new_folder_string(name), "xml").Folder

#returns a string for a new placemark inside of a KML file
def new_placemark_string(name, description, longitude, latitude):
	name = "<name>{0}</name>".format(name)
	desc = "<description>{0}</description>".format(description)
	coor = "<Point><coordinates>{0},{1}</coordinates></Point>".format(longitude, latitude)
	out = "<Placemark>{0}{1}{2}</Placemark>".format(name, desc, coor)
	return out

def new_placemark(name, description, longitude, latitude):
	pmk = new_placemark_string(name, description, longitude, latitude)
	out = BeautifulSoup(pmk, "xml").Placemark
	return out

#input the name of the linestring and a list of coordinate tuples
def new_linestring_placemark(name, coord_list):
	name = "<name>{0}</name>".format(name)
	out_coords = ""
	for coord in coord_list:
		out_coords = out_coords + " " + "{0},{1}".format(coord[1], coord[0]) 
	coor = "<LineString><tessellate>1</tessellate><coordinates>{0}</coordinates></LineString>".format(out_coords)
	out = "<Placemark>{0}{1}</Placemark>".format(name, coor)
	return out


#converts a CSV with the columns: lat,lon, and name fields to a kml of placemarks. 
#ALso adds the entire row into xml or json in the description
#Optional paramers in case the column names in the csv are different
#Note: the CSV must have headers
#To do: add a path folder with a line all of the coordinates
def csv_to_kml(in_file_path, out_file_path, description_type="xml", name="name", lon="lon", lat="lat"):
	in_dict = utility_ops.csv_to_dict(in_file_path)

	kml_soup_obj = BeautifulSoup(new_kml() , "xml")
	folder = BeautifulSoup(new_folder("Points"), "xml").Folder
	kml_soup_obj.Document.append(folder)

	for item in in_dict:
		if description_type == "xml":
			description = utility_ops.dict_to_xml(item)
		elif description_type == "json":
			description = json.dumps(item)

		#create the placemark and append it to the parent stops folder
		pmk = new_placemark( item[name], description, item[lon], item[lat])
		pmk = BeautifulSoup(pmk, "xml").Placemark
		folder.append(pmk)

	out_kml_string = str(kml_soup_obj)
	utility_ops.text_to_file(out_kml_string, out_file_path)




