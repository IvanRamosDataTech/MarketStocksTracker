## Dependency Management
Project uses Poetry as dependency management. Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you. Poetry offers a lockfile to ensure repeatable installs, and can build your project for distribution.

1. If pipx is not already installed, you can follow any of the options in the [official website](https://pipx.pypa.io/stable/installation/).

2. Run 
> pipx install poetry

3. Upgrade poetry 
> pipx upgrade poetry


Instead of creating a new project, POetry can be used to initialise a pre-populated directory. (Project setup was already done by running > poetry new marketstockstracker(must be same name as project's root directory ). This will automatically create a new virtual environment for your project and going to store it at username\AppData\Local\pypoetry\Cache\virtualenvs

> poetry init

then to install the defined dependencies for you project, just run 

> poetry install

updater scripts helps to keep up with last changes from portfolio, gets a snapshot of last portfolio positions and bulks it into Postgresql database. To run this scrip, simply type (inside marketstockstracker/tracker-poetry-src/tracker_poetry)
> poetry run python updater.py

If you need an additional library, all you have to do is run next command (inside )
> poetry add _libraryName_

## Managing environment with Poetry commands

Poetry makes project environment isolation one of its core features.
By default, Poetry will try to use the Python version used during Poetry’s installation to create the virtual environment for the current project.

By default, poetry will use associated virtual environment at the moment project was installed, so move to `MarketStocksTracker/tracker-poetry` folder and you  can see that env by

> poetry env info

You can also list all the virtual environments associated with the current project with the command

> poetry env list

If you project has more than one virtual environment associated, then  you can switch between venvs by

> poetry env use _full/path/to/python_

Finally, you can delete existing virtual environments by using  (You can also use virtual env name provided by poetry env info ), or use flag to remove all environments

> poetry env remove _full/path/to/python_ | _cache_env_name_ | --all

To remove currently activated virtual environment

> poetry env remove

## Database installation

This project uses Postgresql as a database management system. 
Install Postgresql & PgAdmin in your system. Login into your DB system using PGAdmin and make sure to open up a new Query Tool in the postgres default database

From there, copy and paste contents of `create_database.sql` into your Query Tool and execute them as per instructions specified in script.

Then a database `marketstockstracker` should be visible in Object Explorer. Open up a Query Tool from this new database.
From there, Open up `create schema.sql` file using command Ctrl+o and execute its contents. Refresh your database schema and you should see tables there.

## Database Configuration
As security rule, this project uses environment variables to prevent exposing any sensitive password. Make sure to create a new file `MarketStocksTracker/tracker-poetry/src/tracker_poetry/.env` like following one with your own configurations.

```
# .env file will enable you to use environment variables for local development without polluting the global environment namespace
# It will also keep your environment variable names and values isolated to the same project that utilizes them.
# .env file prevents you from directly writing down sensitive information in your code. Instead, processes inject environment variables at runtime.


# Python environment
APP_VERSION=0.1v

# Database config

# Development database credentials
DB_SERVER_DEV=
DB_PORT_DEV=
DB_USER_DEV=
DB_PASSWORD_DEV=
DB_NAME_DEV=


# Production database deployment credentials
DB_SERVER=
DB_PORT=
DB_USER=
DB_PASSWORD=
DB_NAME=

# Excel file config

# Development File path
EXCEL_FILE_DEV = "DEV Portafolio Indizado_Patrimonial.xlsx"
#Production File path
EXCEL_FILE = "Portafolio Indizado_Patrimonial.xlsx"
# Azure App registration 
AZURE_APP_ID = "your-azure-app-id"

```

## Data source configuration

You'll need to specify relative paths for excel files as data sources (when local extraction is preferred) and link urls (when remote extraction is selected) script will take info from as unique data source depending on the environment you are working on.

# Excel file config

# Development File path
EXCEL_FILE_DEV = "./relative/path/to/dev excel.xlsx"

#Production File path
EXCEL_FILE = "./relative/path/to/prod excel.xlsx"