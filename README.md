# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

[Trello](https://trello.com)'s API is used as the backend engine to fetch and save tasks. You'll need to sign up for a [a Trello account](https://trello.com/signup) and [generate API Key and Token](https://trello.com/app-key) as a pre-requisite. You would need to add the same to the `.env` file along with the board and list details.

```bash
#Trello Configurations
TRELLO_API_KEY=<YOUR_API_KEY>
TRELLO_API_TOKEN=<YOUR_TOKEN>
ITEMS_BOARD_ID=<YOUR_BOARD_ID>
TODO_LIST_ID=<YOUR_TODO_LIST_ID>
DONE_LIST_ID=<YOUR_DONE_LIST_ID>
```
## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Testing this app

to run the tests, make sure you are in the todo_app folder:
```bash
cd .\todo_app\
```
And run the tests:
```bash
poetry run pytest
```
For Selenium UI tests, download Firefox and matching version of the Gecko Driver executable and place it in the root of the project. Selenium uses this under the hood to run tests on the browser.
```bash
poetry run pytest tests_e2e
```
## Virtual Machine(VM) using Vagrant
The app can be ran in a virtual machine using Vagrant. 
Vagrant encapsulates development environment in a single configuration file, making it easy to share
between developers and launch without having to worry about Python environments and dependencies.
Download: 
* Hypervisor - Vagrant requires a hypervisor installed. We recommend [VirtualBox](https://www.virtualbox.org/).
* Vagrant - Download and install vagrant from the [official website](https://www.vagrantup.com/). You can check it's installed correctly by running the `vagrant` command in your terminal.

### Starting the app on the VM
* `vagrant up` - Starts your VM, creating and provisioning it automatically if it is required. This command will automatically run the app on the browser.
You can then visit http://localhost:5000/ in your web browser to view the app.
* `vagrant ssh` - explore this VM using the bash shell. 

### Other useful commands
* `vagrant provision` - Runs any VM provisioning steps specified in the Vagrantfile. Provisioning steps are one-off operations that adjust the system provided by the box.
* `vagrant suspend` - Suspends any running VM. The VM will be restarted on the next vagrant up command.
* `vagrant destroy` - Destroys the VM. It will be fully recreated the next time you run vagrant up.

### Using Docker containers

Download: 
* Docker - you'll need to install [Docker Desktop](https://www.docker.com/products/docker-desktop).

#### Running the Dev & Prod Container

There are two flavours of containers that can be built, a development and a production image.

The dev container:
* Uses Flask to run the application
* Enables Flask's debugging/developer mode to provide detailed logging and feedback.
* Allows rapid changes to code files without having to rebuild the image each time.

The production container:
* Uses Gunicorn to run the application

You can create either a development, test or production image from the same Dockerfile, by running the following:
```bash
$ docker build --target development --tag todo-app:dev .
```
or the following for test:
```bash
$ docker build --target test --tag todo-app:test .
```
or the following for production:
```bash
$ docker build --target production --tag todo-app:prod .
```
You can then start the dev container by running:
```bash
$ docker run --env-file .env -p 5000:5000 -v $(pwd)/todo_app:/todo_app/todo_app  todo-app:dev
```
or you can start the test container by running:
```bash
$ docker run todo-app:test ./todo_app/tests
```
```bash
$ docker run --env-file .env todo-app:test ./todo_app/tests_e2e
```
or you can start the production container by running:
```bash
$ docker run --env-file .env -p 5000:5000 todo-app:prod
```