#!/bin/bash

#
# Copyright (c) 2021-2021.
# Julio Cezar Riffel<julioriffel@gmail.com>
#

scriptPath=$(dirname "$(readlink -f "$0")")

#printenv | sed 's/^\(.*\)$/export \1/g' > ${scriptPath}/.env.sh
eval $(printenv | awk -F= '{print "export " "\""$1"\"""=""\""$2"\"" }' >>${scriptPath}/.env.sh)
chmod +x ${scriptPath}/.env.sh
