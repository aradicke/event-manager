import requests
from datetime import datetime, timezone, timedelta

base_url = "http://127.0.0.1:8000/events_api/v1/"

#  Explore the API options
get = requests.get(base_url)

endpoints = get.json()

print("Here's a list of the endpoints")
for k, v in endpoints.items():
    print(f"\t* {k} - {v}")

# Let's get a list of existing events

url = endpoints["events"]

get = requests.get(url)

events = get.json()

print(f"Here's the event list - count: {events['count']}")
for event in events["results"]:
    print("\t ----")
    for k, v in event.items():
        print(f"\t {k}: {v}")

# Now we can add an event and retrieve it

event_time = datetime.now(timezone.utc) + timedelta(days=2)
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

# Let's update our event to add a location - we'll need to get the location id first!

# Let's search for our event to see if one already exists

# Oops, there's a previous version of this event. Let's delete it.
