# API repository


This repository is a recreation of  https://api.spacexdata.com/v4/starlink API endpoint



## Run server

* To start the server locally, use the uvicorn program with the following command:

       uvicorn main:app --reload

## Update database

* To sincronize our database with https://api.spacexdata.com/v4/starlink run the following command:

       python3 update-database.py

## API endpoints implemented:

    "/v4/starlink" Shows information about all satelites
    "/v4/starlink/{object_name}" Shows information about satelite named {object_name}
    "/v4/distance/{latitude}+{longitude}+{distance}" Shows information about satelites within a maximum distance "distance" from (latitude, longitude)

