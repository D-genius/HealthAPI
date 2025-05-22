# Setting Up a REST API Service for Healthcare app
#### A step-by-step guide
1. In your terminal create a virtual environment by running the commands `mkdir env` then `python3 -m venv env/oenv`
2. To start your virtual environment run the command `source env/oenv/bin/activate` .To stop the environment run `deactivate` command
3. Install dependancies using this command in the root directory of the project `pip install -r requirements.txt`
4. To configure your database go to the `settings.py` file and edit the properties below, bearing in mind postgres servers and client is installed on your machine 

DATABASES = {
    'default': {
        'NAME': 'your_DB_name',
        'HOST': 'localhost',
        'USER': 'Your_username',
        'PASSWORD': 'Your_password',
        'PORT': '5432',
    }
}

5. Generate an encryption key and add it to your `.env` file of your root project.
- `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
FIELD_ENCRYPTION_KEY=Your_Key`
- Run the command `python manage.py shell -c "from django.conf import settings; print(settings.FIELD_ENCRYPTION_KEY)"` to verify encryption key

6. Edit you settings with the valid credentials with your database settings `CELERY_BROKER_URL = 'sqla+postgresql://<user>:<password>@<host>/<database>'`
7. Run your celery task queue service using `celery -A healthcare worker --loglevel=info`
8. Run `python manage.py makemigrations` to initialize migrations then run `python manage.py migrate` to migrate models to your database
9. To start you application run the command `python manage.py runserver`
- To access the endpoints `http://127.0.0.1:8000/api/`
- To access the Administrator pannel `http://127.0.0.1:8000/admin/`
- To access the Swagger UI `http://127.0.0.1:8000/swagger/`
- To access the endpoints `http://127.0.0.1:8000/api/`
- To access the Documentation `http://127.0.0.1:8000/redoc/`
- To access the Schema `http://127.0.0.1:8000/schema-viewer/`


