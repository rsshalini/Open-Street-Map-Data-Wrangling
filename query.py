#query.py
#mongoimport -d test -c sanjose --file san-jose_california.osm.json
#PyMongo Queries

def get_db(db_name):
  from pymongo import MongoClient
  client = MongoClient('localhost:27017')
  db = client[db_name]
  return db

#Displays the street, postcode and city counts.
def pipeline_address():
  pipeline = [
    {"$group": { "_id": "$address.street",  #can be changed to postcode or city
                  "count": {"$sum":1}}},
    {"$sort": {"count": -1}}
  ]
  return pipeline

#Displays number of posts each user made (from 1 to 5) and the number of users
def pipeline_onepost():
  pipeline = [
    {"$group":{"_id": "$created.user",
              "count":{"$sum":1}}},
    {"$group":{"_id": "$count",
              "num_users":{"$sum":1}}},
    {"$sort":{"_id":1}},
    {"$limit":5}]

  return pipeline

#top five contributors
def pipeline_top_contributors():
  pipeline = [
    {"$group": {"_id":"$created.user",
                  "count": {"$sum":1}}},
    {"$sort":{"count":-1}},
    {"$limit":5}]

  return pipeline


# gives different types of amenities
def pipeline_amenities_type():
  pipeline = [
    {"$match": {"amenity": {"$ne": None}}},
    {"$group": {"_id": "$amenity",
                "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}]
  return pipeline

# top cuisine
def pipeline_cuisine_type():
  pipeline =[
    {"$match": {"$and": [{"amenity": {"$eq": "restaurant"}}, {"cuisine": {"$ne": None}}]}},
    {"$group": {"_id": "$cuisine",
                "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}]
  return pipeline

def results(db,pipeline):
  return [doc for doc in db.sanjose.aggregate(pipeline)]



def node_query():
  query = {"type":"node"}
  return query

def way_query():
  query = {"type":"way"}
  return query

def find_query(db,query):
  return db.sanjose.find(query)

if __name__ == "__main__":
  db = get_db('test')

  # pipeline = pipeline_amenities_type()
  # amenities_type = results(db, pipeline)

  #pipeline = pipeline_cuisine_type()
  #cuisine_type = results(db, pipeline)

  # pipeline = pipeline_address()
  # address_attribute = results(db, pipeline)
  #
  # pipeline = pipeline_onepost()
  # one_post = results(db, pipeline)
  #
  pipeline = pipeline_top_contributors()
  top_five_contributors = results(db, pipeline)

  import pprint
  #pprint.pprint(cuisine_type)
  #pprint.pprint(amenities_type)
  pprint.pprint(top_five_contributors)
  #pprint.pprint(one_post)
  #pprint.pprint(address_attribute)


  node_count = find_query(db,node_query()).count()
  #print node_count
  way_count = find_query(db,way_query()).count()
  #print way_count






