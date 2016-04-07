__author__ = 'shalini'

#audit.py
# audits postal code, street names as city names

import xml.etree.cElementTree as ET
from collections import defaultdict
import re


OSMFILE = "san-jose_california.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Circle", "Highway"]

# UPDATE THIS VARIABLE
mapping = {"St": "Street",
           "St.": "Street",
           "Rd": "Road",
           "Ave": "Avenue",
           "ave": "Avenue",
           "Blvd": "Boulevard",
           "Cir": "Circle",
           "Dr": "Drive",
           "Sq": "Square",
           "street": "Street",
           "Hwy": "Highway"}


def audit_street_type(street_types, street_name):
  m = street_type_re.search(street_name)
  if m:
    street_type = m.group()
    if street_type not in expected:
      street_types[street_type].add(street_name)


def is_street_name(elem):
  return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
  osm_file = open(osmfile, "r")
  street_types = defaultdict(set)
  for event, elem in ET.iterparse(osm_file, events=("start",)):

    if elem.tag == "node" or elem.tag == "way":
      for tag in elem.iter("tag"):
        if is_street_name(tag):
          audit_street_type(street_types, tag.attrib['v'])
  osm_file.close()
  return street_types
#print audit(OSMFILE)


#this is to update mapping to check if it updates correctly.
def update_name(name, mapping):
  name_list = name.split(" ")
  new_name_list = []
  for word in name_list:
    if word not in mapping.keys():
      new_name_list.append(word)
    else:
      new_name_list.append(mapping[word])
  name = " ".join(new_name_list)
  return name

st_types = audit(OSMFILE)
#print len(st_types) #56
#pprint.pprint(dict(st_types))
for st_type, ways in st_types.iteritems():
  for name in ways:
    better_name = update_name(name, mapping)


#city names audited the similar way as postcodes.
def is_post_code(elem):
  return (elem.attrib['k'] == "addr:postcode") #change to "addr:city" to audit city names.

def audit(osmfile):
  osm_file = open(osmfile, "r")
  post_code_types = {}
  for event, elem in ET.iterparse(osm_file, events=("start",)):

    if elem.tag == "node" or elem.tag == "way":
      for tag in elem.iter("tag"):
        if is_post_code(tag):
          current_postcode = tag.attrib['v']
          if current_postcode not in post_code_types:
            post_code_types[current_postcode] = 1
          else:
            post_code_types[current_postcode] += 1
  osm_file.close()
  return post_code_types