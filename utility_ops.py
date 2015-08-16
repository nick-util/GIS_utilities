import csv
import transitfeed
import os


#Loads a CSV file into a dictionary list. 
#NOTE:Requires HEADERS in the csv file!
def csv_to_dict_list(in_file_path):
  z=[]
  with open(in_file_path, 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      z.append(row)
  return z


def load_file_to_string(in_file_path):
    file_object = open(in_file_path)
    file_text = file.read(file_object)
    return file_text

#outputs a string to a file
def string_to_file(in_string, out_file_path):
    with open(out_file_path, "w") as text_file:
      text_file.write(in_string)


#outputs a list of dictionarys to a CSV file.
def dict_list_to_csv(in_list, out_file_path="output.csv"):
  with open(out_file_path, 'w') as csvfile:
    fieldnames = in_list[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    for item in in_list:
      writer.writerow( item )  

#creates a folder
def create_folder(folder_path):
  if not os.path.isdir(folder_path):
     os.makedirs(folder_path)

#test if a string is empty or blank and if so return a default out_String
def isBlank (my_string, out_string="??"):
    if my_string and my_string.strip():
        #myString is not None AND myString is not empty or blank
        return my_string
    #myString is None OR myString is empty or blank
    return out_string


#Convert a key,value pair to xml.  
#Optional: Include a second paramter to wrap the xml in a parent element
def dict_to_xml(in_dict, parent_element_name=False):
  out_string = ""
  for key,value in in_dict.items():
    out_string = out_string + "<{0}>{1}</{0}>".format(key, value) 
  if parent_element_name == False:
    return out_string
  else:
    return "<{0}>{1}</{0}>".format(parent_element_name, out_string)

