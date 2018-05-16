# Hestia Webserver
## Build status

| Branch      | Build Status                                                                                                                                       |
| :---       | :---                                                                                                                                              |
| Master      | [![Build Status](https://travis-ci.org/RUGSoftEng/2018-Hestia-Web.svg?branch=master)](https://travis-ci.org/RUGSoftEng/2018-Hestia-Web)            |
| Development | [![Build Status](https://travis-ci.org/RUGSoftEng/2018-Hestia-Web.svg?branch=development)](https://travis-ci.org/RUGSoftEng/2018-Hestia-Web)       |

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
For initial setup of the backend. Follow either linux or windows. Apple setup is not known. The general flow for first time setup is Python -> pipenv -> database -> server.

After first time setup, the flow becomes database -> pipenv -> server
### Python
First, make sure that Python 3.6 is installed (3.6 is hard requirement!).
``` sh
python
```

If it is not installed, run the following commands for your respective operating system:
#### Debian (apt)
```sh
sudo apt install python3
```

#### Arch Linux (pacman)
```sh
sudo pacman -S python3
```

#### Windows
Setup is very different for windows. You must first download python 3.6 from their website and run the installer. You must check that python runs from your chosen terminal window (cmd works fine). If it is not, please google "add python to windows path"

### pipenv
The installation for pipenv is the same for all OS. Pipenv is a dependency manager for python applications. Make sure you have pipenv installed through pip.
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
### Database
THere are two ways of setting up the database, depending on your operating system. The first is for Linux, and the other is a Windows application. Windows users can feel free to use docker, but it is not explained here how to setup docker on windows.

#### Docker
Install docker:
##### Debian (apt)
```bash
sudo apt install docker.io
sudo usermod -a -G docker $USER
docker run --name hestia-web-db \
    -p 5432:5432 \
    -e POSTGRES_DB=HestiaDB \
    -e POSTGRES_PASSWORD=hestia \
    -d postgres
```
Now you can docker start hestia-web-db in the future once docker is running. You can enable docker auto-start with OS by using enable instaed of start with the systemctl call.
##### Arch (pacman)
```sh
sudo pacman -S docker
sudo groupadd docker 
sudo gpasswd -a <username> docker
sudo systemctl start docker
sudo docker run --name hestia-web-db \
    -p 5432:5432 \
    -e POSTGRES_DB=HestiaDB \
    -e POSTGRES_PASSWORD=hestia \
    -d postgres
```
Now you can 'docker start hestia-web-db' in the future once docker is running. You can enable docker auto-start with OS by using enable instaed of start with the systemctl call.
##### Windows
You may install postgres on Windows using BigSQL's premade installer. It comes with the servers and pdAdmin3 for you to visually inspect the database and manually edit values if need be.

Just go to: http://openscg.com/bigsql/ and click download->PostgresSQL10.3 Stable. Then follow installation instructions.

Once installed, you will need to add a server, and then database. Use the following information and leave the rest default:
| --:      | :--:      |
| Name     | HestiaDB  |
| Password | hestia    |
| Server   | localhost |

### Server Setup
Now that python, pipenv, and the database are setup we can run the application. Make sure the pipenv environment is enabled. 

```sh
python application.py dev
```
