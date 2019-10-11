#!/bin/bash

service postgresql restart
gunicorn -b localhost:5000 -w 4 storymap_api:app
