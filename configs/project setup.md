## Dependency Management
Project uses Poetry as dependency management. Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you. Poetry offers a lockfile to ensure repeatable installs, and can build your project for distribution.

1. If pipx is not already installed, you can follow any of the options in the [official website](https://pipx.pypa.io/stable/installation/).

2. Run 
> pipx install poetry

3. Upgrade poetry 
> pipx upgrade poetry


Instead of creating a new project, POetry can be used to initialise a pre-populated directory. (Project setup was already done by running > poetry new marketstockstracker(must be same name as project's root directory )

> poetry init

If you need an additional library, all you have to do is run next command (inside )
> poetry add _libraryName_


