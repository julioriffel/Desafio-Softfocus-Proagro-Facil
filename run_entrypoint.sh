#!/bin/bash

#
# Copyright (c) 2021-2021.
# Julio Cezar Riffel<julioriffel@gmail.com>
#

service cron start && gunicorn core.wsgi:application --bind 0.0.0.0:8000
