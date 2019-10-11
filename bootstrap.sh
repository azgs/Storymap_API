#!/bin/bash

service postgresql restart
gunicorn -b 0.0.0.0:5000 -w 4 storymap_api:app
