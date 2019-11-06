#!/bin/bash

DIR=~/dl4g

if [ -d "$DIR" ]; then
    cd $DIR
fi

export FLASK_APP=service.py
export FLASK_ENV=development

flask run --host=0.0.0.0 --port=46960
