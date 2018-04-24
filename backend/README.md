# backend

> This the backend for the hestia server. It defines the following endpoints
1. Describe the endpoints

## Development Setup
### Linux
Make sure you have Python 3.6 installed.

sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.6

Make sure you have pipenv installed through pip.
pip install pipenv

Make sure your cd is `backend` directory.

Now run:
pipenv install
This will create a virtualenv with python3

Finally run:
pipenv shell
This enables the environment with the lock file already included in the repository.

### Windows
Setup is very different for windows. You must first download python 3.6 from their website.

Next download get-pip.py from: https://bootstrap.pypa.io/get-pip.py
Execute it with console by pressing windows key, type in cmd, then press enter. Run python get-pip.py from where you downloaded it to. You may have to put python in your PATH (Google if needed).

Install pipenv through pip:
pip install pipenv
This will create a virtualenv with python3

Make sure your cd is `backend` directory.

Finally run:
pipenv shell
This enables the environment with the lock file already included in the repository.

## Server Setup
### Linux
Assuming the environment is enabled (pipenv shell) in the backend directory, you may now start the server with:
FLASK_APP=application.py flask run

### Windows
Assuming the environment is enabled (pipenv shell) in the backend directory, you may now start the server with:
set FLASK_APP=application.py
flask rungit add
