#! /usr/bin/env bash

if [ $# = 1 ]; then
  export DBNAME=$1
else
  echo "Usage: bash setup_database DBNAME"
  DBNAME=deepdive_grades
fi
echo "Set DB_NAME to ${DBNAME}."
echo "HOST is ${PGHOST}, PORT is ${PGPORT}."

dropdb $DBNAME
createdb $DBNAME

export APP_HOME=`cd $(dirname $0)/; pwd`

psql -d $DBNAME < $APP_HOME/schema.sql
#export FILE=../../../csv_output/TCGA-XC-AA0X.csv
#export FILE=../../../csv_output/TCGA-NC-A5HD.csv
#psql -d $DBNAME -c "copy sentences from STDIN CSV;" < $FILE

export FILES=../../../csv_output/*
for file in $FILES
do
  psql -d $DBNAME -c "copy sentences from STDIN CSV;" < $file
done

