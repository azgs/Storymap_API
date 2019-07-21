#!/bin/bash

service postgresql restart
python3 storymap_api.py
