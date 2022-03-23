#!/bin/sh

gunicorn --bind 0.0.0.0:5000 manage:app --workers 4 --threads 4 --log-level debug --reload