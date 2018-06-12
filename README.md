# Hestia Webserver

This is the back-end system of the [Hestia](https://rugsofteng.github.io/2017-Hestia-Server/) project, which serves as a middleman between local Hestia servers and their users. This document describes the setup and functioning of the back-end.

## Build status

| Branch      | Build Status                                                                                                                                       |
| :---       | :---                                                                                                                                              |
| Master      | [![Build Status](https://travis-ci.org/RUGSoftEng/2018-Hestia-Web.svg?branch=master)](https://travis-ci.org/RUGSoftEng/2018-Hestia-Web)            |
| Development | [![Build Status](https://travis-ci.org/RUGSoftEng/2018-Hestia-Web.svg?branch=development)](https://travis-ci.org/RUGSoftEng/2018-Hestia-Web)       |

## Quick Start
- [Linux Ubuntu](#setup---linux-ubuntu)
- [Linux Arch](#setup---linux-arch)
- [Windows](#setup---windows)

- [Database](#database-setup)

There is also a [quick reference](#quick-command-reference) for commonly used commands.

## Development Setup

### Dependencies
You need the following dependencies to run the Hestia back-end:

- Python 3
- Pip
- Pipenv through Pip
- Docker - _If you want to run a local production server_
- Heroku CLI - _If you want to deploy to Heroku_

Setup information for these dependencies is below.


### Setup - Linux Ubuntu 
Make sure you have Python 3.6 installed.

```sh
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.6
```

Make sure you have pipenv installed through pip.
```bash
pip install pipenv
```

Make sure your cd is `backend` directory.

Now run:
```bash
pipenv install
```
This will create a virtualenv with python3

Finally run:
```bash
pipenv shell
```
This enables the environment with the lock file already included in the repository.

### Setup - Linux Arch
Make sure you have Python 3.6 installed.

```sh
sudo pacman -S python3
sudo pacman -S python-pip
```

Make sure you have pipenv installed through pip.
```bash
sudo pip install pipenv
```

Make sure your cd is `backend` directory.

Now run:
```bash
pipenv install
```
This will create a virtualenv with python3

Finally run:
```bash
pipenv shell
```
This enables the environment with the lock file already included in the repository.


### Setup - Windows
Setup is very different for windows. You must first download python 3.6 from [their website](https://www.python.org/downloads/release/python-360/).

Next download [get-pip.py](https://bootstrap.pypa.io/get-pip.py)
Execute it through the console by pressing the windows key, typing in cmd, then pressing enter. Run python get-pip.py from where you downloaded it to. You may have to put python in your PATH (Google if needed).

Install pipenv through pip:
```bash
pip install pipenv
```
This will create a virtualenv with python3

Make sure your cd is `backend` directory.

Install the dependencies of the project:
```bash
pipenv install --dev
```

Finally run:
```bash
pipenv shell
```
This enables the environment with the lock file already included in the repository.

## Running the Server
### Linux and Windows
Assuming the environment is enabled (pipenv shell) in the backend directory, and the database server is running, you may now start the server in development mode with:
```bash
python application.py dev
```
## Quick Command Reference
| Action              | Command                      |
| :---                | :---                         |
| Start virtual environment (before any other commands can be used  | `pipenv shell` |
| Run the development server   | `python application.py dev`  |
| Run tests | `pytest`    |
| Run tests (coverage) | `pytest --cov=app`    |

## Heroku deployment
In order to deploy to Heroku, simply follow the steps on the following page: https://devcenter.heroku.com/articles/getting-started-with-python.

The current setup does not auto-deploy on succesful commits, instead you have to follow the tutorial using your own account.
Travis CI can be used to automate deployment, otherwise updates need to be manually redeployed.

If you are not deploying to Heroku, you can ignore the files _Procfile_ and _wsgi.py_ in the root directory.

## Database Setup

### Testing and development purposes
You do not need to use Docker for testing or development purposes, instead you can the 

### Local Production Server

#### Docker Ubuntu
First install Docker:
```bash
sudo apt install docker.io
```
Then you need to fix the user permissions on Ubuntu. **Make sure to logout and log back in afterwards.**
```bash
sudo usermod -a -G docker $USER
```
Setup the docker container with the `postgres` database.
```bash
docker run --name hestia-web-db \
    -p 5432:5432 \
    -e POSTGRES_DB=HestiaDB \
    -e POSTGRES_PASSWORD=hestia \
    -d postgres
```
The database will be running immediately. The following commands are also available now.

| Action              | Command                      |
| :---                | :---                         |
| Start the database  | `docker start hestia-web-db` |
| Stop the database   | `docker stop hestia-web-db`  |
| Delete the database | `docker rm hestia-web-db`    |

#### Docker Arch
First install Docker:
```bash
sudo pacman -S docker
```

Create group:
```bash
sudo groupadd docker #may already exist
```

Add yourself to group:
```bash
sudo gpasswd -a *username* docker
```

Now start docker daemon:
```bash
sudo systemctl start docker #for auto-start, use enable instead of start
```

Finally, launch container:
```bash
sudo docker run --name hestia-web-db \
    -p 5432:5432 \
    -e POSTGRES_DB=HestiaDB \
    -e POSTGRES_PASSWORD=hestia \
    -d postgres
```

You should now be able to run the server.


## Model Information
Currently, we use a postgres database to store information of each user and their "controllers". The model is interacted with through the endpoints described below. There are two tables in the model, the users table and the servers table.

### Entity.py
Each table inherits from a class called Entity that contains universal information such as when an entry was created, and when it was last updated. Each table (class) inherits from this Entity class so that code is not duplicated.

### Model.py
Model.py defines each table(class) for our use. With each class within, we define the actual table name, columns, and column information. Then following the class, we define a schema that stores the schema and field types of each column. This is useful for reading payloads and handling valid requests.

The important thing to know about the model (database file path) is that it only declares the schema and table information for the endpoints to use. This must match the actual database being hosted. If you make large changes to the database, you must handle the changes outside of a running server.

## Endpoint Information
Inside the endpoints folder, you will find all of the declared endpoints that can be used. There are two major ones, each dealing with the two respective database tables. The first is the users, and the second being the servers.

### /servers/
 The servers endpoint's NAMESPACE is declared in the init file. It just declares the namespace (from flask_restplus) and gives a description.
 
#### GET
Within the servers, a ServerList class is declared that handles the endpoint for the '/' part of /servers. This means that it handles the broad changes of the overall serverlist, including a GET for all servers in the server table. It fetches each object from the server, and then returns them in JSON format.

#### POST
The second function available at the '/' route of /servers allows a posting of a new server to the database. This function expects a SERVER model which is then posted to the database. If this is successful, a message will be returned with the new server in the payload.

### /servers/<string:id>
This endpoint extends from /servers/, but adds the ability to query a single server based on the identification of the user that sent the query . When an authenticated user needs to communicate with a specific server, they will pass the server ID to the argument of the endpoint. For example, an authenticated user wishes to GET from the server with id="54a8c4h". They will send a request through the endpoint /servers/54a8c4h/. 

#### GET
The GET function acts as previously described and fetches the server as a JSON object from the database. However, the previous endpoint returns a JSON array containing zero or more servers, and this will instead return a single object representing the queried server.

#### DELETE
This function deletes the specific server that was passed in. It will return a code 204 when it completes correctly.

#### PUT
This function will update the name, IP address, or port of a server given its ID.

#### request
This function handles routing a request to the actual controller at the address contained in the server object. A PAYLOAD is defined that takes in the type of request, the endpoint it is going to, and any optional payload in raw form. This payload is sent to the server that is returned from the query (that returns the ONE object after filtering based on ID). It will return a 404 error if the server is not able to be contacted or does not exist. This function utilizes a helper function route_request that handles the actual setup of each request, based on the type of the request.

####ping
This will send an options request to the server and return the ping in milliseconds.

#### batch_request
The function acts similarly to the request endpoint. However, instead of a user specifying a request it will apply a previously saved preset.

##### /servers/<string:server_id>/presets/
The preset endpoint enables users to store a state of all the devices. This enables a user to restore the individual states of each device with one call. The endpoint contains a GET and POST.

###### GET
The function will return a list of all presets associated with a server. If the user attempts to query a server they are not associated with, it will return an exception.

###### POST
The function will post a preset that conforms to the model schema. If successful it will return the name, state, and ID.

##### /servers/<string:server_id>/presets/<string:preset_id>
This endpoint extends from the presets endpoint, adding functionality to individual presets. The added functionality includes deletion and retrieval of a specific preset.

###### GET
The function returns the specific preset with `preset_id` associated with the server with `server_id`.

###### DELETE
The function deletes the preset matching `preset_id` that is associated with the server.

##### /users/
This endpoint deals with the user table and provides the ability to add and delete a user.

###### POST
This function allows the posting of a new user to the database. It expects a USER model which is then posted to the database. If this is successful, a message will be returned with the new user in the payload.

###### delete
This function will remove the authenticated user from the database. This will cascade down to remove all servers associated with that user.


### Other
You may install postgres on Windows using BigSQL's premade installer. It comes with the servers and pdAdmin3 for you to visually inspect the database and manually edit values if need be.

Just go to: http://openscg.com/bigsql/ and click download->PostgresSQL10.3 Stable.
