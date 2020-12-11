# Backend of COA

[![Build Status](https://travis-ci.com/CleanOceanAction/coa_flask_app.svg?branch=master)](https://travis-ci.com/CleanOceanAction/coa_flask_app)

The flask backend REST APIs for the COA website.

## Getting Started

1. Install the dependencies

```
sudo apt install python3.8
sudo python3.8 -m pip install pipenv

# Alternatively with docker
sudo apt install docker
```

2. Setup DB related environment variables (not posted here for security reasons).
3. Start the server

```
make run

# Alternatively with docker
make prod-run
```

## Running the Backend

To test that the flask app is running and properly connected to the database,
use the curl command.

```
# Local
curl localhost:5000/items
curl --header "Content-Type: application/json" --request POST --data '{"username": "", "password": ""}' http://localhost:5000/login
curl --header "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" --request POST --data '{}' http://localhost:5000/events/add


# Prod
curl http://coa-flask-app-prod.us-east-1.elasticbeanstalk.com/items
```
