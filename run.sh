#!/bin/bash

export DATABASE_URL="mysql://root@localhost/flaskcms"

python flask_cms/manage.py runserver
