`moviesapi` is a REST API that communicates with http://www.omdbapi.com/ for details about movie titles.


# Installation instructions

The installation process is straighforward and it requires that you have three things on your machine.

1. Python 3+ language, see https://www.python.org/downloads/ for details.
2. Pip module manager - to manage Python dependencies. You should have had that already installed, if you don't, see https://pip.pypa.io/en/stable/installing/ for details on that.
3. A way to run or connect to a `postgreSQL` database. One of the ways is to run a `postgreSQL` image using docker. See https://www.docker.com/get-started for installation instructions.


## Getting code and installing dependencies

Clone this repository to your machine by typing `git clone https://github.com/mpawlak2/moviesapi` into your terminal.

After you have successfuly downloaded the repository files, you can either setup a `virtualenv` to isolate project-specific Python dependencies (of course you can use another tool of your choosing, e.g., pyvenv, pyenv, etc.) or just install those system-wide, which is less ideal. Set working directory in the terminal to the location of this repository on your machine and after activating virtualenv, type:

```pip install -r requirements.txt```

## Required Python modules (and their purposes)

1. `django` - as a main Web framework in this project
2. `django-rest-framework` - to handle API endpoints and serialize objects
3. `python-dotenv` - to load `.env` settings for the app
4. `requests` - to communicate with external API
5. `psycopg2` - to handle `postgreSQL` database

## Setting up database

> Why postgreSQL in the first place?
> 
> There are some Django ORM's functions used in this application that wouldn't work in SQLite database supplied with Python.

### **I have Docker installed on my machine**

In that case, just type this into your terminal:

```docker run -e POSTGRES_PASSWORD=<password> -p 5432:5432 postgres```

REMEMBER to replace `<password>` with your own password. If you run `postgreSQL` using docker exactly like above, your username and database name both would be `postgres`.

### **I don't have Docker installed on my machine**

If you don't have Docker on your machine, you can either install a `postgreSQL` server or use remote database instance. Heroku offers a easy way to set up your own database in cloud. See https://www.heroku.com/postgres for details.

## Project configuration

### **Getting http://www.omdbapi.com/ API key**

You will need to get your own API key from http://www.omdbapi.com/, it is really straightforward, just click `API Key` on the top bar.

### **Create .env file**

Before you can run this app, you will need to create `.env` file in `/moviesapi/moviesapi` directory, the same location as the `wsgi.py` file location. There is already `.env.example` file, which you can copy and rename to `.env`. Fill every option according to these hints.

setting      |     meaning
-------------|------------------------------
OMDB_API_KEY | Put your OMDBAPI API key here
DB_PASSWORD  | `PostgreSQL` password
DB_HOST      | Database host
DB_USER      | Database user name
DB_NAME      | Database name
DB_PORT      | Database port, `5432` by default
DEBUG      | Set to `0` is the app is run in the production environment and `1` if it is not.


# Running the project

Befor you run this app make sure to deploy all migrations by typing `python manage.py migrate` it will also make sure that the database connection is working as it should.

After succesfull installation you are ready to run the project, all you have to do is to activate the virtualenv (if you are using one) and then from the `moviesapi/` directory run `python manage.py runserver`. This will obviously run a development server. For more production ready solutions look into https://gunicorn.org/.


# Running tests

Test are run from the same directory as the app itself, from `moviesapi/` directory type `python manage.py test` to run all tests.


# Endpoints

method | endpoint | parameters      | description
-------|----------|-----------------|-----------
POST   | /movies  | `title` - title of the movie you want to fetch| Fetch movie details from the OMDBAPI external api and add to app's database if does not exist already. If on the other hand movie with the specified title exists, return it straight from the database.
GET    | /movies  | `ord` (optional) - on which column and in which way to sort, e.g., "`-year`" to sort on colum `year` in a descending way <br> `title` (optional) - filter movies that contain this value in its `title` field <br> `year` (optional) - filter movies that contain this value in its `year` field<br> `rated` (optional) - filter movies that contain this value in its `rated` field<br> `released` (optional) - filter movies that contain this value in its `released` field<br> `runtime` (optional) - filter movies that contain this value in its `runtime` field<br> `genre` (optional) - filter movies that contain this value in its `genre` field<br> `director` (optional) - filter movies that contain this value in its `director` field<br> `writer` (optional) - filter movies that contain this value in its `writer` field<br> `actors` (optional) - filter movies that contain this value in its `actors` field<br> `plot` (optional) - filter movies that contain this value in its `plot` field<br> `language` (optional) - filter movies that contain this value in its `language` field<br> `country` (optional) - filter movies that contain this value in its `country` field<br> `awards` (optional) - filter movies that contain this value in its `awards` field<br> `poster` (optional) - filter movies that contain this value in its `poster` field<br> `metascore` (optional) - filter movies that contain this value in its `metascore` field| Return a list of all, or filtered, movies already in the database.
POST | /comments | `movie` - movie id to add comment to<br>`body` - the body of a comment | Add comments to movies.
GET | /comments | `movie` (optional) - filter comments by its movie id | Return list of all, or filtered, comments in the database
GET | /top | `date_from` - the start date in the YYYY-MM-DD format for this statistics<br>`date_to` - the end date in the YYYY-MM-DD format for this statistics | Return top movies with comment count and its ranking. This will include only comments that were created between `date_from` and `date_to` dates. A `rank` field in the response json is based on a `total_comments` field. Entries with the same number of `total_comments` have the same `rank`.


# Thank you for you attention!