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

By default, poetry will use associated virtual environment at the moment project was installed, you  can see that env by

> poetry env info

You can also list all the virtual environments associated with the current project with the command

> poetry env list

If you project has more than one virtual environment associated, then  you can switch between venvs by

> poetry env use _full/path/to/python_

Finally, you can delete existing virtual environments by using  (You can also use virtual env name provided by poetry env info ), or use flag to remove all environments

> poetry env remove _full/path/to/python_ | _cache_env_name_ | --all

To remove currently activated virtual environment

> poetry env remove

