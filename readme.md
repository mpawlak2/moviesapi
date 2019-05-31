`moviesapi` is a REST API that communicates with http://www.omdbapi.com/ for details about movie titles.


# Installation instructions

The installation process is straighforward and requires three things on your machine.

1. Python 3+ language, see https://www.python.org/downloads/ for details
2. Pip module manager - to manage Python dependencies. You should have had that already installed, if you don't, see https://pip.pypa.io/en/stable/installing/ for details on that.
3. A way to run or connect to a `postgreSQL` database. One of the ways is to run a `postgreSQL` image using docker. See https://www.docker.com/get-started for installation instructions.


## Getting code and installing dependencies

Clone this repository to your machine by typing `git clone ...` into your terminal.

After you have successfuly downloaded the repository files, you can either setup a `virtualenv` to isolate project-specific Python dependencies (of course you can use another tool of your choosing, e.g., pyvenv, pyenv, etc.) or just install those system-wide, which is less ideal. Set working directory in the terminal to the location of this repository on your machine and after activating virtualenv, type:

```pip install -r requirements.txt```

## Required Python modules (and their purposes)

1. django - as a main framework
2. django-rest-framework - to handle API endpoints and serialize objects
3. python-dotenv - to load `.env` settings for the app
4. requests - to communicate with external API
5. psycopg2 - to handle `postgreSQL` database

## Setting up database

> Why postgreSQL in the first place?
> 
> There are some functions used that wouldn't work in SQLite database shipped with Python.

### **I have Docker installed on my machine**

In that case, just type this into your terminal:

```docker run -e POSTGRES_PASSWORD=<password> -p 5432:5432 postgres```

REMEMBER to replace `<password>` with your own password.

### **I don't have Docker installed on my machine**

If you don't have Docker on your machine, you can either install a `postgreSQL` server or use remote database instance. Heroku offers a easy way to set up your own database in cloud. See https://www.heroku.com/postgres for details.

## Project configuration

### **Getting http://www.omdbapi.com/ API key**

You will need to get your own API key from http://www.omdbapi.com/, it is really straightforward, just click `API Key` on the top bar.

### **Create .env file**

Before you can run this app, you will need to create `.env` file in `/moviesapi/moviesapi` directory, the same location as `wsgi.py`. There is already `.env.example` file, which you can copy and rename to `.env`. Fill every option according to these hints.

setting      |     meaning
-------------|------------------------------
OMDB_API_KEY | Put your OMDBAPI API key here
DB_PASSWORD  | `PostgreSQL` password
DB_HOST      | Database host
DB_USER      | Database user name
DB_NAME      | Database name
DB_PORT      | Database port, `5432` by default


# Running the project

After succesfull installation you are ready to run the project, all you have to do is to activate the virtualenv (if you are using one) from the directory of `moviesapi/` run `python manage.py runserver`. This will, obviously, run a development server. For more production ready solution look into https://gunicorn.org/.


# Running tests

Test are run from the same directory as the app itself, from `moviesapi/` type `python manage.py test` to runn all tests.


# Endpoints

