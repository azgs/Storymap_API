#!/usr/bin/env python3

# test connection to DB
import psycopg2
import psycopg2.sql as sql

# Connect to database and establish cursor
connection = psycopg2.connect("dbname=storymap user=postgres")
cursor = connection.cursor()



def printall():
    # Query the database 
    cursor.execute("SELECT * FROM api_tables.storymap_metadata")
    # a = cursor.fetchall()
    a = 34
    while (a):
        a = cursor.fetchone()
        print(a)
        print(" \n")

    # Close communication with the database
    cursor.close()
    connection.close()


# have to have the % to match surrounding things

def printonename():
    # Query the database 
    name = '\'San Pedro\''
    name = 'San Pedro'
    name = '%GEO%'
    name = '%ArIZonA%'
    cursor.execute('SELECT * FROM api_tables.storymap_metadata WHERE name ILIKE %s',  (name, ))
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
        print(" \n")
        print(a)
        print(" \n")

    # Close communication with the database
    cursor.close()
    connection.close()

# printall()
printonename()
