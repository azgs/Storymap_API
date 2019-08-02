#!/usr/bin/env python3

# test connection to DB
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
    cursor.execute('SELECT ST_AsGeoJSON(feature_id, map_id, feature_name, feature_picture, feature, CAST (x AS DOUBLE PRECISION), CAST (y AS DOUBLE PRECISION), wkid, geom) FROM api_tables.storymap_features WHERE feature_id=3 and TRUE')
    # cursor.execute('SELECT feature_id, map_id, feature_name, feature_picture, feature, CAST (x AS DOUBLE PRECISION), CAST (y AS DOUBLE PRECISION), wkid, geom FROM api_tables.storymap_features WHERE feature_id=3 and TRUE')
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





#printall()
# printone()
geom_testing()
