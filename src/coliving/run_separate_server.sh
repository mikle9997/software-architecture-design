#!/bin/bash

additional_args=$1

if [[  -z $additional_args ]];  then
	it_flags=-it
fi


docker build -t col_server:latest -f backend.dockerfile $additional_args .
docker run --rm $it_flags -p 8000:8000 col_server:latest
