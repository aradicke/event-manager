# Event Manager
This is a little setup for running a very basic event managment program locally. It's a demonstrator and template which runs using development servers and without authenticationa and authorization built in. In production, it would be behind a reverse proxy with a WSGI server.
## Prerequisites
To run this, you'll need either Docker or your own Postgres instance. You can probably run in locally in a virtual environment if you have your own Postgres instance.
## Usage
Once you've cloned the repository, you'll need to set up your environment variables.
1. In the `env-templates` directory, you'll find two files.
   - In `database.env` you may want to change `POSTGRES_PASSWORD`. For this demo, it really isn't necessary since only the application will be able to reach it within the Docker network
   - In 'django.env' you can change the `SECRET_KEY` which is used to fill the Django SECRET_KEY. If you're only running locally this is probably not necessary, but should you want to generate a new key, you can use the code below and paste it in. Production keys must never be committed:
   ```
   # If Django is not installed
   pip install Django

   # from your python shell
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```
2. Rename `env-templates` directory to `env`.

3. Running the server
    - If you're using Docker:  
        Run the following from the project directory, where `docker-compose.yaml` is.
        ```
        docker compose build
        
        docker compose up
        ```
        At this point, everything should be up and running. Navigate to http://127.0.0.1:8000/health_check and you should see a simple HTML page.
        ***If there's an error about Django not being able to find the database, there is a race condition that can happen because of how Docker handles the Postgres container's ready signal. If this happens, `docker compose down` followed by `docker compose up` again should let you win the race :-)***

    - If you're not:  
        Create a virtual environment and install the requirements.txt, preferably with pip. Modify the `DATABASES` block in `src/event_manager/settings.py` to point to your postgres instance. Run the following from the project directory.
        ```
        python src/manage.py migrate
        python src/manage.py runserver
        ```

## Browsable API
Navigate to http://127.0.0.1:8000/events_api/v1/ - this should open Django REST Framework's browseable API. You'll be able to go to each endpoint and get a LIST. You can also CREATE from these pages. If you select Extra Actions from the top of the page, you can SEARCH. To RETRIEVE detail pages, you'll need to add an ID to the url in the address bar, like so - http://127.0.0.1:8000/events_api/v1/categories/5/ . From the details page, you can also PUT to UPDATE and DELETE. I'm not sure if it can do a PARTIAL UPDATE but I have an example for that in code below.

## Testing It Out

You can find all the tests in demo_scripts.py if you prefer to run them from there, but here are some code examples.

###  Explore the API options
Each example builds on the previous one - some of the variables may be referenced later, so you may need to modify it if you want to skip around.

```
import requests
from datetime import datetime, timezone, timedelta
import pytz

base_url = "http://127.0.0.1:8000/events_api/v1/"

get = requests.get(base_url)

endpoints = get.json()

print("Here's a list of the endpoints")
for k, v in endpoints.items():
    print(f"\t* {k} - {v}")
```
### Let's get a list of existing events
```
url = endpoints["events"]

get = requests.get(url)

events = get.json()

print(f"Here's the event list - count: {events['count']}")
for event in events["results"]:
    print("\t ----")
    for k, v in event.items():
        print(f"\t {k}: {v}")

```
### Now we can add an event and retrieve it
```
event_time = datetime.now(pytz.timezone("US/Central")) + timedelta(days=2)
event_data = {
    "title": "API discussion",
    "description": "Talk about how the API should work",
    "start_time": event_time,
    "end_time": event_time + timedelta(hours=1),
}

event_add = requests.post(url, data=event_data)
print(f"HTTP status code {event_add.status_code}")

event_url = url + str(event_add.json()["id"])

our_event = requests.get(event_url)
print(f"HTTP status code {our_event.status_code}")

```
### Let's update our event to add a location
```
# we'll need to get the location id first!
locations_url = endpoints["locations"]
locations = requests.get(locations_url)
print(f"HTTP status code {locations.status_code}")
locations = locations.json()
print(locations_url)
print(f"Here's the location list - count: {locations['count']}")
for location in locations["results"]:
    print("\t ----")
    for k, v in location.items():
        print(f"\t {k}: {v}")


# We'll pick whatever is at ID 4. If this code fails, you'll want to pick a different ID based on the info you got above.

update = requests.patch(event_url + "/", data={"location": locations_url + "4/"})
print(f"Update HTTP status code {update.status_code}")

```
### Let's search for our event to see if one like it already exists
```
search = requests.get(endpoints["events"] + "search/", params={"search_term": "api"})
print(f"Search HTTP status code {search.status_code}")
search_results = search.json()

```
### Oops, the event has been cancelled. Let's delete it.
```
destroy = requests.delete(event_url)
print(f"Delete HTTP status code {destroy.status_code}")
```

## Basic Architecture

This is a pretty standard Django app. The project runs on a server (here the Django development server; in production it would be gunicorn or any ASGI or WSGI server behind a reverse proxy like nginx or perhaps even an Amazon ELB). It is laid out as a single app, though there is room for expansion there. It connects to a Postgres database - this is required since it uses a Postgres-specific search feature but barring that it could be deployed with other data backends. The Django ORM will build the necessary tables.

## Design choices
1. Since authentication is assumed, there's not a lot of structure here for authorization. The good thing is that this basically comes built in with Django, and once user identification data is available it's trivial to integrate it into the endpoints via decorators, to handle things like distinguishing among user types. Once you have users, you can create models and the attendant tables to distinguish between user types and abilities, limit who can see what events with filters, and a lot of other things. 
2. Django REST Framework is a great way to let your models do much of the work. Once it's set up a lot of things can just plug and play and added features can be dropped in quickly.
3. I've avoided pre-optimizing. The nature of this application is well within the performance parameters of Django and DRF, but if it suddenly needed better performance there are lots of options like caching, ORM and SQL optimization, and creating extra servers that can be used.
4. This is a highly expandable space. It's easy to add to the models and add the serializers to customize this to fit various needs. Features like bulk uploads, fine-grained authorization, attendance tracking and others all flow naturally.

## Tracking & Logging
There is basic tracking for event updates. Such changes are vital sometimes to be sure of what a client or user saw when they were using the system. Django also has some built-in logging that is readily extensible. For time reasons, I haven't added any new logging but it's a simple add to the various views, especially once there's some user data coming in.