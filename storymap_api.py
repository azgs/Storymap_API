#!/usr/bin/env python3

'''
StoryMap API 
2019
Andrew Zaffos
Stephen Nolan
Laura Bookman
Haley Snellen
Arizona Geological Survey
'''

import collections
import decimal
import flask
from flask import request, jsonify
import json
import psycopg2

app = flask.Flask(__name__)


# Root page
@app.route('/', methods=['GET'])
def home():
    return '''<h1>StoryMap API</h1>
    <p>Example routes: </p>
    <p> </p>
    <p>/api/v1/metadata?all</p>
    <p>/api/v1/metadata?map_id=2</p>
    <p>/api/v1/metadata?name=San%20Pedro</p>
    <p>/api/v1/metadata?creator=Arizona</p>
    <p>/api/v1/metadata?creator=Arizona&name=San%20Pedro</p>
    <p>/api/v1/metadata?creator=Arizona&name=kaibab&map_id=3</p>
    <p></p>
    <p>/api/v1/features?all</p>
    <p>/api/v1/features?map_id=2</p>
    <p>/api/v1/features?feature_id=3</p>
    '''


# Route for metadata lookups
@app.route('/api/v1/metadata', methods=['GET'])
def metadata_lookup():

    # DB connection
    connection = psycopg2.connect("dbname=storymap user=postgres")
    cursor = connection.cursor()

    # Fetch API call parameters
    query_parameters = request.args

    # Specific lookup parameters, special case for "all"
    all_requested = query_parameters.get('all')
    map_id = query_parameters.get('map_id')
    name = query_parameters.get('name')
    creator = query_parameters.get('creator')
    map_link = query_parameters.get('map_link')

    # Request for all entries
    if all_requested:

        query = "SELECT * FROM api_tables.storymap_metadata ORDER BY map_id ASC"

    # Request for filtered entries
    if not all_requested:

        # TODO safety/sanitization
        # Build query string
        query = "SELECT * FROM api_tables.storymap_metadata WHERE"

        if map_id:
            query += ' map_id={} AND'.format(map_id)
        if name:
            query += ' name ILIKE \'%{}%\' AND'.format(name)
        if creator:
            query += ' creator ILIKE \'%{}%\' AND'.format(creator)
        if map_link:
            query += ' map_link=\'{}\' AND'.format(map_link)

        # close the statement with a NOOP
        # TODO verify best practice for this
        # this idea trims trailing 'AND'
        # query = query[:-4] + ';'
        # my idea - NOOP cap instead of string slicing
        query = query + ' TRUE ORDER BY map_id ASC;'

    # Print final query string to console
    print(query)

    # Retrieve all results
    cursor.execute(query)
    results = cursor.fetchall()

    # Close DB connection
    cursor.close()
    connection.close()

    # variable <results> should now reference a list of tuples; the tuples
    # containing all of the values from the columns for each record returned

    # TODO might be able to build these labels into the returned results via the
    # cursor calls. For now just manually build out the appropriate keys for the
    # JSON template

    labelled_results = []

    for record in results:

        keyed_record = collections.OrderedDict()

        keyed_record['map_id'] = record[0]
        keyed_record['name'] = record[1]
        keyed_record['description'] = record[2]
        keyed_record['creator'] = record[3]
        keyed_record['enterer'] = record[4]
        keyed_record['map_link'] = record[5]
        keyed_record['app_id'] = record[6]
        keyed_record['webmap_id'] = record[7]

        labelled_results.append(keyed_record)

    # Return results
    return(jsonify({'success': labelled_results}))


