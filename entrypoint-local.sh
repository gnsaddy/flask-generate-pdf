#!/bin/sh

gunicorn --bind 0.0.0.0:5000 manage:app --workers 2 --threads 2 --log-level debug --reload