# README #

Hello and welcome to the Virtual Door project!

### What is this repository for? ###

* Quick summary:

    This repository is for the development, refinement and storage of the Virtual Door capstone project for the Northern Arizona University Computer Science Majors of the 2016 Fall and 2017 Spring semesters.

* Current Version:

    V 1.0

### How do I get set up? ###

* Setup for coding:

    Getting set up to modify code is as simple as pulling the repo branch you want to work on! If you want to work on the application layer, pull the backend branch. If you want to work on the front end UI, pull the UI branch.

* Dependencies:

    **This is important:** For the application layer the following dependencies **must** be installed:
    1) Python 3.5+
    2) Django 1.10
    3) DjangoRestFramework
    4) Markdown
    5) Django-filter
	6) Pillow
	7) python-social-auth[django]
	8) pycryptodome
	9) pycryptodomex
	10) pyjwkest
    11) django-bootstrap-form

    These dependencies can be installed using pip through the command line with the following command (on a Linux OS):
    *sudo pyhton3 -m pip install django djangorestframework markdown django-filter pillow python-social-auth[django] pycryptodome pycryptodomex pyjwkest django-bootstrap-form*

    **Note it is highly suggested that any work being done on the application-layer be done in a Linux environment as the system will be deployed to a Linux virtual environment on Amazon Web Services. Building on Windows and deploying to Linux does not play well with Django.** 
	
	***Set in your hosts file virtualofficedoor2017.com to point to 127.0.0.1 when developing locally***

* Running Django for development

  1. Pull the most current version of the backend branch from bitbucket to a separate folder. This can be done using Git via the command line: `git clone http://bitbucket-address-to-repo -b backend` or using an IDE's version control system (this process varies between each IDE, please check their documentation for specifics).
  2. Open up a command line interface of your choosing and navigate to the folder containing this README.
  3. Execute the local Django server by typing: `python3.5 manage.py runserver`. If python is not installed into your PATH variables then run: `{your python 3.5 path/location} manage.py runserver`
	
	The django server will now be running on your machine at port 8000.  For full functionality, utilize the hosts file modification above.

### Project Structure ###

* Architecture type:

    Layered.

* Database configuration:

    Schema pending.

* How to run tests:

    Not applicable yet.

* Deployment instructions:

    Deployment to AWS (as of right now) will be handled exclusively by nkm38.
	
### Branch File Structure ###
/root project
	manage.py 
	db.sqlite
	***other essential files to the repo***
	/ApplicationBackend
		settings.py
		urls.py
		wsgi.py
	/Atlas
		***core python files***
		/Templates
			***HTML FILES GO HERE***
		/static
			/js ***JAVASCRIPT FILES GO HERE***
			/css ***CSS FILES GO HERE***
			/images ***IMAGE FILES GO HERE***
