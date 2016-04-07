__author__ = 'shalini'
#preparing for databases, have cleaned street names, postcode names and city names
#data.py
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

post_code_hypen = re.compile(r'([0-9]){5}\-([0-9]){4}')
post_code_city = re.compile(r'([A-Z]){2}\ ([0-9]){5}')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


mapping = {"St": "Street",
           "St.": "Street",
           "Rd": "Road",
           "Ave": "Avenue",
           "Blvd": "Boulevard",
           "Cir": "Circle",
           "Dr": "Drive",
           "Sq": "Square",
           "street": "Street",
           "Hwy": "Highway"}

mapping_city = {"Campbelll": "Campbell",
                "campbell": "Campbell",
                "cupertino": "Cupertino",
                "san Jose": "San Jose",
                "san jose": "San Jose",
                "San jose": "San Jose",
                "Santa clara": "Santa Clara",
                "santa clara": "Santa Clara",
                "santa Clara": "Santa Clara",
                "Los Gato": "Los Gatos",
                "Los Gatos, CA": "Los Gatos",
                "SUnnyvale": "Sunnyvale",
                "Sunnyvale, CA": "Sunnyvale",
                "sunnyvale": "Sunnyvale"}


def update_street_name(name, mapping):
  name_list = name.split(" ")
  new_name_list = []
  for word in name_list:
    if word not in mapping.keys():
      new_name_list.append(word)
    else:
      new_name_list.append(mapping[word])
  name = " ".join(new_name_list)
  return name

#fixing postal codes
def update_post_code(name):
  if len(name) >5:
    p1 = post_code_hypen.search(name)
    p2 = post_code_city.search(name)
    if p1:
      new_name = p1.group()
      name = (new_name.split("-"))[0]
    elif p2:
      new_name = p2.group()
      name = (new_name.split(" "))[1]
    else:
      name = name
  return name

#to update city names as per the mapping dictionary above
def update_city_name(name,mapping):
  if name not in mapping:
    new_name = name
  else:
    new_name = mapping[name]
  return new_name

def shape_element(element):
  node = {}
  if element.tag == "node" or element.tag == "way" :
    # YOUR CODE HERE

    node['created'] = {}
    node['type'] = element.tag
    node['pos'] = []
    address = {}
    node['node_refs'] = []
    for each_key in element.attrib.keys():
      if each_key in CREATED:
        node['created'][each_key] = element.attrib[each_key]
      elif each_key == 'lat' or each_key == 'lon':
        node['pos'].append(float(element.attrib[each_key]))
      else:
        node[each_key] = element.attrib[each_key]
    for child in element.iter('nd'):
      nd_ref = child.attrib['ref']
      node['node_refs'].append(nd_ref)
    for child in element.iter('tag'):
      k_value = child.attrib['k']
      if problemchars.match(k_value):
        pass
      elif lower_colon.match(k_value) and k_value[:5] == "addr:":
        if k_value[5:] == "street":
          address['street'] = update_street_name(child.attrib['v'], mapping)
        elif k_value[5:] == "postcode":
          address['postcode'] = update_post_code(child.attrib['v'])
        elif k_value[5:] == "city":
          address['city'] = update_city_name(child.attrib['v'],mapping_city)
        else:
          address[k_value[5:]] = child.attrib['v']
      else:
        node[child.attrib['k']] = child.attrib['v']
    if address:
      node['address'] = address
    #print node
    return node
  else:
    return None


def process_map(file_in, pretty = False):
  # You do not need to change this file
  file_out = "{0}.json".format(file_in)
  data = []
  with codecs.open(file_out, "w","utf-8") as fo:
    for _, element in ET.iterparse(file_in):
      el = shape_element(element)
      if el:
        data.append(el)
        if pretty:
          fo.write(json.dumps(el, indent=2)+"\n")
        else:
          fo.write(json.dumps(el) + "\n")
  return data

data = process_map('san-jose_california.osm',False)
#pprint.pprint(data)
