#!/bin/sh
/usr/local/bin/uwsgi --http 0.0.0.0:8080 --uid quark --gid quark --wsgi-file server.py --callable app
