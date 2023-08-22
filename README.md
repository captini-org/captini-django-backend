# captini-django-backend
## I will update this further on. This is still a work in progress and I won't expect things to work without some fiddling.

## installation    
 - clone repo `https://github.com/captini-org/captini-django-backend.git`
 - Navigate to repo folder CaptiniAPI
 - Make sure to have python 3.10 installed and pip
 - Install virtualenv with pip
 `pip install virtualenv`
 - Create a virtual environment
   `virtualenv -p python3 <"venv">` (or other name for virtual environment)
 - Activate the virtual environment
 `source venv/bin/activate` for linux
 `\venv\Scripts\activate.bat` for windows
 - Install requirements
 `pip install -r requirements.txt`
 - Create a postgres database
 - Put the correct credentials into settings.py (make sure your database name, user and password are the same.)
 ```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "captini",
        "USER": "postgres",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

 - Run the following to create the database tables   
 `python manage.py migrate`   
 `python manage.py createsuperuser` (admin user)   
 `python manage.py makemigrations captini`   
 `pyton manage.py migrate` to migrate the app models into db   
 - Then to run server on localhost:8000   
 `python manage.py runserver`   
 

In case you need the data in the database locally run (the database generated has the correct numbering for the tasks).
`cd dev`
`pip install psycopg2`
`python savedatalocally.py`
N.B. set the database parameter in case oyu changed it.
N.B. ope lesson parameter number has the same value of id. 