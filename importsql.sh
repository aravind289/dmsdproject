#!/bin/bash

if [ -z "$1" ]; then
    echo "Incorrect Syntax"
    echo "CMD syntax: bash importsql.sh <dir-to-sql-files>/* "

sql_dumps=$1

for d in $sql_dumps ; do
    echo "mysql -d libdata -u root < $d"
    mysql -u root libdata -u root < $d
done