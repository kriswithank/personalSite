# personalSite.

This is just me playing around with the python web framework Django.

### Getting up and running.

To get started, make sure that you have python, pip and virtual environment installed on your machine.
Then, you should be able to just clone this repository and execute the following commands to get a test
server up and running. The website address should be displayed in the terminal after doing the following:

In a terminal, navigate to where this repo is, activate the python virtual environment, and run the test
server. An example is shown below.

    [user@mypc]$ cd /path/to/personalSite/
    [user@mypc]$ source virtualenv/bin/activate
    (virtualenv) [user@mypc]$ python manage.py runserver
    Performing system checks...

    System check identified no issues (0 silenced).
    December 11, 2016 - 20:30:17
    Django version 1.10.4, using settings 'personalSite.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

When you are finished running the server, press *CONTROL-C* to quit the development server and enter 

    (virtualenv) [user@mypc]$ deactivate

to exit the virtual environment.
