# Project Alice Commons
There are literally tons of code that is shared between different Project Alice repositories, such as between the main unit and the satellite.

In order to make it easier to maintain it, this package contains shared classes and functions

# Devs of this tool
- Clone this repository
- Open a terminal on whatever OS you are
- CD to the path where you cloned this repository
- Create a python 3.7+ virtual environment:
  `python -m venv venv`
- Activate your virtual environment
- Install the package in dev mode:
  `pip install --editable .`

# PyCharm
To make it easier to dev within this package:
- Open your main Project Alice project
- Choose "Open" and open this project. Choose "Attach" option, so that both of the projects are in the same workspace!
- Click on File -> Settings
- Under `Project XXXX` -> `Project dependencies`, click on `commons` and set its dependency to the main Project Alice directory.

This will enable code completion for the classes that are not present in this package but are Project Alice main unit only