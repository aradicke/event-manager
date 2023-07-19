# Event Manager
This is a little setup for running a very basic event managment program locally. It's a demonstrator and template which runs using development servers and without authenticationa and authorization built in. In production, it would be behind a reverse proxy with a WSGI server.
## Prerequisites
To run this, you'll need either Docker or your own Postgres instance.
## Usage
Once you've cloned the repository, you'll need to set up your environment variables.
1. In the `env-templates` directory, you'll find two files.
   - In `database.env` you may want to change `POSTGRES_PASSWORD`. For this demo, it really isn't necessary since only the application will be able to reach it within the Docker network
   - In 'django.env' you can change the `OBFUSCATORY_NAME` which is used to fill the Django SECRET_KEY. If you're only running locally this is probably not necessary, but should you want to generate a new key, you can use the code below and paste it in. Production keys must never be committed:
   ```
   # If Django is not installed
   pip install Django

   # from your python shell
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```
2. Rename `env-templates` to `env`.

3. Running the server
    - If you're using Docker:  
        Run the following from the project directory, where `docker-compose.yaml` is.
        ```
        docker compose build
        
        docker compose up
        ```
        At this point, everything should be up and running.
        ***IF DJANGO THROWS AN ERROR WHEN TRYING TO FIND THE DATABASE, YOU'VE FOUND A RACE CONDITION THAT RESULTS BECAUSE POSTGRES LIES ABOUT BEING READY. `docker compose down` followed by `docker compose up` again should let you win the race :-)***

    - If you're not:  
        Modify the `DATABASES` block in `src/event_manager/settings.py` to point to your postgres instance. Run the following from the project directory.
        ```
        python src/manage.py runserver
        ```
3. Navigate to the health check page to verify that everything is working.

## Getting Things Running
1. Spin up the container

2. Run the tests:  
`docker exec event-manager-api-1 python manage.py test events`

## Testing It Out

## Things To Add
