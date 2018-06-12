# Hestia Webserver
## Build status

| Branch      | Build Status                                                                                                                                       |
| :---       | :---                                                                                                                                              |
| Master      | [![Build Status](https://travis-ci.org/RUGSoftEng/2018-Hestia-Web.svg?branch=master)](https://travis-ci.org/RUGSoftEng/2018-Hestia-Web)            |
| Development | [![Build Status](https://travis-ci.org/RUGSoftEng/2018-Hestia-Web.svg?branch=development)](https://travis-ci.org/RUGSoftEng/2018-Hestia-Web)       |

## Quick Start
[Linux Ubuntu](#Setup-Linux-Ubuntu)
Linux Arch
Windows
Database

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
 The servers endpoint's NAMESPACE is declured in the init file. It just declares the namespace (from flask_restplus) and gives a description.
 
#### get
Within the servers, a ServerList class is declared that handles the endpoint for the '/' part of /servers. This means that it handles the broad changes of the overall serverlist. Including a "get" for all servers in the server table. It fetches each object from the server, and then returns them in JSON format.

#### post
The second function available at the '/' route of /servers allows a posting of a new server to the database. This function expects a SERVER model which is then posted to the database. If this is successful, a message will be returned with the new server in the payload.

### /servers/<string:id>
This endpoint extends from the /servers/, but adds the ability to query a single server based on the identitification of the (user) that requested. When an authenticated user needs to communicated with a specific server, they will pass the server id into the argument of the endpoint. For example, an authenticated user wishes to get from server with id="54a8c4h". They will send a request through the endpoint /servers/54a8c4h/. 

#### get
The get function acts like before and fetches the server as an object from the database. This is then returned as a JSON object.

#### delete
This function deletes the specific server that was passed in. It will return a code 204 is this completes correctly.

#### put
This function will update a server given it's id.

#### request
This function handles routing a request to the actual controller residing at the address contained in the server object. A PAYLOAD is defined that takes in the type of request, the endpoint it is going to, and any optional payload in raw form. This payload is sent to the server that is returned from the query (that returns the ONE object after filtering based on id). It will return 404 if the server is not able to be contacted or does not exist. This function utilizes a helper function "route_requset" that handles the actual setup of each request based on the type of request.

## Development Setup

### Dependencies
You need the following dependencies to run the Hestia back-end:

- Python 3
- Pip
- Pipenv through Pip
- Docker - _If you want to run a local production server_
- Heroku CLI - _If you want to deploy to Heroku_

Setup information for these dependencies is below.


### Setup Linux Ubuntu 
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

## Server Setup
### Linux
Assuming the environment is enabled (pipenv shell) in the backend directory, and the database server is running, you may now start the server in development mode with:
```bash
python application.py dev
```

### Windows
Assuming the environment is enabled (pipenv shell) in the backend directory, and the database server is running, you may now start the server with:
```bash
python application.py dev
```

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

### Other
You may install postgres on Windows using BigSQL's premade installer. It comes with the servers and pdAdmin3 for you to visually inspect the database and manually edit values if need be.

Just go to: http://openscg.com/bigsql/ and click download->PostgresSQL10.3 Stable.
