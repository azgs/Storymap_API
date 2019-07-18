#!/usr/bin/env python3

'''
StoryMap API 
2019
Andrew Zaffos
Stephen Nolan
Arizona Geological Survey
'''

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
    '''


# Route for lookups
@app.route('/api/v1/metadata', methods=['GET'])
def storymap_lookup():

    # DB connection
    connection = psycopg2.connect("dbname=storymap user=steve")
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

        query = "SELECT * FROM api_tables.storymap_metadata"

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
        query = query + ' TRUE;'

    # Print final query string to console
    print(query)

    # Retrieve all results
    cursor.execute(query)
    results = cursor.fetchall()

    # Close DB connection
    cursor.close()
    connection.close()

    # Return results
    return jsonify(results)


####### Run configuration ######################################################

# TODO - has to be FALSE on deploy
app.config['DEBUG'] = True      # for testing ONLY
# app.config['DEBUG'] = False

# TODO - has to be app.run() on deploy
# Start the application
app.run()                       # listen on localhost
# app.run(host='0.0.0.0')       # listen on the local IP - for testing ONLY
