# DBquadquery
A backend database for testing OLAP querys

# Description
A Docker app, containing a python script, working on a sqlite database created with sqlite3 and faker, and implemented querys with flask.

# Instalation
Simple download and extract, or clone.

# Project
    │---Dockerfile
    
    │---README.Docker.md
    
    │---app.py

    │---compose.yaml
    
    │---data.db
    
    │---requirements.txt
    
    │---results.txt
    
    │---testing.ipynb
    

Dockerfile, README, are simple docker implements made by docker init.
compose was also made by docker init, but changed to suit the project.
requirements are a file that makes sure you have all the prirequisites to start docker app.
data is an sqlite database file.
app is the main program in python language that is the core of this project, it creates a database, fills it and eventually runs the querys.

# Results
results show the difference of multiple consecutive overlaping querys vs a single isolated query.

# Run the app
Running the app reqires docker instaled, as well as a python interface.
tested option for running the app is VSCode.

# Contact
to contact the author sand an email to one of these adresses:
    boris.zic@gmail.com
    bzic@uniri.hr

# Licence
This project is stritctly readonly and only UNIRI FIDIT students/professors are allowed to read this project.
