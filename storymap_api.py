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
@app.route('/api', strict_slashes=False, methods=['GET'])
@app.route('/api/v1', strict_slashes=False, methods=['GET'])
@app.route('/', methods=['GET'])
def home():
    return '''<h1>StoryMap API</h1>
    <br>
    <h2>Example routes: </h2>
    <br>

    <h3>Metadata queries</h3>

    <a href="/api/v1/metadata?all">/api/v1/metadata?all</a>
    <p>Query all metadata records</p>
    <br>

    <a href="/api/v1/metadata?map_id=2">/api/v1/metadata?map_id=2</a>
    <p>Query metadata records where the map id is 2</p>
    <br>

    <a href="/api/v1/metadata?name=San%20Pedro">/api/v1/metadata?name=San%20Pedro</a>
    <p>Query metadata records where the name contains "San Pedro". The name
    parameter is case-insensitive</p>
    <br>

    <a href="/api/v1/metadata?creator=Arizona">/api/v1/metadata?creator=Arizona</a>
    <p>Query metadata records where the creator contains "Arizona". The creator
    parameter is case-insensitive</p>
    <br>

    <a href="/api/v1/metadata?creator=Arizona&name=San%20Pedro">/api/v1/metadata?creator=Arizona&name=San%20Pedro</a>
    <p>Parameters can be combined </p>
    <br>

    <a href="/api/v1/metadata?creator=Arizona&name=kaibab&map_id=3">/api/v1/metadata?creator=Arizona&name=kaibab&map_id=3</a>
    <p>Parameters can be combined</p>
    <br>
    <br>
    <br>

    <h3>Features queries</h3>

    <a href="/api/v1/features?all">/api/v1/features?all</a>
    <p>Query all features records</p>
    <br>

    <a href="/api/v1/features?all&response=long">/api/v1/features?all&response=long</a>
    <p>The features route supports a "response" parameter. If "long" is passed,
    the map metadata for each feature will be included in the response</p>
    <br>

    <a href="/api/v1/features?map_id=2">/api/v1/features?map_id=2</a>
    <p>Query all features records where the map ID is 2</p>
    <br>

    <a href="/api/v1/features?feature_id=3">/api/v1/features?feature_id=3</a>
    <p>Query all features records where the feature ID is 3</p>
    <br>

    <a href="/api/v1/features?wkt=POLYGON((-191.0742188%2044.8402907,-191.25%2044.7155137,-186.5039063%20-3.337954,-144.4921875%20-1.0546279,-150.2929688%2033.1375512,-191.0742188%2044.8402907))&response=long">/api/v1/features?wkt=POLYGON((-191.0742188%2044.8402907,-191.25%2044.7155137,-186.5039063%20-3.337954,-144.4921875%20-1.0546279,-150.2929688%2033.1375512,-191.0742188%2044.8402907))&response=long</a>
    <p>Query features records by specifying a wkt bounding box. Here the "long"
    response parameter is also utilized</p>
    <br>
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
    response_type = query_parameters.get('response')
    if response_type:
        response_type = response_type.lower()

    # Assumed SRID is 4326
    srid = query_parameters.get('srid', default=4326)

    # Request for all entries
    if all_requested:

        # Casting needed to convert the PostgreSQL numeric type of x and y, to
        # something JSON compatible, here a double precision floating literal
        query = "SELECT feature_id, map_id, feature_name, feature_picture, feature, CAST (x AS DOUBLE PRECISION), CAST (y AS DOUBLE PRECISION), wkid, geom FROM api_tables.storymap_features ORDER BY feature_id ASC;"

    # Request for filtered entries
    if not all_requested:

        # Build query string
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
        if response_type == 'long':
            query += ' TRUE'
            query = 'select * from ({}) as b left join \
                    api_tables.storymap_metadata as a on a.map_id=b.map_id \
                    ORDER by feature_id ASC;'.format(query)

        # short response, default
        else:
            query = query + ' TRUE ORDER BY feature_id ASC;'

    # Print final query string to console
    print('\n' + query + '\n')

    # Retrieve all results
    cursor.execute(query)

    # Special case for long response
    if response_type == 'long':
        features = { "type": "FeatureCollection", "features": [{"type": "Feature", "geometry": f[5], "properties": {"feature_id": f[0], "map_id": f[1], "map_name": f[7], "map_description": f[8], "map_creator": f[9], "map_enterer": f[10], "map_link": f[11], "map_app_id": f[12], "map_web_id": f[13], "feature_name": f[2], "feature_picture": f[3], "feature": f[4]}} for f in cursor.fetchall()]} 

    else:
        features = { "type": "FeatureCollection", "features": [{"type": "Feature", "geometry": f[5], "properties": {"feature_id": f[0], "map_id": f[1], "feature_name": f[2], "feature_picture": f[3], "feature": f[4]}} for f in cursor.fetchall()]} 

    # Close DB connection
    cursor.close()
    connection.close()

    # Return results
    return(features)


####### Run configuration ######################################################

# Prevent JSON responses from being sorted on alphabetical order of keys
app.config['JSON_SORT_KEYS'] = False

# TODO - has to be FALSE on deploy
#app.config['DEBUG'] = True      # for testing ONLY
app.config['DEBUG'] = False


if __name__ == "__main__":
    # TODO - has to be app.run() on deploy

    # Start the application
    app.run()                       # listen on localhost only
    # app.run(host='0.0.0.0')       # listen on the local IP - for testing ONLY
