#!/usr/bin/env python3

# test connection to DB
import json
import psycopg2
# import psycopg2.sql as sql

# Connect to database and establish cursor

def printall():
    connection = psycopg2.connect("dbname=storymap user=steve")
    cursor = connection.cursor()

    # Query the database 
    # returns = cursor.execute("SELECT * FROM api_tables.storymap_metadata ORDER BY map_id ASC;")
    returns = cursor.execute("SELECT * FROM api_tables.storymap_features CAST (x AS DOUBLE PRECISION)ORDER BY feature_id ASC;")
    a = True
    while (a):
        a = cursor.fetchone()
        print(a)
        print(" \n")

    # Close communication with the database
    cursor.close()
    connection.close()


# have to have the % to match surrounding things

def printone():

    connection = psycopg2.connect("dbname=storymap user=steve")
    cursor = connection.cursor()

    # Query the database 
    name = '%%'
    # cursor.execute('SELECT * FROM api_tables.storymap_features WHERE feature_id=3 and TRUE')
    cursor.execute('SELECT feature_id, map_id, feature_name, feature_picture, feature, CAST (x AS DOUBLE PRECISION), CAST (y AS DOUBLE PRECISION), wkid, geom FROM api_tables.storymap_features WHERE feature_id=3 and TRUE')
    # cursor.execute('SELECT * FROM api_tables.storymap_features WHERE name ILIKE %s and TRUE',  (name, ))
    # cursor.execute("SELECT * FROM api_tables.storymap_metadata WHERE name ILIKE '%San Pedro%'")
    # cursor.execute("SELECT * FROM api_tables.storymap_metadata WHERE name ILIKE %s", name)



# 
# cur.execute(
#     'INSERT INTO mytable (ip_id, item) VALUES (%s, %s)',
#     (1, 'someentry')
# )
    #cursor.execute("SELECT * FROM api_tables.storymap_metadata WHERE map_id = 2")
    # cursor.execute("SELECT * FROM api_tables.storymap_metadata WHERE name ILIKE %s" % name)
    # a = cursor.fetchall()
    a = 34
    while (a):
        a = cursor.fetchone()
        print("\n")
        print(a)
        print("\n")

    # Close communication with the database
    cursor.close()
    connection.close()

def geom_testing():

    connection = psycopg2.connect("dbname=storymap user=steve")
    cursor = connection.cursor()

    # Query the database 
    #name = '%%'
    # cursor.execute('SELECT * FROM api_tables.storymap_features WHERE feature_id=3 and TRUE')
    # cursor.execute('SELECT ST_AsGeoJSON(feature_id, map_id, feature_name, feature_picture, feature, CAST (x AS DOUBLE PRECISION), CAST (y AS DOUBLE PRECISION), wkid, geom) FROM api_tables.storymap_features WHERE feature_id=3 and TRUE')
    # cursor.execute('SELECT feature_id, map_id, feature_name, feature_picture, feature, CAST (x AS DOUBLE PRECISION), CAST (y AS DOUBLE PRECISION), wkid, geom FROM api_tables.storymap_features ')
    # cursor.execute('SELECT * FROM api_tables.storymap_features WHERE name ILIKE %s and TRUE',  (name, ))
    # cursor.execute("SELECT * FROM api_tables.storymap_metadata WHERE name ILIKE '%San Pedro%'")
    # cursor.execute("SELECT * FROM api_tables.storymap_metadata WHERE name ILIKE %s", name)
    #cursor.execute("SELECT array_to_json(array_agg(row_to_json(t)))  from ( SELECT * FROM api_tables.storymap_features WHERE feature_name ILIKE '%cotton%') t")




    # interesting option here to return JSON straight from the database
    # cursor.execute("SELECT array_to_json(array_agg(row_to_json(t)))  from ( SELECT * FROM api_tables.storymap_features WHERE feature_name ILIKE '%cotton%') t")
    # cursor.execute("SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type , ST_AsGeoJSON(lg.geog)::json As geometry , row_to_json((SELECT l FROM (SELECT loc_id, loc_name) As l)) As properties FROM locations As lg   ) As f )  As fc;")
#     cursor.execute("SELECT row_to_json(fc) \
#             FROM ( SELECT 'FeatureCollection' \
#             As type, array_to_json(array_agg(f)) \
#             As features \
#             FROM (SELECT 'Feature' As type , ST_AsGeoJSON(lg.geom)::json \
#             As geometry , row_to_json((SELECT l \
#             FROM (SELECT feature_id, map_id ) As l)) \
#             As properties FROM api_tables.storymap_features As lg   ) As f )  As fc;") 

#     cursor.execute("SELECT row_to_json(fc) \
#             FROM ( SELECT 'FeatureCollection' \
#             As type, array_to_json(array_agg(f)) \
#             As features \
#             FROM (SELECT 'Feature' As type , ST_AsGeoJSON(lg.geom)::json \
#             As geometry , row_to_json((SELECT l \
#             FROM (SELECT feature_id, map_id, feature_name, feature_picture, \
#             feature, x, y, wkid, geom  WHERE feature_id=121) As l)) \
#             As properties FROM api_tables.storymap_features As lg   ) As f )\
#             As fc;") 

    cursor.execute("SELECT feature_id, map_id, feature_name, \
            feature_picture, feature, CAST (x AS DOUBLE PRECISION), \
            CAST (y AS DOUBLE PRECISION), wkid, ST_AsGeoJSON(geom) \
            FROM api_tables.storymap_features \
            WHERE ST_Intersects (geom, ST_MakeEnvelope(-111, \
            30, -109, 32, 4326));")

#    cursor.execute("SELECT * from api_tables.storymap_features \
#            WHERE ST_Intersects (geom, ST_MakeEnvelope(-111, \
#            30, -109, 32, 4326));")
# 
#     cursor.execute("SELECT * from api_tables.storymap_features \
#             WHERE ST_Intersects (geom, ST_MakeEnvelope(-12477660, \
#             4311781, -12477650, 4311783, 102100));")
# 
# cur.execute(
#     'INSERT INTO mytable (ip_id, item) VALUES (%s, %s)',
#     (1, 'someentry')
# )
    #cursor.execute("SELECT * FROM api_tables.storymap_metadata WHERE map_id = 2")
    # cursor.execute("SELECT * FROM api_tables.storymap_metadata WHERE name ILIKE %s" % name)
    # a = cursor.fetchall()



#     a = cursor.fetchall()
#     print(a)
#     print(json.dumps(a))
#     return
# 
# 
# 
    a = 34
#     a = cursor.fetchall()
#     print(json.dumps(a))
#     return
    while (a):
        a = cursor.fetchone()
        print("\n")
        print(json.dumps(a))
        print("\n")

    # Close communication with the database
    cursor.close()
    connection.close()





#printall()
# printone()
geom_testing()
