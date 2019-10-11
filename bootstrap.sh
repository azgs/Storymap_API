#!/bin/bash

# Bootstrap script for Storymap API docker container
# Arizona Geological Survey 2019

service postgresql restart
gunicorn -b 0.0.0.0:5000 -w 4 storymap_api:app
