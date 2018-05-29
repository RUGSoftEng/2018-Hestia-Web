# Hestia Webserver
## Build status

| Branch      | Build Status                                                                                                                                 |
| :---        | :---                                                                                                                                         |
| Master      | [![Build Status](https://travis-ci.org/RUGSoftEng/2018-Hestia-Web.svg?branch=master)](https://travis-ci.org/RUGSoftEng/2018-Hestia-Web)      |
| Development | [![Build Status](https://travis-ci.org/RUGSoftEng/2018-Hestia-Web.svg?branch=development)](https://travis-ci.org/RUGSoftEng/2018-Hestia-Web) |

## Model Information
Currently, we use a postgres database to store information of each user and their "controllers". The model is interacted with through the endpoints described below. There are three tables in the model, the users table, the servers table, and the presets table.

## Extensions
The extensions are an example of the singleton pattern. They represent the resources that should be accessible throughout the application. This includes the DB access object and the API to register endpoints to. Their central nature to the functioning of the application justifies the use of this pattern and simplifies design.

## Modules
The modules represent the primary business logic of the application. They define the endpoints clients may access, the database interaction, and the translation between the web technologies and the underlying RDBMS. In our application we have three modules, one for `users`, one for `servers`, and one for `presets`. Though it may increase the complexity of our code, this structure improves the extensibility and maintainability of our code base. This particular structure was recommended by (frol)[https://github.com/frol/flask-restplus-server-example].

### Models - `models.py`
For each module this defines the underlying database table representing that module.

### Schemas - `schemas.py`
For each module this represents the translation to and from the database to an object representing the module.

### Resources - `resources.py`
For each module this represents the brunt the module. It described the endpoints that clients may access to interact with that module, any constraints on that interaction (such as a requirement for authentication), and the actual action associated with that interaction. The interaction is in the form of standard REST verbs acting on the resource the module represents.

## Application Configuration and the Factory Pattern
To aid with building, testing, and deploying our application we use the factory pattern. We define the configuration of our application in `config.py` as an object. The classes of configuration are `Development`, `Testing`, and `Production`. When the application is created via the factory `create_app()` method.

## Endpoint Information
Here we document the endpoints associated with each module. We have endpoints dealing with servers, users, and presets.

### /servers/
 The servers endpoint's NAMESPACE is declared in the modules init file. Each module

 It just declares the namespace (from flask_restplus) and gives a description.

#### get
This will get all servers associated with a user.

#### post
This will post a new server associated with a user to the database. This expects a JSON object representing properties (name, IP address, and port) of the server. If successful this will return a JSON representation of the stored server.

### /servers/<string:server_id>
This endpoint extends from the /servers/, but adds the ability to query a single server based on the identification of the (user) that requested. When an authenticated user needs to communicated with a specific server, they will pass the server id into the argument of the endpoint. For example, an authenticated user wishes to get from server with id="54a8c4h". They will send a request through the endpoint /servers/54a8c4h/.

#### get
The get function acts like before and fetches the server as an object from the database. This is then returned as a JSON object. However, the previous endpoint will return a JSON array containing zero or many servers, this will instead return a single object representing the queried server.

#### delete
This function deletes the specific server that was passed in. It will return a code 204 is this completes correctly. This will cascade to delete all presets associated with the deleted server.

#### put
This function will update the name, IP address, or port of a server given its id.

#### request
This function handles routing a request to the actual controller residing at the address contained in the server object. A `PAYLOAD` is defined that takes in the type of request, the endpoint it is going to, and any optional payload in raw form. This payload is sent to the server that is returned from the query (that returns the ONE object after filtering based on id). It will return 404 if the server is not able to be contacted or does not exist. This function utilizes a helper function `route_request` that handles the actual setup of each request based on the type of request.

#### ping
This will fire an options request to the server and return the ping in ms.

#### batch_request
The function acts similarly to the request endpoint. However, instead of a user specifying a request it will apply a previously saved preset.

### /servers/<string:server_id>/presets/
The preset endpoint enables users to store a state of all the devices. This enables a user to restore the individual states of each device with one call. The endpoint contains a get and post.

#### get
The function will return a list of all presets associated with a server. If the user attempts to query a server they are not associated with, it will return an exception.

#### post
The function will post a preset that conforms to the model schema. If successful it will return the name, state, and id

### /servers/<string:server_id>/presets/<string:preset_id>
This endpoint extends from the presets endpoint, adding functionality to individual presets. The added functionality includes deletion and retrieval of a specific preset.

#### get
The function returns the specific preset with `preset_id` associated with the server with `server_id`.

#### delete
The function deletes the preset matching `preset_id` that is associated with the server.

### /users/
This endpoint deals with the user table and exposes the ability to add and delete a user.

#### post
This function allows the posting of a new user to the database. It expects a USER model which is the n posted to the database. If this is successful, a message will be returned with the new user in the payload.

#### delete
This function will remove the authenticated user from the database. This will cascade down to remove all servers associated with that user.

## Development Setup
For initial setup of the Back-end. Follow either Linux or Windows. Apple setup is not known. The general flow for first time setup is Python -> pipenv -> database -> server.

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
pipenv install --dev
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

| :---      | :---      |
| Name      | HestiaDB  |
| Password  | hestia    |
| Server    | localhost |

### Server Setup
Now that python, pipenv, and the database are setup we can run the application. Make sure the pipenv environment is enabled.

```sh
python application.py dev
```
