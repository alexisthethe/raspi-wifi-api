#!/bin/sh
gunicorn --bind 172.17.0.1:5678 app:app
