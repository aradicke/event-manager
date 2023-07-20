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

# Let's search for our event to see if one like it already exists

search = requests.get(endpoints["events"] + "search/", params={"search_term": "api"})
print(f"Search HTTP status code {search.status_code}")
search_results = search.json()

# Oops, the event has been cancelled. Let's delete it.

destroy = requests.delete(event_url)
print(f"Delete HTTP status code {destroy.status_code}")