# Route for features lookups
@app.route('/api/v1/features', methods=['GET'])
def features_lookup():

    # DB connection
    connection = psycopg2.connect("dbname=storymap user=postgres")
    cursor = connection.cursor()

    # Fetch API call parameters
    query_parameters = request.args

    # Specific lookup parameters, special case for "all"
    all_requested = query_parameters.get('all')
    feature_id = query_parameters.get('feature_id')
    map_id = query_parameters.get('map_id')
    min_x = query_parameters.get('min_x')
    max_x = query_parameters.get('max_x')
    min_y = query_parameters.get('min_y')
    max_y = query_parameters.get('max_y')
    wkt = query_parameters.get('wkt')
    # TODO currently assuming SRID will always be 4326
    srid = query_parameters.get('srid', default=4326)

    # Request for all entries
    if all_requested:

        # query = "SELECT * FROM api_tables.storymap_features ORDER BY feature_id ASC;"
        # Casting needed to convert the PostgreSQL numeric type of x and y, to
        # something JSON compatible, here a double precision floating literal
        query = "SELECT feature_id, map_id, feature_name, feature_picture, feature, CAST (x AS DOUBLE PRECISION), CAST (y AS DOUBLE PRECISION), wkid, geom FROM api_tables.storymap_features ORDER BY feature_id ASC;"

    # Request for filtered entries
    if not all_requested:

        # TODO safety/sanitization
        # Build query string
        #query = "SELECT * FROM api_tables.storymap_features WHERE"
        #query = "SELECT feature_id, map_id, feature_name, feature_picture, feature, CAST (x AS DOUBLE PRECISION), CAST (y AS DOUBLE PRECISION), wkid, geom FROM api_tables.storymap_features WHERE"
        query = "SELECT feature_id, map_id, feature_name, feature_picture, feature,  ST_AsGeoJSON(geom)::jsonb FROM api_tables.storymap_features WHERE"

        if feature_id:
            query += ' feature_id={} AND'.format(feature_id)
        if map_id:
            query += ' map_id={} AND'.format(map_id)
        if min_x and max_x and min_y and max_y:
            query += ' ST_Intersects (geom, ST_MakeEnvelope({}, \
                    {}, {}, {}, {})) AND'.format(min_x, min_y, max_x, max_y, srid)
        if wkt:
            query += ' ST_Intersects (geom, ST_GeomFromText(\'{}\', {})) AND'.format(wkt, srid)

        # close the statement with a NOOP
        # TODO verify best practice for this
        # this idea trims trailing 'AND'
        # query = query[:-4] + ';'
        # my idea - NOOP cap instead of string slicing
        query = query + ' TRUE ORDER BY feature_id ASC;'

    # Print final query string to console
    print('\n' + query + '\n')

    # Retrieve all results
    cursor.execute(query)
    # results = cursor.fetchall()
    # features = { "type": "FeatureCollection", "features": [{"type": "feature", "geometry": f[3], "properties": {"id": int(f[0]), "area": float(f[1]), "perimeter": float(f[2])}} for f in cursor.fetchall()]} 
    features = { "type": "FeatureCollection", "features": [{"type": "Feature", "geometry": f[5], "properties": {"feature_id": f[0], "map_id": f[1], "feature_name": f[2], "feature_picture": f[3], "feature": f[4]}} for f in cursor.fetchall()]} 
    # Close DB connection
    cursor.close()
    connection.close()

    # variable <results> should now reference a list of tuples; the tuples
    # containing all of the values from the columns for each record returned

    # TODO might be able to build these labels into the returned results via the
    # cursor calls. For now just manually build out the appropriate keys for the
    # JSON template

#    labelled_results = []
#
#    for record in results:
#
#        keyed_record = collections.OrderedDict()
#
#        keyed_record['feature_id'] = record[0]
#        keyed_record['map_id'] = record[1]
#        keyed_record['feature_name'] = record[2]
#        keyed_record['feature_picture'] = record[3]
#        keyed_record['feature'] = record[4]
#        keyed_record['x'] = record[5]
#        keyed_record['y'] = record[6]
#        keyed_record['wkid'] = record[7]
#        keyed_record['geom'] = record[8]
#
#        labelled_results.append(keyed_record)

    # Return results
    # return(jsonify({'success': labelled_results}))
    return(features)


####### Run configuration ######################################################

# Prevent JSON responses from being sorted on alphabetical order of keys
app.config['JSON_SORT_KEYS'] = False

# TODO - has to be FALSE on deploy
app.config['DEBUG'] = True      # for testing ONLY
# app.config['DEBUG'] = False

# TODO - has to be app.run() on deploy
# Start the application
# app.run()                       # listen on localhost only
app.run(host='0.0.0.0')       # listen on the local IP - for testing ONLY
