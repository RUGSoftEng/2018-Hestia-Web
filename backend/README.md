# backend

> This the backend for the hestia server. It defines the following endpoints
1. Describe the endpoints

## Development Setup
### Linux
Make sure you have Python 3.6 installed.

```sh
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.6
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

### Windows
Setup is very different for windows. You must first download python 3.6 from their website.

Next download [get-pip.py](https://bootstrap.pypa.io/get-pip.py)
Execute it with console by pressing windows key, type in cmd, then press enter. Run python get-pip.py from where you downloaded it to. You may have to put python in your PATH (Google if needed).

Install pipenv through pip:
```bash
pip install pipenv
```
This will create a virtualenv with python3

Make sure your cd is `backend` directory.

Finally run:
```bash
pipenv shell
```
This enables the environment with the lock file already included in the repository.

## Server Setup
### Linux
Assuming the environment is enabled (pipenv shell) in the backend directory, you may now start the server with:
```bash
FLASK_APP=application.py flask run
```

### Windows
Assuming the environment is enabled (pipenv shell) in the backend directory, you may now start the server with:
```bash
set FLASK_APP=application.py
flask run
```

## Database Setup
### Docker
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

